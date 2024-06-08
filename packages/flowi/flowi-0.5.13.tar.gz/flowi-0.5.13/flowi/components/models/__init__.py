"""
Preprocessing techniques for ml applications in datasets
"""


from ._classification import Classification
from ._regression import Regression
# from ._wrappers import OneHotModel

__all__ = [
    Classification,
    Regression,
    # OneHotModel
]
