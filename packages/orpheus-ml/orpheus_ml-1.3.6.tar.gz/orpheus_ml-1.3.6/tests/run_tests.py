"""
run all tests in the project by running either 'test' or 'py tests/run_tests.py' in the shell.
Adjust the YAML CONFIG_PATH file to adjust the components.
Adjust 'test_configurations.py' to adjust the test settings.
If you want to run only unittests, set the 'TRIALS' parameter to 0.
"""

import sys
import time
import unittest
from typing import List

# THESE LINES ARE NECESSARY TO RUN THE SCRIPT:
sys.path.append(".")
sys.path.append("src")

from src.orpheus.components.preprocessing.tests.tests_downcasting import TestsDowncasting
from src.orpheus.components.preprocessing.tests.tests_feature_adding import TestsFeatureAdding
from src.orpheus.components.preprocessing.tests.tests_scaling import TestsScaling
from src.orpheus.evaluators.tests.tests_evaluator import TestsEvaluator
from src.orpheus.evaluators.tests.tests_model_explainer import TestsModelExplainer
from src.orpheus.orchestrator.data_transfer.tests.tests_pipeline_metadata import TestsPipelineMetadata
from src.orpheus.orchestrator.tests.tests_data_serializer import TestsDataSerializer
from src.orpheus.orchestrator.tests.tests_pipeline_orchestrator import TestsPipelineOrchestrator
from src.orpheus.repository.tests.tests_pipeline_orchestrator_proxy_repository import (
    TestsPipelineOrchestratorProxyRepository,
)
from src.orpheus.services.tests.tests_component_service import TestsComponentService
from src.orpheus.services.tests.tests_multi_estimator_pipeline import TestsMultiEstimatorPipeline
from src.orpheus.test_utils.testcase_base import TestCaseBase
from src.orpheus.utils.logger import logger
from src.orpheus.utils.tests.tests_logger import TestsColoredLogger
from src.orpheus.validations.tests.tests_input_checks import TestsAttributeValidation
from src.orpheus.validations.tests.tests_pipeline_orchestrator_validator import TestsPipelineOrchestratorValidator
from tests.config.test_configurations import CONFIG
from tests.utils.helper_functions import ModelingType, get_current_cest_time, run_multiple_end_to_end_tests

if __name__ == "__main__":
    log_file_path = CONFIG.get("TEST_LOG_FILE_PATH", None)
    logger.set_log_file(log_file_path)
    logger.set_verbose(CONFIG["VERBOSE"])

    logger.notice("Running tests...")
    start_time = time.time()
    logger.notice(f"started end-to-end tests at time { get_current_cest_time()}")
    logger.notice(f"total amount of end-to-end trials: {CONFIG['TRIALS']}")

    error_info = run_multiple_end_to_end_tests(
        scale=CONFIG["SCALE"],
        add_features=CONFIG["ADD_FEATURES"],
        remove_features=CONFIG["REMOVE_FEATURES"],
        modeling_types=[
            ModelingType.REGRESSION_TIMESERIES,
            ModelingType.CLASSIFICATION_TIMESERIES,
            ModelingType.REGRESSION,
            ModelingType.CLASSIFICATION,
        ],
        config_path=CONFIG["CONFIG_PATH"],
        trials=CONFIG["TRIALS"],
        verbose=CONFIG["VERBOSE"],
        n_jobs=CONFIG["N_JOBS"],
        n_features=CONFIG["N_FEATURES"],
        n_samples=CONFIG["N_SAMPLES"],
        top_n_based=CONFIG["TOP_N_BASED"],
        top_n_stacked=CONFIG["TOP_N_STACKED"],
        catch_and_collect_errors=CONFIG["CATCH_AND_COLLECT_ERRORS"],
        timeout_duration=None,
        log_file_path=log_file_path,
    )

    test_classes: List[TestCaseBase] = [
        TestsDowncasting,
        TestsScaling,
        TestsFeatureAdding,
        TestsComponentService,
        TestsPipelineOrchestrator,
        TestsPipelineOrchestratorValidator,
        TestsAttributeValidation,
        TestsMultiEstimatorPipeline,
        TestsDataSerializer,
        TestsColoredLogger,
        TestsPipelineMetadata,
        TestsPipelineOrchestratorProxyRepository,
        TestsModelExplainer,
        TestsEvaluator,
    ]

    total_tests = 0
    total_failures = 0

    # run unit- and integrationtests:
    for test_class in test_classes:
        test_class.set_log_file(log_file_path)
        result_tests: unittest.TestResult = test_class.run_tests()
        total_tests += result_tests.testsRun
        total_failures += len(result_tests.failures) + len(result_tests.errors)

    error_info.display_results()
    logger.notice(f"succesful unit-and-integrationtests: {total_tests - total_failures}/{total_tests}")
    logger.notice(f"finished end-to-end tests at time {get_current_cest_time()}")
    logger.notice(f"total time for all tests: {time.time() - start_time:.2f} seconds")
