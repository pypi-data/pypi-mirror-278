from typing import List

import dask.dataframe as dd
from sklearn.base import BaseEstimator, TransformerMixin

from flowi.utilities.logger import Logger


def filter_columns(df: dd.DataFrame,
                   columns: List[str] = None,
                   exclude_columns: List[str] = None
                   ) -> List[str]:
    if columns:
        columns = columns if isinstance(columns, list) else [columns]
        return columns
    elif exclude_columns:
        exclude_columns = exclude_columns if isinstance(exclude_columns, list) else [exclude_columns]
        return df.columns.difference(exclude_columns).to_list()

    return df.columns.tolist()


class ColumnFilter(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str], exclude_columns: List[str], transformer):
        self.columns = columns
        self.exclude_columns = exclude_columns
        self.transformer = transformer
        self._logger = Logger(__name__)

        if self.columns and self.exclude_columns:
            raise ValueError("Columns and exclude_columns cannot be set together")

        self._filtered_columns = list()

    def _filter_columns(self, X) -> List[str]:
        if self.columns:
            columns = self.columns if isinstance(self.columns, list) else [self.columns]
            return columns
        elif self.exclude_columns:
            exclude_columns = self.exclude_columns if isinstance(self.exclude_columns, list) else [self.exclude_columns]
            return X.columns.difference(exclude_columns).to_list()
        return X.columns.tolist()

    def fit(self, X):
        self._filtered_columns = self._filter_columns(X)

        if self.transformer is not None:
            self.transformer.fit(X[self._filtered_columns])
            for column in self._filtered_columns:
                if X[column].dtype == "category":
                    X[column] = X[column].cat.add_categories(self.transformer.fill_value)

        return self

    def transform(self, X):
        if self.transformer is not None:
            X[self._filtered_columns] = self.transformer.transform(X[self._filtered_columns])

        return X

    def inverse_transform(self, X):
        if self.transformer is not None:
            X[self._filtered_columns] = self.transformer.inverse_transform(X[self._filtered_columns])

        return X
