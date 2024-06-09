"""checks for regression and classification models to make sure they perform well enough."""

import traceback
from typing import Callable, List

import numpy as np
import pandas as pd

from orpheus.services.additional_types.multi_estimator_pipeline import (
    MultiEstimatorPipeline,
)
from orpheus.utils.helper_functions import get_obj_name, keep_common_elements
from orpheus.utils.logger import logger


class ClassificationEvaluator:
    """
    evaluate classifiers in a MultiEstimatorPipeline and return indexes of estimators
    that do not meet requirements.
    """

    def __repr__(self) -> str:
        return "ClassificationEvaluator()"

    def evaluate_classifier(
        self,
        pred_pipeline: np.ndarray,
        max_occurance_pct: float = 0.8,
    ) -> np.ndarray:
        """
        Evaluate classifiers in a pipeline and
        remove estimators that do not meet requirements.

        Parameters
        ----------
        pred_pipeline: np.ndarray
            Predictions of pipeline.

        max_occurance_pct: float
            Maximum percentage of the most common prediction.

        Returns:
        --------
            indexes_to_keep: np.ndarray with indexes of estimators that meet requirements.
        """
        if not (0 < max_occurance_pct <= 1):
            raise ValueError("max_occurance_pct must be a float between 0 and (inclusive of) 1")

        # Indexes of estimators that have at least two unique predictions
        indexes_to_keep = np.where(pd.Series(map(np.unique, pred_pipeline)).apply(len) >= 2)[0]

        if len(indexes_to_keep) != 0:
            # Indexes of estimators that have max occurrence percentage within
            # range
            max_occ_pct = pd.Series(
                [max(np.bincount(predictions.astype(int)) / len(predictions)) for predictions in pred_pipeline]
            )
            indexes_to_keep = indexes_to_keep[max_occ_pct[indexes_to_keep] <= max_occurance_pct]

        return indexes_to_keep


class RegressionEvaluator:
    """
    evaluate regressors in a MultiEstimatorPipeline and return indexes of estimators
    that do not meet requirements.
    """

    def __init__(
        self,
        X_val: np.ndarray,
        y_val: np.ndarray,
        score: Callable,
        maximize_score: bool,
    ):
        self.X_val = X_val
        self.y_val = y_val
        self.score = score
        self.maximize_score = maximize_score

    def __repr__(self) -> str:
        return f"RegressionEvaluator({get_obj_name(self.score)})"

    def evaluate_regressor(self, pipeline: MultiEstimatorPipeline, trials: int = 5) -> List[int]:
        """
        Compare models in a pipeline against random predictions and
        return indexes of models that outperform random predictions.

        parameters
        ----------
        pipeline: MultiEstimatorPipeline
            Pipeline to evaluate.

        trials: int
            Number of trials to run.

        returns
        -------
        indexes_to_keep: List[int]
            Indexes of models that outperform random predictions.

        """
        index_list = []

        for _ in range(trials):
            y_pred = pipeline.predict(self.X_val)
            best_indexes = self._filter_models_vs_random(y_pred)
            index_list.append(best_indexes)

        indexes_to_keep = keep_common_elements(index_list)

        return indexes_to_keep

    def _evaluate_against_random(self, predicted):
        """
        generate random prediction and return the score of
        the actual prediction vs the random prediction
        """
        random_pred = np.random.randn(len(self.y_val)) * np.std(self.y_val) + np.mean(self.y_val)
        score_actual = self.score(self.y_val, predicted)
        score_random = self.score(self.y_val, random_pred)
        return score_actual, score_random

    def _filter_models_vs_random(self, pred_pipeline) -> List[int]:
        """
        Filter indexes of models based on score vs. random predictions.

        :param pred_pipeline: List of predictions from different models.
        :return: Indexes of models that outperformed random predictions.
        """

        # Initialize lists to store evaluation results and indexes to exclude
        preds_against_random = []
        indexes_to_exclude = []

        # Evaluate each prediction against random and handle exceptions
        for idx, pred in enumerate(pred_pipeline):
            try:
                pred_against_random = self._evaluate_against_random(pred)
                preds_against_random.append(pred_against_random)
            except ValueError:
                logger.error(
                    f"a ValueError occured while evaluating regressor models against random in model index {idx}:\n{traceback.format_exc()}"
                )
                indexes_to_exclude.append(idx)

        # Filter out models that outperformed random predictions
        # and exclude the indexes from indexes_to_exclude
        is_better_than_random = lambda pair: (pair[0] > pair[1] if self.maximize_score else pair[0] < pair[1])
        indexes_outperformed_random = [
            i
            for i, result in enumerate(preds_against_random)
            if is_better_than_random(result) and i not in indexes_to_exclude
        ]

        return indexes_outperformed_random
