"""Scaling module for scaling data with different scalers."""

import traceback
import warnings
from functools import partial
from typing import Callable, List, Literal, Optional

import numpy as np
import pandas as pd

from orpheus.components.hypertuner.utils.helper_functions import (
    fit_estimators_parallel,
    get_estimator_scores,
    instantiate_estimator,
    pretty_print_errors,
)
from orpheus.components.preprocessing.constants import SCALERS
from orpheus.utils.type_vars import EstimatorType, ScalerType
from orpheus.utils.logger import logger
from orpheus.validations.input_checks import DataValidation
from orpheus.components.libs._base import _ComponentBase
from orpheus.utils.constants import DEFAULT_VALUES

warnings.filterwarnings("ignore")


class Scaling(_ComponentBase):
    """
    Scaling component. Use this component to scale data with different scalers and eventually transform data with best found scaler.

    Public methods
    ---
    scale()
        Test different scalers on X_train and eventually transform X_train with best found scaler.
    """

    def __init__(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.DataFrame,
        y_test: pd.DataFrame,
        scoring: Optional[Callable] = None,
        maximize_scoring: Optional[bool] = None,
        estimator_list: Optional[List[EstimatorType]] = None,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
        config_path: str = "",
    ):
        # no docstring for __init__ because it is inherited from _ComponentBase.
        # missing parameters in docstring: X_train, X_test, y_train, y_test
        super().__init__(
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            type_estimator=type_estimator,
            num_workers=num_workers,
            config_path=config_path,
        )
        DataValidation.validate_xy_len(X_train, y_train)
        DataValidation.validate_xy_len(X_test, y_test)
        DataValidation.validate_xy_types({"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test})
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.estimator_list = estimator_list

    def scale(
        self,
        timeout: int = 120,
        columns_to_scale: Optional[List[List[str]]] = None,
        compare_to_unscaled_data: bool = True,
        penalty_to_score_if_overfitting: float = 0.0,
        random_subset: float = 1.0,
        **kwargs_for_scaler,
    ) -> dict:
        """
        Test different scalers on X_train and eventually transform X_train with best found scaler.

        Estimators from self.estimator_list are fit per scaler.
        Scaler with best meanscore from estimators is chosen, and added to the pipeline of self.predict

        Parameters:
        ---
        timeout: int = 120
            N amount of seconds it will take to evaluate all scalers. Use this to get more control over total duration.
            timeout will be divided evenly over 7 scalers:
            [MinMaxScaler, MaxAbsScaler, StandardScaler, RobustScaler, Normalizer, QuantileTransformer, PowerTransformer].
            if timeout is None, all scalers will be evaluated without timeout.
            if timeout is 0, no scalers will be evaluated and method will end immediately.

        columns_to_scale: Optional[List[List]] = None
            Test different scalers only on specific groups of features of X_train and eventually transform same features in X_train with best found scaler.

        compare_to_unscaled_data: bool = True
            Also compare scaled data to unscaled (so where the data is not transformed). If unscaled data performs best, no scaling will take place.

        penalty_to_score_if_overfitting: float = 0.0
            NOTE: Using this parameter is only recommended for classification problems!
            It may happen that a specific value is overrepresented in y_pred, compared to self.y_test.
            This usually indicates overfitting and is especially a big problem in for example
            binary classificationmodels, which overfit to predict only one binary value, instead of two.
            To combat this problem, this parameter can be used.

            Interval between 0 and 1 (inclusive) to penalize score if
            ratio of unique values in y_pred diverges too much from self.y_test.
            The bigger the difference, the more the penalty exponentially grows
            and will punish bigger divergances from ratio of values in self.y_test.
        Raises:
            ValueError: if value not between 0 and 1.

        random_subset: float = 1.0
            if < 1.0, use a random subset of the data per iteration.
            This is useful when you have a lot of features or samples and want to speed up the process.

        *args_for_scaler, **kwargs_for_scaler:
            arguments/keyword-arguments which will be passed to each scaler, like: scaler(*args, **kwargs)

        returns
        ---
        X_train_scaled, X_test_scaled, best_scaler_  (can be single scaler or dict with key: list of columns, value: scaler)
        """
        if timeout == 0:
            return {}

        fitted_estimator_list = [est for est, _ in map(instantiate_estimator, self.estimator_list) if est is not None]
        if timeout is not None and columns_to_scale:
            logger.notice(
                f"columns_to_scale is specified: {columns_to_scale}.\nBased on length of columns_to_scale, increased timeout of self.scale() to {timeout} * {len(columns_to_scale)} = {timeout * len(columns_to_scale)} seconds",
            )
            timeout *= len(columns_to_scale)

        _scale_helper = partial(
            self._scale_helper,
            fitted_estimator_list=fitted_estimator_list,
            scalers=SCALERS.copy(),
            timeout=timeout,
            compare_to_unscaled_data=compare_to_unscaled_data,
            penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
            random_subset=random_subset,
            **kwargs_for_scaler,
        )

        if columns_to_scale:
            scaler_scores = {}

            for column_group in columns_to_scale:
                X_train_temp = self.X_train.loc[:, column_group]
                X_test_temp = self.X_test.loc[:, column_group]

                scores = _scale_helper(
                    X_train=X_train_temp, X_test=X_test_temp, y_train=self.y_train, y_test=self.y_test
                )

                scaler_scores.update({tuple(column_group): scores})
        else:
            scaler_scores = _scale_helper(
                X_train=self.X_train,
                X_test=self.X_test,
                y_train=self.y_train,
                y_test=self.y_test,
            )

        return scaler_scores

    def _scale_helper(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.DataFrame,
        y_test: pd.DataFrame,
        scalers: List[ScalerType],
        fitted_estimator_list: List[EstimatorType],
        timeout: int = 120,
        compare_to_unscaled_data: bool = True,
        penalty_to_score_if_overfitting: float = 0.0,
        random_subset: float = 1.0,
        **kwargs_for_scaler,
    ) -> dict:
        """
        helperfunction for self.scale()

        returns
        ---
        scaler_scores

        """
        if compare_to_unscaled_data:
            scalers.append(None)

        timeout_per_scaler = (
            np.true_divide(np.floor(timeout / len(scalers) * 10**1), 10**1) if timeout is not None else None
        )

        scaler_scores = {}
        X_train_scaled_dict = {}
        for scaler in scalers:
            if scaler is not None:
                try:
                    scaler: ScalerType = scaler(**kwargs_for_scaler)
                except Exception:
                    logger.error(
                        f"Could not instantiate {scaler} with kwargs: {kwargs_for_scaler} because of:\n{traceback.format_exc()}"
                    )
                    scaler: ScalerType = scaler()
                X_train_scaled = scaler.fit_transform(X_train.copy())
                X_test_scaled = scaler.transform(X_test.copy())

            returned_results = fit_estimators_parallel(
                timeout_per_scaler,
                fitted_estimator_list,
                num_workers=self.num_workers,
                X_train=X_train_scaled,
                y_train=y_train,
                random_subset=random_subset,
            )
            returned_estimators = [i for i in returned_results if not isinstance(i, list)]
            returned_errors = [i for i in returned_results if isinstance(i, list)]

            if returned_errors:
                pretty_print_errors(returned_errors)

            if not returned_estimators:
                raise ValueError(
                    f"No estimators where returned from {scaler}! Did you assign enough time to 'timeout', which is now set to {timeout}? Else, reduce the number of features in your data."
                )

            logger.notice(f"finished {scaler}")
            sorted_scores = get_estimator_scores(
                returned_estimators,
                X_test=X_test_scaled,
                y_test=y_test,
                scoring_func=self.scoring,
                maximize_scoring=self.maximize_scoring,
                penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
            )
            scaler_scores.update({scaler: sorted_scores})
            X_train_scaled_dict.update({scaler: X_train_scaled})

        return scaler_scores
