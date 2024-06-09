"""Special enumclass for definining different modeling types during testing."""

from enum import Enum


class ModelingType(Enum):
    """Enum for the different types of tests."""

    REGRESSION = 1
    CLASSIFICATION = 2
    REGRESSION_TIMESERIES = 3
    CLASSIFICATION_TIMESERIES = 4

    @classmethod
    def to_dict(cls) -> dict:
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls) -> list:
        """Returns a list of all the enum keys."""
        return [member.name for member in cls]

    @classmethod
    def values(cls)-> list:
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())
