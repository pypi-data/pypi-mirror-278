"""Feature engineering module. Adding and removing features."""

import re
from itertools import combinations
from random import shuffle
from typing import Callable, List, Literal, Optional, Set

import featuretools as ft
import numpy as np
import pandas as pd

from orpheus.components.libs._base import _ComponentBase
from orpheus.utils.constants import DEFAULT_VALUES, ORDER_OF_ADDING
from orpheus.utils.logger import logger
from orpheus.utils.time_series import add_rolling_statistics, is_df_has_time_index
from orpheus.validations.converts import convert_n_jobs_to_num_workers
from orpheus.validations.input_checks import DataValidation


class FeatureAdding(_ComponentBase):
    """
    Add new features using featuretools. After adding features,

    Public methods
    ---
    sequential_order_of_adding()
        Add features in a specific order.

    add_features()
        Automatically add features to X using featuretools.

    add_rolling_stats()
        Add rolling statistics to X.

    add_lags()
        Add lags to X.
    """

    def __init__(
        self,
        y: pd.Series,
        config_path: str = "",
        scoring: Optional[Callable] = None,
        maximize_scoring: bool = True,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
        downcast: bool = False,
    ) -> None:
        # no docstring for __init__ because it is inherited from _ComponentBase.
        # missing parameters are in docstring: downcast, y
        super().__init__(
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            type_estimator=type_estimator,
            num_workers=num_workers,
            config_path=config_path,
        )
        DataValidation.validate_xy_types({"y": y})
        self.y = y
        self.downcast = downcast

        # Initialize attributes
        self._order: Optional[List[str]] = None  # used in self.sequential_order_of_adding
        self._columns_to_exclude_at_end_of_order_of_adding: Optional[
            List[str]
        ] = None  # used in self.sequential_order_of_adding
        self._col_for_lags_or_rolling_stats: Optional[str] = None  # used in self.add_lags and self.add_rolling_stats
        self._generated_features: Optional[str] = None  # used in self.add_features
        self._kept_features_after_cleaning: Optional[List[str]] = None  # used in self.add_features
        self._non_workable_columns: Set[str] = set()  # columns that need to be excluded from lags or rolling statistics
        self.leakage_prevention_slice: List[int] = [
            0,
            0,
        ]  # prevent data leakage by lags or rolling statistics

    def sequential_order_of_adding(
        self,
        _X: pd.DataFrame,
        order: List[str] = ORDER_OF_ADDING,
    ) -> pd.DataFrame:
        """
        Order of adding features for feature engineering.
        Convenience function to add features in a specific order.

        Parameters
        ----------
        _X : pd.DataFrame
            Data to add features to. Must be a pandas DataFrame.
            If firstly executed, adding features is added to self.pipeline_.

        order : list
            List of actions to perform in order.

        Returns
        -------
        _X : pd.DataFrame
        """
        DataValidation.validate_xy_types({"_X": _X})

        logger.notice("Adding features...")
        X = _X.copy()

        if self._order is None:
            self._order = order
            logger.notice(
                f"Order of adding features: {order}, added self._order to FeatureAdding object for future use."
            )

        has_time_index = is_df_has_time_index(X)
        if has_time_index:
            logger.notice("Time index is detected. Time-related features will be added.")
        else:
            logger.notice("Time index is not detected. Skipping the addition of time-related features.")

        POSSIBLE_ACTIONS = {
            "add_features": self.add_features,
            "add_lags": self.add_lags,
            "add_rolling_stats": self.add_rolling_stats,
        }

        for action in order:
            if action not in POSSIBLE_ACTIONS:
                raise ValueError(
                    f"Action {action} is not supported. Please choose from {list(POSSIBLE_ACTIONS.keys())}."
                )

            if (action == "add_lags" or action == "add_rolling_stats") and not has_time_index:
                logger.notice(f"Skipping {action}, because data does not have a time index...")
                continue

            logger.notice(f"{action.replace('_', ' ')}...")
            X = POSSIBLE_ACTIONS[action](X)

        # filter out redundant columns:
        if self._columns_to_exclude_at_end_of_order_of_adding is None:
            # remove columns with only one value:
            self._columns_to_exclude_at_end_of_order_of_adding = X.loc[:, X.nunique() > 1].columns

        return X[self._columns_to_exclude_at_end_of_order_of_adding]

    def add_features(
        self,
        _data: pd.DataFrame,
        max_added_features: int = -1,
        ignore_columns: Optional[List[str]] = None,
        **dfs_kwargs,
    ):
        """
        Automatically add features to X using featuretools.

        Parameters
        ----------
        _data : pd.DataFrame
            Data to add features to. Must be a pandas DataFrame.

        max_features : int, optional
            Maximum amount of features to add. If -1, all features will be added. The default is -1.

        ignore_columns : List[str], optional
            Columns to ignore when adding features. The default is None.


        Returns
        -------
        data : pd.DataFrame
            Data with added features.

        useful links
        ---
        https://docs.featuretools.com/en/stable/generated/featuretools.dfs.html
        https://featuretools.alteryx.com/en/stable/resources/frequently_asked_questions.html
        https://stackoverflow.com/questions/65448806/deep-feature-synthesis-depth-for-transformation-primitives-featuretools
        https://stackoverflow.com/questions/64799320/calculate-time-windowed-profiles-with-featuretools-dfs
        https://stackoverflow.com/questions/50639687/should-we-exclude-target-variable-from-dfs-in-featuretools
        """
        DataValidation.validate_xy_types({"_data": _data})

        if max_added_features != 0:
            data = _data.copy()

            feature_matrix = self._add_features(
                data,
                max_features=max_added_features,
                ignore_columns=ignore_columns,
                **dfs_kwargs,
            )

            # keep index of X after creating feature_matrix
            data: pd.DataFrame = feature_matrix.set_axis(data.index)

            # make sure all columns are kept after adding features
            if len(data.columns) != len(self._kept_features_after_cleaning):
                raise ValueError(
                    f"Not all columns are kept after adding features. Something went wrong. Difference in columns: {set(data.columns) - set(self._kept_features_after_cleaning)}"
                )
            logger.notice(
                f"Amount of features after self.add_features() in X: {data.shape[1]}",
            )

            # some inf values still seem to slip in between end of
            # self._add_features() and here. Not sure why.
            return data.fillna(0, axis=1).replace([np.inf, -np.inf], 0)

        else:
            logger.notice("Skipping adding features because max_features is 0...")
            return _data

    def add_rolling_stats(
        self,
        _data: pd.DataFrame,
        column_to_extract_stats_from: Optional[str] = None,
        lower_bound: int = 0,
        upper_bound: int = 0,
    ):
        """add rolling statistics as features to X."""
        return self._add_lags_or_rolling_stats(
            _data,
            "rolling_stats",
            column_to_extract_from=column_to_extract_stats_from,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def add_lags(
        self,
        _data: pd.DataFrame,
        column_to_extract_lags_from: Optional[str] = None,
        lower_bound: int = 0,
        upper_bound: int = 0,
    ):
        """Add lags as features to X."""
        return self._add_lags_or_rolling_stats(
            _data,
            "lags",
            column_to_extract_from=column_to_extract_lags_from,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def _add_lags_or_rolling_stats(
        self,
        _data: pd.DataFrame,
        method: Literal["lags", "rolling_stats"],
        column_to_extract_from: Optional[str] = None,
        lower_bound: int = 0,
        upper_bound: int = 0,
    ):
        DataValidation.validate_xy_types({"_data": _data})
        DataValidation.validate_that_column_exists(_data, column_to_extract_from, exclude_column_names=["all"])
        bounds_range = self._convert_bounds_to_range(lower_bound, upper_bound)

        if bounds_range is None:
            logger.notice(f"No {method} specified, skipping...")
            return _data

        # Set leakage prevention slice
        self.leakage_prevention_slice[method == "lags"] = max(bounds_range)

        data = _data.copy()
        if self._col_for_lags_or_rolling_stats is None:
            if column_to_extract_from is None:
                self._col_for_lags_or_rolling_stats = self._get_most_correlated_col_with_y(data, self.y)
            else:
                self._col_for_lags_or_rolling_stats = column_to_extract_from

        verbose_str = (
            f"column {self._col_for_lags_or_rolling_stats}"
            if self._col_for_lags_or_rolling_stats is not None and self._col_for_lags_or_rolling_stats.lower() != "all"
            else "all columns"
        )
        logger.notice(f"Adding {bounds_range} {method}s on basis of {verbose_str}...")

        data_columns = data.columns.copy(deep=True)
        data_columns = [col for col in data_columns if col not in self._non_workable_columns]

        if self._col_for_lags_or_rolling_stats is not None and self._col_for_lags_or_rolling_stats.lower() != "all":
            for bound in bounds_range:
                if method == "lags":
                    col_name = f"{self._col_for_lags_or_rolling_stats}_{method}_{bound}"
                    data[col_name] = data[self._col_for_lags_or_rolling_stats].shift(bound)
                else:
                    data = add_rolling_statistics(data, self._col_for_lags_or_rolling_stats, bound)
        else:
            for bound in bounds_range:
                for col in data_columns:
                    if method == "lags":
                        col_name = f"{col}_{method}_{bound}"
                        data[col_name] = data[col].shift(bound)
                    else:
                        data = add_rolling_statistics(data, col, bound)

        logger.notice(
            f"Amount of features after self.add_{method}() in data: {data.shape[1]}",
        )

        # columns that need to be excluded from lags or rolling statistics
        pattern = re.compile(rf".*_{method}_\d+$")
        for col in data.columns:
            if pattern.match(col):
                self._non_workable_columns.add(col)

        return data.fillna(0, axis=1)

    def _add_features(
        self,
        _data: pd.DataFrame,
        max_features: int,
        ignore_columns: List[str],
        **dfs_kwargs,
    ):
        """
        add features to data using `~dfs` from `~featuretools`

        Parameters
        ---

        return_types: list[ColumnSchema]:
            if one only wants to return numerical type in ft.dfs, set return_types = ColumnSchema(semantic_tags=["numeric"]
            see https://github.com/alteryx/featuretools/blob/main/featuretools/synthesis/deep_feature_synthesis.py for more info.
        """
        data = pd.DataFrame(_data) if not isinstance(_data, pd.DataFrame) else _data.copy()
        data.columns = data.columns.map(str)
        data_columns = data.columns
        es, data = self._get_entityset_and_frame(data, "data")

        if self._generated_features is None:
            if max_features >= 1:
                max_features += _data.shape[1]

            transformatives = ft.get_recommended_primitives(es)
            if ((len(transformatives) * data.shape[1]) > max_features) and (max_features > 0):
                # shuffle transformatives randomly if not all are used to make feature addition non-deterministic
                shuffle(transformatives)
                transformatives = transformatives[: (max_features - _data.shape[1])]
            logger.notice(
                f"Adding transformatives: {transformatives})",
            )
            non_faulty_features = self._find_faulty_features(
                max_features=max_features,
                ignore_columns=ignore_columns,
                transformatives=transformatives,
                dfs_kwargs=dfs_kwargs,
                es=es,
            )
            self._generated_features = ft.save_features(non_faulty_features)

        # CREATE FEATURE_MATRIX:

        # cutoff_time doesnt seem to have any effect on the feature matrix,
        # except for slowing down the process.
        generated_features = ft.load_features(self._generated_features)
        feature_matrix: pd.DataFrame = ft.calculate_feature_matrix(
            features=generated_features,
            entityset=es,
            n_jobs=1,  # n_jobs needs to be one here, was causing problems with multiprocessing in certain cases
            verbose=logger.get_verbose() > 0,
        )

        # CLEAN THE FEATURE MATRIX:
        cols_before_cleaning = feature_matrix.columns
        feature_matrix = self._clean_features(feature_matrix)
        logger.notice(
            f"removed {len(cols_before_cleaning) - len(feature_matrix.columns)} features after cleaning because they where not applicable.",
        )
        feature_matrix = self._change_columns_to_numeric(feature_matrix)

        for col in feature_matrix.columns:
            if col not in data_columns:
                self._non_workable_columns.add(col)

        return feature_matrix

    def _change_columns_to_numeric(self, feature_matrix: pd.DataFrame):
        # convert all boolean columns to INT
        boolean_columns = feature_matrix.columns[feature_matrix.dtypes == "boolean"]
        feature_matrix[boolean_columns] = feature_matrix[boolean_columns].astype(int)

        # convert all columns to numeric
        fcols = feature_matrix.select_dtypes("float").columns
        icols = feature_matrix.select_dtypes("integer").columns
        feature_matrix[fcols] = feature_matrix[fcols].apply(pd.to_numeric, downcast="float" if self.downcast else None)
        feature_matrix[icols] = feature_matrix[icols].apply(
            pd.to_numeric, downcast="integer" if self.downcast else None
        )

        # change all categorical columns to numeric:
        for col in feature_matrix.select_dtypes("category").columns:
            feature_matrix[col] = feature_matrix[col].cat.codes

        assert (
            feature_matrix.applymap(lambda x: isinstance(x, (int, float, complex))).all().all()
        ), "not all columns are numeric"

        return feature_matrix

    def _clean_features(self, feature_matrix: pd.DataFrame):
        if self._kept_features_after_cleaning is None:
            # remove columns which have same values for all rows as other
            feature_matrix = self._clean_columns_after_adding_features(feature_matrix)
            self._kept_features_after_cleaning = feature_matrix.columns
        else:
            feature_matrix = feature_matrix[self._kept_features_after_cleaning]

        return feature_matrix

    def _find_faulty_features(
        self,
        max_features,
        ignore_columns,
        transformatives,
        dfs_kwargs,
        es,
    ) -> List[ft.FeatureBase]:
        """
        Find faulty features and remove them from the feature matrix.
        Returns a list of non-faulty features"""
        features = ft.dfs(
            entityset=es,
            target_dataframe_name="data",
            trans_primitives=transformatives,
            max_features=max_features,
            max_depth=1,
            n_jobs=self.num_workers,
            ignore_columns=ignore_columns,
            features_only=True,
            **dfs_kwargs,
        )

        # Filter out faulty features
        non_faulty_features = []
        for idx, feat in enumerate(features, start=1):
            try:
                ft.calculate_feature_matrix([feat], es, n_jobs=1)
                non_faulty_features.append(feat)
                logger.info(f"{idx}/{len(features)} {feat} is valid")
            except Exception as e:
                logger.info(f"{idx}/{len(features)} {feat} is not valid")
                try:
                    logger.error(e)
                except TypeError:
                    pass

        return non_faulty_features

    def _get_entityset_and_frame(self, data: pd.DataFrame, df_name_for_entity: str):
        df = data.copy()
        if isinstance(df.index, pd.DatetimeIndex):
            time_index = df.index.name
            df.reset_index(inplace=True)
            df.rename(columns={time_index: "time"}, inplace=True)

        # make entityset:
        es = ft.EntitySet()
        es.add_dataframe(
            dataframe_name=df_name_for_entity,
            dataframe=df,
            make_index=True,
            index="instance_id",
            time_index=time_index if isinstance(df.index, pd.DatetimeIndex) else None,
        )

        return es, df

    def _clean_columns_after_adding_features(self, feature_matrix: pd.DataFrame):
        # remove cols with only one value:
        feature_matrix = feature_matrix.loc[:, feature_matrix.nunique() > 1]

        # find duplicate columns
        duplicate_cols = []
        for col1, col2 in combinations(feature_matrix.columns, 2):
            if feature_matrix[col1].equals(feature_matrix[col2]):
                duplicate_cols.append(col2)
        feature_matrix = feature_matrix.drop(duplicate_cols, axis=1)

        # replace all inf values with nan
        feature_matrix = feature_matrix.replace([np.inf, -np.inf], np.nan)

        # remove cols with at least 50% nans:
        feature_matrix = feature_matrix.dropna(thresh=feature_matrix.shape[0] * 0.5, axis=1)

        return feature_matrix

    def _convert_bounds_to_range(self, lower_bound: int, upper_bound: int) -> range:
        """
        Convert lower_bound and upper_bound to a valid range object. Upper bound is inclusive.
        """
        if lower_bound == 0 and upper_bound == 0:
            return None
        elif lower_bound < 0 or upper_bound < 0:
            raise ValueError(f"lower_bound and upper_bound must be positive, got {lower_bound} and {upper_bound}")
        elif upper_bound <= lower_bound:
            raise ValueError(f"upper_bound {upper_bound} must be greater than lower_bound {lower_bound}")
        elif lower_bound > 0:
            return range(lower_bound, upper_bound + 1)
        else:
            return range(1, upper_bound + 1)

    def _get_most_correlated_col_with_y(self, data: pd.DataFrame, y: pd.Series) -> str:
        """
        Get the pairwise correlation between the features and the target variable.
        Return the most correlated feature.
        """
        X = data.to_numpy()
        corr = np.corrcoef(X.T, y)
        corr = corr[:-1, -1]
        abs_correlations = np.abs(corr)
        max_corr_column = abs_correlations.argmax()
        most_correlated_feature = data.columns[max_corr_column]
        return most_correlated_feature

    def _transform(self, data: pd.DataFrame, n_jobs: Optional[int] = None):
        """Transforms the data by adding features."""
        DataValidation.validate_xy_types({"data": data})

        # temporarily reroute global verbositylevel to prevent any printing
        initial_verbosity_level = logger.get_verbose()
        logger.set_verbose(0)

        if n_jobs is not None:
            self.num_workers = convert_n_jobs_to_num_workers(n_jobs)

        # add_features pipeline
        if self._order is not None:
            data = self.sequential_order_of_adding(data, order=self._order)

        # turn on printing again
        logger.set_verbose(initial_verbosity_level)

        return data
