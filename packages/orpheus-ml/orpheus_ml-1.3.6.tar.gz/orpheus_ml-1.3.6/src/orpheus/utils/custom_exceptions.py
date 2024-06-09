"""custom exceptions"""

import numpy as np
import pandas as pd
from typing import Optional, Union
from orpheus.utils.logger import logger


class NoRobustModelsInPipelineError(Exception):
    def __init__(
        self,
        threshold_score: Optional[float],
        validation_scores: Union[float, pd.Series, None],
        message: str,
    ):
        validation_scores_repr = None
        logger.error(message)
        logger.error(f"threshold_score: {threshold_score}")
        if validation_scores is not None:
            validation_scores_repr = (
                validation_scores.to_string() if not np.isscalar(validation_scores) else validation_scores
            )
        logger.error(f"validation_scores:\n{validation_scores_repr}")
        super().__init__(message)


class DataPropertyMismatchError(Exception):
    pass
