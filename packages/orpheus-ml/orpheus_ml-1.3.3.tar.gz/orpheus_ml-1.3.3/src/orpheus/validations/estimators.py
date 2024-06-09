"""Custom Estimators Validations."""
from typing import Any


from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import orpheus.utils.custom_estimators as custom_estimators


def is_estimator(estimator: Any) -> bool:
    """Check if the estimator is a valid estimator according to sklearn's definition."""
    return isinstance(estimator, BaseEstimator) and all(hasattr(estimator, attr) for attr in ["fit", "predict"])


def pipeline_has_estimator_step(pipeline: Pipeline) -> bool:
    """Check if the last step of the pipeline is an estimator."""
    return bool(pipeline.steps) and bool(pipeline.steps[-1][1]) and is_estimator(pipeline.steps[-1][1])


def estimators_are_valid(pipeline: Pipeline) -> bool:
    """Check if the estimators in the pipeline are valid for the MultiEstimatorPipeline."""
    return isinstance(pipeline.steps[-1][1], custom_estimators.MultiEstimatorWrapper)
