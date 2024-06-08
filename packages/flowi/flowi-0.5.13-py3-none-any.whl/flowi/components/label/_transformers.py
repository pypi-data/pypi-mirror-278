from typing import List

from dask_ml.preprocessing import OneHotEncoder, LabelEncoder
import dask.dataframe as dd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class OneHotEnc(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str]):
        self._columns = columns
        self._transformer = OneHotEncoder()

    def get_categories(self):
        return self._transformer.categories_

    def fit(self, X, y=None):
        X = X[self._columns]
        self._transformer.fit(X)
        return self

    def transform(self, X):
        X = X[self._columns]
        X = self._transformer.transform(X)
        return X


class LabelEnc(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str]):
        self._columns = columns
        self._transformers = {key: LabelEncoder() for key in columns}

    def fit(self, X, y=None):
        for column in self._transformers.keys():
            self._transformers[column].fit(X[column])
        return self

    def transform(self, X: dd.DataFrame):
        for column in self._transformers.keys():
            X[column] = self._transformers[column].transform(X[column])

        return X

    def inverse_transform(self, X: dd.DataFrame):
        for column in self._transformers.keys():
            if isinstance(X, np.ndarray):
                X = self._transformers[column].inverse_transform(X)
            else:
                X[column] = self._transformers[column].inverse_transform(X[column])

        return X
