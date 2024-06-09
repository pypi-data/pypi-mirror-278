"""Context managers for Orpheus."""

import multiprocessing as mp
import inspect
from typing import Any, Callable, Optional, Union

from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger


class FunctionTimeoutHandler:
    """
    A handler used to set a timeout for a function call with n_jobs parameter.
    This is useful for functions which can hang if n_jobs is set to a high number.

    Known functions which can hang:
    - cross_val_score (sklearn)
    - Parallel (joblib)

    The function will be executed in a separate process and will be terminated if it takes too long.

    Pros:
        - The function will be executed in a separate process, so the main process will not be blocked.
        - The function will be terminated if it takes too long.
    Cons:
        - Starting a new process can cause a significant overhead.

    Attributes:
        func (Callable): The function to be executed. NOTE: The function must have an 'n_jobs' parameter in its signature.
        args (Tuple): The positional arguments for the function.
        kwargs (Dict): The keyword arguments for the function.
        timeout (Optional[Union[int, float]]): Timeout in seconds.
        n_jobs_on_timeout (int): Number of jobs to use if the function times out.
        result (Any): The result of the function after execution.
    """

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        timeout: Optional[Union[int, float]] = None,
        n_jobs_on_timeout: int = 1,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the FunctionTimeoutHandler.

        Parameters:
            func (Callable): The function to be executed.
            *args: Positional arguments to pass to the function.
            timeout (Optional[Union[int, float]]): The maximum time to wait for the function. None means no timeout.
            n_jobs_on_timeout (int): Number of jobs to use if the function times out.
            **kwargs: Keyword arguments to pass to the function.
        """
        if not callable(func):
            raise TypeError("func must be a callable function.")

        is_bound_method = hasattr(func, "__self__") and func.__self__ is not None
        if is_bound_method:
            obj_func = func.__self__
            if not hasattr(obj_func, "n_jobs"):
                raise ValueError(
                    f"The object '{get_obj_name(obj_func)}' with method '{get_obj_name(func)}' must have an 'n_jobs' attribute."
                )
        else:
            if "n_jobs" not in inspect.signature(func).parameters:
                raise ValueError(
                    f"The function '{get_obj_name(func)}' must have an 'n_jobs' parameter in its signature."
                )

        if timeout is not None and not (isinstance(timeout, (int, float)) and timeout > 0):
            raise ValueError("timeout must be a positive number or None.")

        if not isinstance(n_jobs_on_timeout, int) or n_jobs_on_timeout <= 0:
            raise ValueError("n_jobs_on_timeout must be a positive integer.")

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.n_jobs_on_timeout = n_jobs_on_timeout
        self._is_bound_method = is_bound_method
        self.result: Any = None

    def __enter__(self) -> Any:
        """
        Executes the function with the given arguments and returns the result.

        Returns:
            Any: The result of the function execution.
        """
        if self.timeout is None:
            self.result = self.func(*self.args, **self.kwargs)
        else:
            with mp.Pool(processes=1) as pool:
                try:
                    result = pool.apply_async(self.func, self.args, self.kwargs)
                    self.result = result.get(timeout=self.timeout)
                except mp.TimeoutError:
                    logger.error(
                        f"TimeoutError: execution of {get_obj_name(self.func)} took too long. Setting n_jobs to {self.n_jobs_on_timeout} and retrying."
                    )
                    if self._is_bound_method:
                        # replacing n_jobs with n_jobs_on_timeout in the object's n_jobs attribute
                        self.func.__self__.n_jobs = self.n_jobs_on_timeout
                    else:
                        self.kwargs[
                            "n_jobs"
                        ] = self.n_jobs_on_timeout  # replacing n_jobs with n_jobs_on_timeout in kwargs
                    self.result = self.func(*self.args, **self.kwargs)
        return self.result

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
