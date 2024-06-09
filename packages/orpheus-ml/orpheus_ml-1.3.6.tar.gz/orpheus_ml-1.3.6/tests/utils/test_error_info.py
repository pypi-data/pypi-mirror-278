"""Test error info class, which stores information about errors that occur during end-to-end tests."""

import traceback

from tests.config.test_configurations import CONFIG
from tests.utils.modeling_type import ModelingType

from src.orpheus.utils.logger import logger

class EndToEndTestEstimatorErrorInfo:
    def __init__(self):
        self.error_list = []

    def add_error(self, model_type: ModelingType, error: Exception, iteration: int):
        error_traceback = traceback.format_exc()

        error_info = {"model_type": model_type, "error": error, "iteration": iteration, "traceback": error_traceback}
        self.error_list.append(error_info)

    def display_results(self):
        succesful_trials = CONFIG["TRIALS"] - len(self.error_list)
        logger.notice(f"succesful end-to-end trials: {succesful_trials}/{CONFIG['TRIALS']}")
        for index, error_info in enumerate(self.error_list, start=1):
            logger.notice(f"Error {index}:")
            logger.notice(f"  Model Type: {error_info['model_type']}")
            logger.notice(f"  Iteration: {error_info['iteration']}")
            logger.notice(f"  Error: {type(error_info['error']).__name__}")
            logger.notice(f"  Traceback: {error_info['traceback']}")

    def get_error_count(self):
        return len(self.error_list)
