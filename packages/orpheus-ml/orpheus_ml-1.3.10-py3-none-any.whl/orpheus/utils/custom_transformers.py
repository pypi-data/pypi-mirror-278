"""Custom transformers for preprocessing data"""

import re
from typing import Optional, Union

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from orpheus.components.preprocessing.feature_adding import FeatureAdding
from orpheus.components.preprocessing.feature_removing import FeatureRemoving


def replace_special_chars_in_columns(X: pd.DataFrame) -> pd.DataFrame:
    """Replace special characters with underscores in column names"""

    # First remove duplicate columns
    if X.columns.duplicated().any():
        X = X.loc[:, ~X.columns.duplicated()]
    X.columns = [re.sub(r"[^a-zA-Z0-9_]", "_", name) for name in X.columns]

    return X


class FeatureTransformerWrapper(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        feature_transformer: Union[FeatureAdding, FeatureRemoving],
        n_jobs: Optional[int] = None,
    ):
        self.feature_transformer = feature_transformer
        self.n_jobs = n_jobs

    def fit(self, X, y=None):
        # As it seems your FeatureAdding class doesn't need to fit anything
        return self

    def transform(self, X, y=None):
        # Assuming X is the data DataFrame you want to transform
        return self.feature_transformer._transform(X, n_jobs=self.n_jobs)
