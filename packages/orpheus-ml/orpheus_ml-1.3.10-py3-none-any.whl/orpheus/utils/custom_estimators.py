"""Custom estimator-related wrappers for use in pipelines"""

import traceback
from typing import Callable, List, Optional, Union

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.pipeline import FunctionTransformer

from orpheus.utils.custom_types import EstimatorType
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger
from orpheus.validations.estimators import is_estimator


class BaseEstimatorWrapper(BaseEstimator):
    """
    Custom wrapper that enables the implementation of estimators in a MultiEstimatorWrapper.
    Acts as a baseclass for the RegressorWrapper and ClassifierWrapper classes
    """

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y=None, **fit_params) -> "BaseEstimatorWrapper":
        self.estimator.fit(X, y, **fit_params)
        return self

    def predict(self, X, *args, **kwargs):
        return self.estimator.predict(X, *args, **kwargs)

    def __iter__(self):
        if hasattr(self.estimator, "estimators"):
            yield from self.estimator.estimators
        else:
            yield self.estimator

    def __repr__(self):
        return f"{get_obj_name(self)}({self.estimator})"


class PredictFuncWrapper(BaseEstimatorWrapper):
    """
    Wrapper that enables the use of a predict function in a MultiEstimatorWrapper.
    """

    def __init__(self, predict_func: Callable):
        estimator = FunctionTransformer(predict_func)
        super().__init__(estimator)

    def predict(self, X, *args, **kwargs):
        return self.estimator.func(X, *args, **kwargs)


class RegressorWrapper(BaseEstimatorWrapper, RegressorMixin):
    """
    Wrapper that enables the use of a regressor in a MultiEstimatorWrapper.
    """


class ClassifierWrapper(BaseEstimatorWrapper, ClassifierMixin):
    """
    Wrapper that enables the use of a classifier in a MultiEstimatorWrapper.
    """


class ClassifierWrapperWithPredictProba(ClassifierWrapper):
    """
    Wrapper that enables the use of a classifier with predict_proba in a MultiEstimatorWrapper.
    """

    def predict_proba(self, X, *args, **kwargs):
        return self.estimator.predict_proba(X, *args, **kwargs)


class MultiEstimatorWrapper(BaseEstimator):
    """
    Wrapper that enables the use of multiple estimators in a MultiEstimatorPipeline.
    This wrapper needs to be added as the last step in the pipeline.
    """

    def __init__(self, estimators: List[EstimatorType]):
        self.estimators = estimators

    @property
    def estimators(self) -> List[EstimatorType]:
        if not self._estimators:
            return []
            # raise ValueError("No estimators have been set")
        return self._estimators

    @estimators.setter
    def estimators(self, estimators: List[EstimatorType]):
        if is_estimator(estimators):
            estimators = [estimators]
        if not isinstance(estimators, list):
            raise ValueError(f"estimators must be a list, not {type(estimators)}")
        self._estimators = estimators

    def __getitem__(self, index: int):
        return self.estimators[index]

    def __setitem__(self, index: int, estimator: EstimatorType):
        if not is_estimator(estimator):
            raise ValueError(f"estimator must be a valid estimator, not {type(estimator)}")
        self._estimators[index] = estimator

    def __len__(self):
        return len(self.estimators)

    def __iter__(self):
        yield from self.estimators

    def __repr__(self):
        return f"{get_obj_name(self)}({self.estimators})"

    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return bool(self.estimators)

    def fit(self, X, y=None) -> "MultiEstimatorWrapper":
        """Fit all estimators"""
        successful_estimators = []
        for estimator in self.estimators:
            try:
                estimator.fit(X, y)
                successful_estimators.append(estimator)
            except Exception:
                logger.error(
                    f"Error fitting estimator {estimator}, which will be removed from self.estimators:\n{traceback.format_exc()}",
                )

        # Update the estimators list with only successful estimators
        self.estimators = successful_estimators
        return self

    def predict(self, X, **kwargs) -> np.ndarray:
        """
        Return the predictions for data.

        parameters:
        ----------
        X: array-like
            Data to predict
        index: int
            Index of the estimator to use for prediction.  If None, all estimators are used.
            Estimators are sorted by their score, so in general the first estimator is the best.
        n_jobs: int
            Number of jobs to run in parallel. If None, n_jobs is the value as passed to ComponentService.
        **kwargs:
            Additional keyword arguments that may be passed to the superclass method
        """
        return self._predict_wrapper(X, "predict", **kwargs)

    def predict_proba(self, X, **kwargs) -> np.ndarray:
        """
        Return the prediction probabilities for data.

        parameters:
        ----------
        X: array-like
            Data to predict
        index: int
            Index of the estimator to use for prediction.  If None, all estimators are used.
            Estimators are sorted by their score, so in general the first estimator is the best.
        n_jobs: int
            Number of jobs to run in parallel. If None, n_jobs is the value as passed to ComponentService.
        **kwargs:
            Additional keyword arguments that may be passed to the superclass method
        """
        return self._predict_wrapper(X, "predict_proba", **kwargs)

    def predict_log_proba(self, X, **kwargs) -> np.ndarray:
        """
        Return the prediction log probabilities for data.

        parameters:
        ----------
        X: array-like
            Data to predict
        **kwargs:
            Additional keyword arguments that may be passed to the superclass method
        """
        return self._predict_wrapper(X, "predict_log_proba", **kwargs)

    def decision_function(self, X, **kwargs) -> np.ndarray:
        """
        Return the decision function for data.

        parameters:
        ----------
        X: array-like
            Data to predict
        **kwargs:
            Additional keyword arguments that may be passed to the superclass method
        """
        return self._predict_wrapper(X, "decision_function", **kwargs)

    def score(self, X, y, metric: Optional[Callable] = None, **predict_kwargs) -> np.ndarray:
        """
        Return the score for data.
        Included estimators must have a score method.
        """
        scores = []
        for estimator in self.estimators:
            try:
                if metric is None:
                    score = estimator.score(X, y)
                else:
                    y_pred = estimator.predict(X, **predict_kwargs)
                    score = metric(y_pred, y)
                scores.append(score)
            # we prefer to catch all exceptions here, because we want to continue scoring.
            # estimators might fail for a variety of reasons, and we can handle them as nans.
            except Exception as e:
                scores.append(np.nan)
                logger.error(f"Error during scoring of estimator {estimator}: {e}")
        return np.asarray(scores)

    def _predict_wrapper(self, X: pd.DataFrame, predict_func_name: str, **kwargs) -> np.ndarray:
        """
        Wrapper for predict functions that might not be implemented by all estimators.
        """
        index = kwargs.get("index")
        n_jobs = kwargs.get("n_jobs")

        estimators = (
            [estimator for estimator in self.estimators if hasattr(estimator, predict_func_name)]
            if predict_func_name in ["predict_proba", "predict_log_proba"]
            else self.estimators
        )

        if index is not None:
            return getattr(estimators[index], predict_func_name)(X)

        def predict(estimator) -> Union[str, np.ndarray]:
            try:
                return getattr(estimator, predict_func_name)(X)
            except Exception:
                return traceback.format_exc()

        if n_jobs is not None:
            results = Parallel(n_jobs=n_jobs)(delayed(predict)(estimator) for estimator in estimators)
        else:
            results = [predict(estimator) for estimator in estimators]

        predictions = []
        for result in results:
            if isinstance(result, str):
                logger.error(result)
            else:
                predictions.append(result)

        try:
            predictions = np.asarray(predictions)
        except ValueError as e:
            if str(e).startswith("setting an array element with a sequence"):
                logger.error(f"Error during {predict_func_name}:\n{traceback.format_exc()}")
                primary_shape = [pred.shape[0] for pred in predictions if pred is not None]
                all_shapes_are_equal = all(element == primary_shape[0] for element in primary_shape)
                if not all_shapes_are_equal:
                    raise e from None
                predictions = np.asarray([pred.flatten() for pred in predictions if pred is not None])

        return predictions
