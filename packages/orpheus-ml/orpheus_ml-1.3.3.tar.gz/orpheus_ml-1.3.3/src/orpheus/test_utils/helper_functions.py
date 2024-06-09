import numpy as np
from sklearn.utils.validation import check_is_fitted
from orpheus.utils.type_vars import ScalerType, EstimatorType


def arr_equality_msg(arr1, arr2):
    """
    Return a message describing the equality of two arrays.

    Usage:
    >>> import numpy as np

    >>> self.assertTrue(np.array_equal(arr1, arr2),
        msg=arr_equality_msg(arr1, arr2),)
    """
    shape_equality = arr1.shape == arr2.shape
    value_equality = np.array_equal(arr1, arr2) if shape_equality else False

    msg = f"Arrays are not equal. Shape Equality: {shape_equality}, Value Equality: {value_equality}, "
    msg += f"Dtype of arr1: {arr1.dtype}, "
    msg += f"Dtype of arr2: {arr2.dtype}, "
    msg += f"Shape of arr1: {arr1.shape}, "
    msg += f"Shape of arr2: {arr2.shape}"

    return msg


def scalers_are_equal(scaler1: ScalerType, scaler2: ScalerType) -> bool:
    """compare 2 fitted scalers for equality"""
    if not hasattr(scaler1, "mean_"):
        raise ValueError(f"scaler1 {scaler1} is not fitted yet!")

    if not hasattr(scaler2, "mean_"):
        raise ValueError(f"scaler2 {scaler2} is not fitted yet!")

    return (
        np.allclose(scaler1.scale_, scaler2.scale_)
        and np.allclose(scaler1.mean_, scaler2.mean_)
        and np.allclose(scaler1.var_, scaler2.var_)
    )


def estimators_are_equal(estimator1: EstimatorType, estimator2: EstimatorType) -> bool:
    """compare 2 fitted estimators for equality"""
    check_is_fitted(estimator1)
    check_is_fitted(estimator2)

    return estimator1.get_params() == estimator2.get_params()
