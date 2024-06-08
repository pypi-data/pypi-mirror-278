from typing import Any

import numpy as np
from dask_ml import metrics
from sklearn import metrics

from flowi.components.component_base import ComponentBase
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger


class Regression(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        experiment_tracking.log_metric(metric_name=method_name, value=result)
        return {f"metric_{method_name}": result}

    def mean_squared_error(self, y_pred: np.array, y_true: np.array):
        score = metrics.mean_squared_error(y_true=y_true, y_pred=y_pred)
        self._logger.debug(f"Mean Squared Error: {score}")

        return score

    def mean_absolute_error(self, y_pred: np.array, y_true: np.array):
        score = metrics.mean_absolute_error(y_true=y_true, y_pred=y_pred)
        self._logger.debug(f"Mean Absolute Error: {score}")

        return score

    def mean_squared_log_error(self, y_pred: np.array, y_true: np.array):
        score = metrics.mean_squared_log_error(y_true=y_true, y_pred=y_pred)
        self._logger.debug(f"Mean Squared Log Error: {score}")

        return score

    def r2_score(self, y_pred: np.array, y_true: np.array):
        score = metrics.r2_score(y_true=y_true, y_pred=y_pred)
        self._logger.debug(f"F1 Score: {score}")

        return score
