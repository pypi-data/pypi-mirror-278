from typing import Iterable

from sklearn.model_selection import ParameterGrid

from flowi.connections.aws.s3 import S3
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.flow_chart.node import Node
from flowi.flow_chart.topology import Topology
from flowi.settings import FLOW_NAME_FQDN, RUN_ID, VERSION
from flowi.global_state import GlobalState
from flowi.utilities.airflow_xcom import write_xcom
from flowi.utilities.logger import Logger
from flowi.utilities.mongo import Mongo
import random
import numpy as np

random.seed(42)
np.random.seed(42)


class FlowChart(object):
    def __init__(self, flow_chart: dict, metric: str, threshold: str):
        self._logger = Logger(logger_name=__name__)
        self._logger.info("Initializing FlowChart")

        self._global_state = GlobalState()
        self._mongo = Mongo()
        self._flow_chart = flow_chart
        self._metric = metric
        self._threshold = float(threshold)

        self._experiment_tracking: ExperimentTracking = ExperimentTracking()
        self._runs_params = []
        self._parameter_tuning_types = ["Preprocessing"]
        self._nodes_execution_order = []
        self._nodes = {}
        self._num_experiments = 0

        self._global_state.set(key="metric", value=self._metric)

        self._init_nodes()
        self._logger.info("FlowChart initialized")

    def _init_nodes(self):
        nodes = self._flow_chart["nodes"]
        links = self._flow_chart["links"]

        topology = Topology(nodes)
        for node_id in nodes:
            self._add_node(node=nodes[node_id])

        for link in links:
            node_from = links[link]["from"]["nodeId"]
            node_to = links[link]["to"]["nodeId"]
            topology.add_edge(node_from=node_from, node_to=node_to)

            self._add_node(node=nodes[node_from], next_node_id=node_to)
            self._add_node(node=nodes[node_to], previous_node_id=node_from)

        self._nodes_execution_order = topology.topological_sort()
        self._logger.debug(f"Nodes running order: {self._nodes_execution_order}")
        self.generate_runs()

    def _add_node(self, node: dict, previous_node_id: str or None = None, next_node_id: str or None = None):
        node_id = node["id"]
        previous_node = self._nodes.get(previous_node_id, None)
        next_node = self._nodes.get(next_node_id, None)

        if node_id not in self._nodes:
            self._nodes[node_id] = Node(id_=node_id, node=node, previous_node=previous_node, next_node=next_node)
            if node["type"] == "Models":
                self._num_experiments += 1
        else:
            self._nodes[node_id].add_previous_node(previous_node=previous_node)
            self._nodes[node_id].add_next_node(next_node=next_node)

    def generate_runs(self):
        combined_grid_params = {}
        for node_id in self._nodes_execution_order:
            node: Node = self._nodes[node_id]
            if node.type not in self._parameter_tuning_types:
                continue

            for attribute in node.attributes:
                if isinstance(node.attributes[attribute], str) \
                        or not isinstance(node.attributes[attribute], Iterable) \
                        or attribute == "columns" or attribute == "exclude_columns":
                    node.attributes[attribute] = [node.attributes[attribute]]

            combined_grid_params[node_id] = list(ParameterGrid(node.attributes))
        combined_params = list(ParameterGrid(combined_grid_params))

        self._runs_params = combined_params

    def compare_models(self) -> dict:
        self._logger.info("Comparing models. Flow Name {} | RUN ID {} | Version {}".format(FLOW_NAME_FQDN, RUN_ID, VERSION))
        models = self._mongo.get_models_by_version(run_id=RUN_ID, version=VERSION)
        best_model = None
        best_performance = 0.0
        for model in models:
            if self._metric not in model["metrics"]:
                continue

            model_performance = model["metrics"][self._metric]
            if model_performance > best_performance:
                best_performance = model_performance
                best_model = model

        self._logger.info(best_model)

        return best_model

    def stage_model(self, model: dict):
        metric_value = model["metrics"][self._metric]
        write_xcom(key="metric_value", value=metric_value)

        self._logger.info(f"Comparing {self._metric} for staging.\n"
                          f"Training value {metric_value} | Threshold: {self._threshold}")
        if metric_value >= self._threshold:
            self._logger.info("Staging trained model!")
            experiment_id = model["experiment_id"]
            model_version = self._experiment_tracking.stage_model(experiment_id=experiment_id)
            write_xcom(key="staged_model_version", value=model_version)

            self._mongo.stage_model(model["_id"])
        else:
            self._logger.info("Trained model didnt match desired threshold. Not staging it.")
            write_xcom(key="staged_model_version", value="")

    def run(self):
        self._logger.info(f"NUMBER OF COMBINATIONS: {len(self._runs_params)}")
        self._logger.debug(str(self._runs_params))
        for run_params in self._runs_params:
            self._logger.debug("PARAMS")
            self._logger.debug(str(run_params))
            global_variables = {}
            self._experiment_tracking.reset_experiments(num_experiments=self._num_experiments)

            for node_id in self._nodes_execution_order:
                node: Node = self._nodes[node_id]
                self._logger.info(f"Processing node {node_id} | {node.type} - {node.method_name}")
                if node.type in self._parameter_tuning_types:
                    node.attributes = run_params[node_id]
                node.run(global_variables=global_variables)

            self._experiment_tracking.end_experiments()

        best_model = self.compare_models()
        self.stage_model(model=best_model)
