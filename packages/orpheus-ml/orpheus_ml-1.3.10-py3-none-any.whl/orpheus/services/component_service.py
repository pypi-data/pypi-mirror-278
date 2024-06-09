"""ComponentService class for data preprocessing and model training and creation of a pipeline.
Basicly everything needed to perform a machine learning task in one place."""

import os
import sys
import traceback
from copy import deepcopy
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruamel.yaml
import schema
from numpy.testing import assert_array_equal
from sklearn import set_config
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, train_test_split

from orpheus.components.hypertuner.hypertuner import HyperTuner
from orpheus.components.hypertuner.hypertuner_stacked import HyperTunerStacked
from orpheus.components.hypertuner.utils.helper_functions import (
    check_estimator_list,
    check_scoring,
    check_type_estimator,
)
from orpheus.components.libs.config_manager import ConfigManager
from orpheus.components.preprocessing.feature_adding import FeatureAdding
from orpheus.components.preprocessing.feature_removing import FeatureRemoving
from orpheus.components.preprocessing.scaling import Scaling
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.services.utils.decorators import initialize_check
from orpheus.services.utils.helper_functions import find_optimal_n_splits
from orpheus.services.utils.private_functions import (
    _create_hypertuners,
    _create_preprocessing_pipeline,
    _deploy_pipeline_of_stacked_models,
    _encode_non_numerical_features,
    _optimize_estimator_list_order,
    _stacked_predict_range,
)
from orpheus.utils.constants import DEFAULT_VALUES
from orpheus.utils.context_managers import FunctionTimeoutHandler
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.utils.custom_types import PredictorType
from orpheus.utils.helper_functions import get_obj_name, optimize_splits_and_test_size, standardize_config_path_to_yaml
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import CrossValidatorType, EstimatorType
from orpheus.validations.config_schema import config_schema, validate_bounds_FeatureAdding
from orpheus.validations.converts import convert_cross_platform_path, convert_n_jobs_to_num_workers
from orpheus.validations.input_checks import AttributeValidation, DataValidation

# set output of all transformers to pandas dataframes instead of numpy arrays
set_config(transform_output="pandas")


class ComponentService:
    """
    Central class for data preprocessing, hyperparameter tuning, model training, and pipeline creation.
    This class provides a streamlined interface for executing end-to-end machine learning tasks.

    Usage
    -----
    1. Instantiate the `ComponentService` class.
    2. On the first run, a configuration file will be created at the config_path specified in the constructor, and the program will halt.
    3. Adjust component settings in the configuration file and initialize method parameters.
    4. Run the initialize method to preprocess data and train models.
    5. Generate a pipeline using either generate_pipeline_for_base_models or generate_pipeline_for_stacked_models.

    Public Methods
    --------------
    initialize:
        Preprocess data, train and fit models on it.

    generate_pipeline_for_stacked_models:
        Generate a pipeline for stacked models.

    generate_pipeline_for_base_models:
        Generate a pipeline for single models.

    optimize_n_splits:
        Find the optimal number of splits for cross-validation.
        Apply this optimization to `n_splits` of cv_obj.

    Optimize_n_splits_and_test_size:
        Find the optimal number of splits and test_size for cross-validation.
        This is achieved through Bayesian Optimization.
        Apply found optimization to test_size of the test data and `n_splits` of cv_obj.

    optimize_estimator_list:
        Find the optimal estimator_list order so that quicker estimators are trained first.

    Example
    -------
    >>> from sklearn.model_selection import ShuffleSplit, train_test_split
    >>> from sklearn.datasets import make_regression
    >>> from orpheus import ComponentService
    >>> import pandas as pd
    # specify path to configfile
    >>> config_path = "configurations.yaml"
    >>> cv_obj = ShuffleSplit(n_splits=2, random_state=42)
    >>> X, y = make_regression(n_samples=1000, n_features=10, random_state=42)
    # be sure to convert X to pd.DataFrame and y to pd.Series
    >>> X = pd.DataFrame(X)
    >>> X.columns = [f"feature_{N}" for N in range(1, X.shape[1] + 1)]
    >>> y = pd.Series(y)
    # split data into train and test
    >>> X_train, X_test, y_train, y_test = train_test_split(
    ...     X, y, test_size=0.2, random_state=42, shuffle=True)
    # initialize ComponentService
    >>> if __name__ == "__main__":
    ...     # First time running the program, a configfile will be created and
    ...     # program will stop execution
    ...     component_service = ComponentService(
    ...         X_train,
    ...         X_test,
    ...         y_train,
    ...         y_test,
    ...         config_path=config_path,
    ...         cv_obj=cv_obj,
    ...         n_jobs=4,
    ...         verbose=3,
    ...     )
    ...     # Optimize several important parameters before calling initialize:
    ...     component_service.optimize_estimator_list()
    ...     component_service.optimize_n_splits_and_test_size()
    ...     # Kick-off the whole process:
    ...     component_service.initialize(
    ...         scale=True,
    ...         add_features=True,
    ...         remove_features_by_correlation=True,
    ...         remove_features_by_selection=True
    ...        )
    ...     # Create pipelines for base models and stacked models:
    ...     pipe_base = component_service.generate_pipeline_for_base_models(top_n_per_tuner=5)
    ...     pipe_stacked = component_service.generate_pipeline_for_stacked_models(top_n_per_tuner_range=[2, 3])
    ...     # Fit and predict with pipelines:
    ...     pipe_base.fit(X_train, y_train)
    ...     pipe_stacked.fit(X_train, y_train)
    ...     y_pred_base = pipe_base.predict(X_test)
    ...     y_pred_stacked = pipe_stacked.predict(X_test)
    """

    def __init__(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        cv_obj: CrossValidatorType,
        config_path: str,
        *,
        scoring: Optional[Callable[[pd.Series, pd.Series], float]] = None,
        maximize_scoring: bool = True,
        verbose: int = DEFAULT_VALUES["verbose"],
        n_jobs: int = DEFAULT_VALUES["n_jobs"],
        estimator_list: Optional[List[EstimatorType]] = None,
        use_sklearn_estimators_aside_estimator_list: bool = True,
        exclude_estimators: Optional[List[str]] = None,
        estimator_list_order_state: Optional[int] = None,
        predict_proba_only: bool = False,
        ordinal_features: Optional[Dict[str, List[str]]] = None,
        categorical_features: Optional[List[str]] = None,
        categorical_features_pca_variance_threshold: Optional[float] = None,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        log_file_path: Optional[str] = None,
        log_file_mode: str = "a+",
    ):
        """
        Initialize the ComponentService class.

        Parameters
        ----------
        X_train : pd.DataFrame
        Training data. Assumes axis=0 is samples and axis=1 is features.
        X_test : pd.DataFrame
        Test data. Assumes axis=0 is samples and axis=1 is features.
        y_train : pd.Series
        Training target. Assumes axis=0 is samples and axis=1 is targets.
        y_test : pd.Series
        Test target. Assumes axis=0 is samples and axis=1 is targets.

        cv_obj : CrossValidatorType
        Instantiated Sklearn cross-validation object from sklearn.model_selection, e.g., KFold, StratifiedKfold, TimeSeriesSplit.
        Note: Splits will only be applied to training data (X_train & y_train).

        config_path : str
        Path to a YAML configuration file. If the file doesn't exist, it will be created and the program will halt.

        scoring : Optional[Callable] = None
        Custom scoring function for evaluating model performance. Set maximize_scoring to determine optimization direction.
        If None, the estimator's "score" method or "r2"/"accuracy" will be used depending on the estimator type.

        maximize_scoring : bool = True
        If True, the best estimator will have the highest score. If False, the best estimator will have the lowest score.

        verbose : int = {-1, -2, -3, 0, 1, 2, 3}
        Controls verbosity of printed messages. Negative values log to a file ("log.txt") instead of printing to console.

        n_jobs : int, optional
        Number of parallel jobs to run. By default, one core (1) will be used.

        estimator_list : Optional[List[EstimatorType]] = None
        List of uncalled estimators to use, e.g., [RandomForestClassifier, LogisticRegression]. If None, all sklearn estimators will be used.

        use_sklearn_estimators_aside_estimator_list : Optional[bool] = True
        If True, use sklearn estimators alongside those provided in estimator_list.

        exclude_estimators : Optional[List[str]] = None
        List of substrings for excluding matching estimators from the estimator_list.

        estimator_list_order_state : int, optional
        Random state for estimator_list order. Earlier estimators are trained first in each component.

        predict_proba_only : bool = False
        If True, only estimators with a predict_proba method will be used.

        ordinal_features: Optional[Dict[str, List[str]]] = None
            Dict of ordinal features, where the key is the column name and the value is a list of ordered values.
            Values which are not in the list will be encoded as -1 in the data.
            If None, assumes no ordinal features will be used.

        categorical_features : Optional[List[str]] = None
            List of categorical features. If None, assumes no categorical features will be used.

        categorical_features_pca_variance_threshold : float = None
            Variance threshold to be used for PCA on categorical features.
            Only active if categorical_features are provided.
            Should be a float between 0 and 1.

        type_estimator : Optional[str] = None
            Specifies the estimator type: 'regressor', 'classifier', or None (auto-detection).

        log_file_path : Optional[str] = None
            The path to the log file.
            If None, messages will be printed to the console given verbose > 0.
            Otherwise, messages will be logged to the file and not printed to the console.

        log_file_mode : str = "a+"
            Mode to open log file. Default is "a+" (append). Use "w+" to overwrite.
        """
        # Validation checks
        if ordinal_features:
            AttributeValidation.validate_ordinal_features(X_train, ordinal_features)
        else:
            ordinal_features = {}
        if categorical_features:
            AttributeValidation.validate_categorical_features(X_train, categorical_features)
        else:
            categorical_features = []
        data_dict = {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
        }
        DataValidation.validate_xy_types(
            data_dict, non_numerical_columns=list(ordinal_features.keys()) + categorical_features
        )
        DataValidation.validate_xy_len(X_train, y_train)
        DataValidation.validate_xy_len(X_test, y_test)
        AttributeValidation.validate_verbose(verbose)
        AttributeValidation.validate_config_path(config_path)
        AttributeValidation.validate_cv_obj(cv_obj)
        if estimator_list:
            AttributeValidation.validate_estimator_list(estimator_list)
        if exclude_estimators:
            AttributeValidation.validate_exclude_estimators(exclude_estimators)

        # Convert to correct values
        n_jobs = convert_n_jobs_to_num_workers(n_jobs)
        config_path = convert_cross_platform_path(config_path)

        # configure logger
        logger.set_verbose(verbose)
        if log_file_path is not None and logger.filename is None:
            logger.warning(
                f"Log file path set to '{log_file_path}' with mode '{log_file_mode}'. All messages will be logged to this file and not printed to the console."
            )
            logger.set_log_file(log_file_path, mode=log_file_mode)

        # Set attributes
        self.config_path = self._create_or_load_config_from_yaml(config_path)
        self.X_train = X_train.copy()
        self.y_train = y_train.copy()
        self.X_test = X_test.copy()
        self.y_test = y_test.copy()
        self.cv_obj = cv_obj
        self.maximize_scoring = maximize_scoring
        self.n_jobs = n_jobs
        self.random_state = estimator_list_order_state
        self.ordinal_features = ordinal_features
        self.categorical_features = categorical_features
        self.categorical_features_pca_variance_threshold = categorical_features_pca_variance_threshold

        self.type_estimator = check_type_estimator(
            y=self.y_train,
            type_estimator=type_estimator,
            maximize_scoring=self.maximize_scoring,
        )
        self.scoring = check_scoring(
            scoring=scoring,
            maximize_scoring=self.maximize_scoring,
            type_estimator=self.type_estimator,
        )
        self.estimator_list = check_estimator_list(
            estimator_list=estimator_list,
            use_sklearn_estimators_aside_estimator_list=use_sklearn_estimators_aside_estimator_list,
            exclude_estimators=exclude_estimators,
            type_estimator=self.type_estimator,
            random_state=estimator_list_order_state,
        )

        if predict_proba_only:
            predict_proba_list = [est for est in self.estimator_list if hasattr(est, "predict_proba")]
            if len(predict_proba_list) == 0:
                raise ValueError("No estimators with `predict_proba` method found.")
            dropped_estimators = ", ".join(
                get_obj_name(est) for est in self.estimator_list if est not in predict_proba_list
            )
            logger.notice(
                f"Only estimators with `predict_proba` method are used. Dropped estimators: {dropped_estimators}"
            )
            self.estimator_list = predict_proba_list

        # Set other attributes
        self._executed_initialize = False
        self.pipeline: Optional[MultiEstimatorPipeline] = None
        self.list_of_tuners: Optional[List[HyperTuner]] = None
        self.hypertuner_stacked: Optional[HyperTunerStacked] = None

    def initialize(
        self,
        downcast=True,
        scale=True,
        add_features=True,
        remove_features=True,
        remove_features_estimator: Optional[EstimatorType] = None,
    ) -> "ComponentService":
        """
        Train all models and deploy the pipeline.
        Do this by disabling/enabling preprocessing steps in parameters of this method,
        in combination with altering the configuration file.

        After this step is done, it is possible to deploy pipelines.
        This can be done by calling methods `generate_pipeline_for_stacked_models`
        and `generate_pipeline_for_base_models`.

        Parameters
        ----
        downcast : bool = False
            Whether to downcast X and y to smaller size for memory purposes.

        scale : bool = False
            Whether to scale X.
            This applies to component:
            `Scaling`\n
            methods:
            `scale`

        add_features : bool = False
            Whether to add features to X.
            This applies to component:
            `FeatureAdding`\n
            methods:
            `add_features`, `add_lags`, `add_rolling_stats`, `sequential_order_of_adding`

        remove_features : bool = False
            Whether to remove features from X.
            This applies to component:
            `FeatureRemoving`\n
            methods:
            `remove_features_by_selection`, `remove_features_by_correlation`, `remove_features_by_top_n`,

        remove_features_estimator : Optional[EstimatorType] = None
            Estimator to be used for `remove_features_by_selection` and `remove_features_by_correlation`.
            If None, RandomForestClassifier or RandomForestRegressor will be used,
            depending on the type of estimator.
            NOTE: Estimator needs to be passed instantiated!

        creates attributes:
        --------------------
        self.hypertuner_stacked : HyperTunerStacked
            A `HyperTunerStacked` object
            which can be seen as a container for all `HyperTuner` instances.

        returns
        ---
        self
        """
        assert self._executed_initialize is False, "initialize() can only be called once."

        # procedural checks
        if logger.get_verbose() > 0:
            estimated_duration = self._estimate_total_duration(self.config_path, scaling=scale)
            logger.notice(
                f"Estimated duration of the program, based on timeout-configurations * n_splits, is at least: {estimated_duration} seconds."
            )
            logger.notice(
                "Note that estimation does not take into account the timeout-configurations set to 'null'. Also, program might finish earlier if trainingdata is small."
            )

        end_to_end_pipe, X_preprocessed = _create_preprocessing_pipeline(
            X=self.X_train.copy(),
            y=self.y_train.copy(),
            cv_obj=self.cv_obj,
            downcast=downcast,
            scale=scale,
            add_features=add_features,
            remove_features=remove_features,
            type_estimator=self.type_estimator,
            config_path=self.config_path,
            return_X=True,
            scoring=self.scoring,
            maximize_scoring=self.maximize_scoring,
            estimator_list=self.estimator_list,
            num_workers=self.n_jobs,
            remove_features_estimator=remove_features_estimator,
            ordinal_features=self.ordinal_features,
            categorical_features=self.categorical_features,
            categorical_features_pca_variance_threshold=self.categorical_features_pca_variance_threshold,
        )

        # next step achieves 2 things at the same time:
        # 1. it makes sure that the pipeline is fitted on the data
        # 2. it checks if the pipeline returns the expected result when transforming X,
        assert_array_equal(
            np.sort(X_preprocessed, axis=1),
            np.sort(end_to_end_pipe.fit_transform(self.X_train.copy()), axis=1),
        )

        tuner_list = _create_hypertuners(
            X=X_preprocessed,
            y=self.y_train,
            cv_obj=self.cv_obj,
            leakage_prevention_slice=end_to_end_pipe.leakage_prevention_slice,
            config_path=self.config_path,
            scoring=self.scoring,
            maximize_scoring=self.maximize_scoring,
            estimator_list=self.estimator_list,
            num_workers=self.n_jobs,
            type_estimator=self.type_estimator,
            random_state=self.random_state,
        )

        hypertuner_stacked = HyperTunerStacked(
            tuner_list,
            pipeline=end_to_end_pipe,
            num_workers=self.n_jobs,
        )

        self.pipeline = end_to_end_pipe
        self.pipeline.train_data_mean = self.X_train.mean(numeric_only=True).mean()
        self.pipeline.test_data_mean = self.X_test.mean(numeric_only=True).mean()
        self.list_of_tuners = tuner_list
        self.hypertuner_stacked = hypertuner_stacked
        self._executed_initialize = True

        return self

    def __repr__(self) -> str:
        return f"ComponentService(config_path={self.config_path})"

    @initialize_check(initialize_must_be_run=True)
    def generate_pipeline_for_stacked_models(
        self,
        top_n_per_tuner_range: Union[List[Union[int, int]], Tuple[Union[int, int]]] = [
            1,
            5,
        ],
        return_top_n_models: Optional[int] = None,
        *,
        stacked: bool = True,
        stacked_unfit: bool = True,
        voting_hard: bool = True,
        voting_hard_unfit: bool = True,
        voting_soft: bool = True,
        voting_soft_unfit: bool = True,
        averaged: bool = True,
        averaged_weighted: bool = True,
        averaged_predictor: Optional[Union[PredictorType, int]] = None,
        stacked_final_estimator: Optional[EstimatorType] = None,
        round_floats_in_pred_if_classifier: bool = False,
        timeout_duration: Optional[int] = None,
    ) -> MultiEstimatorPipeline:
        """
        Test-predicts and deploys a pipeline from the best scoring models of a `HyperTunerStacked` object.
        Under the hood a high-level wrapper of the `_stacked_predict_range` and `_deploy_pipeline_of_stacked_models` functions.
        Makes the pipeline available for deployment on new data.

        Use X_train and y_train to train a stacked model,
        and X_test and y_test to evaluate the modelpredictions.
        Deploy a pipeline from the best scoring models on X_test to make predictions on new data.

        Parameters:
        -----------
        top_n_per_tuner_range: Union[List[Union[int, int]], Tuple[Union[int, int]]]
            The range of top scoring models per `HyperTuner` instance
            which will be evaluated. These models were scored on the
            training data and are sorted by their score.
            Default is [1,5].

        return_top_n_models : int, default=None
            The top_n models, to include in the scoring process of the models.
            They will be scored on the test data and sorted by their score.

        stacked: bool
            Whether to include the stacked model in the pipeline.
            Default is True.

        stacked_unfit: bool
            Whether to include the stacked model with unfitted estimators in the pipeline.
            Default is True.

        voting_hard: bool
            Whether to include the voting hard model in the pipeline in the pipeline.
            Default is True.

        voting_hard_unfit: bool
            Whether to include the voting hard model with unfitted estimators in the pipeline.
            Default is True.

        voting_soft: bool
            Whether to include the voting soft model in the pipeline.
            Only estimators with a predict_proba method will be used. Default is True.

        voting_soft_unfit: bool
            Whether to include the voting soft model with unfitted estimators in the pipeline.
            Only estimators with a predict_proba method will be used. Default is True.

        averaged: bool
            Whether to include the averaged model in the pipeline.
            Default is True.

        averaged_weighted: bool
            Whether to include the averaged weighted model in the pipeline.
            Default is True.

        averaged_predictor: Optional[Union[PredictorType, int]]
            The `PredictorType` per `HyperTuner` instance to use for the averaged model.
            This applies to both `averaged` and `averaged_weighted`.
            Default is None, meaning all models of a `HyperTuner` instance will be used.

        stacked_final_estimator: Optional[EstimatorType]
            The final estimator to use for the stacked model.
            Default is None, meaning the final estimator will be
            the best estimator found from all crossvalidations.
            Optionally, insert an own (sklearn compatible) estimator
            to use as custom final estimator.

        round_floats_in_pred_if_classifier: bool
            Whether to round floats in the prediction if the task is classification,
            which might be the case if `averaged` or `averaged_weighted` is True.
            This way, these predictions will be in the same format as the predictions of the
            other models and be eligable for the scoring process.
            It is mainly aimed to prevent:
            'ValueError: Classification metrics can't handle a mix of multiclass and continuous targets'
            Default is False.
            NOTE: Beware of rounding errors when using this option. Use with caution.

        timeout_duration: Optional[int]
            The maximum time in seconds, to wait for the fitting to finish during the scoring process.
            If None, no timeout will be set.
            Else, if the timeout is reached, the fitting process will be canceled forcefully.
            Use this to prevent hanging of the fitting process.
            NOTE: This uses multiprocessing.Pool, which will cause overhead. Only use this if necessary!

        Creates attributes:
        --------
        scores added as an attribute to the Pipeline object

        Returns:
        --------
        pipeline: MultiEstimatorPipeline
            A pipeline containing the preprocessing-steps and all estimators of
            the top N best scoring models.
            Call predict on the pipeline to make predictions on new data.
            Predictions early in index are from the better scoring estimators,
            predictions later in index are from less scoring estimators.
        """
        assert (
            top_n_per_tuner_range[0] < top_n_per_tuner_range[1]
        ), "top_n_per_tuner_range[0] must be smaller than top_n_per_tuner_range[1]"
        assert all(i > 0 for i in top_n_per_tuner_range), "Both numbers in top_n_per_tuner_range should be positive"

        X_train = self.X_train.copy()
        X_test = self.X_test.copy()
        y_train = self.y_train.copy()

        if logger.get_verbose() <= 2:
            total_amt_of_models = sum(
                [
                    stacked,
                    stacked_unfit,
                    voting_hard,
                    voting_hard_unfit,
                    voting_soft,
                    voting_soft_unfit,
                    averaged,
                    averaged_weighted,
                ]
            ) * (top_n_per_tuner_range[1] - top_n_per_tuner_range[0])
            logger.notice(f"Generating pipeline for {total_amt_of_models} stacked models...")

        pred_df, fitted_models = _stacked_predict_range(
            hypertuner_stacked=self.hypertuner_stacked,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            top_n_per_tuner_range=top_n_per_tuner_range,
            stacked=stacked,
            stacked_unfit=stacked_unfit,
            voting_hard=voting_hard,
            voting_hard_unfit=voting_hard_unfit,
            voting_soft=voting_soft,
            voting_soft_unfit=voting_soft_unfit,
            averaged=averaged,
            averaged_weighted=averaged_weighted,
            averaged_predictor=averaged_predictor,
            stacked_final_estimator=stacked_final_estimator,
            timeout_duration=timeout_duration,
        )

        multi_estimator_pipeline = _deploy_pipeline_of_stacked_models(
            self.hypertuner_stacked,
            pred_df,
            fitted_models,
            self.y_test,
            return_top_n_models=return_top_n_models,
            round_floats_in_pred_if_classifier=round_floats_in_pred_if_classifier,
        )

        multi_estimator_pipeline.generation = "stacked"

        return multi_estimator_pipeline

    def _scoring_base_models(
        self, name, model, X_test, y_test, cv_obj, scoring, verbose, n_jobs
    ) -> Union[np.ndarray, None]:
        try:
            logger.info(f"generate_pipeline_for_base_models: Evaluating model {name}...")
            cv_results = cross_val_score(
                model,
                X_test,
                y_test,
                cv=cv_obj,
                scoring=scoring,
                verbose=verbose,
                n_jobs=n_jobs,
            )
            return cv_results
        except ValueError:
            logger.error(
                f"generate_pipeline_for_base_models: Error while evaluating model {name}:\n{traceback.format_exc()}"
            )
            return None

    @initialize_check(initialize_must_be_run=True)
    def generate_pipeline_for_base_models(
        self,
        top_n_per_tuner: Optional[int] = None,
        return_top_n_models: Optional[int] = None,
        *,
        plot_title: str = "Evaluation of models",
        plotting: bool = False,
        timeout_duration: Optional[int] = None,
    ) -> MultiEstimatorPipeline:
        """
        Evaluate all base models from a list of `HyperTuner` instances and
        deploy a pipeline from the best scoring models.\n
        Perform a cross-validated score with all sorted fitted estimators
        from a list of `HyperTuner` instances over X and y.
        The best scoring models are then deployed as a pipeline,
        which can be used to predict on new data.

        Parameters
        ----
        top_n_per_tuner: int, default=None
            The top number of models per `HyperTuner` object to evaluate.
            These models were scored on the training data and are sorted by their score.
            Default is None, meaning all models will be evaluated.

        return_top_n_models : int, default=None
            The top_n models, to include in the scoring process of the models.
            They will be scored on the test data and sorted by their score.

        plot_title: str, default="Evaluation of models"
            The title of the plot, if plotting is True.

        plotting: bool, default=False
            If True, a plot will be generated, showing the scores of the models.

        timeout_duration: Optional[int], default=None
            The maximum time in seconds, to wait for the fitting to finish during the scoring process.
            If None, no timeout will be set.
            Else, if the timeout is reached, the fitting process will be canceled forcefully.
            Use this to prevent hanging of the fitting process.
            NOTE: This uses multiprocessing.Pool, which will cause overhead. Only use this if necessary!

        Creates:
        --------
        scores added as an attribute to the Pipeline object

        Returns:
        --------
        pipeline: MultiEstimatorPipeline
            A pipeline containing the preprocessing-steps and all estimators
            of the top N best scoring models.
            Call predict on the pipeline to make predictions on new data.
            Predictions early in index are from the better scoring estimators,
            predictions later in index are from less scoring estimators.

        Source: https://towardsdatascience.com/time-series-modeling-using-scikit-pandas-and-numpy-682e3b8db8d1
        """
        X_test = self.X_test.copy()
        y_test = self.y_test.copy()

        if not self.list_of_tuners:
            raise ValueError("list_of_tuners is empty")

        if logger.get_verbose() <= 2:
            amt_tuners = len(self.list_of_tuners)
            total_amt_of_models = (
                amt_tuners * top_n_per_tuner
                if top_n_per_tuner
                else amt_tuners * len(self.list_of_tuners[0]._get_all_fitted_estimators())
            )
            logger.notice(f"Generating pipeline for {total_amt_of_models} base models...")

        X_test = self.pipeline.transform(X_test)

        scoring = self.list_of_tuners[0].scoring
        scoring = make_scorer(scoring) if scoring is not None else None
        maximize_scoring = self.list_of_tuners[0].maximize_scoring

        sorted_scores = bool(top_n_per_tuner)

        models = []
        for tuner in self.list_of_tuners:
            models_from_tuner = list(tuner._get_all_fitted_estimators(sort_scores=sorted_scores, top_n=top_n_per_tuner))
            models.extend(models_from_tuner)

        models = [(str(i), i) for i in models]

        results = []
        names = []

        for name, model in models:
            try:
                with FunctionTimeoutHandler(
                    self._scoring_base_models,
                    name,
                    model,
                    X_test,
                    y_test,
                    self.cv_obj,
                    scoring,
                    0 if logger.get_verbose() < 1 else logger.get_verbose(),
                    self.n_jobs,
                    timeout=timeout_duration,
                    n_jobs_on_timeout=1,
                ) as cv_results:
                    pass

                if cv_results is None:
                    logger.error(
                        f"generate_pipeline_for_base_models: Getting results for model {name} failed due to an error in {self._scoring_base_models.__name__}(). Skipping..."
                    )
                    continue

                if cv_results.any():
                    results.append(cv_results)
                    names.append(name)
                    logger.notice(f"{name}: {cv_results.mean()} ({cv_results.std()})")
            except Exception:
                logger.error(
                    f"generate_pipeline_for_base_models: Error while evaluating model {name}:\n{traceback.format_exc()}"
                )

        result_dict = dict(zip(names, results))
        if not result_dict:
            raise ValueError("result_dict is empty! No models were evaluated properly.")
        top_n_models = dict(
            sorted(
                result_dict.items(),
                key=lambda x: np.mean(x[1]),
                reverse=maximize_scoring,
            )
        )

        if plotting:
            try:
                fig = plt.figure()
                fig.suptitle(plot_title, fontsize=18, fontweight="bold")
                ax = fig.add_subplot(111)
                ax.boxplot(
                    top_n_models.values(),
                    labels=[n[:30] for n in top_n_models.keys()],
                    vert=False,
                )
                ax.set_title(
                    f"mean: {np.mean(list(top_n_models.values())):.5f} with std: {np.std(list(top_n_models.values())):.5f} over {self.cv_obj.get_n_splits()} folds",
                    fontsize=12,
                    fontstyle="italic",
                )
                ax.set_xlabel("score")
                ax.set_ylabel("estimators")
                plt.show()
            except Exception as e:
                logger.error(f"plotting failed because of {e}")

        multi_estimator_pipeline = deepcopy(self.pipeline)

        top_n_models_scores = pd.Series(top_n_models)[:return_top_n_models]
        estimators = []

        for model_str, _ in top_n_models_scores.items():
            model = (i for i in models if i[0] == model_str).__next__()[1]
            estimators.append(model)

        estimators_wrapper = MultiEstimatorWrapper(estimators)
        multi_estimator_pipeline.steps.append(("estimators", estimators_wrapper))

        for score_list in zip(*top_n_models_scores):
            multi_estimator_pipeline.update_scores(np.array(score_list))

        multi_estimator_pipeline.generation = "base"

        return multi_estimator_pipeline

    @initialize_check(initialize_must_be_run=False)
    def optimize_n_splits_and_test_size(
        self,
        shuffle: bool,
        stratify=False,
        estimator: Optional[EstimatorType] = None,
        min_splits: int = 2,
        max_splits: int = 10,
        test_size_range: Tuple[float, float] = (0.1, 0.5),
        init_points: int = 10,
        n_iter: int = 20,
        random_state: Optional[int] = None,
        **bayesian_kwargs,
    ) -> "ComponentService":
        """
        Heuristic method, which optimises the number of cross-validation splits and the size of the test set.
        This is done by using Bayesian Optimization to find the best combination of splits and test size.
        Reassamble X and y and and resplit them using the new test size and number of splits.
        NOTE: Use this method before calling initialize().
        NOTE: This method will modify self.X_train, self.X_test, self.y_train, self.y_test, and self.cv_obj.

        Parameters
        ----------
        shuffle: bool
            Whether to shuffle the data before splitting into batches.
        stratify: bool
            Whether to stratify the data before splitting into batches.
            If true, if `self.type_estimator` is "classifier", then the data is stratified by y.
            If false, the data is not stratified.
        estimator: Optional[EstimatorType]
            The estimator to use for the optimization.
            if `self.type_estimator` is "classifier", then a LogisticRegression is used.
            If `self.type_estimator` is "regressor", then a LinearRegression is used.
            One could for example use a RandomForestRegressor() or RandomForestClassifier() here if
            the relationship between the features and the target is non-linear.
        split_range: Tuple[int, int]
            The range of splits to optimize over. Last value is exclusive.
        test_size_range: Tuple[float, float]
            The range of test sizes to optimize over. Last value is exclusive.
        init_points: int
            The number of random points to sample before fitting the model.
        n_iter: int
            The number of iterations to run the optimization for.
        random_state: Optional[int]
            The random state to use for the optimization.
        **bayesian_kwargs:
            Additional keyword arguments to pass to `BayesianOptimization.maximize`.
            See documentation of `BayesianOptimization` for more information.

        Returns
        -------
        self: ComponentService
        """
        X = pd.concat([self.X_train, self.X_test], axis=0)
        y = pd.concat([self.y_train, self.y_test], axis=0)

        X_copy = self._transform_non_numerical_feats_in_X(X.copy())

        if stratify and self.type_estimator == "classifier":
            stratify = y
        else:
            stratify = None

        (optimal_n_splits, optimal_test_size, optimal_params,) = optimize_splits_and_test_size(
            X=X_copy,
            y=y,
            cv_obj=self.cv_obj,
            type_estimator=self.type_estimator,
            maximize_scoring=self.maximize_scoring,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            shuffle=shuffle,
            estimator=estimator,
            min_splits=min_splits,
            max_splits=max_splits,
            test_size_range=test_size_range,
            init_points=init_points,
            n_iter=n_iter,
            random_state=random_state,
            **bayesian_kwargs,
        )
        logger.notice(
            f"Optimal n_splits for cv_obj used for X_train when rounded: {optimal_n_splits}\noptimal test_size for train_test_split: {optimal_test_size}\noptimal params: {optimal_params}"
        )
        self.cv_obj.n_splits = optimal_n_splits
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=optimal_test_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=y if (self.type_estimator == "classifier" and shuffle) else None,
        )

        return self

    @initialize_check(initialize_must_be_run=False)
    def optimize_estimator_list(
        self, len_data: int = 100, timeout_duration: Optional[int] = None
    ) -> "ComponentService":
        """
        Heuristic method which optimizes the order of self.estimator_list.
        NOTE: Use this method before calling initialize().

        Parameters
        ----------
        len_data: int
            The first number of rows to use for the optimization.
            This is useful if the dataset is very large and the optimization takes too long.

        timeout_duration: int, default=None
            The maximum time in seconds to spend on fitting an estimator. If None, no timeout will be set.
            This is useful for preventing the optimization from getting stuck on a single estimator.

        Returns
        -------
        self: ComponentService
        """
        logger.notice("Optimizing estimator list order...")
        X = self.X_train.iloc[:len_data]
        y = self.y_train.iloc[:len_data]

        X_copy = self._transform_non_numerical_feats_in_X(X.copy())

        results: pd.Series = _optimize_estimator_list_order(
            estimator_list=self.estimator_list,
            X=X_copy,
            y=y,
            num_processes=self.n_jobs,
            timeout=timeout_duration,
        )
        logger.notice(
            f"Optimized estimator_list order results in seconds:\n{results.to_string()}",
        )
        self.estimator_list = results.index.to_list()

        return self

    def optimize_n_splits(
        self,
        min_splits: int = 2,
        max_splits: int = 10,
        estimator: Optional[EstimatorType] = None,
        **cv_obj_kwargs,
    ) -> "ComponentService":
        """
        Heuristic method which optimizes the number of
        splits for the cross-validation object.
        NOTE:Use this method before calling initialize().

        Parameters
        ----------
        min_splits: int
            Minimum number of splits to test.

        max_splits: int
            Maximum number of splits to test.
            Last value is inclusive.

        estimator: None or EstimatorType
            Estimator to use for the cross-validation. If None,
            if type_estimator is "classifier", then a LogisticRegression is used.
            If type_estimator is "regressor", then a LinearRegression is used.

        cv_obj_kwargs: dict
            Keyword arguments to pass to the cross-validation object.

        Returns
        -------
        self: ComponentService
        """
        if self._executed_initialize:
            raise ValueError("You cannot optimize the number of splits after calling initialize().")
        cv_obj_uninit = self.cv_obj.__class__

        results = find_optimal_n_splits(
            X=self.X_train,
            y=self.y_train,
            type_estimator=self.type_estimator,
            estimator=estimator,
            min_splits=min_splits,
            max_splits=max_splits,
            cv_obj=cv_obj_uninit,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            verbose=logger.get_verbose(),
            **cv_obj_kwargs,
        )

        optimal_n_splits = results.idxmax() if self.maximize_scoring else results.idxmin()
        self.cv_obj = cv_obj_uninit(n_splits=optimal_n_splits, **cv_obj_kwargs)
        logger.notice(
            f"Results of n_splits optimization:\n{results.sort_values(ascending=not self.maximize_scoring).to_string()}",
        )
        logger.notice(f"n_splits of self.cv_obj set to {optimal_n_splits}")

        return self

    def _create_or_load_config_from_yaml(self, config_path: str) -> str:
        """
        Create or load the config file and validate it against the schema

        Parameters
        ----------
        config_path : str
            The path to the config file

        Returns
        -------
        config_path : str
            The path to the config file
        """
        config_path = standardize_config_path_to_yaml(config_path)

        if not os.path.isfile(config_path):
            ConfigManager.create_config(
                config_path,
                Scaling,
                FeatureAdding,
                FeatureRemoving,
                HyperTuner,
            )
            # exit the program after creating the config file
            sys.exit(0)

        # Load the config file
        with open(config_path, encoding="utf-8") as file:
            config = ruamel.yaml.safe_load(file)

        # Validate the config file against the schema
        validator = schema.Schema(config_schema)
        validator.validate(config)
        validate_bounds_FeatureAdding(config["FeatureAdding"])

        return config_path

    def _estimate_total_duration(self, config_path: str, scaling: bool):
        with open(config_path, encoding="utf-8") as file:
            config = ruamel.yaml.safe_load(file)

            total_timeout = 0

            if scaling:
                scale_timeout = config["Scaling"]["scale"]["timeout"] or 0
                if config["Scaling"]["scale"]["columns_to_scale"]:
                    scale_timeout *= len(config["Scaling"]["scale"]["columns_to_scale"])
                total_timeout += scale_timeout

            total_timeout += config["HyperTuner"]["fit"]["R1_timeout"] or 0
            total_timeout += config["HyperTuner"]["fit"]["R2_timeout"] or 0
            total_timeout += config["HyperTuner"]["fit"]["R3_timeout"] or 0

            return total_timeout * self.cv_obj.get_n_splits()

    def _transform_non_numerical_feats_in_X(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.categorical_features or self.ordinal_features:
            X, _ = _encode_non_numerical_features(
                X,
                categorical_features=self.categorical_features,
                ordinal_features=self.ordinal_features,
                categorical_features_pca_variance_threshold=self.categorical_features_pca_variance_threshold,
            )

        return X
