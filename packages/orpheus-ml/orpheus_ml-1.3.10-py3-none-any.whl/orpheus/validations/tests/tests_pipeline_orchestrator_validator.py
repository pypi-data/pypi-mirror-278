import numpy as np
import pandas as pd

from orpheus.validations.pipeline_orchestrator_validator import PipelineOrchestratorValidator
from orpheus.test_utils.testcase_base import TestCaseBase


class TestsPipelineOrchestratorValidator(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""

    def tearDown(self):
        """Clean up the objects after running the test"""

    def test_ValidateParameters_InvalidTypes_ShouldRaiseTypeError(self):
        """Test that passing invalid X and y arguments raises a ValueError"""
        invalid_X_values = [np.array([1, 2, 3]), None, 88.66]
        invalid_y_values = [np.array([1, 2, 3]), None, 4]

        for X in invalid_X_values:
            for y in invalid_y_values:
                with self.assertRaises(TypeError):
                    PipelineOrchestratorValidator.validate_parameters(X, y, ensemble_size=0.2, validation_size=0.2, verbose=0)

    def test_ValidateParameters_InvalidArguments_ShouldRaiseValueError(self):
        """Test that passing invalid X and y arguments raises a ValueError"""
        invalid_X_values = [pd.DataFrame()]
        invalid_y_values = [pd.Series()]

        for X in invalid_X_values:
            for y in invalid_y_values:
                with self.assertRaises(ValueError, msg=f"ValueError not raised for X={X} and y={y}"):
                    PipelineOrchestratorValidator.validate_parameters(
                        X, y, ensemble_size=0.2, validation_size=0.2, verbose=0
                    )
