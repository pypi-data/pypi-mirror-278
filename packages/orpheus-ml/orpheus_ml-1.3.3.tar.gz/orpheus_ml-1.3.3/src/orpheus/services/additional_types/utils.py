from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd

from orpheus.utils.helper_functions import ensure_numpy


class MultiEstimatorPipelineScoreTracker:
    """
    A class for tracking the scores and weights of a MultiEstimatorPipeline object.
    """

    def __init__(self):
        self.scores: list = []
        self.scoretype: dict = None

    def __repr__(self):
        return f"MultiEstimatorPipelineScoreTracker(scores={self.scores}, scoretype={self.scoretype})"

    def update_scores(self, scores: Union[np.ndarray, Sequence[float]], max_len: int = 10) -> None:
        """
        Update the scores of the pipeline. The scores must have the same properties as the
        scores initially passed to the pipeline during its creation by the
        `generate_pipeline_for_stacked_models` or
        `generate_pipeline_for_base_models` methods of the ComponentService class.

        The max_len follows the FILO principle.
        scores are placed at the start of the list, and when max_len is reached, the oldest score is removed.
        Weights are updated according to scores if using self.get_weights().

        Parameters:
        ----------
        scores : array-like
            Scores to add to the pipeline

        max_len : int, optional
            Maximum number of scores to keep. If the number of scores exceeds
            max_len, the oldest score is removed.
        """

        try:
            self._update_scores(scores, max_len)
        except ValueError as e:
            self._handle_value_error_update_scores(scores, max_len, e)

    def get_weights(self, maximize_scoring: bool, decay_rate: Optional[float] = None) -> pd.Series:
        """
        See MultiEstimatorPipeline.get_weights() for more information.
        """
        if not isinstance(maximize_scoring, bool):
            raise ValueError("maximize_scoring must be a boolean.")
        if self.scores:
            if decay_rate is not None:
                decay_rate_weights = self._get_decay_rate(decay_rate)
                scores = [
                    (self.scores[idx] * w) if maximize_scoring else (self.scores[idx] / w)
                    for idx, w in enumerate(decay_rate_weights)
                ]
            else:
                scores = self.scores

            single_weight = 1 / len(scores[0])
            mean_scores = pd.DataFrame(scores).mean()
            weights = mean_scores / single_weight if maximize_scoring else single_weight / mean_scores
            return weights / weights.sum()

    def _get_decay_rate(self, decay_rate: float) -> np.ndarray:
        """
        generate a list of weights to decline as the index of self.scores increases.

        Parameters:
        -----------
        decay_rate: float
            factor to make the weights decline with starting first index to last.
            The higher, the older the scores later in the index are weighted less.
            Should be higher than 0.
        """
        if not decay_rate > 0:
            raise ValueError("decay_rate should be higher than 0!")

        return 1 / (np.arange(len(self.scores)) * decay_rate + 1)

    def _update_scores(self, scores: Union[np.ndarray, Sequence[float]], max_len: int = 10) -> None:
        scores = self._validation_update_scores(scores)

        # if score is inserted the first time,
        # set the score types and length for later checks
        if self.scoretype is None:
            outer_type = type(scores)
            inner_type = type(scores[0])
            self.scoretype = {
                "outer_type": outer_type,
                "inner_type": inner_type,
                "length": len(scores),
            }
        else:
            outer_type = self.scoretype["outer_type"]
            inner_type = self.scoretype["inner_type"]
            length = self.scoretype["length"]
            if not isinstance(scores, outer_type) or not isinstance(scores[0], inner_type) or len(scores) != length:
                if np.isscalar(scores):
                    inner_type_scores = np.nan
                    len_scores = np.nan
                else:
                    inner_type_scores = type(scores[0])
                    len_scores = len(scores)
                raise ValueError(
                    f"Scores must be of type {outer_type} and have an inner type of {inner_type} with a length of {length}. The type of the given scores is {type(scores)} with an inner type of {inner_type_scores} and a length of {len_scores}."
                )

        scores = ensure_numpy(scores)
        if len(self.scores) > max_len:
            self.scores = self.scores[:max_len]
        self.scores.insert(0, scores)

    def _validation_update_scores(self, scores):
        if np.isscalar(scores):
            scores = np.array([scores])
        elif isinstance(scores, list):
            scores = np.array(scores)
        elif isinstance(scores, (pd.Series, pd.DataFrame)):
            scores = ensure_numpy(scores)
        elif not isinstance(scores, np.ndarray):
            raise TypeError("Input 'scores' must be a scalar, list, or NumPy array")
        return scores

    def _handle_value_error_update_scores(
        self, scores: Union[np.ndarray, Sequence[float]], max_len: int, e: ValueError
    ):
        if self.scoretype["length"] == len(scores) and self.scoretype["outer_type"] == np.ndarray:
            self.update_scores(scores, max_len)
        else:
            raise e
