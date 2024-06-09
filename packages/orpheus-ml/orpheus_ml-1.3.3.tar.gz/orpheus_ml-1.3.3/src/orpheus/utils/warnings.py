"""Warnings for specific conditions or errors."""
from sklearn.metrics._scorer import _BaseScorer

from orpheus.utils.logger import logger


def _check_sklearn_metrics():
    """Check if all metrics are registered in the sklearn.metrics module."""
    from src.orpheus.metrics.constants import SCORE_TYPES
    from sklearn.metrics import __all__ as all_sklearn_metrics

    all_registered_scores = []
    for task_type in SCORE_TYPES.values():
        for score_list in task_type.values():
            all_registered_scores.extend(score_list)
    score_diff = set(all_registered_scores) - set(
        all_sklearn_metrics
    )  # Check if there are any scores that are not in the sklearn.metrics module
    if score_diff:
        logger.warn_always(
            f"Registered scores {score_diff} from the SCORE_TYPES constant are not in the sklearn.metrics module"
        )

    # score_diff = set(all_sklearn_metrics) - set(all_registered_scores)  # Check if there are any scores that are not registered
    # if score_diff:
    #     logger.warn_always(f"Scores {score_diff} from sklearn.metrics are not registered in the SCORE_TYPES constant")


def _warn_error_metrics_and_cross_val_score(scoring: _BaseScorer):
    """Warn if the scoring function is an error metric and cross_val_score is used."""
    if scoring:
        if not isinstance(scoring, _BaseScorer):
            raise TypeError(f"scoring must be a callable or a _BaseScorer object, but got {type(scoring)} instead.")
        func_name = scoring._score_func.__name__
        if func_name.lower().endswith("error"):
            logger.warn_always(
                "Scoring function '{}' is an error metric. "
                "\nDue to sklearn's implementation of error metrics and cross_val_score, "
                "this might lead to unexpected results when using 'FeatureRemoving.remove_features_by_correlation()'."
                "\nConsider registering a custom scoring function that returns the negative of the error metric, with the maximize_scoring parameter set to True.".format(
                    func_name
                )
            )
