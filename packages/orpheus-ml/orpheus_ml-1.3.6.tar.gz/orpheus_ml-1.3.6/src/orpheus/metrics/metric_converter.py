"""MetricConverter class to convert a scoring function to properties related to minimizing/maximizing and type estimator."""

from typing import Callable, Tuple
from orpheus.metrics.constants import SCORE_TYPES
from orpheus.utils.helper_functions import get_obj_name


class MetricConverter:
    """
    Utility class to convert a scoring function to properties related to the
    type estimator and maximization/minimization.

    public attributes:
        metric: Callable
            Scoring function.
        name: str
            Name of the scoring function.
        maximize_scoring: bool
            (This attribute is not initialized in __init__. It's set in another method.)
        type_estimator: str
            (This attribute is not initialized in __init__. It's set in another method.)
    """

    def __init__(self, metric: Callable):
        """
        Initialize a MetricConverter object.

        Parameters
        ----------
        metric: Callable
            Scoring function. Must be a function that takes two arguments: y_true and y_pred.
        """
        self.metric = metric
        self.name = get_obj_name(metric)

    def __repr__(self):
        return f"MetricConverter({self.name}, {self.type_estimator}, {self.maximize_scoring})"

    @property
    def maximize_scoring(self) -> bool:
        return self._get_task_and_optimization()[1] == "maximize"

    @property
    def type_estimator(self) -> str:
        task, _ = self._get_task_and_optimization()
        if task == "regression":
            return "regressor"
        elif task == "classification":
            return "classifier"
        else:
            raise ValueError(f"type_estimator of metric {self.name} is not supported.")

    def _get_task_and_optimization(self) -> Tuple[str, str]:
        """Get the task and optimization of a scoring function."""
        function_name = self.name
        if function_name not in [
            f for opt_functions in SCORE_TYPES.values() for functions in opt_functions.values() for f in functions
        ]:
            raise ValueError(f"Function {function_name} is not supported.")

        task = None
        optimization = None

        for t, opt_functions in SCORE_TYPES.items():
            for o, functions in opt_functions.items():
                if function_name in functions:
                    task = t
                    optimization = o
                    break
            if task is not None:
                break

        return task, optimization
