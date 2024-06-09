"""Helperfunctions for HyperTuner related classes."""

import functools
import inspect
import multiprocessing as mp
import random
import sys
import time
import traceback
from collections import deque
from typing import Any, Callable, Deque, Dict, Generator, List, Optional, Set, Tuple, Type, Union

import numpy as np
from sklearn.utils import all_estimators

from orpheus.metrics.constants import SCORE_TYPES
from orpheus.metrics.helper_functions import get_all_registered_metrics_in_SCORE_TYPES
from orpheus.utils.constants import ARGS_TO_IGNORE_HYPERTUNER
from orpheus.utils.custom_types import EstimatorErrorInfo
from orpheus.utils.helper_functions import (
    ensure_numpy,
    get_default_args,
    get_max_occurance_pct,
    get_obj_name,
    target_is_classifier,
)
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import EstimatorType


def strip_alpha_from_string(string: str) -> str:
    """strip alpha characters from a string and return the result in lowercase."""
    return "".join([char for char in string if char.isalpha()]).lower()


def instantiate_estimator(
    estimator: Type["EstimatorType"], **params
) -> Tuple[Optional["EstimatorType"], List[EstimatorErrorInfo]]:
    """
    Instantiate an estimator with the found faulty parameters, handling any error that occurs.


    Parameters
    ---
    estimator: Type[EstimatorType]
        The estimator to instantiate.
    **params:
        The parameters to pass to the estimator.

    Returns
    ---
    Tuple[Optional["EstimatorType"], List[EstimatorErrorInfo]]
        If an estimator is instantiated succesfully, return the estimator together with the found faulty params.
        If estimator instantionation failed, return None. Together with the found faulty params.
    """
    param_queue: Deque[Dict] = deque([params])
    tried_params: Set[str] = set()
    faulty_params: List[EstimatorErrorInfo] = []

    while param_queue:
        current_params = param_queue.popleft()
        hashable_params = tuple(current_params.items())
        if hashable_params in tried_params:
            return None, faulty_params
        else:
            tried_params.add(hashable_params)

        try:
            instantiated = estimator(**current_params)
            return instantiated, faulty_params
        except Exception as err:
            logger.error(f"{estimator} : {traceback.format_exc()}")
            error_string = strip_alpha_from_string(str(err))
            found_faulty_params = [
                EstimatorErrorInfo(estimator, err, param, val)
                for param, val in current_params.items()
                if strip_alpha_from_string(param) in error_string
            ]
            faulty_params.extend(found_faulty_params)
            new_params = {
                k: v for k, v in current_params.items() if k not in (err_info.parameter for err_info in faulty_params)
            }
            param_queue.append(new_params)

    return None, faulty_params


@functools.lru_cache()
def get_numerical_defaultargs_from_estimator(
    estimator: EstimatorType,
) -> Tuple[dict, dict]:
    """
    get numerical default-values from args of estimator

    returns
    ---
    dict, dict -> default_ints, default_floats
    """
    default_values = get_all_defaultargs_from_estimator(estimator)
    args_to_pass = {p for s in ARGS_TO_IGNORE_HYPERTUNER for p in default_values if s in p}

    default_floats = {p: v for p, v in default_values.items() if (isinstance(v, float) and p not in args_to_pass)}
    default_ints = {p: v for p, v in default_values.items() if (isinstance(v, int) and p not in args_to_pass)}

    return default_ints, default_floats


@functools.lru_cache()
def get_all_defaultargs_from_estimator(estimator) -> dict:
    """
    Get all default-values from args of estimator
    Remove all bools, infs and args_to_pass
    """
    default_values = {
        k: v
        for k, v in get_default_args(get_uncalled_estimator(estimator)).items()
        if not isinstance(v, (bool)) and k not in ARGS_TO_IGNORE_HYPERTUNER
    }

    return default_values


@functools.lru_cache()
def get_uncalled_estimator(estimator: EstimatorType):
    """return uncalled estimator."""
    if isinstance(estimator, functools.partial):
        return estimator.func
    return estimator if isinstance(estimator, type) else type(estimator)


def get_estimator_scores(
    estimator_list: List[EstimatorType],
    X_test: np.ndarray,
    y_test: np.ndarray,
    scoring_func: Callable,
    maximize_scoring: bool,
    penalty_to_score_if_overfitting: float,
) -> dict:
    """
    get the score out of a list of estimators.

    Parameters
    ---
    penalty_to_score_if_overfitting: float = None
        see docs of 'fit()' for information about this parameter.
    """

    if not 0 <= penalty_to_score_if_overfitting <= 1:
        raise ValueError('"penalty_to_score_if_overfitting" should be between 0 and 1!')

    # initialise variables:
    score_dict = {}
    msg_penalize_factor = ""
    y_pred = None

    for estimator in estimator_list:
        try:
            if scoring_func is None:
                score = estimator.score(X_test, y_test)
            else:
                y_pred = estimator.predict(X_test)
                score = scoring_func(y_pred, y_test)

            if penalty_to_score_if_overfitting > 0:
                if y_pred is None:
                    y_pred = estimator.predict(X_test)
                max_occurance_y_pred = get_max_occurance_pct(y_pred)
                diff_max_occurance = abs(max_occurance_y_pred - get_max_occurance_pct(y_test))
                _ = -5.266412 + (7.0175 - -5.266412) / (1 + (penalty_to_score_if_overfitting / 0.7495224) ** 0.76419)
                penalize_factor = 1 + ((diff_max_occurance**_) * 10)
                msg_penalize_factor = f"|| % diff_max_occurance {(diff_max_occurance*100):.2f} % || penalize_factor of score: {penalize_factor:.3f} "
                if maximize_scoring:
                    score /= penalize_factor
                else:
                    score *= penalize_factor
            score_dict.update({estimator: score})
            logger.info(f"{estimator} : {score} {msg_penalize_factor}")
        except Exception:
            logger.error(f"{estimator} : {traceback.format_exc()}")

    sorted_scores = {
        r: score_dict[r]
        for r in sorted(score_dict, key=score_dict.get, reverse=maximize_scoring)
        if not np.isnan(score_dict[r])
    }

    return sorted_scores


def fit_estimator(
    estimator: EstimatorType,
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> Union[EstimatorType, MemoryError, List[List[Union[EstimatorType, Exception, str]]]]:
    """
    fit estimator  and catch MemoryError and other Exceptions.
    Used in 'fit_estimators_parallel()'
    """
    try:
        estimator.fit(X_train, y_train)
    except MemoryError as memory_err:
        logger.critical(f"{estimator} : {traceback.format_exc()}")
        logger.critical(
            f"MemoryError: {estimator} could not be fitted. Consider reducing the size of your trainingdata or use another estimator."
        )
        return memory_err
    except Exception as err:
        return [estimator, err, traceback.format_exc()]
    return estimator


def fit_estimators_parallel(
    timeout: int,
    estimator_list: List[EstimatorType],
    num_workers: int,
    X_train: np.ndarray,
    y_train: np.ndarray,
    random_subset: float = 1.0,
) -> List[Union[EstimatorType, List[List[Union[EstimatorType, Exception, str]]]]]:
    """
    fit estimators in parallel.

    Parameters
    ---
    timeout: int
        timeout in seconds when all childprocesses should end.
        If None, no timeout is used.

    estimator_list: List[EstimatorType]
        list of estimators to fit

    num_workers: int
        number of workers to use in the multiprocessing pool

    X_train: np.ndarray
        training data

    y_train: np.ndarray
        training target

    random_subset: float = 1.0
        if < 1.0, use a random subset of the data per iteration.
        This is useful when you have a lot of features or samples and want to speed up the process.

    Returns
    ---
    List[Union[EstimatorType, List[EstimatorType, Exception, str]]]
        List, containing fitted estimators or list of [estimator, exception, traceback]

    """
    X_train = ensure_numpy(X_train)
    y_train = ensure_numpy(y_train)

    pool = mp.Pool(num_workers)

    if random_subset < 1.0:
        indices_generator = generate_subset_indices_from_estimator_list(estimator_list, X_train, random_subset)

        results = [
            pool.apply_async(
                fit_estimator,
                args=(estimator_list[idx],),
                kwds={
                    "X_train": X_train[item],
                    "y_train": y_train[item],
                },
            )
            for idx, item in enumerate(indices_generator)
        ]
    else:
        results = [
            pool.apply_async(
                fit_estimator,
                args=(item,),
                kwds={
                    "X_train": X_train,
                    "y_train": y_train,
                },
            )
            for item in estimator_list
        ]

    returned_results = []
    if timeout is not None:
        time_to_wait = timeout
        start_time = time.time()
        for idx, result in enumerate(results, start=1):
            try:
                # wait for up to time_to_wait seconds
                returned_results.append(result.get(time_to_wait))
            except mp.TimeoutError:
                break
            except Exception:
                logger.error(traceback.format_exc())
            else:
                logger.info(f"Finished iteration {idx}")
                # how much time has exprired since we began waiting?
            t = time.time() - start_time
            time_to_wait = max(timeout - t, 0)
        pool.terminate()  # all processes, busy or idle, will be terminated
        pool.join()  # wait for the worker processes to terminate
    else:
        pool.close()
        pool.join()
        for idx, result in enumerate(results, start=1):
            try:
                returned_results.append(result.get())
            except Exception:
                logger.error(traceback.format_exc())
            else:
                logger.notice(f"Finished iteration {idx}")

    has_memory_error = any(isinstance(i, MemoryError) for i in returned_results)
    if has_memory_error:
        logger.error("Program will exit now, as MemoryError was found, which is a fatal error.")
        sys.exit(0)

    return returned_results


def create_random_indices(X_train: np.ndarray, random_subset: float) -> np.ndarray:
    """create random indices from a subset of the data"""
    return np.random.choice(
        np.arange(X_train.shape[0]),
        size=int(X_train.shape[0] * random_subset),
        replace=False,
    )


def generate_subset_indices_from_estimator_list(
    estimator_list: List[EstimatorType], X_train: np.ndarray, random_subset: float
) -> Generator:
    """create multiple indices for taking a random subset of the data per iteration,
    where the number of indices is equal to the number of estimators in the estimator_list.
    """
    if not 0 < random_subset < 1.0:
        raise ValueError('"subset" should be between 0 and 1!')
    logger.notice(f"Using a random subset of {random_subset*100:.2f}% of the data per iteration.")

    create_random_indices_partial = functools.partial(
        create_random_indices, X_train=X_train, random_subset=random_subset
    )

    indices_generator = (create_random_indices_partial() for _ in range(len(estimator_list)))

    return indices_generator


def _get_attr(obj: Any, attr: str, additional_error_msg: Optional[str] = None):
    """check if attr exists and return it, else raise (custom) AttributeError."""
    try:
        return getattr(obj, attr)
    except AttributeError:
        raise AttributeError(f"{attr} does not exist! {additional_error_msg}") from None


def check_type_estimator(y, type_estimator, maximize_scoring):
    """
    Automaticly detect type_estimator if None. Else check if type_estimator is valid.
    If type_estimator is correct, just return it.
    This function can be used in the constructor of any component in the pipeline.
    """
    if type_estimator is None:
        if target_is_classifier(y):
            type_estimator = "classifier"
        else:
            type_estimator = "regressor"
        logger.notice(
            f"AUTO-DETECTED TYPE ESTIMATOR AS {type_estimator.upper()}, WHERE SCORE IS {'MAXIMIZED' if maximize_scoring else 'MINIMIZED'}."
        )
    elif type_estimator not in {"regressor", "classifier"}:
        raise ValueError(
            'Make sure that during instantiation: attribute "type_estimator" is: {None, "regressor", "classifier"}.'
        )

    return type_estimator


def check_scoring(
    scoring: Optional[Callable],
    maximize_scoring: bool,
    type_estimator: str,
) -> Optional[Callable]:
    """
    Check if scoring is valid. type_estimator must be known and
    either be "classifier" or "regressor".
    """
    if type_estimator is None or type_estimator not in ["classifier", "regressor"]:
        raise ValueError("type_estimator must be known and either be 'classifier' or 'regressor'.")
    if scoring is not None:
        scoring_name = get_obj_name(scoring)
        if scoring_name not in get_all_registered_metrics_in_SCORE_TYPES():
            logger.warning(f"'{scoring_name}' is not a registered metric in the SCORE_TYPES constant.")
            return scoring
        modeling_type = "classification" if type_estimator == "classifier" else "regression"
        optimization_direction = "maximize" if maximize_scoring else "minimize"
        list_of_metrics = SCORE_TYPES[modeling_type][optimization_direction]
        if scoring_name not in list_of_metrics:
            raise ValueError(f"scoring '{scoring_name}' is not valid for {modeling_type} and {optimization_direction}.")

    return scoring


def check_estimator_list(
    estimator_list,
    use_sklearn_estimators_aside_estimator_list,
    exclude_estimators,
    type_estimator,
    random_state,
) -> List[EstimatorType]:
    """
    Check if estimator_list is valid and transform it to the required format.
    """
    if estimator_list is None:
        if use_sklearn_estimators_aside_estimator_list:
            estimator_list = _get_sklearn_estimator_list(type_estimator, random_state)
        else:
            raise ValueError(
                "No estimators found! Did you pass 'estimator_list'? If not, is 'use_sklearn_estimators_aside_estimator_list' set to True? "
            )
    else:
        if use_sklearn_estimators_aside_estimator_list:
            sklearn_estimators = _get_sklearn_estimator_list(type_estimator, random_state)
            # Use set operations to merge two lists without duplicates
            estimator_list = list(set(estimator_list).union(set(sklearn_estimators)))

    if exclude_estimators:
        estimator_list = remove_excluded_estimators(estimator_list, exclude_estimators)
    return estimator_list


def remove_excluded_estimators(
    estimator_list: List[EstimatorType],
    exclude_estimators: Optional[List[str]] = None,
) -> List[EstimatorType]:
    """
    Remove estimators from the list if their names contain any of the excluded words.
    """
    exclude_estimators = [word.lower() for word in exclude_estimators]
    for word in exclude_estimators:
        for est in estimator_list.copy():
            estimator_name = get_obj_name(est)
            if word in estimator_name.lower():
                estimator_list.remove(est)
                logger.warning(f"Excluding {estimator_name} from estimator list, as it contains the word '{word}'.")
    return estimator_list


def exclude_hyperparameters_from_paramgrid(
    paramgrid: Dict[str, List],
    exclude_hyperparameters: Optional[List[str]] = None,
    for_round_2: bool = False,
) -> Dict[str, List]:
    """
    Remove hyperparameters from the paramgrid if their names contain any of the excluded words.
    """
    if not exclude_hyperparameters:
        return paramgrid

    exclude_hyperparameters = [word.lower() for word in exclude_hyperparameters]
    new_paramgrid = {}

    if for_round_2:
        for estimator, params in paramgrid.items():
            new_params = {
                param: value
                for param, value in params.items()
                if all(word not in param.lower() for word in exclude_hyperparameters)
            }
            if new_params:
                new_paramgrid[estimator] = new_params
                removed_params = set(params.keys()) - set(new_params.keys())
                for removed_param in removed_params:
                    logger.warning(
                        f"Excluding hyperparameter '{removed_param}' from estimator '{estimator}' in paramgrid, as it contains one of the words '{exclude_hyperparameters}'."
                    )
    else:
        new_paramgrid = {
            param: value
            for param, value in paramgrid.items()
            if all(word not in param.lower() for word in exclude_hyperparameters)
        }
        if new_paramgrid:
            removed_params = set(paramgrid.keys()) - set(new_paramgrid.keys())
            for removed_param in removed_params:
                logger.warning(
                    f"Excluding hyperparameter '{removed_param}' from paramgrid, as it contains one of the words '{exclude_hyperparameters}'."
                )
    return new_paramgrid


def all_estimators_extended(type_filter: str) -> List[Tuple[str, EstimatorType]]:
    """get all sklearn estimators and, if installed, estimators from lightgbm, catboost and xgboost."""

    # Try importing libraries, set to None if not available
    try:
        import lightgbm as lgb  # type: ignore
    except ImportError:
        lgb = None

    try:
        import xgboost as xgb  # type: ignore
    except ImportError:
        xgb = None

    if type_filter not in {"classifier", "regressor"}:
        raise ValueError("type_filter must be one of {'classifier', 'regressor'}.")

    estimator_list = all_estimators(type_filter=type_filter)

    if lgb:
        lgb_module = lgb.sklearn
        lgb_base_class = getattr(lgb, f"LGBM{type_filter.capitalize()}")
        estimator_list.extend(
            [
                (name, cls)
                for name, cls in inspect.getmembers(lgb_module)
                if inspect.isclass(cls) and issubclass(cls, lgb_base_class)
            ]
        )

    if xgb:
        xgb_base_class = getattr(xgb, f"XGB{type_filter.capitalize()}")
        estimator_list.extend(
            [
                (name, cls)
                for name, cls in inspect.getmembers(xgb)
                if inspect.isclass(cls) and issubclass(cls, xgb_base_class)
            ]
        )

    return estimator_list


def pretty_print_errors(returned_errors: List[List[Union[EstimatorType, Exception, str]]]) -> None:
    """Print the errors from the tracback returned by the parallel fit process."""
    logger.warning(f"{len(returned_errors)} estimators failed during fit:")
    for est, err, tb in returned_errors:
        logger.error(f"estimator: {est}\n{tb}")


def _get_sklearn_estimator_list(type_estimator: str, random_state: int) -> List[EstimatorType]:
    """get all sklearn estimators in a list and randomly shuffle the list."""
    estimator_list = [e[1] for e in all_estimators_extended(type_filter=type_estimator)]
    random.seed(random_state)
    random.shuffle(estimator_list)
    return estimator_list


def _collect_bound_errors(
    estimator: EstimatorType,
    returned_errors: List[Exception],
    bounds_paramgrid_R2: List[Dict[str, EstimatorErrorInfo]],
) -> Tuple[List[EstimatorErrorInfo], List[EstimatorErrorInfo]]:
    """
    Collects the errors that are returned from the bound counting process.

    Returns:
        upper_bound_errors: list of errors (EstimatorErrorInfo) that occured when counting the upper bound
        lower_bound_errors: list of errors (EstimatorErrorInfo) that occured when counting the lower bound
    """
    upper_bound_errors = []
    lower_bound_errors = []

    for idx, (error, param) in enumerate(zip(returned_errors, bounds_paramgrid_R2)):
        param, val_to_replace = param.popitem()
        found_error = EstimatorErrorInfo(estimator, error, param, val_to_replace)
        if idx % 2 == 0:  # if lower_bound_error
            lower_bound_errors.append(found_error)
        else:  # upper_bound_error
            upper_bound_errors.append(found_error)

    return upper_bound_errors, lower_bound_errors


def _create_paramgrid_from_distance_factors(
    n_vals_per_param,
    int_distance_factor,
    float_distance_factor,
    default_values,
    default_ints,
    default_floats,
) -> Dict[str, List]:
    """
    create paramgrid with distance factors from configuration file.
    The default values of the estimator are the center point.
    """
    paramgrid = {}

    for k in default_ints:
        if default_values[k] in {0, None}:
            paramgrid[k] = [0] + [n * int_distance_factor for n in range((n_vals_per_param - 1), 0, -1)]
        else:
            right_splitter = (n_vals_per_param - 1) // 2
            left_splitter = (n_vals_per_param - 1) // 2
            paramgrid[k] = (
                [default_values[k] / (int_distance_factor * n) for n in range(1, left_splitter + 1)]
                + [default_values[k]]
                + [default_values[k] * (int_distance_factor * n) for n in range(1, right_splitter + 1)]
            )
            paramgrid[k] = list(map(int, paramgrid[k]))

    for k in default_floats:
        if default_values[k] in {0, None}:
            paramgrid[k] = [0] + [1 / float_distance_factor**n for n in range((n_vals_per_param - 1), 0, -1)]
        else:
            right_splitter = (n_vals_per_param - 1) // 2
            left_splitter = (n_vals_per_param - 1) // 2
            paramgrid[k] = (
                [default_values[k] / (float_distance_factor * n) for n in range(1, left_splitter + 1)]
                + [default_values[k]]
                + [default_values[k] * (float_distance_factor * n) for n in range(1, right_splitter + 1)]
            )

    return paramgrid
