"""Constants for preprocessing components."""

from sklearn.preprocessing import (
    MaxAbsScaler,
    MinMaxScaler,
    Normalizer,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)

SCALERS = [
    MinMaxScaler,
    MaxAbsScaler,
    StandardScaler,
    RobustScaler,
    Normalizer,
    QuantileTransformer,
    PowerTransformer,
]
