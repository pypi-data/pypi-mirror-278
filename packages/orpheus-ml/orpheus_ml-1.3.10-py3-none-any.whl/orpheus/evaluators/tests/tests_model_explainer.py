"""Tests for ModelExplainer class."""

from unittest.mock import patch
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.evaluators.model_explainer import ModelExplainer


class TestsModelExplainer(TestCaseBase):
    """Tests for ModelExplainer class."""

    def setUp(self):
        """Initialize objects for testing."""
        self.X_train = pd.DataFrame({"feature_1": [0.1, 0.2, 0.3, 0.4, 0.5], "feature_2": [1, 2, 3, 4, 5]})
        self.y_train = pd.Series([0, 1, 0, 1, 1])
        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)
        self.class_names = ["class_0", "class_1"]
        self.mode = "classification"
        self.explainer = ModelExplainer(self.model, self.X_train, self.mode, self.class_names)

    def tearDown(self):
        """Clean up the objects after running the test."""

    def test_Init_ValidInput_ObjectCreated(self):
        """Test if ModelExplainer object is created with valid inputs."""
        self.assertEqual(self.explainer.model, self.model)
        self.assertTrue((self.explainer.train_data == self.X_train.to_numpy()).all())
        self.assertEqual(self.explainer.feature_names, list(self.X_train.columns))
        self.assertEqual(self.explainer.class_names, self.class_names)
        self.assertEqual(self.explainer.mode, self.mode)

    def test_Repr_ObjectCreated_ReprString(self):
        """Test if __repr__ method returns the expected representation string."""
        expected_repr = f"ModelExplainer(model={self.model}, train_data={self.X_train.to_numpy()}, feature_names={list(self.X_train.columns)}, class_names={self.class_names}, mode={self.mode})"
        self.assertEqual(str(self.explainer), expected_repr)

    @patch("matplotlib.pyplot.show")
    def test_ExplainSample_ValidInput_ExplanationReturned(self, mock_show):
        """Test if explain_sample method returns valid explanation."""
        sample = self.X_train.iloc[0]
        explanation = self.explainer.explain_sample(sample, num_features=2, plot=True)
        self.assertIsNotNone(explanation)
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    def test_ExplainAll_ValidInput_DataFrameReturned(self, mock_show):
        """Test if explain_all method returns a valid DataFrame."""
        df = self.explainer.explain_all(self.X_train, fraction=1.0, plot=True)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape[0], self.X_train.shape[0])
        mock_show.assert_called_once()

    def test_InvalidMode_InvalidMode_ExceptionRaised(self):
        """Test if an invalid mode raises a ValueError."""
        with self.assertRaises(ValueError):
            ModelExplainer(self.model, self.X_train, "invalid_mode")

    def test_InvalidSampleType_InvalidInput_ExceptionRaised(self):
        """Test if an invalid sample type raises a ValueError."""
        with self.assertRaises(ValueError):
            self.explainer.explain_sample(np.array([0.1, 1]), num_features=2)
