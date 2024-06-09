"""Collect metadata of a `MultiEstimatorPipeline`."""

from typing import Optional

import pandas as pd

from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline


class PipelineMetadata:
    """
    A class to store metadata of a single `MultiEstimatorPipeline`. Use this after `PipelineOrchestrator.fortify()` has been called.
    Metatata collected in `PipelineOrchestrator.fortify() -> PipelineMetadataCollector._stress_test_pipeline()`

    Public Attributes
    -----------------
    pipeline_name : str
        The name of the pipeline.
    pipeline : MultiEstimatorPipeline
        The pipeline.
    explained_features : pd.Series
        A series of the features that were used in the pipeline and their importance.
    explained_distribution : pd.Series
        A series of the distribution of the predictions compared the real values.
    is_robust : bool
        Whether the pipeline is robust or not.
    scores: pd.DataFrame
        A dataframe of scores of the estimators the pipeline.
    performance: float
        The overall performance of the pipeline in one single scalar.
        calculated by the weighted average of the scores of the estimators in the pipeline.
    """

    def __init__(self, pipeline_name: str, pipeline: MultiEstimatorPipeline, is_robust: bool) -> None:
        """
        Parameters
        ----------
        pipeline_name : str
            The name of the pipeline.
        pipeline : `MultiEstimatorPipeline`
            The pipeline.
        is_robust : bool
            Whether the pipeline is robust or not.
        """
        self.pipeline_name: str = pipeline_name
        self.pipeline: MultiEstimatorPipeline = pipeline
        self.explained_features: Optional[pd.Series] = None
        self.explained_distribution: Optional[pd.DataFrame] = None
        self.is_robust: bool = is_robust

    def __repr__(self) -> str:
        return f"PipelineMetadata(pipeline_name={self.pipeline_name}, pipeline={self.pipeline}, explained_features={self.explained_features}, explained_distribution={self.explained_distribution}, is_robust={self.is_robust})"

    @property
    def scores(self) -> pd.DataFrame:  # pylint: disable=missing-function-docstring
        return self.pipeline.scores

    @property
    def performance(self) -> float:  # pylint: disable=missing-function-docstring
        return self.pipeline.performance

    @property
    def metric(self) -> float:  # pylint: disable=missing-function-docstring
        return self.pipeline.metric

    @property
    def maximize_scoring(self):  # pylint: disable=missing-function-docstring
        return self.pipeline.maximize_scoring

    @property
    def type_estimator(self):  # pylint: disable=missing-function-docstring
        return self.pipeline.type_estimator

    @property
    def generation(self) -> int:  # pylint: disable=missing-function-docstring
        return self.pipeline.generation
