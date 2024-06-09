"""Feature engineering module. Adding and removing features."""

from functools import partial
from typing import Callable, List, Literal, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import RFECV, SelectKBest, f_classif, f_regression
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV, cross_val_score

from orpheus.components.hypertuner.utils.helper_functions import create_random_indices
from orpheus.components.libs._base import _ComponentBase
from orpheus.utils.constants import DEFAULT_VALUES, ORDER_OF_REMOVING
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import EstimatorType
from orpheus.validations.converts import convert_n_jobs_to_num_workers
from orpheus.validations.input_checks import DataValidation
from orpheus.utils.warnings import _warn_error_metrics_and_cross_val_score


class FeatureRemoving(_ComponentBase):
    """
    Class for removing features from a dataset.

    Public methods
    ---
    sequential_order_of_removing()
        Order of removing features for feature engineering.
        Convenience function to remove features in a specific order.

    remove_features_by_correlation()
        Remove highly correlated features from X which also have low correlation to the target.

    remove_features_by_selection()
        determine the optimal stopping point in terms of number of features using Recursive feature elimination
        with cross-validation in combination with a RandomForest estimator.

    remove_features_by_top_n()
        Quick and dirty feature selection using SelectKBest from sklearn.feature_selection.
    """

    def __init__(
        self,
        config_path: str = "",
        scoring: Optional[Callable] = None,
        maximize_scoring: bool = True,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
        downcast: bool = False,
    ) -> None:
        # no docstring for __init__ because it is inherited from _ComponentBase.
        # missing parameters in docstring: downcast, y

        if scoring is not None:
            scoring = make_scorer(scoring, greater_is_better=maximize_scoring)
        else:
            scoring = None

        # initialize _ComponentBase
        super().__init__(
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            type_estimator=type_estimator,
            num_workers=num_workers,
            config_path=config_path,
        )
        self.downcast = downcast

        # Initialize attributes
        self._order = None
        self._kept_features_by_correlation = None
        self._kept_features_by_selection = None
        self._kept_features_by_top_n = None

    def sequential_order_of_removing(
        self,
        _X: pd.DataFrame,
        _y: pd.Series,
        _cv_obj,
        _estimator: Optional[EstimatorType] = None,
        order: List[str] = ORDER_OF_REMOVING,
        use_scoring_for_random_forest_selection: bool = True,
        random_subset: float = 1.0,
    ) -> pd.DataFrame:
        """
        Order of removing features.
        Convenience function to remove features in a specific order.

        Parameters
        ----------
        _X : pd.DataFrame
            Data to remove features from. Must be a pandas DataFrame.
            If firstly executed, removing features is added to self.pipeline_.

        _y : pd.Series
            Target data. Must be a pandas Series.

        _cv_obj : cross_validation object from sklearn.model_selection.

        _estimator : EstimatorType, optional
            Estimator to use for removing features. If None, a RandomForestClassifier or RandomForestRegressor will be used.

        order : list
            List of actions to perform in order.

        use_scoring_for_random_forest_selection : bool, optional
            Whether to use self.scoring or None for selecting a RandomForest estimator if no _estimator is given.
            If False, the default scoring of the RandomForest-estimator (R2 or accuracy) will be used.

        random_subset : float, optional
            If < 1.0, a random subset of the data will be used to remove features.

        Returns
        -------
        _X : pd.DataFrame
        """
        DataValidation.validate_xy_types({"_X": _X, "_y": _y})
        logger.notice("Removing features...")

        if random_subset < 1.0:
            logger.notice(f"Using a random subset of {random_subset*100:.2f}% of the data to remove features...")
            random_indices = create_random_indices(_X, random_subset)
            X = _X.copy().iloc[random_indices, :]
            y = _y.copy().iloc[random_indices]
        else:
            X = _X.copy()
            y = _y.copy()

        if self._order is None:
            self._order = order
            logger.notice(
                f"Order of removing features: {order}, added self._order to FeatureRemoving object for future use."
            )

        POSSIBLE_ACTIONS = {
            "remove_features_by_correlation": partial(
                self.remove_features_by_correlation,
                _y=y,
                _estimator=_estimator,
                _use_scoring_for_random_forest_selection=use_scoring_for_random_forest_selection,
                _cv_obj=_cv_obj,
            ),
            "remove_features_by_selection": partial(
                self.remove_features_by_selection,
                _y=y,
                _estimator=_estimator,
                _use_scoring_for_random_forest_selection=use_scoring_for_random_forest_selection,
                _cv_obj=_cv_obj,
            ),
            "remove_features_by_top_n": partial(
                self.remove_features_by_top_n,
                _y=y,
            ),
        }

        for action in order:
            if action not in POSSIBLE_ACTIONS:
                raise ValueError(
                    f"Action {action} is not supported. Please choose from {list(POSSIBLE_ACTIONS.keys())}."
                )
            logger.notice(f"{action.replace('_', ' ')}...")
            X = POSSIBLE_ACTIONS[action](X)

        return _X.loc[:, X.columns]

    def remove_features_by_correlation(
        self,
        _X: pd.DataFrame,
        _y: pd.Series,
        _cv_obj,
        _estimator: Optional[EstimatorType] = None,
        _use_scoring_for_random_forest_selection: bool = True,
        n_steps: int = 10,
        min_features_to_keep: int = 5,
        early_stopping: bool = False,
    ):
        """
        Remove highly correlated features from X which also have low correlation to the target.
        To address multicollinearity.
        Removes features with correlation >= threshold with other features and correlation <= (1-threshold) with y.

        Parameters
        ----------
        n_steps: int, optional
            Number of steps to explore the correlation searchspace between 0 and 1. The default is 10.

        early_stopping: bool, optional
            Whether to stop the search for the best threshold when the current score is worse than the previous score.

        Returns
        -------
        data : pd.DataFrame
        """
        DataValidation.validate_xy_types({"_X": _X, "_y": _y})
        _warn_error_metrics_and_cross_val_score(self.scoring)

        # get correlation of features with target:
        corr_with_y = abs(_X.corrwith(_y))
        search_space = np.linspace(1.0, 0.05, n_steps)
        estimator = self._select_estimator_for_removing_features(
            _estimator, _X, _y, _cv_obj, _use_scoring_for_random_forest_selection
        )
        # create baseline score with all features:
        last_score = cross_val_score(
            estimator,
            _X,
            _y,
            cv=_cv_obj,
            scoring=self.scoring,
            n_jobs=self.num_workers,
            verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
        ).mean()

        logger.notice(f"Correlation baseline score with all features: {last_score}")
        result_dict = {search_space[0]: {"score": last_score, "features": _X.columns}}

        for threshold in search_space[1:]:
            _X_temp = self._remove_features_by_correlation(_X.copy(), corr_with_y, threshold)
            if _X_temp is None:
                logger.notice(
                    f"No features are lower than {((1-threshold) * 100):.2f} % correlated with y, so no features are removed. Skipping threshold {threshold:.4f}...",
                )
                continue
            elif len(_X_temp.columns) == len(_X.columns):
                logger.notice(f"None of the current features changed. Skipping threshold {threshold}...")
                continue
            elif len(_X_temp.columns) < min_features_to_keep:
                logger.notice(
                    f"Number of features after removing correlated features is lower than min_features. Skipping threshold {threshold:.4f}..."
                )
                continue
            train_score = cross_val_score(
                estimator,
                _X_temp,
                _y,
                cv=_cv_obj,
                scoring=self.scoring,
                n_jobs=self.num_workers,
                verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
            ).mean()
            logger.notice(f"Correlation threshold: {threshold}, score: {train_score}")
            result_dict[threshold] = {"score": train_score, "features": _X_temp.columns}
            if early_stopping:
                if self.maximize_scoring:
                    if train_score > last_score:
                        last_score = train_score
                    else:
                        logger.notice("Early stopping...")
                        break
                else:
                    if train_score < last_score:
                        last_score = train_score
                    else:
                        logger.notice("Early stopping...")
                        break

        result_df = pd.DataFrame(result_dict).T.sort_values(by="score", ascending=not self.maximize_scoring)
        best_threshold = result_df.index[0]
        self._kept_features_by_correlation = result_df.loc[best_threshold]["features"].to_list()

        logger.notice(
            f"Best correlation threshold: {best_threshold:.4f} with score: {result_df.loc[best_threshold]['score']}"
        )
        logger.notice(
            f"Amount of features after self.remove_features_by_correlation() in X: {len(self._kept_features_by_correlation)}",
        )

        return _X[self._kept_features_by_correlation]

    def remove_features_by_selection(
        self,
        _X: pd.DataFrame,
        _y: pd.Series,
        _cv_obj,
        _estimator: Optional[EstimatorType] = None,
        _use_scoring_for_random_forest_selection: bool = True,
        n_steps_per_iter: int = 1,
        min_features_to_keep: int = 1,
        top_n_features: Union[int, float] = -1,
        plotting: bool = False,
    ) -> pd.DataFrame:
        """
        determine the optimal stopping point in
        terms of number of features using Recursive feature elimination
        with cross-validation in combination with a RandomForest estimator.

        For scoring, self.scoring will be used if not None.

        NOTE: if amount of features is big, this can take a while!
        To decrease waiting time:
        - increase 'step'
        - increase 'min_features_to_keep'
        - decrease 'cv'

        creates attributes
        ---

        self.feature_selector_
            access more detailed information about selected features, eg. by:\n
            self.feature_selector_.ranking_\n
            self.feature_selector_.grid_scores_\n
            self.feature_selector_.cv_results_

            Object belongs to `~sklearn.feature_selection.RFECV`

        info about `~sklearn.feature_selection.RFECV` :
        https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html

        info about Feature Selection approach:
        https://www.yourdatateacher.com/2021/10/11/feature-selection-with-random-forest/#:~:text=What%20is%20a%20Random%20Forest,to%20fit%20a%20decision%20tree

        Parameters
        ---
        estimator: Optional[EstimatorType], default = RandomForestClassifier / RandomForestRegressor
            Optionally insert an estimator which will select optimal N features.
            Estimator needs to be passed instantiated!
            If None is given, default is RandomForestClassifier / RandomForestRegressor.

        _cv_obj : int, cross-validation generator or an iterable, default=2
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - integer, to specify the number of folds.
            - :term:`CV splitter`,
            - An iterable yielding (train, test) splits as arrays of indices.

            For integer inputs, if ``y`` is binary or multiclass,
            :class:`~sklearn.model_selection.StratifiedKFold` is used. If the
            estimator is a classifier or if ``y`` is neither binary nor multiclass,
            :class:`~sklearn.model_selection.KFold` is used.

        n_steps_per_iter : int or float, default=1
            If greater than or equal to 1, then step corresponds to
            the (integer) number of features to remove at each iteration.
            If within (0.0, 1.0), then step corresponds to
            the percentage (rounded down) of features to remove at each iteration.
            Note that the last iteration may remove fewer than step features in order to
            reach min_features_to_keep.

        min_features_to_keep : int, default=2
            The minimum number of features to be selected.
            This number of features will always be left in the dataset, although more features may also remain.,
            even if the difference between the original feature count and
            min_features_to_keep isn't divisible by step.

        cv : int, cross-validation generator or an iterable, default=2
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - integer, to specify the number of folds.
            - :term:`CV splitter`,
            - An iterable yielding (train, test) splits as arrays of indices.

            For integer inputs, if ``y`` is binary or multiclass,
            :class:`~sklearn.model_selection.StratifiedKFold` is used. If the
            estimator is a classifier or if ``y`` is neither binary nor multiclass,
            :class:`~sklearn.model_selection.KFold` is used.

        plotting : bool, default=False
            Whether to plot the results of the feature selection.
            Gives an insight in which features where most important and
            the cross-validation score for each iteration.

        returns
        ---
        X : pd.DataFrame

        """
        DataValidation.validate_xy_types({"_X": _X, "_y": _y})

        top_n_features = self._sanitize_top_n_features(_X, top_n_features)

        X = _X.copy()
        logger.notice(f"Removing features by Recursive Feature Elimination with n_jobs={self.num_workers}...")
        X_features = X.columns

        estimator = self._select_estimator_for_removing_features(
            _estimator, X, _y, _cv_obj, _use_scoring_for_random_forest_selection
        )
        logger.notice(f"Estimator used for feature selection: {estimator}")

        self.feature_selector_ = RFECV(
            estimator=estimator,
            step=n_steps_per_iter,
            scoring=self.scoring,
            cv=_cv_obj,
            min_features_to_select=min_features_to_keep,
            n_jobs=self.num_workers,
            verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
        )

        self.feature_selector_.fit(X, _y)
        self._kept_features_by_selection: List[str] = X.columns[self.feature_selector_.get_support()].to_list()
        ranking_dict = dict(zip(X.columns, self.feature_selector_.ranking_))
        ranking_df = pd.DataFrame(data=ranking_dict.items(), columns=["Feature", "Ranking"])
        ranking_df = ranking_df.sort_values(by="Ranking", ascending=True)
        logger.info("Ranking of features:")
        logger.info(ranking_df.to_string(index=False))

        # transform X:
        len_cols_old = X.shape[-1]
        X = X.loc[:, self._kept_features_by_selection]
        logger.notice(f"Kept features: {self._kept_features_by_selection}")
        logger.notice(f"Removed features: {[ i for i in X_features if i not in self._kept_features_by_selection]}")
        len_cols_new = X.shape[-1]
        logger.notice(f"removed {len_cols_old-len_cols_new}/{len_cols_old} features by feature selection.")

        # print feature importances:
        feature_importances_df = self._get_feature_importances(X, estimator)
        logger.notice(f"Feature importances:\n{feature_importances_df.to_string(index=False)}")

        # plot feature importances and optimal number of features:
        if plotting:
            self._plot_optimal_num_of_feats(min_features_to_keep, self.feature_selector_)
            self._plot_feature_importances(feature_importances_df=feature_importances_df)

        if top_n_features == -1:
            logger.notice("top_n_features is -1. Skipping remove_features_by_top_n...")
        else:
            if top_n_features >= X.shape[1]:
                logger.notice(
                    f"top_n_features ({top_n_features}) is larger than or equal to number of features ({X.shape[1]}), skipping...",
                )
                return X
            if feature_importances_df.empty:
                logger.warning(
                    f"feature_importances_df is empty, meaning that estimator has no attribute feature_importances_. Removing top {top_n_features} features on index instead..."
                )
                self._kept_features_by_selection = self._kept_features_by_selection[:top_n_features]
                return X.iloc[:, :top_n_features]
            self._kept_features_by_selection = feature_importances_df["Feature"].iloc[:top_n_features].to_list()
            logger.notice(f"Keeping only top {top_n_features} features: {self._kept_features_by_selection}")
            X = X.loc[:, self._kept_features_by_selection]

        return X

    def remove_features_by_top_n(
        self,
        _X: pd.DataFrame,
        _y: pd.Series,
        top_n_features: Union[int, float] = -1,
    ) -> pd.DataFrame:
        """
        Quick and dirty feature selection using SelectKBest from sklearn.feature_selection.
        """
        if top_n_features == -1:
            logger.notice("top_n_features is -1. Skipping remove_features_by_top_n...")
            return _X

        DataValidation.validate_xy_types({"_X": _X})

        top_n_features = self._sanitize_top_n_features(_X, top_n_features)

        if top_n_features > _X.shape[1]:
            logger.notice(
                f"top_n_features ({top_n_features}) is larger than number of features ({_X.shape[1]}), skipping...",
            )
            return _X

        logger.notice(f"Keeping only top {top_n_features} features...")
        score_func = f_classif if self.type_estimator == "regressor" else f_regression
        selector = SelectKBest(score_func=score_func, k=top_n_features)
        selector.fit(_X, _y)
        self._kept_features_by_top_n = _X.columns[selector.get_support()].to_list()
        selected_data = _X.loc[:, self._kept_features_by_top_n]
        logger.notice(
            f"Amount of features after self.remove_features_by_top_n() in X: {selected_data.shape[1]}",
        )
        return selected_data

    def _remove_features_by_correlation(self, _X, corr_with_y, threshold):
        non_correlated_features_with_y = (corr_with_y <= (1 - threshold)).to_numpy().nonzero()[0]
        if not any(non_correlated_features_with_y):
            return None
        corr_matrix = _X.corr().abs()
        np_corr_matrix = corr_matrix.to_numpy()

        # Create a boolean mask to filter out upper triangular matrix
        mask = np.triu(np.ones_like(np_corr_matrix, dtype=bool), k=1)

        # Get the coordinates (row and column indices) of elements with correlation above the threshold
        coords = np.column_stack(np.where((np_corr_matrix >= threshold) & mask))

        # Get unique column indices to remove
        columns_to_remove = np.unique(coords[:, 1])
        columns_to_remove = np.intersect1d(columns_to_remove, non_correlated_features_with_y)

        return _X.drop(columns=_X.columns[columns_to_remove])

    def _select_estimator_for_removing_features(
        self,
        estimator: EstimatorType,
        X,
        y,
        _cv_obj,
        _use_scoring_for_random_forest_selection,
    ):
        if estimator is None:
            estimator = RandomForestClassifier() if self.type_estimator == "classifier" else RandomForestRegressor()
            estimator = self._find_best_random_forest_estimator(
                estimator, X, y, _cv_obj, _use_scoring_for_random_forest_selection
            )
        else:
            # check if estimator is instantiated:
            if isinstance(estimator, type):
                raise TypeError(f"{estimator} was passed uninstantiated. Please pass instantiated estimator!")

        return estimator

    def _find_best_random_forest_estimator(
        self, estimator, X, y, _cv_obj, _use_scoring_for_random_forest_selection
    ) -> EstimatorType:
        """Find the best randomforest estimator by using RandomizedSearchCV."""
        if self.type_estimator == "classifier":
            param_grid = {
                "n_estimators": [100, 200, 500],
                "max_features": ["auto", "sqrt", "log2"],
                "max_depth": [4, 6, 8, 10],
                "criterion": ["gini", "entropy"],
            }
        else:
            param_grid = {
                "n_estimators": [100, 200, 500],
                "max_features": ["auto", "sqrt", "log2"],
                "max_depth": [4, 6, 8, 10],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            }

        grid_search = RandomizedSearchCV(
            estimator,
            param_grid,
            cv=_cv_obj,
            n_jobs=self.num_workers,
            verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
            scoring=self.scoring if _use_scoring_for_random_forest_selection else None,
            refit=True,
            n_iter=max(10, self.num_workers * 2),
        )

        grid_search.fit(X, y)
        estimator = grid_search.best_estimator_
        logger.notice(f"Best found randomforest estimator using RandomizedSearchCV: {estimator}")
        logger.notice(f"Best found randomforest estimator score using RandomizedSearchCV: {grid_search.best_score_}")
        logger.notice(
            f"All scores randomforest estimator using RandomizedSearchCV: {grid_search.cv_results_['mean_test_score']}"
        )
        return estimator

    def _plot_feature_importances(self, feature_importances_df: pd.DataFrame) -> None:
        """Plot feature importances."""
        feature_importances_df = feature_importances_df[::-1]
        features = feature_importances_df["Feature"]
        importances = feature_importances_df["Importance"]

        # Create the bar plot
        plt.barh(features, importances)
        plt.title("Feature Importances")
        plt.xlabel("Importance (% of maximum)")
        plt.ylabel("Feature")
        plt.show()

    def _get_feature_importances(self, X: pd.DataFrame, estimator: EstimatorType) -> pd.DataFrame:
        if not hasattr(estimator, "feature_importances_"):
            logger.warning(f"Estimator {estimator} has no attribute feature_importances_")
            return pd.DataFrame(columns=["Feature", "Importance"])

        importances = estimator.feature_importances_
        importances_dict = dict(zip(X.columns, importances))

        # Sort the feature importances by their ranking
        sorted_importances = dict(sorted(importances_dict.items(), key=lambda item: -item[1]))

        feature_importances_df = pd.DataFrame(sorted_importances.items(), columns=["Feature", "Importance"])
        feature_importances_df["Importance"] = feature_importances_df["Importance"].map(lambda x: f"{x * 100:.2f} %")
        return feature_importances_df

    def _plot_optimal_num_of_feats(self, min_features_to_keep: int, feature_selector_: RFECV) -> None:
        logger.notice(f"Optimal number of features : {feature_selector_.n_features_}")
        # Plot number of features VS. cross-validation scores
        plt.figure()
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation score")

        test_scores = feature_selector_.cv_results_["mean_test_score"]
        plt.plot(
            range(
                min_features_to_keep,
                len(test_scores) + min_features_to_keep,
            ),
            test_scores,
        )

        # Set the x-axis ticks to be whole numbers
        plt.xticks(
            range(
                min_features_to_keep,
                len(test_scores) + min_features_to_keep,
            )
        )

        plt.show()

    def _sanitize_top_n_features(self, _X, top_n_features) -> int:
        if isinstance(top_n_features, float) and 0 < top_n_features <= 1:
            top_n_features = int(top_n_features * _X.shape[1])

        return top_n_features

    def _transform(
        self,
        data: pd.DataFrame,
        n_jobs: Optional[int] = None,
    ):
        """Transforms the data by removing features."""
        DataValidation.validate_xy_types({"data": data})

        # temporarily set verbosity level to 0 to prevent printing
        initial_verbosity_level = logger.get_verbose()
        logger.set_verbose(0)

        if n_jobs is not None:
            self.num_workers = convert_n_jobs_to_num_workers(n_jobs)

        if self._order is not None:
            # search for list with the lowest length, which are the remaining features.
            cols_to_keep = [
                lst
                for lst in [
                    self._kept_features_by_correlation,
                    self._kept_features_by_selection,
                    self._kept_features_by_top_n,
                ]
                if lst is not None
            ]

            if cols_to_keep != []:
                cols_to_keep = min(cols_to_keep, key=len)
                data = data.loc[:, cols_to_keep]

        # reset verbosity level
        logger.set_verbose(initial_verbosity_level)

        return data
