"""Custom datatypes."""

from typing import TypeVar, Union

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit

EstimatorType = TypeVar("EstimatorType", bound=BaseEstimator)
ScalerType = TypeVar("ScalerType", bound=TransformerMixin)
TransformerType = TypeVar("TransformerType", bound=TransformerMixin)
CrossValidatorType = TypeVar("CrossValidatorType", bound=Union[BaseCrossValidator, BaseShuffleSplit])
ArrayLike = TypeVar("ArrayLike", bound=Union[pd.DataFrame, pd.Series])
