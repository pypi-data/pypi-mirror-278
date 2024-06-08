import logging
from typing import Any, List

import dask.dataframe as dd

from flowi.components.component_base import ComponentBase
from flowi.components.label._transformers import OneHotEnc, LabelEnc
from flowi.components.preprocessing.transformers import filter_columns
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.utilities.logger import Logger


class Label(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        del methods_kwargs["df"]

        experiment_tracking = ExperimentTracking()
        df = result[0]
        transformer = result[1]
        # method_name = "_".join([method_name, str(id(transformer))])
        transform_input = True if methods_kwargs["is_target_column"] == "false" else False
        transform_output = True if methods_kwargs["is_target_column"] == "true" else False

        if method_name == "label_encoder":
            suffix = "input" if methods_kwargs["is_target_column"] == "false" else "output"
            method_name = method_name + "_" + suffix

        logging.info(f"_label method_name: {method_name}")
        experiment_tracking.log_transformer_param(key=method_name, value=methods_kwargs)
        return {
            "df": df,
            "object": transformer,
            "transform_input": transform_input,
            "transform_output": transform_output,
        }

    def label_encoder(self,
                      df: dd.DataFrame,
                      columns: List[str] = None,
                      exclude_columns: List[str] = None,
                      is_target_column: bool = False
                      ):

        self._logger.debug(f"is_target_column: {is_target_column}")

        filtered_columns = filter_columns(df=df, columns=columns, exclude_columns=exclude_columns)
        transformer = LabelEnc(columns=filtered_columns)

        transformer.fit(df)

        df = transformer.transform(df)
        return df, transformer

    def one_hot_encoder(self,
                        df: dd.DataFrame,
                        columns: List[str] = None,
                        exclude_columns: List[str] = None,
                        is_target_column: bool = False
                        ):

        self._logger.debug(f"is_target_column: {is_target_column}")

        filtered_columns = filter_columns(df=df, columns=columns, exclude_columns=exclude_columns)
        transformer = OneHotEnc(columns=filtered_columns)
        # transformer = ColumnFilter(columns=columns, exclude_columns=exclude_columns, transformer=base_transformer)
        transformer.fit(df)

        df = transformer.transform(df)
        return df, transformer
