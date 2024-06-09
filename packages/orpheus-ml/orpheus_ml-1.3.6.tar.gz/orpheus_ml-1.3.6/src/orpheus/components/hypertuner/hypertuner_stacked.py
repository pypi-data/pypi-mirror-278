"""
HyperTunerStacked class. Use the HyperTunerStacked class to
stack `HyperTuner` instances` and perform
specialized operations with them.
"""

import os
import sys
import traceback
import warnings
from copy import deepcopy
from functools import partial
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import StackingClassifier, StackingRegressor, VotingClassifier, VotingRegressor

from orpheus.components.hypertuner.hypertuner import HyperTuner
from orpheus.components.libs.predict_object import PredictObject
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.utils.constants import DEFAULT_VALUES
from orpheus.utils.context_managers import FunctionTimeoutHandler
from orpheus.utils.custom_types import PredictorType
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import EstimatorType

# solution to block warnings from sklearn.
# source:
# https://stackoverflow.com/questions/53784971/how-to-disable-convergencewarning-using-sklearn
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"  # Also affect subprocesses

# https://bobrupakroy.medium.com/create-ensemble-methods-in-3-lines-of-code-b87fff6d3178
# https://towardsdatascience.com/combine-your-machine-learning-models-with-voting-fa1b42790d84
# https://stackoverflow.com/questions/26205922/calculate-weighted-average-using-a-pandas-dataframe
# https://www.analyticsvidhya.com/blog/2020/12/improve-predictive-model-score-stacking-regressor/


class HyperTunerStacked:

    """
    Use the HyperTunerStacked class to stack `HyperTuner` instances` and perform specialized operations with them.

    Public methods:
    ---
    predict_average :
        Get an averaged or weighted averaged prediction from all estimators, depending on the chosen predictor.

    fit_stacked :
        Fit a stacked model on the data.
    """

    def __init__(
        self,
        saved_tuners: List[HyperTuner],
        pipeline: Optional[MultiEstimatorPipeline] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
    ):
        """
        Parameters:
        ---
        data : pd.DataFrame
            Data to be predicted.

        saved_tuners : List[HyperTuner]
            Provide a list of HyperTuner instances, a list of paths to HyperTuner instances.
            Assumes all HyperTuner instances where fitted during several crossvalidations.

        pipeline : Optional[MultiEstimatorPipeline], Default = None
            Optionally add a pipeline to the HyperTunerStacked instance to integrate it into the prediction process.

        num_workers : int = DEFAULT_VALUES["n_jobs"]
            Number of workers to use for parallelization.

        Public methods & quick summary:
        ---
        """
        if len(saved_tuners) == 0:
            raise ValueError("saved_tuners must not be empty!")

        if isinstance(saved_tuners, list) and isinstance(saved_tuners[0], HyperTuner):
            self.saved_tuners = saved_tuners
        else:
            raise ValueError('"saved_tuners" is not valid!')

        self.pipeline = pipeline
        self.type_estimator = self.saved_tuners[0].type_estimator
        self.maximize_scoring = self.saved_tuners[0].maximize_scoring
        self.scoring = self.saved_tuners[0].scoring
        self.num_workers = num_workers
        self.predict_obj = PredictObject()

    def __repr__(self):
        return f"{self.saved_tuners}"

    def predict_averaged(
        self,
        _data: pd.DataFrame,
        predictor: Union[PredictorType, int, None] = None,
        top_n_per_tuner: Optional[int] = None,
        weighted: bool = False,
        pipeline: Optional[MultiEstimatorPipeline] = None,
        use_pipeline: bool = True,
        **predictor_params,
    ) -> Union[np.ndarray, float]:
        """
        get an averaged or weighted averaged prediction from all estimators, depending on the chosen predictor.

        Parameters
        ---
        _data : pd.DataFrame
            Data to be predicted.

        predictor : Union[PredictorType, None, int], Default = None : {PredictorType.SOLO, PredictorType.ENSEMBLE_R1, PredictorType.ENSEMBLE_R2_WEIGHTED, PredictorType.ENSEMBLE_R2, PredictorType.ENSEMBLE_R3}, None or {0, 1, 2, 3, 4, 5}
            Type of estimator or estimators to use for prediction. PredictorType.SOLO uses the best estimator found from last round after finishing 'self.fit'.
            Optionally, models saved in 'self.scores_R1_', 'self.scores_R2_WEIGHTED', 'self.scores_R2_' or 'self.scores_R3_' can be accessed by PredictorType.ensemble_Rx.
            Each estimator in self.scores_Rx attribute will make a prediction.\n
            If None is explicitely passed, all fitted models in the HyperTuner object found in all 'self.score_Rx' will make a prediction.

            For convenience, one can access all types above by passing an integer in the range {0, 1, 2, 3, 4, 5}, where the ints correspond to the following types:
            0: None
            1: PredictorType.SOLO
            2: PredictorType.ENSEMBLE_R1
            3: PredictorType.ENSEMBLE_R2_WEIGHTED
            4: PredictorType.ENSEMBLE_R2
            5: PredictorType.ENSEMBLE_R3

        top_n_per_tuner: int = None
            Only select top N estimators per tuner to filter out possibly weaker models before averaging.
            NOTE: prevent memory errors by setting top_n_per_tuner to a low number, eg. 5.

        weighted: bool = False

        pipeline: Optional[MultiEstimatorPipeline] = None
            If None, self.pipeline is used.

        use_pipeline: bool = True,
            If True, self.pipeline is as the `pipeline` argument,
            given that self.pipeline is not None.
            If False, no pipeline is used.

        **predictor_params

        Returns
        ---
        Union[np.ndarray, float]

        """
        if use_pipeline:
            if self.pipeline is not None:
                pipeline = self.pipeline

            if pipeline is not None and hasattr(pipeline, "transform"):
                _data = pipeline.transform(_data)

        df = self._get_pred_df(
            data=_data,
            predictor=predictor,
            top_n_per_tuner=top_n_per_tuner,
            **predictor_params,
        )
        df["prediction"] = df["prediction"].apply(lambda x: x.ravel())  # make sure all rows are 1D
        if weighted:
            m = df["score"].mean()
            df["weights"] = df["score"] / m if self.maximize_scoring else m / df["score"]
            prediction = np.average(df["prediction"], weights=df["weights"])
        else:
            prediction = df["prediction"].mean()

        return prediction

    def fit_stacked(
        self,
        _X: np.ndarray,
        _y: np.ndarray,
        _final_estimator: Optional[EstimatorType] = None,
        top_n_per_tuner: Optional[int] = None,
        unfit: bool = False,
        timeout_duration: Optional[int] = None,
        **estimator_kwargs,
    ) -> EstimatorType:
        """
        fit a stacked model on the given data using the estimators
        from all `HyperTuner` instances in `self.saved_tuners`.

        Parameters
        ----------
        _X : np.ndarray
            training data
        _y : np.ndarray
            target data
        _final_estimator : EstimatorType, optional
            final estimator to be used in the stacking process, by default None.
            if None, the final estimator will be a LinearRegression or LogisticRegression depending on the type of the estimator
        top_n_per_tuner : int, optional
            number of estimators to be used from each tuner, by default None
            if None, all estimators will be used
        unfit : bool, optional
            if True, the estimators will be cloned (and thus unfitted if they where fitted on other data), by default False
        timeout_duration : int, optional
            timeout duration in seconds, by default None.
            Use this to prevent hanging during the fitting process.
        estimator_kwargs : dict, optional
            additional kwargs for the final estimator, by default {}

        Returns
        -------
        final estimator if self.pipeline is None, else MultiEstimatorPipeline with the final estimator as last step
        """
        _X = self._transform(_X, unfit)

        d = self._get_fitted_estimators_from_all_tuners(top_n_per_tuner)
        estimators = self._collect_estimators(unfit, d)
        if _final_estimator is None:
            # take the best estimator from all tuners as final estimator
            _final_estimator = estimators[0][1]

        estimator = self._fit_estimator_with_error_handling(
            partial(self._get_stacking_estimator, estimators=estimators),
            X=_X,
            y=_y,
            estimators=estimators,
            max_tries=len(estimators),
            final_estimator=_final_estimator,
            **estimator_kwargs,
            timeout_duration=timeout_duration,
        )

        if self.pipeline is not None:
            return self._add_estimator_to_pipe_and_return_pipe(estimator)

        return estimator

    def fit_voting(
        self,
        _X: np.ndarray,
        _y: np.ndarray,
        voting: str = "hard",
        top_n_per_tuner: Optional[int] = None,
        unfit: bool = False,
        timeout_duration: Optional[int] = None,
        **estimator_kwargs,
    ) -> EstimatorType:
        """
        Fit a voting model on the given data from
        the estimators found in the `HyperTuner` instances.
        """
        _X = self._transform(_X, unfit)

        d = self._get_fitted_estimators_from_all_tuners(top_n_per_tuner)
        estimators = self._collect_estimators(unfit, d)

        if voting == "soft" and self.type_estimator == "classifier":
            estimators = [est for est in estimators if hasattr(est[1], "predict_proba")]

        if len(estimators) == 0:
            raise ValueError(
                f"no estimators to fit {voting} voting model. Check if the estimators are fitted and if they have the method 'predict_proba' if voting='soft'"
            )

        estimator = self._fit_estimator_with_error_handling(
            partial(self._get_voting_estimator, estimators=estimators),
            X=_X,
            y=_y,
            estimators=estimators,
            max_tries=len(estimators),
            voting=voting,
            timeout_duration=timeout_duration,
            **estimator_kwargs,
        )

        if self.pipeline is not None:
            return self._add_estimator_to_pipe_and_return_pipe(estimator)

        return estimator

    def _add_estimator_to_pipe_and_return_pipe(self, estimator):
        """make a deepcopy so that self.pipeline stays unchanged."""
        pipeline = deepcopy(self.pipeline)
        pipeline.steps.append(("estimator", estimator))
        return pipeline

    def _fit_estimator_with_error_handling(
        self,
        estimator_func,
        X,
        y,
        estimators,
        max_tries,
        timeout_duration: Optional[int] = None,
        **estimator_func_kwargs,
    ):
        """iterate over estimators and try to fit and predict with them.
        If an error occurs, the faulty estimator will be removed from the list of
        estimators and the process will be repeated."""

        amount_of_nans = np.isnan(X).sum().sum()
        if amount_of_nans > 0:
            X = X.fillna(0, axis=1).copy()
            logger.notice(f"replaced {amount_of_nans} Nans out of total {X.size} values with 0 in X.")

        for i in range(max_tries):
            try:
                voting_estimator = estimator_func(**estimator_func_kwargs)
                with FunctionTimeoutHandler(
                    voting_estimator.fit,
                    X,
                    y,
                    timeout=timeout_duration,
                    n_jobs_on_timeout=estimator_func_kwargs.get("n_jobs", 1),
                ) as voting_estimator:
                    pass

            except Exception as e:
                logger.error(
                    f"During fitting of estimator {voting_estimator}, {type(e).__name__} occured",
                )
                logger.error(traceback.format_exc())
                faulty_estimators = self._find_faulty_fitted_estimators(estimators, e)
                estimators = [est for est in estimators if est not in faulty_estimators]
            else:
                try:
                    voting_estimator.predict(X)
                except (AttributeError, ValueError) as e:
                    popped_estimator = estimators.pop(-1)
                    logger.error(
                        f"During predicting of estimator {voting_estimator}, {type(e).__name__} occured",
                    )
                    logger.error(traceback.format_exc())
                    logger.notice(
                        f"removed estimator from {len(estimators)} remaining: {popped_estimator}",
                    )
                else:
                    # breaks loop if voting_estimator.predict(X) was succesful
                    break

            if i == max_tries - 1:
                raise ValueError(f"Failed to fit a voting model after {max_tries} attempts")

        return voting_estimator

    def _collect_estimators(self, unfit, d) -> List[EstimatorType]:
        """collect estimators from all tuners and remove duplicates."""
        estimators_temp = list(d.keys())
        if unfit:
            estimators_temp = clone(estimators_temp)

        seen = set()
        estimators = []
        for est in estimators_temp:
            est_repr = str(est)
            if est_repr not in seen:
                estimators.append((est_repr, est))
                seen.add(est_repr)
        return estimators

    def _transform(self, _X, unfit) -> np.ndarray:
        if self.pipeline is not None:
            _X = self.pipeline.transform(_X) if not unfit else self.pipeline.fit_transform(_X)

        return _X

    def _get_fitted_estimators_from_all_tuners(self, top_n_per_tuner) -> Dict[EstimatorType, float]:
        """get fitted estimators from all HyperTuner instances and return a dictionary,
        sorted on scores, with the top_n_per_tuner estimators

        parameters
        ----------
        top_n_per_tuner: int
            best scoring estimators to return per `HyperTuner` instance.
        """
        d: Dict[EstimatorType, float] = {}
        for tuner in self.saved_tuners:
            estimator_slice = list(tuner._get_all_fitted_estimators(sort_scores=True, top_n=top_n_per_tuner).items())
            d.update(estimator_slice)
        return d

    def _get_stacking_estimator(self, estimators, final_estimator, **estimator_kwargs) -> EstimatorType:
        estimator = (
            StackingRegressor(
                estimators,
                n_jobs=self.num_workers,
                final_estimator=final_estimator,
                **estimator_kwargs,
            )
            if self.type_estimator == "regressor"
            else StackingClassifier(
                estimators,
                final_estimator=final_estimator,
                n_jobs=self.num_workers,
                **estimator_kwargs,
            )
        )

        return estimator

    def _get_voting_estimator(self, estimators: List[EstimatorType], voting: str, **estimator_kwargs) -> EstimatorType:
        estimator = (
            VotingRegressor(estimators, n_jobs=self.num_workers, **estimator_kwargs)
            if self.type_estimator == "regressor"
            else VotingClassifier(
                estimators,
                voting=voting,
                n_jobs=self.num_workers,
                **estimator_kwargs,
            )
        )
        return estimator

    def _find_faulty_fitted_estimators(self, estimators, error_raised_by_estimator) -> List[int]:
        """
        Handle error by identifying matching estimator in error-string.
        """
        # Convert error to lowercase string for easier matching
        err_str = str(error_raised_by_estimator).lower()

        # Generate list of lowercase estimator names
        estimator_strings = [get_obj_name(i[1]).lower() for i in estimators]

        # Identify faulty estimators based on presence in error message
        faulty_est_indexes = {idx for idx, est_str in enumerate(estimator_strings) if est_str in err_str}

        # If no faulty estimators were found, raise an error
        if not faulty_est_indexes:
            raise RuntimeError(
                f"Error could not be handled properly, as estimator causing issues could not be found! "
                f"Compiling model failed\nLast error: {err_str}\nestimators: {estimators}"
            )

        return list(faulty_est_indexes)

    def _get_pred_df(
        self,
        data,
        predictor: Union[PredictorType, int, None],
        top_n_per_tuner: Optional[int] = None,
        **predictor_params,
    ) -> pd.DataFrame:
        """get a sorted DataFrame, containing estimators,
        scores and predictions from all saved `HyperTuner` instances."""

        df = pd.DataFrame()
        err = None

        for fold, tuner in enumerate(self.saved_tuners, start=1):
            try:
                preds = self.predict_obj.predict(
                    data,
                    tuner=tuner,
                    predictor=predictor,
                    top_n=top_n_per_tuner,
                    **predictor_params,
                )
                preds["fold"] = fold
                df = pd.concat([df, preds], axis=0)
            except Exception as e:
                err = e
                logger.error(traceback.format_exc())

        if df.empty:
            raise ValueError(
                f"DataFrame with predictions is empty, indicating that something structural went wrong within self.predict_obj.predict().\nLast found error: {err}\nConsider turning on verbose=3 to see more details about this error!"
            )

        return df.sort_values(by="score", ascending=not self.maximize_scoring)
