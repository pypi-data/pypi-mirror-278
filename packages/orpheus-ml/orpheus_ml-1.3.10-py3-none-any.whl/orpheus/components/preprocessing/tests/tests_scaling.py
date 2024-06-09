"""Tests for scaling.py."""

from unittest.mock import MagicMock

import numpy as np
import sklearn
from sklearn.metrics import accuracy_score

from orpheus.components.hypertuner.hypertuner import HyperTuner
from orpheus.components.preprocessing.scaling import Scaling
from orpheus.services.utils.private_functions import _get_best_scaler
from orpheus.test_utils.stubs import get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.utils.type_vars import ScalerType


class TestsScaling(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""
        estimator_list = get_estimator_list(random_state=0)
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(random_state=0, is_regression=False)

        self.scaler_obj = Scaling(
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test,
            scoring=accuracy_score,
            maximize_scoring=True,
            num_workers=2,
            estimator_list=estimator_list,
        )

    def tearDown(self):
        """Clean up the objects after running the test"""
        self.scaler_obj = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def test_Scale_TransformWholeArray_ScalerAppliedCorrectly(self):
        # arrange
        tuner = MagicMock(spec=HyperTuner)
        tuner.maximize_scoring = True

        # act
        scaler_scores = self.scaler_obj.scale(timeout=90, compare_to_unscaled_data=False)
        scaler: ScalerType = _get_best_scaler(
            scaler_scores=scaler_scores,
            scaler_obj=self.scaler_obj,
            columns_are_passed=None,
        )
        X_train_scaled = scaler.fit_transform(self.scaler_obj.X_train)

        # assert
        self.assertTrue(hasattr(scaler, "transform"))
        self.assertTrue(hasattr(scaler, "fit_transform"))
        self.assertEqual(self.scaler_obj.X_train.shape, X_train_scaled.shape)

        # Check if means and standard deviations are different after scaling
        original_means = self.scaler_obj.X_train.mean(axis=0)
        scaled_means = X_train_scaled.mean(axis=0)
        original_stds = self.scaler_obj.X_train.std(axis=0)
        scaled_stds = X_train_scaled.std(axis=0)

        self.assertFalse(np.allclose(original_means, scaled_means))
        self.assertFalse(np.allclose(original_stds, scaled_stds))

    def test_Scale_TransformMultipleFeaturesInArray_ShouldBeRightTypeInAllLayers(self):
        # arrange
        columns_to_scale = [["col1", "col2"], ["col3", "col4"]]

        # act
        score_dict = self.scaler_obj.scale(columns_to_scale=columns_to_scale, timeout=90)

        # assert
        self.assertIsInstance(score_dict, dict)
        self.assertEqual(len(score_dict), len(columns_to_scale))

        # Access the first element of columns_to_scale and convert to a hashable type if necessary
        column_key = tuple(columns_to_scale[0]) if isinstance(columns_to_scale[0], list) else columns_to_scale[0]

        for key in score_dict[column_key].keys():
            self.assertIsInstance(key, (sklearn.base.BaseEstimator, type(None)))

        for value in score_dict[column_key].values():
            self.assertIsInstance(value, dict)

        for inner_val in list(score_dict[column_key].values())[0].values():
            self.assertIsInstance(inner_val, float)
