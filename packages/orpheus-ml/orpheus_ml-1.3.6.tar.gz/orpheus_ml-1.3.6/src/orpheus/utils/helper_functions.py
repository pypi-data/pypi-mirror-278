"""generic helper-functions which are vital for the functionality of the program."""

import functools
import inspect
import re
import os
from collections import deque
from itertools import islice, product
from typing import Callable, Generator, List, Optional, Union

import numpy as np
import pandas as pd
from bayes_opt import BayesianOptimization
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, train_test_split

from orpheus.utils.constants import ARGS_TO_IGNORE_HYPERTUNER
from orpheus.utils.logger import logger


@functools.lru_cache()
def get_default_args(func: Callable):
    """get all default arguments from a function"""
    signature = inspect.signature(func)
    return {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}


@functools.lru_cache()
def get_string_args_from_estimator(estimator):
    """get all passable string parameters from arguments in estimator"""

    default_values = get_default_args(estimator)
    default_values = {p: v for p, v in default_values.items() if p not in ARGS_TO_IGNORE_HYPERTUNER}

    doc_string = estimator.__doc__
    start_index = doc_string.find("arameters") - 1
    lines = doc_string[start_index:].splitlines()

    param_dict = {}
    for param in default_values:
        for line in lines:
            if param in line:
                try:
                    if line.index(":") < line.index(param):
                        continue
                except ValueError:
                    continue
                search = re.findall(r"{(.+?)}", line)
                if search:
                    try:
                        search = list(eval(search[0]))
                    except SyntaxError:  # handle typos with single quote in docstring
                        search = [i.replace("'", "").strip() for i in search[0].split(",")]
                    # last check to make sure all values are valid
                    pattern = r"^[a-zA-Z_]\w*$"
                    all_valid_params = all(re.match(pattern, val) for val in search if isinstance(val, str))
                    if all_valid_params:
                        param_dict[param] = search
                        break

    return param_dict


def optimize_splits_and_test_size(
    X,
    y,
    type_estimator,
    cv_obj,
    estimator=None,
    min_splits=2,
    max_splits=10,
    test_size_range=(0.1, 0.5),
    init_points=10,
    n_iter=20,
    shuffle=True,
    stratify=None,
    scoring=None,
    maximize_scoring=True,
    n_jobs=None,
    random_state=None,
    **bayes_kwargs,
) -> pd.Series:
    """
    Analyzes the data using cross-validation and finds the optimal number of splits
    based on the average accuracy, R-squared score or custom scoring function across all splits.

    A simple regression algorithm is used to find the optimal number of splits.

    Parameters:
    X (numpy array or pandas DataFrame): Input data
    y (numpy array or pandas Series): Target values
    estimator (estimator object): Scikit-learn estimator object
    cv_obj (cross-validation object): Scikit-learn cross-validation object
    min_splits (int): Minimum number of splits to test
    max_splits (int): Maximum number of splits to test. Last value is INCLUSIVE.
    init_points (int): Number of random points to sample before fitting the model
    n_iter (int): Number of iterations to perform
    shuffle (bool): Whether to shuffle the data before splitting
    stratify (numpy array or pandas Series): If not None, data is split in a stratified fashion
    scoring (str or callable): Scoring function to use
    maximize_scoring (bool): Whether to maximize or minimize the scoring function
    n_jobs (int): Number of jobs to run in parallel
    verbose (int): Verbosity level
    random_state (int): Random state
    **bayes_kwargs: optional kwargs for `optimizer.maximize`

    Returns:
    optimal_n_splits (int): Optimal number of splits
    optimal_test_size (float): Optimal test size
    optimal_params (dict): Dictionary with the optimal parameters
    """

    if not isinstance(cv_obj, type):
        cv_obj = type(cv_obj)

    # Determine the score function based on the type of the target variable
    if estimator is None:
        if type_estimator == "regressor":
            estimator = LinearRegression()
        else:
            estimator = LogisticRegression()
    else:
        # check if estimator is instantiated:
        if isinstance(estimator, type):
            raise TypeError(f"{estimator} was passed uninstantiated. Please pass instantiated estimator!")

    scoring = make_scorer(scoring, greater_is_better=maximize_scoring) if scoring is not None else None

    def evaluate_splits(n_splits: int, test_size: float):
        n_splits = int(round(n_splits))

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=stratify,
        )

        # Set the number of splits in the cross-validation object
        cv_obj_init = cv_obj(n_splits=n_splits)

        # Calculate cross-validation score
        train_score = cross_val_score(
            estimator,
            X_train,
            y_train,
            cv=cv_obj_init,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
        )

        nan_ratio = np.isnan(train_score).sum() / len(train_score)
        if nan_ratio > 0.5:
            raise ValueError(f"More than 50 percent of values in train_score are NaN: {train_score}")
        else:
            train_score = np.nanmean(train_score)

        estimator.fit(X_train, y_train)
        if scoring is None:
            test_score = estimator.score(X_test, y_test)
        else:
            test_score = scoring(estimator, X_test, y_test)

        # Save the score and check if it's the best so far
        return np.mean([train_score, test_score])

    # Initialize the Bayesian optimization object
    # Set the bounds for Bayesian optimization
    pbounds = {
        "n_splits": (min_splits, max_splits),
        "test_size": test_size_range,
    }

    # Instantiate the Bayesian optimizer
    optimizer = BayesianOptimization(
        f=evaluate_splits,
        pbounds=pbounds,
        random_state=random_state,
        allow_duplicate_points=True,
    )
    # Perform the optimization
    optimizer.maximize(init_points=init_points, n_iter=n_iter, **bayes_kwargs)

    # Get the optimal number of splits and test size
    optimal_params = optimizer.max["params"]
    optimal_n_splits = int(round(optimal_params["n_splits"]))
    optimal_test_size = optimal_params["test_size"]

    return optimal_n_splits, optimal_test_size, optimal_params


def dict_product_R2(dicts: List[dict], max_index: Optional[int] = None) -> Generator:
    """
    >>> list(dict_product_R2(dict(number=[1,2], character='ab')))
    [{'character': 'a', 'number': 1},
     {'character': 'a', 'number': 2},
     {'character': 'b', 'number': 1},
     {'character': 'b', 'number': 2}]
    """
    for x in islice(product(*dicts.values()), 0, max_index):
        yield dict(zip(dicts, x))


def dict_product_R3(d: dict, max_index: Optional[int] = None) -> Generator:
    """lengthen all lists in dict to be equal length"""
    max_len = max(map(len, d.values()))
    d = {k: v * max_len for k, v in d.items()}

    keys, values = list(d.keys())[::-1], list(d.values())

    # initialise deque:
    deq_values = deque(maxlen=len(values))
    deq_keys = deque(keys)

    if max_index is not None:
        max_index = int(max_index / len(d))
        iterator = islice(zip(*values), 0, max_index)
    else:
        iterator = zip(*values)

    for i in iterator:
        for j in i:
            if len(deq_values) == len(values):
                yield dict(zip(deq_keys, deq_values))
            deq_values.appendleft(j)
            deq_keys.rotate()


def has_only_int(arr: np.ndarray) -> bool:
    """determine whether an array only has integer-values or not."""
    if isinstance(arr, pd.Series):
        arr = arr.to_numpy()
    arr = arr.astype(np.float32)  # not using np.unique saves considerable time
    if isinstance(arr[0], np.ndarray):
        arr = arr.flatten()
    return np.all(arr % 1 == 0)


def target_is_classifier(arr: Union[np.ndarray, pd.Series]) -> bool:
    """determine whether an array with targetvariables is regressor or classification

    returns
    -------
        True if all values are integers, False otherwise
    """
    if arr.ndim != 1:
        raise ValueError("Input array must be one-dimensional.")

    return has_only_int(arr)


def get_max_occurance_pct(arr: np.ndarray) -> float:
    """find the percentage of occurances of most common value in an array."""
    counts = np.unique(arr, return_counts=True)[1]
    max_occurance_value = max(map(lambda x: x / counts.sum(), counts))
    return max_occurance_value


def ensure_numpy(X: Union[np.ndarray, pd.DataFrame, pd.Series]) -> np.ndarray:
    """Ensure that X is a numpy array."""
    if isinstance(X, (pd.DataFrame, pd.Series)):
        return X.to_numpy()
    return np.asarray(X)


def keep_common_elements(lists):
    """Returns a list of elements that are common to all lists in `lists`"""
    sets = [set(l) for l in lists]
    common_integers = set.intersection(*sets)
    return list(common_integers)


def get_obj_name(obj: object):
    """Returns the name of an object, whether it is a class, function, or partial function."""

    # If object is a class or function, return its __name__
    if hasattr(obj, "__name__"):
        return obj.__name__

    # If object is a functools.partial instance, return the name of the wrapped function
    if isinstance(obj, functools.partial) and hasattr(obj, "func"):
        return obj.func.__name__

    # If object is an instance of a class (not a class itself), return class name
    if isinstance(obj, object):
        return obj.__class__.__name__

    # Fallback - return string representation of the object type
    return str(type(obj))


def standardize_config_path_to_yaml(config_path: str) -> str:
    """Standardize the config_path to a .yaml file."""
    config_path_base, config_path_ext = os.path.splitext(config_path)

    # Check if the extension is empty or not '.yaml'
    if not config_path_ext or config_path_ext.lower() != ".yaml":
        config_path = config_path_base + ".yaml"

    config_path = os.path.abspath(config_path)
    return config_path
