import time

from flowi.components.component_base import ComponentBase
from flowi.utilities.logger import Logger
import dask.dataframe as dd
import dask.array as da


class DataPreparationSKLearn(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)

    def prepare_train(self, df: dd.DataFrame, target_column: str) -> (da.Array, da.Array):
        data_columns = list(df.columns)
        data_columns.remove(target_column)
        self._logger.info("Data columns: {}".format(data_columns))

        self._logger.info("Persisting")
        start_time = time.time()
        df = df.persist()
        self._logger.info("Elapsed: {:.2f}s".format(time.time() - start_time))

        X_df = df[data_columns]
        y_df = df[[target_column]]

        self._logger.info("X To Dask Array")
        start_time = time.time()
        X = X_df.to_dask_array(lengths=True)
        self._logger.info("Elapsed: {:.2f}s".format(time.time() - start_time))

        self._logger.info("Y To Dask Array")
        start_time = time.time()
        y = y_df.to_dask_array(lengths=True)
        self._logger.info("Elapsed: {:.2f}s".format(time.time() - start_time))

        # X = X_df.to_dask_array()
        # y = y_df.to_dask_array()

        return X, y
