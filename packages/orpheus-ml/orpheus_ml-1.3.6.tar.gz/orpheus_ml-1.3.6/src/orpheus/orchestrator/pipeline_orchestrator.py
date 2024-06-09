"""
This module contains the PipelineOrchestrator class. 
It is a facade for the services in this package and provides a simple interface for the user to interact with.

The mainidea is that the dataset gets split into three partitions: train, test and validation.
The train set is used to train the models, the test set is used to evaluate the models and the validation set is used as a final check for performance.

Three different pipelines are created in the end:
- self.pipelines["base"]: pipeline trained on the best base estimators from different folds. (GEN 1)
- self.pipelines["stacked"] pipeline trained on the best stacked estimators, which on their turn are formed from the best base estimators from different folds stacked on top of each other. (GEN 2)
- self.pipelines["evolved"]: pipeline evolved from self.pipelines["stacked"]. This pipeline is evolved using a genetic algorithm. (GEN 3)

Next to the estimators, all pipelines include preprocessing steps, feature engineering steps and feature selection steps.
"""
import traceback
from copy import deepcopy
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

import pandas as pd

from orpheus import (ComponentService, PerformanceService,
                     PipelineEvolverService, PreparatorService)
from orpheus.metrics.constants import SCORE_TYPES
from orpheus.metrics.metric_converter import MetricConverter
from orpheus.orchestrator.data_transfer.pipeline_metadata import \
    PipelineMetadata
from orpheus.orchestrator.pipeline_manager import PipelineManager
from orpheus.services.additional_types.multi_estimator_pipeline import \
    MultiEstimatorPipeline
from orpheus.utils.constants import DEFAULT_VALUES
from orpheus.utils.custom_exceptions import NoRobustModelsInPipelineError
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import CrossValidatorType, EstimatorType
from orpheus.validations.pipeline_orchestrator_validator import \
    PipelineOrchestratorValidator


class PipelineOrchestrator:
    """
    This class is the main entry point of the application and provides a simple interface for the user to interact with.
    It uses a facade-pattern for all the services in this package.
    It is responsible for splitting the data, preprocessing the data, training and evaluating the models and building the pipelines.
    It also provides methods to fortify the pipelines and get the metadata of the pipelines.

    The main idea is that the dataset gets split into three partitions: train, test and validation.
    The train set is used to train the models, the test set is used to evaluate the models and the validation set is used as a final check for performance.

    Public methods
    ---------------
    register_metric (static):
        Used to register custom metrics before instantiating the PipelineOrchestrator class.
    fit_pipelines_with_data:
        Fits the pipelines on passed new data.
    refit_pipelines:
        Refits the pipelines on the train and/or test and/or validation set.
    pre_optimize:
        Pre-optimizes the estimator list, the number of cross-validation splits and test size for the cross validation.
    build:
        Builds the pipelines for the base models, stacked models and evolution of the stacked models.
    fortify:
        Fortifies the pipelines by testing them on robustness.
    get_pipeline_metadata:
        Returns the metadata of the pipelines as a dictionary. Only available after fortify() has been called.
    get_explained_features:
        Returns the mean feature importance of the features in the pipelines.

    Public attributes:
    ------------------
        X_train: pd.DataFrame
            The train feature matrix.
        X_test: pd.DataFrame
            The test feature matrix.
        y_train: pd.Series
            The train target vector.
        y_test: pd.Series
            The test target vector.
        X_val: pd.DataFrame
            The validation feature matrix.
        y_val: pd.Series
            The validation target vector.
        config_path: str
            The path to the configuration file of the components (scaling, adding/removing features and hyperparameter tuning).
        estimator_list: List[EstimatorType]
            The list of estimators to use.
        use_sklearn_estimators_aside_estimator_list: bool
            Whether to use the sklearn estimators aside from the estimator list, if passed.
        cv_obj: CrossValidatorType
            The cross validator object to use. For example, KFold, StratifiedKFold, etc.
        pipelines: PipelineManager
            The pipelines that are built, being: "base", "stacked" and "evolved".
        metric: Callable[[pd.Series, pd.Series], float]
            The metric to optimize for. Usually imported from sklearn.metrics. Must be a function which is registered in the SCORE_TYPES dictionary.
        maximize_scoring: bool
            Whether the metric should be maximized or minimized.
        type_estimator: str
            The type of estimator the metric is used for. Should be either "regressor" or "classifier".
        n_jobs: int
            The number of jobs to run in parallel, depending on available CPU cores.
        ensemble_size: float
            The size of the ensemble set. This dataset will be used specificly for scoring newly generated ensemble models.
            Must be a positve float between 0 and 1.
            NOTE: Due to the way Orpheus is set up, this value cannot be 0.0. If ensemble learning is not needed, set this value to a negliglable percentage of the data (eg. 0.01 or lower).
        validation_size: float
            The size of the validation set. Must be a positve float between 0 and 1.
        random_state: Optional[int]
            The random state to use for all applicable methods.
        shuffle: bool
            Whether to shuffle the data before splitting.
        stratify: bool
            Whether to stratify the data before splitting.
    """

    def __init__(
        self,
        X: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]],
        y: Union[pd.Series, Tuple[pd.Series, pd.Series, pd.Series]],
        metric: Callable[[pd.Series, pd.Series], float],
        config_path: str,
        verbose: int = DEFAULT_VALUES["verbose"],
        n_jobs: int = DEFAULT_VALUES["n_jobs"],
        ensemble_size: float = 0.2,
        validation_size: float = 0.05,
        shuffle: bool = False,
        stratify: bool = False,
        cv_obj: Optional[CrossValidatorType] = None,
        n_splits_if_cv_obj_is_none: int = 5,
        time_series_gap: int = 0,
        estimator_list: Optional[List[EstimatorType]] = None,
        use_sklearn_estimators_aside_estimator_list: bool = True,
        exclude_estimators: Optional[List[str]] = None,
        predict_proba_only: bool = False,
        ordinal_features: Optional[Dict[str, List[str]]] = None,
        categorical_features: Optional[List[str]] = None,
        categorical_features_pca_variance_threshold: Optional[float] = None,
        infer_type_estimator_from_data: bool = True,
        random_state: Optional[int] = None,
        log_file_path: Optional[str] = None,
        log_file_mode: str = "a+",
        log_cpu_memory_usage: bool = False,
    ):
        """
        Initialize the PipelineOrchestrator class.

        parameters
        ----------
        X: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]
            The feature matrix or a tuple of the train, test and validation feature matrices.
            This last option is useful when you want to preprocess the data before splitting it in the orchestrator's constructor.
        y: Union[pd.Series, Tuple[pd.Series, pd.Series, pd.Series]]
            The target vector or a tuple of the train, test and validation target vectors.
            This last option is useful when you want to preprocess the data before splitting it in the orchestrator's constructor.
        metric: Callable[[pd.Series, pd.Series], float]
            The metric to optimize for. Must be a function which is registered in the SCORE_TYPES dictionary.
            If you want to use a custom metric, use the PipelineOrchestrator.register_metric() method to register the metric.
        config_path: str
            The path to the configuration file of the components (scaling, adding/removing features and hyperparameter tuning).
        verbose: int
            The verbosity level
        n_jobs: int
            The number of jobs to run in parallel
        ensemble_size: float
            The size of the test set.
            Must be a positve float between 0 and 1 or a positive integer, in which case it will be the number of samples.
            This must be given because of the way the data is split.
            NOTE: If the data is already split, this parameter is ignored.
        validation_size: float
            The size of the validation set.
            Must be a positve float between 0 and 1 or a positive integer, in which case it will be the number of samples.
            This must be given because of the way the data is split.
            NOTE: If the data is already split, this parameter is ignored.
        shuffle: bool
            Whether to shuffle the data before splitting
        stratify: bool
            Whether to stratify the data before splitting
        cv_obj: Optional[CrossValidatorType]
            The cross validator object to use
        n_splits_if_cv_obj_is_none_: int
            The number of splits to use for the cross validator object.
            Only used if cv_obj is None.
        time_series_gap: int
            The gap to use for the time series split, if applicable.
        estimator_list: Optional[List[EstimatorType]]
            The list of estimators to use. if Nonne and use_sklearn_estimators_aside_estimator_list is True,
            all available sklearn estimators will be used in addition to the estimator list provided.
            NOTE: Similar estimators with different str arguments might be passed to the estimator_list with `functools.partial`.
            Like so: `partial(RandomForestClassifier, criterion="entropy")`.
        use_sklearn_estimators_aside_estimator_list: bool
            Whether to use the sklearn estimators aside from the estimator list.
            If True, all available sklearn estimators will be used in addition to the estimator list provided.
        exclude_estimators: Optional[List[str]]
            The list of estimators to exclude. Does not need to match the name of the estimator exactly.
        predict_proba_only: bool
            Whether to only use estimators that have a predict_proba method.
        ordinal_features: Optional[Dict[str, List[str]]] = None
            Dict of ordinal features, where the key is the column name and the value is a list of ordered values.
            Values which are not in the list will be encoded as -1 in the data.
            If None, assumes no ordinal features will be used.
        categorical_features : Optional[List[str]] = None
            List of categorical features.
            If None, assumes no categorical features will be used.
        categorical_features_pca_variance_threshold : float = None
            Variance threshold to be used for PCA on categorical features.
            Only active if categorical_features are provided.
            Should be a float between 0 and 1.
        infer_type_estimator_from_data: bool = True
            Whether to infer the type of estimator (classifier or regressor) from the target vector.
            If False, the type of estimator will be inferred from the metric.
            If True (default), the type of estimator will be inferred from the target vector.
        random_state: Optional[int]
            The random state to use for all applicable methods.
        log_file_path: Optional[str]
            The path to the log file.
            If None, messages will be printed to the console given verbose > 0.
            Otherwise, messages will be logged to the file and not printed to the console.
        log_file_mode : str = "a+"
            Mode to open log file. Default is "a+" (append). Use "w+" to overwrite.
        log_cpu_memory_usage: bool
            Whether to also log the cpu and memory usage. This can be useful for debugging purposes.
        """
        PipelineOrchestratorValidator.validate_parameters(
            X=X,
            y=y,
            ensemble_size=ensemble_size,
            validation_size=validation_size,
            verbose=verbose,
        )

        logger.set_verbose(verbose)
        logger.set_cpu_and_memory_usage(log_cpu_memory_usage)
        if log_file_path is not None and logger.filename is None:
            logger.warning(
                f"Log file path set to '{log_file_path}' with mode '{log_file_mode}'. All messages will be logged to this file and not printed to the console."
            )
            logger.set_log_file(log_file_path, mode=log_file_mode)

        self.metric = metric
        self.n_jobs = n_jobs
        self.ensemble_size = ensemble_size
        self.validation_size = validation_size
        self.random_state = random_state
        self.shuffle = shuffle
        self.stratify = stratify

        metric_converter = MetricConverter(self.metric)
        try:
            self.maximize_scoring = metric_converter.maximize_scoring
        except ValueError as e:
            raise ValueError(
                f"Metric {metric_converter.name} is not supported. Use PipelineOrchestrator.register_metric() if you wanted to register a custom metric"
            ) from e

        if isinstance(X, (pd.DataFrame, pd.Series)):
            # if X and y are not split:
            (X_train, X_test, X_val, y_train, y_test, y_val,) = PreparatorService.split_data(
                X=X,
                y=y,
                test_size=ensemble_size,
                val_size=validation_size,
                random_state=random_state,
                shuffle=self.shuffle,
                stratify=self.stratify,
            )
        elif isinstance(X, (tuple, list)) and len(X) == 3:
            # if X and y are split and passed as items in a tuple or list:
            X_train, X_test, X_val = X
            y_train, y_test, y_val = y
        else:
            raise ValueError(
                f"X and y must be either a tuple/list of length 3 or a {type(pd.DataFrame)} or {type(pd.Series)} object, but are {type(X)} and {type(y)}."
            )

        # determine the type of estimator from the target vector
        self.preperator_service = PreparatorService(X_train, y_train, verbose=verbose)
        if infer_type_estimator_from_data:
            self.type_estimator = "regressor" if self.preperator_service.is_regression else "classifier"
        else:
            self.type_estimator = metric_converter.type_estimator

        # select across validator suitable for the data
        if cv_obj is None:
            self.cv_obj = self.preperator_service.select_cross_validator(
                shuffle=self.shuffle,
                random_state=self.random_state,
                time_series_gap=time_series_gap,
                n_splits=n_splits_if_cv_obj_is_none,
            )
        else:
            self.cv_obj = cv_obj

        self._X_val = X_val
        self._y_val = y_val

        self.component_service = ComponentService(
            X_train,
            X_test,
            y_train,
            y_test,
            config_path=config_path,
            scoring=self.metric,
            maximize_scoring=self.maximize_scoring,
            cv_obj=self.cv_obj,
            n_jobs=self.n_jobs,
            verbose=verbose,
            type_estimator=self.type_estimator,
            estimator_list=estimator_list,
            estimator_list_order_state=self.random_state,
            use_sklearn_estimators_aside_estimator_list=use_sklearn_estimators_aside_estimator_list,
            exclude_estimators=exclude_estimators,
            predict_proba_only=predict_proba_only,
            ordinal_features=ordinal_features,
            categorical_features=categorical_features,
            categorical_features_pca_variance_threshold=categorical_features_pca_variance_threshold,
        )

        self._data_metadata = self._initialize_metadata_data()
        self._pipeline_metadata: Dict[str, PipelineMetadata] = {}
        self.pipelines: PipelineManager = PipelineManager()

    def __repr__(self):
        return f"PipelineOrchestrator(metric={get_obj_name(self.metric)}, config_path={self.config_path}, verbose={logger.get_verbose()}, n_jobs={self.n_jobs}, ensemble_size={self.ensemble_size}, validation_size={self.validation_size}, random_state={self.random_state}, shuffle={self.shuffle}, stratify={self.stratify}, cv_obj={self.cv_obj})"

    @property
    def X_train(self) -> pd.DataFrame:
        return self.component_service.X_train

    @property
    def X_test(self) -> pd.DataFrame:
        return self.component_service.X_test

    @property
    def y_train(self) -> pd.Series:
        return self.component_service.y_train

    @property
    def y_test(self) -> pd.Series:
        return self.component_service.y_test

    @property
    def X_val(self) -> pd.DataFrame:
        return self._X_val

    @property
    def y_val(self) -> pd.Series:
        return self._y_val

    @property
    def config_path(self) -> str:
        return self.component_service.config_path

    @property
    def estimator_list(self) -> List[EstimatorType]:
        return self.component_service.estimator_list

    @staticmethod
    def register_metric(
        metric: Callable,
        maximize_scoring: bool,
        type_estimator: Literal["regressor", "classifier"],
    ) -> None:
        """
        Used to register custom metrics before instantiating the PipelineOrchestrator class.

        Parameters
        ----------
        metric: Callable
            The metric to register.
        maximize_scoring: bool
            Whether the metric should be maximized or minimized.
        type_estimator: str
            The type of estimator the metric is used for. Either "regressor" or "classifier".

        Raises
        ------
        ValueError
            If the type_estimator parameter is not "regressor" or "classifier".
        """
        if type_estimator not in ["regressor", "classifier"]:
            raise ValueError("type_estimator must be 'regressor' or 'classifier'")

        modeling_type = "regression" if type_estimator == "regressor" else "classification"
        optimization_direction = "maximize" if maximize_scoring else "minimize"
        metric_name = get_obj_name(metric)

        # Remove the metric if it is already registered anywhere in SCORE_TYPES
        for category in SCORE_TYPES:
            for score_type in SCORE_TYPES[category]:
                if metric_name in SCORE_TYPES[category][score_type]:
                    SCORE_TYPES[category][score_type].remove(metric_name)

        # Then add the metric to the appropriate category
        SCORE_TYPES[modeling_type][optimization_direction].append(metric_name)

    def refit_pipelines(
        self, on_train: bool = True, on_test: bool = True, on_validation: bool = True
    ) -> "PipelineOrchestrator":
        """
        Refit the pipelines.

        Parameters:
        ----------
        on_train (bool, optional):
            If True, the pipelines will be refitted on the train set.
        on_test (bool, optional):
            If True, the pipelines will be refitted on the test set.
        on_validation (bool, optional):
            If True, the pipelines will be refitted on the validation set.
        NOTE: Refitting all models can take a long time. Use this method with caution.

        Returns:
        ----------
        self (PipelineOrchestrator):
            The PipelineOrchestrator object.
        """
        X, y = self._reassemble_Xy_for_refitting(on_train, on_test, on_validation)

        logger.notice(
            f"Refitting pipelines on the selected datasets: train={on_train}, test={on_test}, validation={on_validation}."
        )

        self._refit_pipelines_attr(X, y)

        return self

    def get_pipeline_metadata(self) -> Dict[str, PipelineMetadata]:
        """
        Returns a list of metadata objects, each containing information about a pipeline.
        NOTE: Only available after fortify() has been called.
        """
        if not self._pipeline_metadata:
            raise ValueError("No metadata available. Please run fortify() first to generate the metadata.")
        return self._pipeline_metadata

    def get_explained_features(self) -> Dict[str, pd.DataFrame]:
        """
        Get the feature importance of the features from all pipelines, using the LIME algorithm.

        Returns
        -------
        explained_features: Dict[str, pd.DataFrame]
            A dictionary containing the feature importance of the features from all pipelines,
            where the key is the name of the pipeline and the value is a dataframe containing the feature importances.
        """
        metadata_dict: Dict[str, PipelineMetadata] = self.get_pipeline_metadata()

        explained_features_dict = {
            obj.pipeline_name: obj.explained_features
            for name, obj in metadata_dict.items()
            if obj.explained_features is not None
        }

        return explained_features_dict

    def pre_optimize(
        self,
        max_splits: int = 10,
        n_iter: int = 20,
        init_points: int = 10,
        timeout_duration: Optional[int] = None,
    ) -> "PipelineOrchestrator":
        """
        This method is used to perform a preliminary optimization before building the pipelines.
        It pre-optimizes the order of estimator list, the number of cross-validation splits and ratio between train-and testsize for the cross validation.

        Parameters
        ----------
        max_splits: int, default=10
            The maximum number of cv splits to optimize.

        n_iter: int, default=20
            The number of iterations to perform in the bayesian optimization.

        init_points: int, default=10
            The number of random points to sample before fitting the gaussian process.

        timeout_duration: int, default=None
            The maximum time in seconds to spend on fitting an estimator. If None, no timeout will be set.
            This is useful for preventing the optimization from getting stuck on a single estimator.

        Returns
        -------
        self: PipelineOrchestrator
        """
        self.component_service.optimize_estimator_list(timeout_duration=timeout_duration)
        self.component_service.optimize_n_splits_and_test_size(
            stratify=self.stratify,
            shuffle=self.shuffle,
            max_splits=max_splits,
            n_iter=n_iter,
            init_points=init_points,
            random_state=self.random_state,
        )
        return self

    def build(
        self,
        downcast: bool = True,
        scale: bool = True,
        add_features: bool = True,
        remove_features: bool = True,
        top_n_per_tuner_base: int = 5,
        top_n_per_tuner_stacked_min: int = 2,
        top_n_per_tuner_stacked_max: int = 3,
        generations: List[str] = ["base", "stacked", "evolved"],
        timeout_duration: Optional[int] = None,
    ) -> "PipelineOrchestrator":
        """
        Builds the pipelines for the base models, stacked models and evolution of the stacked models.

        Parameters
        ----------
        downcast: bool = True
            Whether to downcast the data types of the features.
        scale: bool = True
            Whether to scale the features.
        add_features: bool = True
            Whether to add features.
        remove_features: bool = True
            Whether to remove features.
        top_n_per_tuner_base: int = 5
            The number of best models per tuner to include in the base models.
        top_n_per_tuner_stacked_min: int = 2
            The minimum number of best models per tuner to include in the stacked models.
        top_n_per_tuner_stacked_max: int = 3
            The maximum number of best models per tuner to include in the stacked models.
        generations: List[str] = ["base", "stacked", "evolved"]
            The generations to build. Can be "base", "stacked" or "evolved".
        timeout_duration: Optional[int] = None
            The maximum time in seconds, to wait for the fitting to finish during the scoring process of
            self.component_service.generate_pipeline_for_base_models() and self.component_service.generate_pipeline_for_stacked_models().
            If None, no timeout will be set.
            Else, if the timeout is reached, the fitting process will be canceled forcefully.
            Use this to prevent hanging of the fitting process.
            NOTE: This uses multiprocessing which will cause overhead. Only use this if necessary!
        """
        self._validate_generations(generations)

        # Kick off the preprocessing and training process
        self.component_service.initialize(
            downcast=downcast,
            scale=scale,
            add_features=add_features,
            remove_features=remove_features,
        )

        # Generate fitted pipelines for best individual models and stacked models
        if "base" in generations:
            self.pipelines["base"] = self.component_service.generate_pipeline_for_base_models(
                top_n_per_tuner=top_n_per_tuner_base,
                timeout_duration=timeout_duration,
            )

        if "stacked" in generations:
            self.pipelines["stacked"] = self.component_service.generate_pipeline_for_stacked_models(
                top_n_per_tuner_range=[
                    top_n_per_tuner_stacked_min,
                    top_n_per_tuner_stacked_max,
                ],
                timeout_duration=timeout_duration,
            )

        # Evolve the pipelines through stack generalization
        if "evolved" in generations:
            evolver = PipelineEvolverService(self.pipelines["stacked"])
            try:
                self.pipelines["evolved"] = evolver.evolve_voting(
                    voting="hard" if self.preperator_service.is_regression else "soft"
                )
                self.pipelines["evolved"].fit(self.X_train, self.y_train)
            except Exception:
                logger.error(
                    f"An error occurred during the creation process of pipeline_evolved:\n{traceback.format_exc()}"
                )

        return self

    def fortify(
        self,
        threshold_score: Optional[float] = None,
        reg_trials: int = 5,
        clf_max_occurance_pct: float = 0.8,
        optimize_n_jobs: bool = False,
        fraction_to_explain: float = 1.0,
        shuffle_explaining: bool = False,
        plot_explaining: bool = False,
        refit_on_all_data: bool = False,
    ) -> PipelineManager:
        """
        Fortifies the pipelines by testing them on robustness on the validation set.\n
        Removes the estimators from the pipelines that do not pass the robustness test.\n
        Adds the pipelines and related information to self._pipeline_metadata.\n
        Feature explanations are also created on a per-sample basis. These can be retrieved with get_explained_features().\n
        NOTE: self.pipelines gets updated in-place.

        Parameters
        ----------
        threshold_score: Optional[float]
            Set a threshold score for the robustness test.
            If None (default), the threshold is set to the mean of the test scores.
            Only if the score of the pipeline is above the threshold score, the pipeline will be fortified.
            This is useful if a certain score is required for the pipeline to be useful.
        reg_trials: int
            Amount of trials for the regression stress test, where the pipeline is compared against random predictions.
        clf_max_occurance_pct: float
            The maximum allowed percentage of the most occurring class in the predictions of the pipeline.
            If the percentage of the most occurring class is higher than this value, the pipeline will be removed.
        optimize_n_jobs: bool
            Optimize the n_jobs parameter of the estimators in the pipeline.
            This ensures `predict` method will be executed in the most efficient way.
        fraction_to_explain: float
            The fraction of the dataset to explain.
            Must be between 0.0 and 1.0.
            if 0.0, no features will be explained.
            if 1.0, all features will be explained.
        shuffle_explaining: bool
            If True, the dataset will be shuffled before explaining.
            If False, the dataset will not be shuffled before explaining and the first n rows will be explained.
        plot_explaining: bool
            Whether to plot the explaining plots for feature importance and distribution.
        refit_on_all_data: bool
            Utility-option which refits the pipelines on all data at the end (train, test and validation).
            Calls self.refit_pipelines() internally.

        Returns
        -------
        PipelineManager:
            A dictionary containing the fortified pipelines.
            If empty, no pipelines passed the robustness test.
        """
        pipelines_copy = deepcopy(
            {name: pipe for name, pipe in self.pipelines.items() if pipe is not None}
        )  # make a copy to iterate over, so we can delete pipelines from the original dict. skip pipelines that are None.

        for pipeline_name, pipeline in pipelines_copy.items():
            if not pipeline.estimators:
                logger.warning(f"'{pipeline_name}' has no estimators. It will be removed.")
                del self.pipelines[pipeline_name]
                continue

            robust_pipeline = self._stress_test_pipeline(
                pipeline_name,
                pipeline,
                threshold_score=threshold_score,
                reg_trials=reg_trials,
                clf_max_occurance_pct=clf_max_occurance_pct,
                fraction_to_explain=fraction_to_explain,
                shuffle_explaining=shuffle_explaining,
                plot_explaining=plot_explaining,
            )

            if robust_pipeline is not None:
                logger.notice(f"MultiEstimatorPipeline '{pipeline_name}' is fortified successfully")
                if optimize_n_jobs:
                    robust_pipeline.optimize_n_jobs(self.X_val)
                self.pipelines[pipeline_name] = robust_pipeline
            else:
                logger.warning(
                    f"MultiEstimatorPipeline '{pipeline_name}' is not fortified, meaning it was not robust enough."
                )
                del self.pipelines[pipeline_name]

        if refit_on_all_data:
            self.refit_pipelines(on_train=True, on_test=True, on_validation=True)

        return self.pipelines

    def _stress_test_pipeline(
        self,
        pipeline_name: str,
        pipeline_to_test: Union[MultiEstimatorPipeline, None],
        threshold_score: Optional[float] = None,
        reg_trials: int = 5,
        clf_max_occurance_pct: float = 0.8,
        fraction_to_explain: float = 1.0,
        shuffle_explaining: bool = False,
        plot_explaining: bool = False,
    ) -> Union[MultiEstimatorPipeline, None]:
        """
        Test the pipeline on robustness through 2 stress tests.
        Removes the estimators from the pipeline that do not pass the stress tests.

        Parameters
        ----------
        pipeline_name: str
            The name of the pipeline to test.
        pipeline_to_test: MultiEstimatorPipeline
            The pipeline to test.
        threshold_score: Optional[float]
            Set a custom threshold score for the robustness test.
            If None (default), the threshold is set to the mean of the test scores.
            Only if the score of the pipeline is above the threshold score, the pipeline will be fortified.
            This is useful if a certain score is required for the pipeline to be useful.
        reg_trials: int
            Amount of trials for the regression stress test, where the pipeline is compared against random predictions.
        clf_max_occurance_pct: float
            The maximum allowed percentage of the most occurring class in the predictions of the pipeline.
            If the percentage of the most occurring class is higher than this value, the pipeline will be removed.
        fraction_to_explain: float
            The fraction of the dataset to explain.
        shuffle_explaining: bool
            If True, the dataset will be shuffled before explaining.
            If False, the dataset will not be shuffled before explaining and the first n rows will be explained.
        plot_explaining: bool
            Whether to plot the explaining feature importance plot.
        """
        if pipeline_to_test is None:
            msg = f"'{pipeline_name}' is None. Please run build() first."
            logger.error(msg)
            raise ValueError(msg)

        performance_service = PerformanceService(
            pipeline_to_test,
            self.X_train,
            self.X_val,
            self.y_val,
            metric=self.metric,
        )

        # flag to pass to the pipeline metadata
        pipeline_is_robust = False
        robust_pipeline = None
        try:
            robust_pipeline = performance_service.stress_test_pipeline(
                threshold_score=threshold_score,
                clf_max_occurance_pct=clf_max_occurance_pct,
                reg_trials=reg_trials,
                pipeline_name=pipeline_name,
            )
            pipeline_is_robust = True
        except NoRobustModelsInPipelineError:
            logger.error(
                traceback.format_exc(),
            )
            pipeline_is_robust = False
            return None
        finally:
            metadata_obj = PipelineMetadata(
                pipeline_name,
                pipeline_to_test if robust_pipeline is None else robust_pipeline,
                pipeline_is_robust,
            )
            if fraction_to_explain:  # if more than 0.0
                try:
                    logger.notice(f"Getting explained features for pipeline '{pipeline_name}'...")
                    explained_features = performance_service.get_explained_features(
                        fraction=fraction_to_explain,
                        shuffle=shuffle_explaining,
                        plot=plot_explaining,
                    )
                    metadata_obj.explained_features = explained_features
                except Exception as e:
                    logger.error(
                        f"An {type(e).__name__} occurred during the creation process of the feature importance plot:\n {traceback.format_exc()}",
                    )

            logger.notice(f"Getting explained distribution for pipeline '{pipeline_name}'...")
            explained_distribution = performance_service.get_distribution(plot=plot_explaining)
            metadata_obj.explained_distribution = explained_distribution

            self._pipeline_metadata[pipeline_name] = metadata_obj

        return robust_pipeline

    def _reassemble_Xy_for_refitting(self, on_train: bool, on_test: bool, on_validation: bool):
        X_parts = []
        y_parts = []

        if on_train:
            X_parts.append(self.X_train)
            y_parts.append(self.y_train)

        if on_test:
            X_parts.append(self.X_test)
            y_parts.append(self.y_test)

        if on_validation:
            X_parts.append(self.X_val)
            y_parts.append(self.y_val)

        X = pd.concat(X_parts, axis=0)
        y = pd.concat(y_parts, axis=0)
        return X, y

    def _refit_pipelines_attr(self, X: pd.DataFrame, y: pd.Series) -> None:
        if not any(self.pipelines.values()):
            raise ValueError(
                "No pipelines in self.pipelines to refit. This might be because build() is not run yet or because all pipelines were not robust enough"
            )

        for name, pipeline in self.pipelines.items():
            if pipeline is not None:
                try:
                    pipeline.fit(X, y)
                    logger.notice(f"Successfully refitted {name}")
                except ValueError:
                    logger.error(
                        f"A ValueError occurred during the fitting process of {name}: {traceback.format_exc()}",
                    )
            else:
                logger.notice(
                    f"Trying to (re)fit the pipeline '{name}', but '{name}' is None. This could be intentional. If not, please run build() first.",
                )

    def _validate_generations(self, generations: List[str]) -> None:
        choices = {"base", "stacked", "evolved"}
        if not choices.issuperset(generations):
            raise ValueError(f"generations must be from: {choices}")
        if "evolved" in generations and not "stacked" in generations:
            raise ValueError("generations must include 'stacked' if 'evolved' is included")

    def _initialize_metadata_data(self) -> dict:
        data_metadata = {
            "X": {
                "length": len(self.X_train),
                "type": type(self.X_train),
                "columns": self.X_train.columns.tolist(),
            },
            "y": {
                "length": len(self.y_train),
                "type": type(self.y_train),
            },
        }
        return data_metadata
