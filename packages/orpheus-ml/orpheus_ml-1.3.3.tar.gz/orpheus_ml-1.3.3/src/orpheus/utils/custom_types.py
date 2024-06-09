"""Custom datatypes."""

from enum import Enum
from typing import Any, Optional


from orpheus.utils.type_vars import EstimatorType
from orpheus.utils.helper_functions import get_obj_name


class SuperEnum(Enum):
    """
    A custom Enum class that allows for easy conversion to dictionary and list.

    Also see: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
    """

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_  # pylint: disable=E1101

    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())


class EstimatorErrorInfo:
    """EstimatorErrorInfo class for storing information about errors that occur during HyperTuner.fit()."""

    # we use slots because a lot of EstimatorErrorInfo objects are created
    __slots__ = ["estimator", "error", "parameter", "value"]

    def __init__(
        self,
        estimator: EstimatorType,
        error: Exception,
        parameter: Optional[str],
        value: Any,
    ):
        self.estimator = estimator
        self.error = error
        self.parameter = parameter
        self.value = value

    def __repr__(self):
        return f"EstimatorErrorInfo: {get_obj_name(self.estimator)}({self.parameter}={self.value})"

    def __eq__(self, other: "EstimatorErrorInfo"):
        est_name = get_obj_name(self.estimator)
        other_est_name = get_obj_name(other.estimator)
        return est_name == other_est_name and self.parameter == other.parameter and self.value == other.value

    def __hash__(self):
        return hash((self.estimator, self.parameter, self.value))

    @property
    def error_type(self):
        return type(self.error).__name__

    @property
    def error_message(self):
        return str(self.error)


class PredictorType(SuperEnum):
    """
    Enum type representing different stages in the prediction process.

    This special enumerated type is used indirectly by the `PredictObject.predict` method
    to determine the type of prediction to be made. Each value represents a stage in the
    `HyperTuner.fit` process and corresponds to a different group of estimator(s) used for prediction.

    To fully understand the types and the estimators that can be used for prediction, it is
    important to understand the `HyperTuner.fit` process. Please refer to the documentation
    of the `HyperTuner.fit` method for more information.

    Attributes:
        SOLO (int): Represents the best single estimator found at the end of the `HyperTuner.fit` process.
        ENSEMBLE_R1 (int): Represents the best found estimators during ROUND 1.
        ENSEMBLE_R2_WEIGHTED (int): Represents the best found estimators during ROUND 2, if R2_weights were specified.
        ENSEMBLE_R2 (int): Represents the best found estimators during ROUND 2.
        ENSEMBLE_R3 (int): Represents the best found estimators during ROUND 3.
    """

    SOLO = 1
    ENSEMBLE_R1 = 2
    ENSEMBLE_R2_WEIGHTED = 3
    ENSEMBLE_R2 = 4
    ENSEMBLE_R3 = 5
