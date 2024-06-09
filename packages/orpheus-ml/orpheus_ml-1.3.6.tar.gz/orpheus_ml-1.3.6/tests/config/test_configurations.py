"""
Configuration file for the tests. This should be used as an entrypoint from run_tests.ps1.
Alternatively, use these default values if you run the script "tests/run_tests" directly, for example for debugging.

set the 'TRIALS' parameter to 0 if you want to run only unittests.
set the 'TRIALS' parameter to 4 if you want to run the end-to-end tests on all different modeling types of data.
"""
import os
from datetime import datetime

# logic for setting variables from run_tests.ps1
LOG_FILE_NAME = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
N_JOBS = max(1, int(os.cpu_count() / 2))
N_TRIALS = int(os.environ.get("N_TRIALS", 0))
ENABLE_LOGGING_AND_DISABLE_CONSOLE_OUTPUT = int(os.environ.get("ENABLE_LOGGING_AND_DISABLE_CONSOLE_OUTPUT", 0))
if ENABLE_LOGGING_AND_DISABLE_CONSOLE_OUTPUT:
    LOG_FILE_DIR = os.environ.get("LOG_FILE_DIR", None)
    if LOG_FILE_DIR is None:
        raise ValueError(
            "LOG_FILE_DIR must be set to a valid directory if ENABLE_LOGGING_AND_DISABLE_CONSOLE_OUTPUT is True"
        )
    TEST_LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)
else:
    TEST_LOG_FILE_PATH = None


CONFIG = {
    "CONFIG_PATH": "tests/config/test_config.yaml",
    "TRIALS": N_TRIALS,
    "VERBOSE": 3,
    "TEST_LOG_FILE_PATH": None,  # TEST_LOG_FILE_PATH,
    "N_JOBS": N_JOBS,
    "N_FEATURES": 10,
    "N_SAMPLES": 1000,
    "CATCH_AND_COLLECT_ERRORS": True,
    "SCALE": True,
    "ADD_FEATURES": True,
    "REMOVE_FEATURES": True,
    "TOP_N_BASED": 5,
    "TOP_N_STACKED": [2, 4],
}
