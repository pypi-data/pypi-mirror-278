"""Performance Service for combining several performance-based metrics in one place"""

from copy import deepcopy
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from orpheus.evaluators.evaluator import Evaluator
from orpheus.evaluators.model_explainer import ModelExplainer
from orpheus.metrics.metric_converter import MetricConverter
from orpheus.services.additional_types.multi_estimator_pipeline import (
    MultiEstimatorPipeline,
)
from orpheus.utils.custom_exceptions import NoRobustModelsInPipelineError
from orpheus.utils.logger import logger
from orpheus.validations.input_checks import ClassValidation


class PerformanceService:
    """
    Performance Service for combining several performance-based metrics in one place on a trained MultiEstimatorPipeline

    Public Methods
    --------------
    stress_test_pipeline
        Utility function that tests the robustness of the model(s) through 2 stresstests
        and returns a pipeline with only the robust models.
        Raises an NoRobustModelsInPipelineError if no models in the pipeline are robust enough.

    get_robustness
        Calculates the robustness of the model(s).
        If one model is used, the list will contain one integer if model is robust.
        If multiple models are used, the list will contain integers, representing the indexes of the robust models.
        If the list is empty, no models are robust.

    get_distribution
        Calculates the distribution of the model predictions.
        First column represents distribution of y_true,
        the following column(s) represent the distribution of model predictions.

    get_scores
        Calculates the scores of the model predictions.

    get_explained_features
        Explains the model predictions for a given dataset.
    """

    def __init__(
        self,
        pipeline: MultiEstimatorPipeline,
        X_train: pd.DataFrame,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        metric: Callable,
    ):
        """
        Initializes the PerformanceService class.
        NOTE: Make sure X_val and y_val are unseen data to get reliable results. Meaning X_test and y_test used in `ComponentService` should not be used here.

        Parameters
        ----------
        pipeline : MultiEstimatorPipeline
            The trained MultiEstimatorPipeline object to evaluate.
        X_train : pd.DataFrame
            A pandas dataframe containing the training dataset that was used to train the pipeline.
        X_val : pd.DataFrame
            A pandas dataframe containing the validation dataset that will be used to evaluate the pipeline.
        y_val : pd.Series
            A pandas series containing the target variable of the validation dataset.
        metric : Callable
            A callable object representing the performance metric.
        """
        self.X_train = X_train
        self.X_val = X_val
        self.y_val = y_val
        self.metric = metric

        self.evaluator = Evaluator(metric)
        metric_converter = MetricConverter(metric)
        self.type_estimator = metric_converter.type_estimator
        self.maximize_scoring = metric_converter.maximize_scoring
        self.pipeline = pipeline

    def __repr__(self):
        return f"PerformanceService(pipeline={self.pipeline}, X_val shape={self.X_val.shape}, y_val shape={self.y_val.shape}, metric={self.metric})"

    @property
    def pipeline(self) -> MultiEstimatorPipeline:
        """Returns the pipeline."""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline: MultiEstimatorPipeline):
        """Sets the pipeline."""
        ClassValidation.validate_performance_service(pipeline, self.X_train, self.X_val, self.metric)
        self.explainer = ModelExplainer(
            model=pipeline,
            X_train=self.X_train,
            mode=("regression" if self.type_estimator == "regressor" else "classification"),
        )
        self._pipeline = pipeline

    def set_pipeline(self, pipeline: MultiEstimatorPipeline):
        """Sets the pipeline."""
        self.pipeline = pipeline

    def get_pipeline(self) -> MultiEstimatorPipeline:
        """Returns the current pipeline."""
        return self.pipeline

    def stress_test_pipeline(
        self,
        clf_max_occurance_pct: float = 0.8,
        reg_trials: int = 5,
        overwrite_pipeline: bool = False,
        threshold_score: Optional[float] = None,
        pipeline_name: str = "",
    ) -> MultiEstimatorPipeline:
        """
        Utility function that tests the robustness of self.pipeline through 2 stresstests
        and returns a pipeline with only the robust models.
        Raises an NoRobustModelsInPipelineError if no models in the pipeline are robust enough.

        Parameters
        ----------
        clf_max_occurance_pct: float, default=0.8
            The maximum percentage of occurrences of a class in the dataset.
            Especially useful against overfitting.
            Only used if the model is a classifier.
        reg_trials: int, default=5
            The number of trials to run.
            The more trials, the more robust the model will be.
            Only used if the model is a regressor.
        overwrite_pipeline: bool, default=False
            If True, self.pipeline will be overwritten with the robust pipeline.
        threshold_score: float or None, default=None
                The threshold score for robustness.
                If None, the threshold is set to the mean of the test scores.
                Otherwise, only models with validation scores
                greater than or equal to the threshold score (if maximize_scoring is True)
                or less than or equal to the threshold score (if maximize_scoring is False)
                will be considered robust.
        """
        pipeline = deepcopy(self.pipeline)

        robust_model_indexes = self._first_stress_test(clf_max_occurance_pct, reg_trials, pipeline)
        if robust_model_indexes:
            logger.notice(
                f"Models in pipeline '{pipeline_name}' which passed first stress test: {robust_model_indexes}"
            )

            (
                threshold_score,
                robust_model_indexes,
                validation_scores,
            ) = self._second_stress_test(threshold_score, pipeline, robust_model_indexes)

            if not robust_model_indexes:
                raise NoRobustModelsInPipelineError(
                    threshold_score,
                    validation_scores,
                    f"No robust models found in pipeline '{pipeline_name}'. Failed at second stress test.",
                )

            self._display_models_which_passed_second_stress_test(
                threshold_score,
                pipeline,
                robust_model_indexes,
                validation_scores,
                pipeline_name,
            )

            # modify the estimators in pipeline by removing the non-robust ones
            pipeline.estimators = [pipeline.estimators[i] for i in robust_model_indexes]

            # modify the scores of the pipeline by bypassing the "official" way of updating them,
            # as that would possibly cause an error with because of different length.
            pipeline._modify_indexes_scores(robust_model_indexes)
            pipeline.update_scores(validation_scores[robust_model_indexes])
        else:
            validation_scores = None
            raise NoRobustModelsInPipelineError(
                threshold_score,
                validation_scores,
                f"No robust models found in pipeline {pipeline_name}. Failed at first stress test.",
            )

        if overwrite_pipeline:
            self.pipeline = pipeline
        return pipeline

    def get_robustness(
        self,
        clf_max_occurance_pct: float = 0.8,
        reg_trials: int = 5,
        pipeline: Optional[MultiEstimatorPipeline] = None,
    ) -> List[int]:
        """
        Calculates the robustness of the model(s).
        If one model is used, the list will contain one integer if model is robust.
        If multiple models are used, the list will contain integers, representing the indexes of the robust models.
        If the list is empty, no models are robust.

        Parameters
        ----------
        clf_max_occurance_pct: float = 0.8
            The maximum percentage of occurances of a value in the dataset.
            Only used if the model is a classifier.
        reg_trials: int = 5,
            The number of reg_trials to run.

        Returns:
            List[int]: A list of integers representing the robustness of the model.
        """
        return self.evaluator.evaluate_robustness(
            self.X_val,
            self.y_val,
            pipeline=pipeline,
            clf_max_occurance_pct=clf_max_occurance_pct,
            reg_trials=reg_trials,
        )

    def get_distribution(self, plot: bool = False, y_pred: Optional[np.ndarray] = None) -> pd.DataFrame:
        """
        Calculates the distribution of the model predictions.
        First column represents distribution of y_true,
        the following column(s) represent the distribution of model predictions.

        Parameters
        ----------
        plot: bool = False
            Whether to plot the distribution.

        Returns:
            pd.DataFrame: A pandas dataframe representing the distribution of the model predictions.
        """
        if y_pred is None:
            y_pred = self.pipeline.predict(self.X_val)
        return self.evaluator.get_distribution(self.y_val, y_pred, plot=plot)

    def get_scores(self) -> Union[float, pd.Series]:
        """
        Calculates the scores of the model predictions.

        Returns:
            np.ndarray[float] | pd.Series: A numpy array or pandas series representing the performance of the model.
        """
        y_pred = self.pipeline.predict(self.X_val)
        return self.evaluator.evaluate_performance(self.y_val, y_pred)

    def get_explained_features(
        self,
        fraction: float = 1.0,
        plot=False,
        num_features: Optional[int] = None,
        shuffle: bool = False,
        random_state: Optional[int] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Explains the model predictions for a given dataset.

        Parameters
        ----------
        fraction: float = 1.0
            The fraction of the dataset to explain.

        plot: bool = False
            Whether to plot the explained features.

        num_features: Optional[int] = None
            The number of features to explain.
            Default is all features in the dataset.

        shuffle: bool = False
            Whether to shuffle the dataset before explaining.

        random_state: Optional[int] = None
            The random state to use for shuffling the dataset.

        Returns:
            Explanation: An Explanation object representing the model's predicted values.
        """
        return self.explainer.explain_all(
            self.X_val,
            fraction=fraction,
            shuffle=shuffle,
            plot=plot,
            num_features=num_features,
            random_state=random_state,
            **kwargs,
        )

    def _display_models_which_passed_second_stress_test(
        self,
        threshold_score: Optional[float],
        pipeline: MultiEstimatorPipeline,
        robust_model_indexes: List[int],
        validation_scores: Union[float, pd.Series],
        pipeline_name: Optional[str],
    ):
        logger.notice(
            f"Keeping {len(robust_model_indexes)}/{len(pipeline.estimators)} robust models in pipeline {pipeline_name} which passed both stresstests.",
        )
        logger.notice(f"threshold_score: {threshold_score}")
        if not np.isscalar(validation_scores):
            results = pd.Series({i: validation_scores[i] for i in robust_model_indexes})
            logger.notice(
                f"Robust models in pipeline {pipeline_name} validation scores which passed second stresstest:\n{results.to_string()}",
            )
        else:
            logger.notice(
                f"Robust models in pipeline {pipeline_name} validation score which passed second stresstest: {validation_scores}"
            )

    def _first_stress_test(
        self,
        clf_max_occurance_pct: float,
        reg_trials: int,
        pipeline: MultiEstimatorPipeline,
    ):
        robust_model_indexes = self.get_robustness(
            pipeline=pipeline,
            clf_max_occurance_pct=clf_max_occurance_pct,
            reg_trials=reg_trials,
        )

        return robust_model_indexes

    def _second_stress_test(
        self,
        threshold_score: Optional[float],
        pipeline: MultiEstimatorPipeline,
        robust_model_indexes: List[int],
    ) -> Tuple[Optional[float], List[int], Union[float, pd.Series]]:
        validation_scores = self.get_scores()
        validation_scores = (
            validation_scores.loc[robust_model_indexes] if not np.isscalar(validation_scores) else validation_scores
        )
        test_scores = pipeline.get_scores()
        test_score_mean = test_scores.mean().mean()

        if threshold_score is None:
            threshold_score = test_score_mean

        if not np.isscalar(validation_scores):
            robust_model_indexes = [
                model_idx
                for model_idx, validation_score in validation_scores.items()
                if not np.isnan(validation_score)
                and (
                    validation_score >= threshold_score
                    if self.maximize_scoring
                    else validation_score <= threshold_score
                )
            ]
        else:
            if not (
                validation_scores >= threshold_score if self.maximize_scoring else validation_scores <= threshold_score
            ):
                robust_model_indexes = []
        return threshold_score, robust_model_indexes, validation_scores
