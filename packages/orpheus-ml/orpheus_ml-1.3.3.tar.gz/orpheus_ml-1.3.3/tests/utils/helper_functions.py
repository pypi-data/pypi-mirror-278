"""Helper functions and classes for end-to-end tests."""


import datetime
import inspect
import random
import string
import traceback
from functools import partial
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.datasets import make_classification, make_regression
from sklearn.metrics import accuracy_score, r2_score

from src.orpheus.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from src.orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from src.orpheus.services.component_service import ComponentService
from src.orpheus.services.pipeline_evolver_service import PipelineEvolverService
from src.orpheus.services.preparator_service import PreparatorService
from src.orpheus.utils.constants import DEFAULT_VALUES
from src.orpheus.utils.custom_types import EstimatorType
from src.orpheus.utils.logger import logger
from tests.customize_test import pass_pipelines_for_testing
from tests.utils.modeling_type import ModelingType
from tests.utils.test_error_info import EndToEndTestEstimatorErrorInfo


def run_multiple_end_to_end_tests(
    modeling_types: List[ModelingType],
    config_path: str,
    downcast: bool = True,
    scale: bool = True,
    add_features: bool = True,
    remove_features: bool = True,
    trials: int = 9,
    n_jobs: int = DEFAULT_VALUES["n_jobs"],
    verbose: int = DEFAULT_VALUES["verbose"],
    n_samples: int = 100,
    n_features: int = 10,
    top_n_based=5,
    top_n_stacked=[2, 3],
    catch_and_collect_errors: bool = False,
    timeout_duration: Optional[int] = None,
    log_file_path: Optional[str] = None,
) -> EndToEndTestEstimatorErrorInfo:
    """
    Run end-to-end tests for all modeling types.

    Parameters
    ----------
    modeling_types : List[ModelingType]
        List of modeling types to run the end-to-end tests for.

    config_path : str
        Path to the config file.

    trials : int, optional
        Number of times to run the end-to-end tests.
        Will run N trials * 3 modeling types tests.
        Defaults to 1.

    n_jobs : int, optional
        Number of jobs to run in parallel. Defaults to 1.

    verbose : int, optional
        Verbosity level. Defaults to 0.

    n_samples : int, optional
        Number of samples to use in the end-to-end tests. Defaults to 100.

    n_features : int, optional
        Number of features to use in the end-to-end tests. Defaults to 10.

    catch_and_collect_errors : bool, optional
        Whether to handle errors or not so that the tests wont break.
        Collect the number of failed tests and print it at the end.

    timeout_duration : Optional[int], optional
        Timeout duration during component_service.generate_pipeline_for_base_models and
        component_service.generate_pipeline_for_stacked_models.
        Used if fitting causes hanging. Defaults to None.

    log_file_path : Optional[str], optional
        Path to the log file. Defaults to None.
        If given, the log file will be used to log the results of the end-to-end tests.
        else (if None), the results will be printed to the console.
    """
    execute_test = partial(
        run_single_end_to_end_test,
        config_path=config_path,
        verbose=verbose,
        n_jobs=n_jobs,
        n_samples=n_samples,
        n_features=n_features,
        top_n_based=top_n_based,
        top_n_stacked=top_n_stacked,
        downcast=downcast,
        scale=scale,
        add_features=add_features,
        remove_features=remove_features,
        timeout_duration=timeout_duration,
        log_file_path=log_file_path,
    )

    error_info = EndToEndTestEstimatorErrorInfo()
    modeling_types_list = [modeling_types[i % len(modeling_types)] for i in range(trials)]

    for n, modeling_type in enumerate(modeling_types_list, start=1):
        modeling_type_name = modeling_type.name
        logger.notice(f"Running end_to_end_test {n, modeling_type_name}")
        if catch_and_collect_errors:
            try:
                execute_test(modeling_type)
                logger.notice(f"end_to_end_test {n, modeling_type_name} passed")
            except Exception as e:
                logger.notice(
                    f"end_to_end_test {n, modeling_type_name} failed with an error on line {inspect.currentframe().f_lineno}:"
                )
                logger.notice(f"Error type: {type(e).__name__}")
                logger.notice(f"Error message: {traceback.format_exc()}")
                error_info.add_error(modeling_type, e, n)
        else:
            execute_test(modeling_type)

    return error_info


def run_single_end_to_end_test(
    test_type: ModelingType,
    config_path: str,
    estimator_list: Optional[List[EstimatorType]] = None,
    verbose: int = DEFAULT_VALUES["verbose"],
    n_jobs: int = 1,
    n_samples: int = 100,
    n_features: int = 10,
    top_n_based=5,
    top_n_stacked=[2, 3],
    scale=True,
    add_features=True,
    remove_features=True,
    downcast=True,
    maximize_scoring=True,
    timeout_duration: Optional[int] = None,
    log_file_path: Optional[str] = None,
    **component_service_kwargs,
) -> Tuple[MultiEstimatorPipeline, MultiEstimatorPipeline]:
    """
    This function is used to test the whole program. It is not meant to be run as a script, but rather as a test.

    Parameters
    ----------
    test_type : ModelingType
        The type of test to run. Can be either REGRESSION, CLASSIFICATION or TIMESERIES.

    config_path : str
        The path to the config file.

    estimator_list : Optional[List[EstimatorType]], optional
        Extra estimators to add to the list of estimators to test. If None, the default list of estimators will be used.

    verbose : int, optional
        The verbosity level. Defaults to 3.

    n_jobs : int, optional
        The number of jobs to run in parallel. Defaults to 1.

    n_samples : int
        The number of samples to use in the test. Defaults to 100.

    n_features : int
        The number of features to use in the test. Defaults to 10.

    top_n_based : int
        The number of best scoring estimators to use in the "base" generation pipeline. Defaults to 5.

    top_n_stacked : List[int]
        The range of best scoring estimators to use in the "stacked" generation pipeline. Defaults to [2, 3].

    scale : bool
        Whether to scale the data or not. Defaults to True.

    add_features : bool
        Whether to add features or not. Defaults to True.

    remove_features : bool
        Whether to remove features or not. Defaults to True.

    downcast : bool
        Whether to downcast the data or not. Defaults to True.

    maximize_scoring : bool
        Whether to maximize the scoring function or not. Defaults to True.

    timeout_duration : Optional[int], optional
        Timeout duration during component_service.generate_pipeline_for_base_models and
        component_service.generate_pipeline_for_stacked_models.
        Used if fitting causes hanging. Defaults to None.

    log_file_path : Optional[str], optional
        Path to the log file. Defaults to None.

    Returns
    -------
    bool
        True if the test was successful, False otherwise.

    """

    if test_type == ModelingType.CLASSIFICATION:
        X, y = get_testdata(regression=False, n_samples=n_samples, n_features=n_features)
        scoring = accuracy_score
    elif test_type == ModelingType.REGRESSION:
        X, y = get_testdata(regression=True, n_samples=n_samples, n_features=n_features)
        scoring = r2_score
    elif test_type == ModelingType.CLASSIFICATION_TIMESERIES:
        X, y = get_testdata_timeseries(n_samples=n_samples, n_features=n_features, is_regression=False)
        scoring = accuracy_score
    elif test_type == ModelingType.REGRESSION_TIMESERIES:
        X, y = get_testdata_timeseries(n_samples=n_samples, n_features=n_features, is_regression=True)
        scoring = r2_score
    else:
        raise ValueError(f"test_type {test_type} is not supported")

    IS_REGRESSION = test_type in {ModelingType.REGRESSION, ModelingType.REGRESSION_TIMESERIES}

    X_train, X_test, X_val, y_train, y_test, y_val = PreparatorService.split_data(
        X=X, y=y, test_size=0.2, val_size=0.2, random_state=42
    )

    cv_obj = model_selection.ShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    component_service = ComponentService(
        X_train,
        X_test,
        y_train,
        y_test,
        cv_obj,
        config_path=config_path,
        verbose=verbose,
        n_jobs=n_jobs,
        estimator_list=estimator_list,
        scoring=scoring,
        maximize_scoring=maximize_scoring,
        log_file_path=log_file_path,
        **component_service_kwargs,
    )
    component_service.initialize(
        scale=scale,
        add_features=add_features,
        remove_features=remove_features,
        downcast=downcast,
    )

    # Test if the pipelines work
    pipeline_base = component_service.generate_pipeline_for_base_models(
        top_n_per_tuner=top_n_based, timeout_duration=timeout_duration
    )
    assert pipeline_base.generation == "base"
    pipeline_stacked = component_service.generate_pipeline_for_stacked_models(
        top_n_per_tuner_range=top_n_stacked, timeout_duration=timeout_duration
    )
    assert pipeline_stacked.generation == "stacked"
    evolver = PipelineEvolverService(pipeline_stacked)
    pipeline_evolved = evolver.evolve_voting(voting="hard" if IS_REGRESSION else "soft")
    assert pipeline_evolved.generation == "evolved"
    pipeline_evolved.fit(X_train, y_train)

    pass_pipelines_for_testing(
        IS_REGRESSION,
        X_train,
        X_test,
        y_test,
        X_val,
        y_val,
        pipeline_base,
        pipeline_stacked,
        pipeline_evolved,
    )

    logger.notice("testing PipelineOrchestrator")
    results = test_pipeline_orchestrator(
        X=X_test,
        y=y_test,
        metric=scoring,
        config_path=config_path,
        verbose=verbose,
        n_jobs=n_jobs,
        shuffle=False,
        stratify=False,
        ensemble_size=0.2,
        validation_size=0.2,
        scale=scale,
        add_features=add_features,
        remove_features=remove_features,
        log_file_path=log_file_path,
    )

    for key, value in results.items():
        logger.notice(f"{key}:\n{value}")


def generate_random_column_names(num_cols):
    """
    Generates unique random alphabetic column names up to 8 letters long.

    Args:
        num_cols (int): The number of column names to generate.

    Returns:
        A list of random column names.
    """
    names = set()
    while len(names) < num_cols:
        name = "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 8)))
        names.add(name)
    return list(names)


def get_testdata(regression=False, n_samples=100, n_features=20, random_state=0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate a testset of data for classification or regression."""
    data = (
        make_regression(n_samples, n_features, random_state=random_state)
        if regression
        else make_classification(n_samples, n_features, random_state=random_state)
    )
    X = pd.DataFrame(data[0])
    X.columns = generate_random_column_names(X.shape[1])
    y = pd.Series(data[1])

    return X, y


def get_testdata_timeseries(
    n_samples: int, n_features: int, is_regression: bool = False, random_state: int = 0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Produce a testset of timeseries data with a specified number of samples and features."""
    rng = np.random.default_rng(random_state)  # create a Generator instance with the specified random state

    date_rng = pd.date_range(start="1/1/2021", periods=n_samples, freq="H")

    X = pd.DataFrame(date_rng, columns=["date"])
    for i in range(1, n_features + 1):
        X[f"feature_{i}"] = rng.integers(0, 100, size=n_samples)

    if is_regression:
        y = pd.Series(X["feature_1"] + rng.normal(0, 1, size=n_samples))  # continuous values
    else:
        y = pd.Series((X["feature_1"] > 50).astype(int))  # binary classification

    X.set_index("date", inplace=True)
    X.index.name = None

    return X, y


def get_current_cest_time() -> str:
    """Get the current time in UTC"""
    current_utc_time = datetime.datetime.utcnow()

    # Calculate the CEST time offset (UTC+2) and add it to the current UTC time
    cest_offset = datetime.timedelta(hours=2)
    current_cest_time = current_utc_time + cest_offset
    return current_cest_time.strftime("%Y-%m-%d %H:%M:%S")


def test_pipeline_orchestrator(
    X: pd.DataFrame,
    y: pd.Series,
    metric: Union[accuracy_score, r2_score],
    config_path: str,
    verbose: int,
    n_jobs: int,
    shuffle: bool,
    stratify: bool,
    ensemble_size: Union[int, float],
    validation_size: Union[int, float],
    scale: bool,
    add_features: bool,
    remove_features: bool,
    log_file_path: Optional[str],
) -> dict:
    """Test the PipelineOrchestrator class as part of the end-to-end tests."""
    orchestrator = PipelineOrchestrator(
        X,
        y,
        metric=metric,
        config_path=config_path,
        verbose=verbose,
        n_jobs=n_jobs,
        shuffle=shuffle,
        stratify=stratify,
        ensemble_size=ensemble_size,
        validation_size=validation_size,
        log_file_path=log_file_path,
    )

    pipe_dict = (
        orchestrator.pre_optimize(max_splits=2).build(
            scale=scale,
            add_features=add_features,
            remove_features=remove_features,
            generations=["base", "stacked", "evolved"],
        )
        # .refit_pipelines()
        .fortify(
            optimize_n_jobs=False,
            threshold_score=0.50,
            fraction_to_explain=0.1,
        )
    )

    base_score = orchestrator.pipelines["base"].score(orchestrator.X_test, orchestrator.y_test)
    base_predict = orchestrator.pipelines["base"].predict(orchestrator.X_test, n_jobs=2)
    base_predict_proba = orchestrator.pipelines["base"].predict_proba(orchestrator.X_test, transform_discrete=True)

    stacked_score = orchestrator.pipelines["stacked"].score(orchestrator.X_test, orchestrator.y_test)
    stacked_predict = orchestrator.pipelines["stacked"].predict(orchestrator.X_test, n_jobs=2)
    stacked_predict_proba = orchestrator.pipelines["stacked"].predict_proba(
        orchestrator.X_test, transform_discrete=True
    )

    explained_features = orchestrator.get_explained_features()

    return {
        "pipeline_base_score": base_score,
        "pipeline_base_predict": base_predict,
        "pipeline_base_predict_proba": base_predict_proba,
        "pipeline_stacked_score": stacked_score,
        "pipeline_stacked_predict": stacked_predict,
        "pipeline_stacked_predict_proba": stacked_predict_proba,
        "explained_features": explained_features,
    }
