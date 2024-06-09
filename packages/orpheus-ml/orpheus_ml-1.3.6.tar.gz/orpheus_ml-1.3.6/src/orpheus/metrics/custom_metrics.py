"""Define custom metrics here. Register your custom metrics to the MetricConverter class by using the @register_scoring decorator."""

import numpy as np
from orpheus.metrics.decorators import register_scoring


@register_scoring("regression", "minimize")
def root_mean_squared_error(y_true, y_pred):
    """
    Calculate the Root Mean Squared Error (RMSE)
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))
