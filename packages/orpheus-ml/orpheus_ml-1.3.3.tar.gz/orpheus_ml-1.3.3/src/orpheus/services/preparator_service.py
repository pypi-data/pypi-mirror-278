"""Preperator Service Module. Service for preparing data for modeling."""

from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import (
    KFold,
    StratifiedKFold,
    StratifiedShuffleSplit,
    TimeSeriesSplit,
    train_test_split,
)

from orpheus.utils.helper_functions import target_is_classifier
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import CrossValidatorType


class PreparatorService:
    """
    Preperator Service Class. Service for preparing data for modeling.


    Public Methods
    --------------
    split_data
        Split data into train, test and optional validation sets.

    select_cross_validator
        Select cross validator based on the input data X and y.
    """

    def __init__(self, X: pd.DataFrame, y: pd.Series, verbose: int = 1):
        """
        Initialize the PreparatorService class.

        Parameters
        ----------
        X : array-like
            Features data.
        y : array-like
            Target data.
        """
        self._X = X
        self._y = y
        self.is_regression = not target_is_classifier(y)
        logger.set_verbose(verbose)

    @property
    def X(self):
        return self._X

    @property
    def y(self):
        return self._y

    @staticmethod
    def split_data(
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        val_size: float = 0.05,
        shuffle: bool = False,
        random_state: Optional[int] = None,
        stratify: bool = False,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """
        Split data into train, test, and optional validation sets.

        Parameters
        ----------
        test_size : float, default: 0.2
            Proportion of the dataset to include in the test split.
        val_size : float, default: 0.05
            Proportion of the dataset to include in the validation split.
        shuffle : bool, optional, default: False
            Whether or not to shuffle the data before splitting.
        random_state : int or RandomState instance, optional, default: None
            Controls the randomness of the training and testing indices produced.
        stratify: bool, default: False
            If True, data is split in a stratified fashion, using this as the class labels.

        Returns
        -------
        X_train, X_test, X_val, y_train, y_test, y_val: array-like
            The split feature and target data.
        """

        stratify_array = y if stratify else None

        X_train, X_test_val, y_train, y_test_val = train_test_split(
            X,
            y,
            test_size=test_size + val_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=stratify_array,
        )

        test_val_size = val_size / (test_size + val_size)
        X_test, X_val, y_test, y_val = train_test_split(
            X_test_val,
            y_test_val,
            test_size=test_val_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=y_test_val if stratify else None,
        )

        return X_train, X_test, X_val, y_train, y_test, y_val

    def select_cross_validator(
        self,
        n_splits: int = 5,
        shuffle: bool = False,
        random_state: Optional[int] = None,
        time_series_gap: int = 0,
        imbalanced_classes_threshold: float = 0.1,
        min_samples_per_group: int = 2,
    ) -> CrossValidatorType:
        """
        Select the most appropriate cross-validator based on the attributes X and y.

        Parameters:
        - n_splits (int): Number of folds. Must be at least 2.
        - shuffle (bool): Whether to shuffle the data before splitting into batches.
        - random_state (int, RandomState instance or None, optional): If int, random_state is the seed used by the random number generator;
        - time_series_gap (int): Gap between test and train for TimeSeriesSplit
        - imbalanced_classes_threshold (float): Threshold to determine if the classes are imbalanced.
        - min_samples_per_group (int): Minimum number of samples required for each group when using TimeSeriesSplit.

        Returns:
        - cv (CrossValidatorType): A cross-validator object.
        """

        is_time_series = isinstance(self.X.index, pd.DatetimeIndex)

        if is_time_series:
            if min_samples_per_group * n_splits > len(self.y):
                raise ValueError("Not enough samples for the specified number of splits and minimum samples per group.")
            cv = TimeSeriesSplit(n_splits=n_splits, gap=time_series_gap)

        elif not self.is_regression:
            is_binary_classification = len(np.unique(self.y)) == 2
            is_imbalanced = self._is_imbalanced(self.y, threshold=imbalanced_classes_threshold)

            if is_imbalanced or is_binary_classification:
                cv = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
            else:
                cv = StratifiedShuffleSplit(n_splits=n_splits, random_state=random_state)

        else:  # Regression
            cv = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)

        logger.notice(f"Chosen cross-validation: {cv}")

        return cv

    def _is_imbalanced(self, y: pd.Series, threshold: float = 0.1) -> bool:
        """Check if the target is imbalanced."""
        if isinstance(y, pd.Series):
            y = y.to_numpy()
        counts = np.bincount(y) if np.issubdtype(y.dtype, np.integer) else np.unique(y, return_counts=True)[1]
        max_count = np.max(counts)
        min_count = np.min(counts)
        return (max_count - min_count) / max_count > threshold
