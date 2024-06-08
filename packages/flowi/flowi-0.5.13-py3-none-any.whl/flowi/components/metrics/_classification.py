from typing import Any

import numpy as np
from dask_ml.metrics import accuracy_score
from sklearn import metrics
import dask.array as da

from flowi.components.component_base import ComponentBase
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger


class Classification(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        experiment_tracking.log_metric(metric_name=method_name, value=result)
        return {f"metric_{method_name}": result}

    @staticmethod
    def _calculate_matrix_metrics(y_pred: np.array, y_true: np.array):
        y_pred_da = da.from_array(y_pred, chunks=y_pred.shape)
        y_true_da = da.from_array(y_true, chunks=y_true.shape)

        class_labels = da.unique(y_true_da).compute()

        true_positives = da.zeros_like(y_pred_da, dtype=int)
        true_negatives = da.zeros_like(y_pred_da, dtype=int)
        false_positives = da.zeros_like(y_pred_da, dtype=int)
        false_negatives = da.zeros_like(y_pred_da, dtype=int)

        for class_label in class_labels:
            # Convert 'y_pred' and 'y_true' to binary arrays for the current class
            y_pred_binary = da.where(y_pred_da == class_label, 1, 0)
            y_true_binary = da.where(y_pred_da == class_label, 1, 0)

            # Update true positives, false positives, and false negatives
            true_positives += da.logical_and(y_pred_binary, y_true_binary)
            true_negatives += da.logical_and(1 - y_pred_binary, 1 - y_true_binary)
            false_positives += da.logical_and(y_pred_binary, 1 - y_true_binary)
            false_negatives += da.logical_and(1 - y_pred_binary, y_true_binary)

        return true_positives, true_negatives, false_positives, false_negatives

    @staticmethod
    def _prepare_data(y_true: np.array, y_pred: np.array):
        if y_true.ndim > 1 and y_true.shape[1] == 1:
            y_true = y_true.reshape(-1)
        if y_pred.ndim > 1 and y_pred.shape[1] == 1:
            y_pred = y_pred.reshape(-1)

        return y_true, y_pred

    @staticmethod
    def _get_pos_label(y_pred: np.array, average: str):
        pos_label = 1
        if average == 'binary':
            pos_label = y_pred[0]

        return pos_label

    def accuracy(self, y_pred: np.array, y_true: np.array, normalize: bool = True):
        y_true, y_pred = self._prepare_data(y_true=y_true, y_pred=y_pred)

        score = accuracy_score(y_true=y_true, y_pred=y_pred, normalize=normalize)
        self._logger.debug(f"Accuracy: {score}")

        return score

    def precision(self, y_pred: np.array, y_true: np.array, average: str):
        # TODO: implement in dask
        y_true, y_pred = self._prepare_data(y_true=y_true, y_pred=y_pred)

        pos_label = self._get_pos_label(y_pred=y_pred, average=average)
        score = metrics.precision_score(y_true=y_true, y_pred=y_pred, average=average, pos_label=pos_label)
        self._logger.debug(f"Precision: {score}")

        return score

    def recall(self, y_pred: np.array, y_true: np.array, average: str):
        # TODO: implement in dask
        y_true, y_pred = self._prepare_data(y_true=y_true, y_pred=y_pred)

        pos_label = self._get_pos_label(y_pred=y_pred, average=average)
        score = metrics.recall_score(y_true=y_true, y_pred=y_pred, average=average, pos_label=pos_label)
        self._logger.debug(f"Recall: {score}")

        return score

    def f1_score(self, y_pred: np.array, y_true: np.array, average: str):
        # TODO: implement in dask
        y_true, y_pred = self._prepare_data(y_true=y_true, y_pred=y_pred)

        pos_label = self._get_pos_label(y_pred=y_pred, average=average)
        score = metrics.f1_score(y_true=y_true, y_pred=y_pred, average=average, pos_label=pos_label)
        self._logger.debug(f"F1 Score: {score}")

        return score
