"""Tests for Evaluator class."""

from unittest.mock import patch, Mock
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, r2_score
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.evaluators.evaluator import Evaluator


class TestsEvaluator(TestCaseBase):
    """Tests for Evaluator class."""

    def setUp(self):
        """Initialize objects for testing."""

    def tearDown(self):
        """Clean up the objects after running the test."""

    def test_Init_ValidInput_ObjectCreated(self):
        """Test if Evaluator object is created with valid inputs."""
        metric = accuracy_score
        evaluator = Evaluator(metric)
        self.assertEqual(evaluator.name, "accuracy_score")

    def test_EvaluatePerformance_ValidInput_PerformanceEvaluated(self):
        """Test if evaluate_performance method returns valid performance."""
        metric = accuracy_score
        evaluator = Evaluator(metric)
        y_true = np.array([1, 0, 0])
        y_pred = np.array([[1, 0, 1]])
        result = np.round(evaluator.evaluate_performance(y_true, y_pred), 3)
        expected_result = pd.Series({0: 0.667})
        self.assertEqual(result[0], expected_result[0])

    @patch("orpheus.evaluators.model_evaluators.ClassificationEvaluator")
    def test_EvaluateRobustnessClassifier_ValidInput_EvaluationReturned(self, mock_ClassificationEvaluator):
        """Test if evaluate_robustness method returns valid evaluation for classifier."""
        metric = accuracy_score
        evaluator = Evaluator(metric)
        mock_ClassificationEvaluator_instance = Mock()
        mock_ClassificationEvaluator.return_value = mock_ClassificationEvaluator_instance
        mock_ClassificationEvaluator_instance.evaluate_classifier.return_value = [0, 1]

        evaluator.type_estimator = "classifier"
        pipeline = Mock()
        pipeline.predict.return_value = np.array([[0, 1], [1, 0]])
        X_val = np.array([[1, 2], [2, 3]])
        y_val = np.array([0, 1])

        result = evaluator.evaluate_robustness(X_val, y_val, pipeline)
        self.assertEqual(result, [0, 1])

    def test_EvaluateRobustnessRegressor_ValidInput_EvaluationReturnedWithoutRobustIndexes(self):
        """Test if evaluate_robustness method returns valid evaluation for regressor."""
        metric = r2_score
        evaluator = Evaluator(metric)  # Assuming Evaluator is your class
        evaluator.type_estimator = "regressor"

        pipeline = Mock()
        pipeline.predict.return_value = np.array([[0, 1], [1, 0]])
        X_val = np.array([[1, 2], [2, 3]])
        y_val = np.array([0, 1])  # matches index 0 of pipeline.predict, so we expect [0]

        result = evaluator.evaluate_robustness(X_val, y_val, pipeline)
        self.assertEqual(result, [0])
