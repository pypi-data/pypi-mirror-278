"""Decorators for scoring functions."""

from typing import Literal
from orpheus.metrics.constants import SCORE_TYPES
from orpheus.utils.helper_functions import get_obj_name


def register_scoring(
    modeling_type: Literal["regression", "classification"],
    optimization_direction: Literal["minimize", "maximize"],
):
    """
    A decorator to register a scoring function to the SCORE_TYPES dictionary.
    modeling_type: str
        The type of modeling task. Must be one of "regression" or "classification".

    optimization_direction: str
        The direction of optimization. Must be one of "minimize" or "maximize".
    """
    if modeling_type not in SCORE_TYPES:
        raise ValueError(f"modeling_type must be one of {list(SCORE_TYPES.keys())}")

    if optimization_direction not in SCORE_TYPES[modeling_type]:
        raise ValueError(f"optimization_direction must be one of {list(SCORE_TYPES[modeling_type].keys())}")

    def decorator(scoring_func):
        SCORE_TYPES[modeling_type][optimization_direction].append(get_obj_name(scoring_func))
        return scoring_func

    return decorator
