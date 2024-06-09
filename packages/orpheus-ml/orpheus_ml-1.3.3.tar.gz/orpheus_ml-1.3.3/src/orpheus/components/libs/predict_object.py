"""This module contains the PredictObject class, which is used to make predictions after running HyperTuner.fit()."""

import traceback
from itertools import islice
from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd

from orpheus.components.hypertuner.hypertuner import HyperTuner
from orpheus.components.hypertuner.utils.helper_functions import _get_attr
from orpheus.utils.custom_types import PredictorType
from orpheus.utils.type_vars import EstimatorType
from orpheus.utils.helper_functions import ensure_numpy
from orpheus.utils.logger import logger
from orpheus.validations.input_checks import DataValidation


class PredictObject:
    """
    NOTE: This class should not be used on its own, but is an integral part of a HyperTuner object.
    Several attributes in this class can only be accessed through the HyperTuner class!
    """

    def predict(
        self,
        data: np.ndarray,
        tuner: HyperTuner,
        predictor: Union[PredictorType, int, None] = PredictorType.SOLO,
        top_n: Optional[int] = None,
        _err_count: int = 0,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """
        make a prediction after running tuner.fit(). Acts as pipeline, depending on transformations done prior to calling tuner.predict.

        predictor : Union[PredictorType, None, int] = PredictorType.SOLO : {PredictorType.SOLO, PredictorType.ENSEMBLE_R1,
            PredictorType.ENSEMBLE_R2_WEIGHTED, PredictorType.ENSEMBLE_R2, PredictorType.ENSEMBLE_R3}, None or {0, 1, 2, 3, 4, 5}

            Type of estimator or estimators to use for prediction.
            PredictorType.SOLO uses the best estimator found from last round after finishing 'tuner.fit'.
            Optionally, models saved in 'HyperTuner.scores_R1_', 'HyperTuner.scores_R2_WEIGHTED', 'HyperTuner.scores_R2_' or 'HyperTuner.scores_R3_'
            can be accessed by PredictorType.ensemble_Rx. Each estimator in tuner.scores_Rx attribute will make a prediction.\n
            If None is explicitely passed, all fitted models in the HyperTuner object found in all 'tuner.score_Rx' will make a prediction.

            For convenience, one can access all types above by passing an integer in the range {0, 1, 2, 3, 4, 5},
            where the ints correspond to the following types:
            0: None
            1: PredictorType.SOLO
            2: PredictorType.ENSEMBLE_R1
            3: PredictorType.ENSEMBLE_R2_WEIGHTED
            4: PredictorType.ENSEMBLE_R2
            5: PredictorType.ENSEMBLE_R3

         returned as a pd.DataFrame, where index is estimator, column 1 is score and column 2 is prediction.

        top_n: int = None
            index can be passed to that only top N models are selected.
            This might produce better results, as worse performing models are left out.

        _err_count: int = 0
            counter to handle errors during prediction.
            Its use is to prevent endless recursion and handle errors to its value accordingly.
            NOTE: DO NOT USE THIS PARAMETER!! Only used for passing new values recursively!!

        Returns
        ---
        pd.DataFrame, where index is estimator, column 1 is 'score' and column 2 is 'prediction'.
        """
        # validationchecks
        DataValidation.validate_array_is_not_3d(data)
        data = ensure_numpy(data)
        assert isinstance(
            top_n, (int, type(None))
        ), f"top_n must be of type int or None, but is of type {type(top_n)}: {top_n}"

        # generate predictions
        if hasattr(tuner, "best_estimator_"):
            try:
                if predictor in {1, PredictorType.SOLO}:
                    pred = tuner.best_estimator_.predict(data)
                    estimators_and_score = {
                        tuner.best_estimator_: {
                            "score": tuner.best_score_,
                            "prediction": pred,
                        }
                    }
                elif predictor in {2, PredictorType.ENSEMBLE_R1}:
                    estimators_and_score = self._ensemble_predict(_get_attr(tuner, "scores_R1_")[:top_n], data)
                elif predictor in {3, PredictorType.ENSEMBLE_R2_WEIGHTED}:
                    estimators_and_score = self._ensemble_predict(
                        _get_attr(
                            tuner,
                            "scores_R2_WEIGHTED",
                            "Did you specify a list of weights for 'R2_weights' in 'tuner.fit()' ? ",
                        )[:top_n],
                        data,
                    )
                elif predictor in {4, PredictorType.ENSEMBLE_R2}:
                    estimators_and_score = self._ensemble_predict(_get_attr(tuner, "scores_R2_")[:top_n], data)
                elif predictor in {5, PredictorType.ENSEMBLE_R3}:
                    estimators_and_score = self._ensemble_predict(_get_attr(tuner, "scores_R3_")[:top_n], data)

                elif predictor in {None, 0}:
                    estimators_and_score = {}
                    for estimator, score in tuple(
                        islice(
                            tuner._get_all_fitted_estimators(sort_scores=True).items(),
                            0,
                            top_n,
                        )
                    ):
                        pred = None
                        try:
                            pred = estimator.predict(data)
                        except ValueError as ve:
                            try:
                                pred = estimator.predict(data.reshape(1, -1))
                            except BaseException as exc:
                                raise ve from exc
                        except Exception:
                            logger.error(traceback.format_exc())
                        finally:
                            if pred is not None:  # if prediction is succesfull, add it to dict.
                                estimators_and_score.update({estimator: {"score": score, "prediction": pred}})

                else:
                    raise Exception(f"predictor {predictor} is not of the right value for making a prediction!")

                df = pd.DataFrame.from_dict(estimators_and_score).T.sort_values(
                    by="score", ascending=not tuner.maximize_scoring
                )
                return df

            except ValueError as ve:
                if _err_count == 0:
                    pred = self.predict(
                        data.reshape(1, -1),
                        tuner,
                        predictor,
                        top_n,
                        1,
                        *args,
                        **kwargs,
                    )
                    return pred
                # elif _err_count==1:
                # pred = tuner.predict(....err_count=2)
                # return pred
                else:
                    # _err_count is 1, meaning ValueError got dealt with 1 time
                    # and was not succesful.
                    raise ve

        else:
            raise AttributeError(
                'predict can only be run after "best_estimator_" is created with "tuner.fit" method. call "tuner.fit" first!'
            )

    def _ensemble_predict(self, estimator_scores: Tuple[EstimatorType, float], data: np.ndarray) -> dict:
        """use this method in predict_obj.predict to make a prediction when PredictorType ensemble_Rx is selected."""

        d = {}

        for item in estimator_scores:
            estimator = item[0]
            score = item[1]
            try:
                pred = estimator.predict(data)
            except ValueError:
                pred = estimator.predict(data.reshape(1, -1))
            except Exception:
                logger.error(traceback.format_exc())
                continue
            d.update({estimator: {"score": score, "prediction": pred}})

        if not d:
            raise IndexError("no predictions were made!")

        return d
