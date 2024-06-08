from typing import Any, List

import dask.dataframe as dd
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor

from flowi.components.component_base import ComponentBase
from flowi.components.model_selection import ModelSelection
# from flowi.components.models._wrappers import OneHotModel, CategoryModel, BaseModel, RegressionModel
from flowi.components.models._wrappers import BaseModel, RegressionModel
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger
from flowi.utilities.tune import tune_param


class Regression(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        model: BaseModel = result[0]
        parameters = result[1]
        model_type = result[2]

        model_uri = experiment_tracking.save_model(obj=model.model, file_path="model")
        experiment_tracking.log_tag(tag_name="model_type", value=model_type)
        experiment_tracking.log_model_param(key=model.model.__class__.__name__, value=parameters)
        return {
            "model": model,
            "parameters": parameters,
            "target_column": methods_kwargs["target_column"],
            "object": model,
            "model_uri": model_uri,
        }

    @staticmethod
    def _fit_sklearn(
        df: dd.DataFrame,
        model,
        parameters: dict,
        target_column: str,
        verbose: int = 0,
        has_model_selection_in_flow: bool = False,
    ):
        if not has_model_selection_in_flow:
            model_selection = ModelSelection()
            model, parameters = model_selection.tpe(
                df=df, model=model, parameters=parameters, target_column=target_column
            )

        return model, parameters

    @staticmethod
    def _to_list(x: Any):
        return x if isinstance(x, list) else [x]

    def random_forest_regressor(
            self,
            df: dd.DataFrame,
            target_column: str,
            n_estimators: int or List[int] = 10,
            max_depth: int or List[int] = 0,
            min_samples_split: int or List[int] = 2,
            min_samples_leaf: int or List[int] = 1,
            min_weight_fraction_leaf: float or List[float] = 0.0,
            bootstrap: bool or List[bool] = True,
            oob_score: bool or List[bool] = True,
            verbose: int = 0,
            has_model_selection_in_next_step: bool = False,
    ):
        max_depth = None if max_depth == 0 else max_depth

        parameters = {
            "n_estimators": tune_param(label="n_estimators", values=n_estimators, value_type=int),
            "max_depth": tune_param(label="max_depth", values=max_depth, value_type=float),
            "min_samples_split": tune_param(label="min_samples_split", values=min_samples_split, value_type=int, min_value=2),
            "min_samples_leaf": tune_param(label="min_samples_leaf", values=min_samples_leaf, value_type=int, min_value=1),
            "min_weight_fraction_leaf": tune_param(label="min_weight_fraction_leaf", values=min_weight_fraction_leaf,
                                                   value_type=float),
            "bootstrap": tune_param(label="bootstrap", values=bootstrap, value_type=bool),
            "oob_score": tune_param(label="oob_score", values=oob_score, value_type=bool),
        }

        model = RandomForestRegressor()
        model_type = "regression"
        model = RegressionModel(model=model)
        model, parameters = self._fit_sklearn(
            model=model,
            parameters=parameters,
            df=df,
            target_column=target_column,
            verbose=verbose,
            has_model_selection_in_flow=has_model_selection_in_next_step,
        )

        return model, parameters, model_type
