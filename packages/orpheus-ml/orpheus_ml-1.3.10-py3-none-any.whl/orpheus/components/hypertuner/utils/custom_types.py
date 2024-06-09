"""Custom types for HyperTuner component."""

from typing import Dict, List, Optional, Union

from orpheus.components.hypertuner.utils.helper_functions import (
    get_all_defaultargs_from_estimator,
    get_uncalled_estimator,
)
from orpheus.utils.custom_types import EstimatorErrorInfo
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.type_vars import EstimatorType


class ErrorDict:
    """
    ErrorDict class for storing instances of EstimatorErrorInfo.
    Keep track of errors that occur during HyperTuner.fit().
    """

    _error_dict: Dict[str, Dict[str, float]] = {
        "lower_bound": {},
        "upper_bound": {},
        "unknown": {},
    }

    @classmethod
    def get(
        cls, error_key: str, estimator_str: Optional[str] = None
    ) -> Union[Dict[str, float], List[EstimatorErrorInfo]]:
        if error_key not in {"lower_bound", "upper_bound", "unknown"}:
            raise ValueError(
                f"error_key should be one of 'lower_bound', 'upper_bound' or 'unknown', but is {error_key}"
            )
        if estimator_str is None:
            return cls._error_dict[error_key]
        return cls._error_dict[error_key].get(estimator_str, [])

    @classmethod
    def get_all(cls):
        return cls._error_dict

    @classmethod
    def set(
        cls, error_key: str, estimator_str: str, error_data: Union[EstimatorErrorInfo, List[EstimatorErrorInfo]]
    ) -> None:
        """Sets the error_data in cls._error_dict[error_key][estimator_str]"""

        # check if error_data is not empty
        if not error_data:
            return

        if error_key not in {"lower_bound", "upper_bound", "unknown"}:
            raise ValueError(
                f"error_key should be one of 'lower_bound', 'upper_bound' or 'unknown', but is {error_key}"
            )

        if isinstance(error_data, EstimatorErrorInfo):
            error_data = [error_data]
        elif isinstance(error_data, list):
            if not all(isinstance(error_info, EstimatorErrorInfo) for error_info in error_data):
                raise TypeError(
                    "error_data should be a list with type EstimatorErrorInfo, but the list contains other types than EstimatorErrorInfo"
                )
        else:
            raise TypeError(
                f"error_data should be of type EstimatorErrorInfo or list with EstimatorErrorInfo, but is of type {type(error_data)}"
            )

        for error_info in error_data:
            error_key = error_key if isinstance(error_info.value, (int, float)) else "unknown"
            if error_info not in cls._error_dict[error_key].get(estimator_str, []):
                cls._error_dict[error_key].setdefault(estimator_str, []).append(error_info)

    @classmethod
    def update(
        cls,
        error_dict: dict,
    ) -> None:
        """Updates cls._error_dict with the found errors after R2 and R3"""
        for estimator_str, error_data in error_dict.items():
            default_args = DefaultArgsDict.get(estimator_str)
            for error_info in error_data:
                param, faulty_val = error_info.parameter, error_info.value
                default_val = default_args[param]
                try:
                    if faulty_val < default_val:
                        cls.set("lower_bound", estimator_str, error_info)
                    elif faulty_val > default_val:
                        cls.set("upper_bound", estimator_str, error_info)
                    else:
                        continue
                except TypeError:
                    cls.set("unknown", estimator_str, error_info)


class DefaultArgsDict:
    """DefaultArgsDict class for storing the default args of the estimators."""

    _default_args_dict: Dict = {}

    @classmethod
    def get(cls, estimator_str: str, param: Optional[str] = None) -> Union[Dict[str, float], float, None]:
        return (
            cls._default_args_dict.get(estimator_str, {}).get(param, None)
            if param
            else cls._default_args_dict.get(estimator_str, {})
        )

    @classmethod
    def get_all(cls) -> Dict[str, Dict[str, float]]:
        return cls._default_args_dict

    @classmethod
    def set(cls, estimator_list: List[EstimatorType]) -> None:
        """Update the default_args dict with the default args of
        the estimator if not yet present."""
        for est in estimator_list:
            estimator_str = get_obj_name(est)
            if not isinstance(estimator_str, str):
                raise TypeError(f"Estimator_str should be a string, but is of type {type(estimator_str)}")
            if estimator_str not in cls._default_args_dict.keys():
                default_args_est = get_all_defaultargs_from_estimator(get_uncalled_estimator(est))
                cls._default_args_dict[estimator_str] = default_args_est


class ParamGridDict:
    """ParamGridDict class for storing the paramgrids of the estimators."""

    _paramgrid_dict: Dict = {}

    @classmethod
    def get(cls, estimator_str):
        return cls._paramgrid_dict.get(estimator_str, {})

    @classmethod
    def get_all(cls):
        return cls._paramgrid_dict

    @classmethod
    def set(cls, estimator_str, paramgrid, inner_key=None):
        if not isinstance(paramgrid, dict):
            raise TypeError(f"paramgrid should be a dictionary, but is of type {type(paramgrid)}")
        if inner_key is not None:
            cls._paramgrid_dict.setdefault(estimator_str, {})[inner_key] = paramgrid
        else:
            cls._paramgrid_dict[estimator_str] = paramgrid
