import os
from flowi.flow_chart.node import Node
import dill
import dask.dataframe as dd

from flowi.experiment_tracking.utils import download_artifacts, load_model_by_version
from flowi.prediction.dummy import DummyTransformer
from flowi.utilities.logger import Logger
from flowi.utilities.airflow_xcom import write_xcom
from flowi.settings import FLOW_NAME_FQDN, MODEL_VERSION
from alibi_detect.saving import load_detector


_logger = Logger(logger_name=__name__)


def _load(file_path: str):
    _logger.info(f"Loading {file_path}")
    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            return dill.load(f)
    else:
        _logger.info(f"Loading dummy {file_path}")
        return DummyTransformer()


def predict(source: dict, destiny: dict, result_only: bool = True):
    download_artifacts(model_name=FLOW_NAME_FQDN, version=MODEL_VERSION)

    source_node = Node(id_="source", node=source, previous_node=None, next_node=None)
    destiny_node = Node(id_="destiny", node=destiny, previous_node=source_node, next_node=None)

    source_result = source_node.run(global_variables={})
    X = source_result["test_df"]

    # Filtering columns
    columns = _load("columns/columns.pkl")
    X = X[columns]

    # transform
    input_transformer = _load("transformers/input_transformer.pkl")
    if input_transformer:
        _logger.info("Transforming input")
        X = input_transformer.transform(X)

    # drift detection
    drift_detector = load_detector("drift")

    n_samples = 400
    length = len(X)
    fraction = min(n_samples / length, 1)
    x = X.sample(frac=fraction)
    x = x.values.compute()

    preds = drift_detector.predict(x)
    is_drift = preds["data"]["is_drift"]

    if is_drift:
        _logger.info("Drift Detected!")
        _logger.info("Finished Batch without predicting")
        write_xcom(key="drift", value="1")
        return -1

    _logger.info("No drift detected. Predicting...")
    model = load_model_by_version(model_name=FLOW_NAME_FQDN, version=MODEL_VERSION)
    y_pred = model.predict(X)

    output_transformer = _load("transformers/output_transformer.pkl")
    if output_transformer:
        _logger.info("Transforming Output")
        y_pred = output_transformer.inverse_transform(y_pred)

    # save
    _logger.info("Saving results")
    result_df = dd.from_array(y_pred, columns=["flowi_label_class"])
    source_node.state["df"] = source_result["test_df"].merge(result_df)
    destiny_node.run(global_variables={})

    _logger.info("Finished Batch predict")

    write_xcom(key="drift", value="0")
