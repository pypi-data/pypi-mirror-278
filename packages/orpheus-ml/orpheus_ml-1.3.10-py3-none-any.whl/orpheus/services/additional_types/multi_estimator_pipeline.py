"""
Instances of this class are generated through the ComponentService class,
with the methods `generate_pipeline_for_stacked_models` and `generate_pipeline_for_base_models`.
It extends the sklearn Pipeline class with additional functionality,
such as the ability to add multiple estimators, update scores and weights of the estimators.
"""

import inspect
import multiprocessing as mp
import timeit
import traceback
from functools import partial
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from orpheus.services.additional_types.utils import MultiEstimatorPipelineScoreTracker
from orpheus.utils.constants import DEFAULT_VALUES
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.utils.custom_types import EstimatorType
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger
from orpheus.validations import input_checks
from orpheus.validations.converts import convert_n_jobs_to_num_workers
from orpheus.validations.estimators import (
    estimators_are_valid,
    is_estimator,
    pipeline_has_estimator_step,
)
from orpheus.validations.transformers import is_transformer


class MultiEstimatorPipeline(Pipeline):
    """
    A scikit-learn pipeline with additional functionality, the main one being the ability
    to add multiple estimators and make predictions with them.

    This pipeline also keeps track of the scores of the estimators in the pipeline.
    The scores can be updated and can be used to determine the weights of
    the estimators when making predictions.

    While indexes of estimators in the pipeline are based on their performance of the
    first scores used to initialize the pipeline, depending on the nature of the data,
    performance of the estimators can change over time.
    In that case, it is recommended to regularly update the scores of the estimators
    in the pipeline, and to use the `get_weights` method to determine the weights of the estimators.

    Attributes:
    ----------
    scores : list
        List of scores for the estimators in the pipeline.
        The scores are sorted in the same order as
        the estimators in the pipeline.

    estimators : list
        List of estimators in the pipeline.
        The estimators are sorted in the same order as
        the initial scores in the pipeline.

    n_jobs : int, optional
        Number of jobs to run in parallel.
        If not provided, estimators are run with the setting passed to the ComponentService.

    public methods:
    -------
    predict(X, index=None, n_jobs=None, **kwargs)
        Return the predictions for the given data.

    predict_proba(X, index=None, n_jobs=None, **kwargs)
        Return the predictions as probabilities for the given data.
        Only works if estimators in the pipeline have a predict_proba method.

    def score(X, y, update_scores=False, max_mem_size_scores=10, sample_weight=None)
        Return the score for the given data.
        If update_scores is True, the score is added to the scores attribute, aka the "memory".
        The memory is used to update the weights of the estimators in the pipeline.

    optimize_n_jobs(X, **kwargs)
        Optimize the number of jobs to use for the estimators in the pipeline.
        It is recommended to use this method before making predictions with the pipeline,
        to ensure that speed of the predictions is optimal.

    save(path)
        Save the MultiEstimatorPipeline to disk.

    @staticmethod::
    load(path)
        Load a MultiEstimatorPipeline from disk.

    utility methods:
    -------
    get_weights(decay_rate=None)
        Return the weights of the estimators in the pipeline.
        It can be used to get an idea of the performance of the estimators.

    get_name_by_index(index)
        Return the name of the estimator at the given index.

    get_scores()
        Return list of scores for the estimators in the pipeline. Also gettable through the scores attribute.

    get_stats()
        Return a DataFrame with the index, estimatornames, weights and estimators in the pipeline.


    ---all other methods and attributes from sklearn Pipeline class---

    public attributes:
    -------
    scores: List[NDArray[np.float64]]
        List of scores for the estimators in the pipeline.

    performance: float
        Weighted average of all models in the pipeline.
        Aimes to use one single scalar to describe the overall (scoring) performance of the pipeline.

    estimators: List[EstimatorType]
        List of estimators in the pipeline.

    generation: Optional[Literal["base", "stacked", "evolved"]]
        The generation of the MultiEstimatorPipeline.
        This attribute is set when the MultiEstimatorPipeline is generated through and specific to the ComponentService class.

    type_estimator: Literal["regressor", "classifier"]
        The type of estimator to be used.

    estimators_are_set: bool
        Whether the estimators are set as last step of the pipeline or not.
    """

    def __init__(
        self,
        steps: List,
        type_estimator: Literal["regressor", "classifier"],
        metric: Callable[[pd.Series, pd.Series], float],
        maximize_scoring: bool,
        verbose: int = DEFAULT_VALUES["verbose"],
        **kwargs,
    ):
        """
        Parameters:
        ----------
        steps : list
            List of (name, transform) tuples (implementing fit/transform) that are chained,
            in the order in which they are chained, with the last object a collection of estimators.

        type_estimator : str
            Type of estimator to be used. Options are 'regressor' and 'classifier'.

        maximize_scoring : bool
            Whether the scoring function is maximized or minimized.
            If True, the best estimator is the one with the highest score.
            If False, the best estimator is the one with the lowest score.


        verbose : int, default=1
            Controls the verbosity of the pipeline.
            1=no output, 1=warnings+errors only, 2=notice, 3=info
            The Pipeline class, where this class is a subclass of, also has a verbose attribute,
            which is a boolean. This attribute is set to True if verbose is 1, else False.

            If there are other instances of MultiEstimatorPipeline as steps in the pipeline,
            the verbose attribute of this MultiEstimatorPipeline class is also set to the value of verbose.
        """
        input_checks.AttributeValidation.validate_type_estimator(type_estimator)
        super().__init__(steps, **kwargs)
        self._type_estimator = type_estimator
        self._metric = metric
        self.maximize_scoring = maximize_scoring

        self.generation: Optional[Literal["base", "stacked", "evolved"]] = None
        self._score_tracker = MultiEstimatorPipelineScoreTracker()
        self.leakage_prevention_slice: List[int] = [0, 0]
        self.train_data_mean: Optional[float] = None
        self.test_data_mean: Optional[float] = None

        self.set_verbose(verbose)

    def __repr__(self) -> str:
        return f"MultiEstimatorPipeline(generation={self.generation}, estimators_are_set={self.estimators_are_set}, metric={get_obj_name(self.metric)}, maximize_scoring={self.maximize_scoring}, type_estimator={self._type_estimator}, verbose={logger.get_verbose()}, length scores={self.scores.shape[1]}, performance={self.performance})"

    @property
    def scores(self) -> pd.DataFrame:
        scores = self._score_tracker.scores
        df = pd.DataFrame(scores).T
        df.columns = [f"iteration_{n+1}" for n in df.columns]
        return df

    @property
    def performance(self) -> float:
        try:
            return np.mean(np.average(self.scores, weights=self.get_weights(), axis=0))
        except Exception:
            return np.nan

    @property
    def type_estimator(self) -> str:
        return self._type_estimator

    @property
    def estimator_wrapper(self) -> MultiEstimatorWrapper:
        self._check_if_estimator_wrapper_is_set()
        return self.steps[-1][1]

    @property
    def estimators(self) -> List[EstimatorType]:
        return self.estimator_wrapper.estimators

    @estimators.setter
    def estimators(self, estimators: List[EstimatorType]):
        if is_estimator(estimators):
            estimators = [estimators]
        if not isinstance(estimators, list):
            raise ValueError(f"estimators must be a list, not {type(estimators)}.")
        if not estimators:
            raise ValueError("List of estimators cannot be empty.")
        if not all(is_estimator(estimator) for estimator in estimators):
            non_compatibles = [get_obj_name(type(estimator)) for estimator in estimators if not is_estimator(estimator)]
            raise ValueError(
                f"All estimators in the list must have either a fit or transform method, but the following estimators do not: {non_compatibles}."
            )
        self.steps[-1] = ("estimators", MultiEstimatorWrapper(estimators))

    @property
    def estimators_are_set(self) -> bool:
        return pipeline_has_estimator_step(self) and isinstance(self.steps[-1][1], MultiEstimatorWrapper)

    @property
    def metric(self) -> Callable[[pd.Series, pd.Series], float]:
        return self._metric

    @metric.setter
    def metric(self, metric: Callable[[pd.Series, pd.Series], float]):
        input_checks.AttributeValidation.validate_metric(metric)
        self._metric = metric

    def transform_only(self, X: pd.DataFrame, y=None):
        """
        Transform the data using the transformers in the pipeline.
        Method is named `transform_only` to avoid unexpected behaviour with the `transform` method in the underlying transformers in the pipeline.
        """
        Xt = X
        for _, name, transform in self._iter(with_final=False):
            Xt = transform.transform(Xt)

        return Xt

    def predict(
        self,
        X: pd.DataFrame,
        index: Optional[int] = None,
        n_jobs: Optional[int] = None,
        exclude_transformers: bool = False,
        **kwargs,
    ) -> np.ndarray:
        """
        Return the predictions for the given data.

        Parameters:
        ----------
        X : array-like
            Data to predict
        index : int, optional
            Index of the estimator to use for prediction.
            If not passed, all estimators are used.
            The index of the estimators in the pipeline is determined by scores.
            The first estimator added to the pipeline will have an index of 0,
            the second will have an index of 1, and so on.
            The estimators in the pipeline is sorted based on the first scores added to it.
        n_jobs : int, optional
            Number of jobs to run in parallel for the prediction.
        exclude_transformers : bool, default=False
            Whether to exclude the transformers in the pipeline from the prediction.
            Data is then only passed to the final estimators in the pipeline.
            Keep in mind that the data has to match the input of the final estimator.
        **kwargs:
            Additional keyword arguments that may be passed to the Pipeline (superclass) method.
        Returns:
        -------
        array-like
            Predictions for the given data
        """
        kwargs = self._check_kwargs(index, n_jobs, kwargs)
        return self._predict_func_error_handler("predict", X, exclude_transformers=exclude_transformers, **kwargs)

    def predict_proba(
        self,
        X: pd.DataFrame,
        index: Optional[int] = None,
        n_jobs: Optional[int] = None,
        exclude_transformers: bool = False,
        transform_discrete: bool = False,
        **kwargs,
    ) -> np.ndarray:
        """
        Return the prediction probabilities for the given data.

        Parameters
        ----------
        X : pd.DataFrame
            Data to predict.
        index : int, optional
            Index of the estimator to use for prediction.
            If not passed, all estimators are used.
            The index of the estimators in the pipeline is determined by scores.
            The first estimator added to the pipeline will have an index of 0,
            the second will have an index of 1, and so on.
            The estimators in the pipeline are sorted based on the first scores added to it.
        exclude_transformers : bool, default=False
            Whether to exclude the transformers in the pipeline from the prediction.
            Data is then only passed to the final estimators in the pipeline.
            Keep in mind that the data has to match the input of the final estimator.
        n_jobs : int, optional
            Number of jobs to run in parallel for the prediction.
        transform_discrete : bool, default=False
            Transforms discrete predictions from all estimators to probabilities by dividing each prediction by the sum of all predictions.
            This is useful if for example there are no estimators present in the pipeline with a `predict_proba` method.
        **kwargs
            Additional keyword arguments that may be passed to the superclass method.

        Returns
        -------
        np.ndarray
            Predictions for the given data.
        """
        kwargs = self._check_kwargs(index, n_jobs, kwargs)

        if transform_discrete:
            return self._discrete_predict_proba(X, exclude_transformers=exclude_transformers, **kwargs)

        return self._predict_func_error_handler("predict_proba", X, **kwargs)

    def predict_log_proba(self, X, **kwargs) -> np.ndarray:
        """
        Return the prediction log probabilities for the given data.

        Parameters
        ----------
        X : array-like
            Data to predict.
        **kwargs
            Additional keyword arguments that may be passed to the superclass method.

        Returns
        -------
        array-like
            Predictions for the given data.
        """
        return self._predict_func_error_handler("predict_log_proba", X, **kwargs)

    def decision_function(self, X, **kwargs) -> np.ndarray:
        """
        Return the decision function for the given data.

        Parameters
        ----------
        X : array-like
            Data to predict.
        **kwargs
            Additional keyword arguments that may be passed to the superclass method.

        Returns
        -------
        array-like
            Predictions for the given data.
        """
        return self._predict_func_error_handler("decision_function", X, **kwargs)

    def score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        update_scores: bool = False,
        max_mem_size_scores: int = 10,
        **predict_kwargs,
    ) -> np.ndarray:
        """
        Return the score for data.
        Included estimators must have a score method.

        Parameters
        ----------
        X : pd.DataFrame
            Data to score.
        y : pd.Series
            Target values.
        update_scores : bool, default=False
            Whether to update the scores attribute with the new score.
        max_mem_size_scores : int, default=10
            Maximum number of scores to keep in memory.
        **predict_kwargs
            Additional keyword arguments that may be passed to the superclass method.

        Returns
        -------
        np.ndarray[float]
            Scores for the given data, where each score corresponds to the score of an estimator in the pipeline.
        """
        if X is None or not isinstance(X, pd.DataFrame) or X.empty:
            raise ValueError("Invalid input data. X must be a non-empty DataFrame.")

        if y is not None and (not isinstance(y, pd.Series) or y.empty):
            raise ValueError("Invalid input data. y must be a non-empty Series.")

        X_transformed = self.transform_only(X, y)
        scores = self.estimator_wrapper.score(X_transformed, y, metric=self.metric, **predict_kwargs)

        if update_scores:
            self.update_scores(scores, memory_size=max_mem_size_scores)

        return scores

    def optimize_n_jobs(
        self,
        X: pd.DataFrame,
        n_iter: int = 10,
        exclude: Optional[Literal["transformers", "estimators"]] = None,
    ) -> Tuple[int, Dict[int, float]]:
        """
        Find the optimal n_jobs value for the pipeline to improve the speed of the predict method.
        This is done by implementing a binary search algorithm to find the optimal n_jobs value.
        If found, set the n_jobs value for all estimators, transformers, and the predict method in the pipeline to the optimal value.

        Parameters:
        -----------
        X: array-like
            Data to predict.
        n_iter: int, default=10
            Number of iterations to perform for each n_jobs value for self.predict.
        exclude: str, default=None
            Whether to exclude the transformers or the estimators from the optimization.

        Returns:
        --------
        optimal_n_jobs: int or None
            The optimal n_jobs value.
        results: Dict[int, float]
            A dictionary containing the execution times for different n_jobs values.
            The key is the n_jobs value, and the value is the execution time.
        """
        if exclude not in [None, "transformers", "estimators"]:
            raise ValueError(f"exclude should be either None, transformers, or estimators, but is {exclude}")
        X = X.copy()

        measure_time = lambda func: timeit.timeit(lambda: func(X), number=n_iter)

        if exclude == "transformers":
            fn = self.transform_only
        elif exclude == "estimators":
            fn = partial(self.predict, exclude_transformers=True)
        else:
            fn = self.predict

        # Prepare a list of n_jobs options, including None and a range of integers up to the CPU count
        min_time = float("inf")
        n_cpu = mp.cpu_count()
        n_jobs_options = list(range(n_cpu + 1))
        results = dict.fromkeys(n_jobs_options, min_time)
        results["initial"] = measure_time(fn)

        # Perform a binary search over the n_jobs options
        left = 0
        right = len(n_jobs_options) - 1

        while left <= right:
            mid = (left + right) // 2
            n_jobs = n_jobs_options[mid]
            if n_jobs == 0:
                n_jobs = None

            if exclude == "transformers":
                self._set_n_jobs(n_jobs, exclude="transformers")
            elif exclude == "estimators":
                self._set_n_jobs(n_jobs, exclude="estimators")
            else:
                self._set_n_jobs(n_jobs, exclude=None)

            total_time = measure_time(fn)
            results[n_jobs] = total_time

            if total_time < min_time:
                min_time = total_time

            if mid > 0 and total_time < results[n_jobs_options[mid - 1]]:
                right = mid - 1
            elif mid < len(n_jobs_options) - 1 and total_time < results[n_jobs_options[mid + 1]]:
                left = mid + 1
            else:
                break

        results = sorted(results.items(), key=lambda kv: kv[1])
        optimal_n_jobs, best_time = results[0]

        if optimal_n_jobs != "initial":
            if optimal_n_jobs == 0:
                optimal_n_jobs = None
            self._set_n_jobs(optimal_n_jobs, exclude=exclude)

        return optimal_n_jobs, dict(results)

    # TODO: weights can be negative if there are outliers in the scores. Should we allow this?
    def get_weights(self, decay_rate: Optional[float] = None) -> pd.Series:
        """
        Get weights for the estimators based on their scores.
        These scores can be updated by the self.score(update_memory=True) method.
        If decay_rate is passed, the scores are also weighted by their index,
        where the more recent scores weigh more.

        Parameters:
        ----------
        decay_rate : float, optional
            Decay rate for the scores.
            If passed, the scores are weighted by their index.

        Returns:
        -------
        weights : pd.Series
            Weights for the estimators
        """
        return self._score_tracker.get_weights(self.maximize_scoring, decay_rate)

    def get_name_by_index(self, index: int) -> Union[str, None]:
        """
        Get the name of the estimator by indexposition.
        If the index is not found, None is returned.
        """
        return get_obj_name(self.estimators[index])

    def get_scores(self) -> pd.DataFrame:
        """
        Get the current scores of the estimators.
        """
        return self.scores

    def get_stats(self) -> pd.DataFrame:
        """
        Get statistics for the estimators in the pipeline.
        """
        try:
            estimator_names = {idx: self.get_name_by_index(idx) for idx in range(len(self.estimators))}
            stats = pd.DataFrame.from_dict(data=estimator_names, orient="index")
            weights = self.get_weights()
            estimators = pd.Series(self.estimators)
            stats = pd.concat([stats, weights, estimators], axis=1)
            stats.columns = ["name", "weight", "estimator"]
            return stats
        except KeyError:
            logger.error(
                f"A KeyError occured in self.get_stats:\n{traceback.format_exc()}.\nReturning empty DataFrame.",
            )
        except Exception:
            logger.error(
                f"An Unknown Exception occured in self.get_stats:\n{traceback.format_exc()}.\nReturning empty DataFrame.",
            )
        return pd.DataFrame()

    def set_verbose(self, verbose: int) -> None:
        """
        Set the verbosity level for this pipeline, inner pipelines and steps.
        """
        logger.set_verbose(verbose)  # for all other steps in the pipeline, where verbose is an int
        self.verbose = verbose == 1  # for Parent class, where verbose is a bool
        for name, step in self.named_steps.items():
            if isinstance(step, MultiEstimatorPipeline):
                step.set_verbose(verbose)
            else:
                self._set_verbose_for_step(step, verbose)

    def update_scores(self, scores: np.ndarray, memory_size: int = 10) -> None:
        """
        Update the scores of the estimators in the pipeline.

        The scores must have the same properties as the
        scores initially passed to the pipeline during its creation by the
        `ComponentService.generate_pipeline_for_stacked_models` or
        `ComponentService.generate_pipeline_for_base_models` methods.

        The max_len follows the FILO principle.
        Scores are placed at the start of the list, and when max_len is reached, the oldest score is removed.
        Weights of the estimators are updated according to the scores if using self.get_weights().

        Parameters:
        ----------
        scores : np.ndarray[float]
            Scores for the estimators in the pipeline

        memory_size : int, optional
            Number of scores to keep in memory.
            If memory_size is reached, the oldest score is removed.
        """
        self._score_tracker.update_scores(scores, max_len=memory_size)

    def save(self, path: str, compress: Optional[Union[int, bool]] = None) -> None:
        """
        Save the pipeline to disk.

        Parameters:
        ----------
        path : str
            Path to save the pipeline to
        compress: int from 0 to 9 or bool, optional
            Optional compression level for the data. 0 or False is no compression.
            Higher value means more compression, but also slower read and
            write times. Using a value of 3 is often a good compromise.
            If compress is True, the compression level used is 3.
        """
        joblib.dump(self, path, compress=compress)

    @staticmethod
    def load(path: str) -> "MultiEstimatorPipeline":
        """
        Load the pipeline from disk.

        Parameters:
        ----------
        path : str
            Path to load the pipeline from
        """
        return joblib.load(path)

    def _set_parallel_params(self, step, n_jobs):
        if hasattr(step, "n_jobs"):
            step.n_jobs = n_jobs
        elif hasattr(step, "num_workers"):
            step.num_workers = convert_n_jobs_to_num_workers(n_jobs)

    def _set_n_jobs_for_step(self, name, step, n_jobs, exclude):
        try:
            if isinstance(step, MultiEstimatorWrapper) and exclude != "estimators":
                for estimator in step.estimators:
                    self._set_parallel_params(estimator, n_jobs)
            elif is_transformer(step) and exclude != "transformers":
                if isinstance(step, FunctionTransformer):
                    params = inspect.signature(step.func).parameters
                    if "n_jobs" in params or "num_workers" in params:
                        step.kw_args = (
                            {"n_jobs": n_jobs}
                            if "n_jobs" in params
                            else {"num_workers": convert_n_jobs_to_num_workers(n_jobs)}
                        )
            self._set_parallel_params(step, n_jobs)
            if isinstance(step, MultiEstimatorPipeline):
                step._set_n_jobs(n_jobs)
        except (AttributeError, TypeError):
            logger.error(
                f"Could not set n_jobs for step '{name}' to {n_jobs}: {traceback.format_exc()}",
            )

    def _set_n_jobs(
        self,
        n_jobs: int,
        exclude: Optional[Literal["transformers", "estimators"]] = None,
    ) -> None:
        for name, step in self.named_steps.items():
            self._set_n_jobs_for_step(name, step, n_jobs, exclude)

    def _check_kwargs(self, index: Optional[int], n_jobs: Optional[int], kwargs: dict) -> dict:
        """Check if index and n_jobs are passed and add them to kwargs if so."""
        if index is not None:
            kwargs["index"] = index
        if n_jobs is not None:
            kwargs["n_jobs"] = n_jobs

        return kwargs

    def _predict_func_error_handler(
        self,
        predict_func: str,
        X: pd.DataFrame,
        exclude_transformers: bool = False,
        **kwargs,
    ) -> np.ndarray:
        """Handle possible errors in predictor-functions in one place."""
        if not isinstance(X, pd.DataFrame) or X.empty:
            raise ValueError(
                f"Invalid input data. X must be a non-empty DataFrame, but is of type {type(X)} and length {len(X)}"
            )

        if exclude_transformers:
            predict_func = getattr(self.estimator_wrapper, predict_func)
        else:
            predict_func = getattr(super(MultiEstimatorPipeline, self), predict_func)

        try:
            return predict_func(X, **kwargs)
        except TypeError as e:
            if "n_jobs" in kwargs and "n_jobs" in str(e):
                kwargs.pop("n_jobs")
            return predict_func(X, **kwargs)

    def _discrete_predict_proba(self, X: pd.DataFrame, exclude_transformers: bool = False, **kwargs) -> np.ndarray:
        pred_list = self.predict(X, exclude_transformers=exclude_transformers, **kwargs)
        transformed_pred_list = pd.DataFrame(pred_list).T.to_numpy()

        # Identify unique classes
        unique_classes = np.unique(transformed_pred_list)

        # Initialize an empty array for storing class probabilities
        class_probabilities = np.zeros((transformed_pred_list.shape[0], len(unique_classes)))

        # Calculate probabilities for each class
        for i, cls in enumerate(unique_classes):
            class_probabilities[:, i] = np.mean(transformed_pred_list == cls, axis=1)

        return class_probabilities

    def _check_if_estimator_wrapper_is_set(self):
        """Check if all estimators are set. if last step is valid estimator, wrap it in a MultiEstimatorWrapper."""
        if not pipeline_has_estimator_step(self):
            raise ValueError("Pipeline has no estimator step.")
        if not estimators_are_valid(self):
            self.steps[-1] = (
                self.steps[-1][0],
                MultiEstimatorWrapper(self.steps[-1][1]),
            )

    def _set_verbose_for_step(self, step, verbose):
        if hasattr(step, "verbose"):
            if isinstance(step.verbose, bool):
                step.verbose = verbose == 1
            elif isinstance(step.verbose, int):
                step.verbose = verbose
        elif hasattr(step, "_verbose"):
            if isinstance(step._verbose, bool):
                step._verbose = verbose == 1
            elif isinstance(step._verbose, int):
                step._verbose = verbose

    def _modify_indexes_scores(self, indexes: List[int]):
        """
        Modify the indexes and scores of the score tracker, changing the validations in self.update_scores().
        Use this only if estimators are removed from the pipeline.
        """
        self._score_tracker.scoretype["length"] = len(indexes)
        for idx in range(len(self._score_tracker.scores)):
            score = self._score_tracker.scores[idx]
            if np.isscalar(score):
                score = np.array([score])
            self._score_tracker.scores[idx] = score[indexes]
