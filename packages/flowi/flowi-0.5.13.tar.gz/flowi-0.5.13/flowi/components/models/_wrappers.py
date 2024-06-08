from typing import Any

import dask.dataframe as dd
import dask.array as da
from dask_ml.preprocessing import DummyEncoder, LabelEncoder

# from scikeras.wrappers import KerasClassifier
import numpy as np


class BaseModel:

    def __init__(self, model: Any, encoder):
        self.model = model
        self.encoder = encoder


class RegressionModel(BaseModel):
    def __init__(self, model):
        super().__init__(model, None)

    def encode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array:
        if isinstance(y, np.ndarray):
            y = da.from_array(y)

        # if isinstance(y, da.Array):
        #     y = y.to_dask_dataframe()

        # y = y.astype("category")
        # y = y.categorize()

        # y = da.from_array(y)

        return y

    def decode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array or np.ndarray:
        # if isinstance(y, np.ndarray):
        #     y = self.encoder.inverse_transform(y)
        #     return y
        #
        # y = self.encoder.inverse_transform(y)

        return y

    def predict(self, X) -> da.Array:
        y = self.model.predict(X)
        y = self.decode(y)
        return y


class CategoryModel(BaseModel):
    def __init__(self, model):
        super().__init__(model, LabelEncoder())

    def encode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array:
        if isinstance(y, np.ndarray):
            y = da.from_array(y)

        if isinstance(y, da.Array):
            y = y.to_dask_dataframe()

        # y = y.astype("category")
        # y = y.categorize()

        self.encoder.fit(y)
        y = self.encoder.transform(y)
        y = da.from_array(y)

        return y

    def decode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array or np.ndarray:
        if isinstance(y, np.ndarray):
            y = self.encoder.inverse_transform(y)
            return y

        y = self.encoder.inverse_transform(y)

        return y

    def predict(self, X) -> da.Array:
        y = self.model.predict(X)
        y = self.decode(y)
        return y


# class OneHotModel(BaseModel):
#     def __init__(self, model: KerasClassifier):
#         super().__init__(model, DummyEncoder())
#
#     def encode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array:
#         if isinstance(y, np.ndarray):
#             y = da.from_array(y)
#
#         if isinstance(y, da.Array):
#             y = y.to_dask_dataframe()
#
#         y = y.astype("category")
#         y = y.categorize()
#
#         self.encoder.fit(y)
#         y = self.encoder.transform(y)
#         y = y.to_dask_array()
#
#         return y
#
#     def decode(self, y: dd.DataFrame or da.Array or np.ndarray) -> da.Array or np.ndarray:
#         is_ndarray = False
#         if isinstance(y, np.ndarray):
#             y = da.from_array(y)
#             is_ndarray = True
#
#         y = self.encoder.inverse_transform(y)
#         y = y.to_dask_array()
#         if is_ndarray:
#             y = y.compute()
#
#         return y
#
#     def predict(self, X) -> da.Array:
#         y = self.model.predict(X)
#         y = self.decode(y)
#         return y
