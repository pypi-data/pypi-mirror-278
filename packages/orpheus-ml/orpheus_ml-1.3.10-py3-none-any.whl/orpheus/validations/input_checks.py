"""This module contains all the asserts used in the package."""

import math
from functools import partial
from typing import Callable, List, Optional, Dict, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit

from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.utils.custom_exceptions import DataPropertyMismatchError
from orpheus.utils.type_vars import CrossValidatorType, EstimatorType


class AttributeValidation:
    @staticmethod
    def validate_metric(metric: Callable[[pd.Series, pd.Series], float]):
        if not callable(metric):
            raise TypeError(f"metric must be a callable, but is {type(metric)}! Please provide a callable metric.")

    @staticmethod
    def validate_verbose(verbose: int):
        if not isinstance(verbose, int):
            raise TypeError(f"verbose must be an integer, but is {type(verbose)}! Please provide an integer verbose.")

    @staticmethod
    def validate_cv_obj(cv_obj: CrossValidatorType):
        if isinstance(cv_obj, type):
            raise TypeError(
                "cv_obj must be instantiated, but is not! Please provide an instantiated cv_obj argument from sklearn.model_selection."
            )
        if not issubclass(type(cv_obj), (BaseCrossValidator, BaseShuffleSplit)):
            raise TypeError(
                f"cv_obj must be a subclass of BaseCrossValidator or BaseShuffleSplit from sklearn.model_selection, but is {type(cv_obj)}! Please provide a valid cv_obj argument from sklearn.model_selection."
            )
        if not hasattr(cv_obj, "get_n_splits"):
            raise AttributeError(
                "cv_obj must have a get_n_splits method, but does not! Please provide a valid cv_obj argument from sklearn.model_selection."
            )

    @staticmethod
    def validate_type_estimator(type_estimator: str):
        if type_estimator not in {"regressor", "classifier"}:
            raise ValueError(
                f"Invalid type_estimator: {type_estimator}. Valid options are 'regressor' and 'classifier'."
            )

    @staticmethod
    def validate_estimator_list(estimator_list: List[EstimatorType]):
        if not isinstance(estimator_list, list):
            raise TypeError(
                f"estimator_list must be a list, but is {type(estimator_list)}! Please provide a valid estimator_list argument."
            )

        for estimator in estimator_list:
            # check if the estimator is a functools.partial instance
            if isinstance(estimator, partial):
                # get the function or class wrapped by functools.partial
                wrapped = estimator.func
            else:
                wrapped = estimator

            if not isinstance(wrapped, type):
                raise TypeError(
                    f"estimator_list must contain only types of estimators which are uninstantiated, which are not: {wrapped}"
                )

            if not issubclass(wrapped, BaseEstimator):
                raise TypeError(
                    f"estimator_list must contain only sklearn-valid estimators (which inherit from BaseEstimator), but contains non-sklearn-estimators: {wrapped}."
                )

    @staticmethod
    def validate_exclude_estimators(exclude_estimators: List[str]):
        """Validate the input list of strings for the exclude_estimators attribute
        found in several classes in the project."""
        if not isinstance(exclude_estimators, list):
            raise TypeError("exclude_estimators must be a list")
        if not all(isinstance(est, str) for est in exclude_estimators):
            raise TypeError("exclude_estimators must be a list of strings")

    @staticmethod
    def validate_config_path(config_path: str):
        """Validate the input string for the config_path attribute found
        in several classes in the project."""
        if not config_path or not isinstance(config_path, str):
            raise TypeError("config_path must be a non-empty string")
        if any(char in config_path for char in r':*?"<>|'):
            raise ValueError('config_path cannot contain any of the following characters: \\ / : * ? " < > |')

    @staticmethod
    def validate_categorical_features(df: pd.DataFrame, features: List[str]):
        """Validate that the features are in the dataframe."""
        if not isinstance(features, list):
            raise TypeError(f"features must be a list of strings, but is : {type(features)}")
        if not all(isinstance(feature, str) for feature in features):
            raise TypeError(f"features must be a list of strings, but is: {[type(feature) for feature in features]}")
        if not all(feature in df.columns for feature in features):
            features_not_in_df = [feature for feature in features if feature not in df.columns]
            raise ValueError(f"features {features_not_in_df} not found in dataframe columns")

    @staticmethod
    def validate_ordinal_features(df: pd.DataFrame, ordinal_features: Dict[str, List[str]]):
        """Validate that the features are in the dataframe."""
        if not isinstance(ordinal_features, dict):
            raise TypeError(f"ordinal_features must be a dict, but is: {type(ordinal_features)}")
        if not all(isinstance(feature, str) for feature in ordinal_features.keys()):
            raise TypeError(
                f"ordinal_features must be a list of strings, but is: {[type(feature) for feature in ordinal_features.keys()]}"
            )

        if not all(feature in df.columns for feature in ordinal_features):
            features_not_in_df = [feature for feature in ordinal_features if feature not in df.columns]
            raise ValueError(f"features {features_not_in_df} not found in dataframe columns")
        for col, values in ordinal_features.items():
            if not all(val in df[col].unique() for val in values):
                missing_values = [val for val in values if val not in df[col].unique()]
                raise ValueError(f"Missing values {missing_values} in column {col}.")


class DataValidation:
    @staticmethod
    def validate_single_output_y(y: pd.Series):
        if y.ndim != 1 and (y.ndim != 2 or y.shape[1] != 1):
            raise ValueError(
                f"y should be 1-dimensional, but has {y.ndim} dimensions! HyperTuner only accepts single-output."
            )

    @staticmethod
    def validate_array_is_not_3d(array: np.ndarray):
        if array.ndim == 3:
            raise ValueError(
                "array is 3d, but should be 2d! Consider changing array by array.reshape(array.shape[0], -1)"
            )

    @staticmethod
    def validate_xy_len(X, y):
        """Validate that X and y have the same number of rows."""
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"X and y must have the same number of rows! X: {X.shape[0]}, y: {y.shape[0]}.")

    @staticmethod
    def validate_xy_types(
        data_dict: Dict[str, Union[pd.DataFrame, pd.Series]], non_numerical_columns: Optional[List[str]] = None
    ):
        """
        Validate that the input arrays are of the correct type.
        Because it checks the names of the inputted variables,
        it can be flexibly reused in any other class.

        Parameters
        ----------
        arrs : dict
            Dictionary of arrays to validate. Keys are the names of the series/dataframes,
            values are the data themselves.
            NOTE:
            Assumes (case insensitive) names of the variables:
            start with x, _x, data, _data for dataframes,
            start with y, _y for series.

        non_numerical_columns : list[str]
            List of columns to exclude from the numerical columns check.
        """
        if non_numerical_columns is None:
            non_numerical_columns = []

        if (
            not isinstance(data_dict, dict)
            and not all(isinstance(var, str) for var in data_dict.keys())
            and not all(isinstance(arr, (pd.DataFrame, pd.Series)) for arr in data_dict.values())
        ):
            raise TypeError("arrs must be a dict with string keys and pd.DataFrame or pd.Series values")

        for var, arr in data_dict.items():
            # check types first:
            if var.lower().startswith(("x", "_x", "data", "_data")):
                DataValidation.validate_array_is_not_3d(arr)
                if not isinstance(arr, pd.DataFrame):
                    raise TypeError(f"{var} must be a pd.DataFrame, but is {type(arr)}")
                if any(not isinstance(col, str) for col in arr.columns):
                    raise ValueError(f"{var} must have string column names")
                arr_numerical = arr.drop(non_numerical_columns, axis=1, errors="ignore")
                assert (
                    arr_numerical.select_dtypes(exclude=["number"]).shape[1] == 0
                ), f"DataFrame contains non-numeric columns: {arr_numerical.dtypes[arr_numerical.dtypes != 'number'].index.tolist()}"

            elif var.lower().startswith(("y", "_y")):
                DataValidation.validate_single_output_y(arr)
                if not isinstance(arr, pd.Series):
                    raise TypeError(f"{var} must be a pd.Series, but is {type(arr)}")
                if not np.issubdtype(arr.dtype, np.number):
                    raise ValueError(f"{var} must be numerical, but contains non-numerical values")

            # check for nans and infs:
            if arr.isin([float("inf")]).any().any():
                raise ValueError(f"{var} contains inf values")
            if arr.isna().values.any():
                raise ValueError(f"{var} contains NaN values")

    @staticmethod
    def validate_that_column_exists(
        df: pd.DataFrame, column_name: Optional[str], exclude_column_names: Optional[List[str]] = None
    ):
        """Validate that a given column exists in the input dataframe,
        and is not included in the list of columns to exclude."""

        if exclude_column_names is None:
            exclude_column_names = []

        if column_name is not None:
            if not isinstance(column_name, str):
                raise TypeError("column_name must be a string or None")
            if column_name not in df.columns:
                raise ValueError(f"column_name {column_name} not found in dataframe columns")

        if not isinstance(exclude_column_names, list):
            raise TypeError("exclude_column_names must be a list of strings")

        if not all(isinstance(col, str) for col in exclude_column_names):
            raise TypeError("exclude_column_names must be a list of strings")

        if column_name in exclude_column_names:
            raise ValueError(f"column_name {column_name} found in exclude_column_names")

    @staticmethod
    def validate_complex_data(X):
        if np.iscomplexobj(X):
            raise ValueError("Complex data not supported")


class ClassValidation:
    @staticmethod
    def validate_performance_service(
        pipeline: MultiEstimatorPipeline, X_train: pd.DataFrame, X_val: pd.DataFrame, metric: Callable
    ):
        """Validate the PerformanceService parameters when setting the pipeline."""
        AttributeValidation.validate_metric(metric)
        if not isinstance(pipeline, MultiEstimatorPipeline):
            raise TypeError("The pipeline parameter must be of type MultiEstimatorPipeline.")
        if not isinstance(X_train, pd.DataFrame):
            raise TypeError("The X_train parameter must be of type pd.DataFrame.")
        if not isinstance(X_val, pd.DataFrame):
            raise TypeError("The X_val parameter must be of type pd.DataFrame.")

        tolerance = 1e-4
        X_train_mean = X_train.mean(numeric_only=True).mean()
        if not math.isclose(X_train_mean, pipeline.train_data_mean, rel_tol=tolerance):
            raise DataPropertyMismatchError(
                f"pipeline.train_data_mean {pipeline.train_data_mean} and X_train_mean {X_train_mean} do not match, indicating that the pipeline was not trained on the same data as the X_train parameter."
            )
        X_val_mean = X_val.mean(numeric_only=True).mean()
        if math.isclose(X_val_mean, pipeline.test_data_mean, rel_tol=tolerance):
            raise DataPropertyMismatchError(
                f"pipeline.test_data_mean {pipeline.test_data_mean} and X_val_mean {X_val_mean} match, indicating that X_val is the same as the testdata used to evaluate the pipeline on. Make sure to pass in a validation set of unseen data instead of the test set."
            )
