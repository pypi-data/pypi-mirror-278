from orpheus.metrics.constants import SCORE_TYPES


def get_all_registered_metrics_in_SCORE_TYPES() -> list:
    """Get all registered metrics of the SCORE_TYPES constant."""
    metric_names = [
        metric_name
        for metric_type in SCORE_TYPES.values()
        for optimization_type in metric_type.values()
        for metric_name in optimization_type
    ]
    return metric_names
