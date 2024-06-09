"""Define custom metrics here. Register your custom metrics to the MetricConverter class by using the @register_scoring decorator."""

import numpy as np
from orpheus.metrics.decorators import register_scoring


@register_scoring("regression", "minimize")
def root_mean_squared_error(y_true, y_pred):
    """
    Calculate the Root Mean Squared Error (RMSE)
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


@register_scoring("regression", "minimize")
def log_root_mean_squared_error(y_true, y_pred):
    return np.sqrt(np.mean((np.log(y_pred + 1) - np.log(y_true + 1)) ** 2))
