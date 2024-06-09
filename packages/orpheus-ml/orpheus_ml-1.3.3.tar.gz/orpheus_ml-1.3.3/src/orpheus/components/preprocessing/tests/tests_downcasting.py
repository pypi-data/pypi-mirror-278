"""Tests for downcasting.py."""

import sys

import numpy as np

from orpheus.components.preprocessing.downcasting import Downcasting
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.test_utils.stubs import get_X_y_train_test


class TestsDowncasting(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(random_state=0, is_regression=False)

    def tearDown(self):
        """Clean up the objects after running the test"""
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def test_Downcast_DowncastNumpyArrays_NoPrecisionLost(self):
        # arrange
        decimalPlace = 6

        # act
        X_train_casted = Downcasting.downcast(self.X_train)
        X_test_casted = Downcasting.downcast(self.X_test)
        y_train_casted = Downcasting.downcast(self.y_train)
        y_test_casted = Downcasting.downcast(self.y_test)

        # assert
        np.testing.assert_array_almost_equal(X_train_casted, self.X_train, decimalPlace, "X_train_casted != X_train")
        np.testing.assert_array_almost_equal(X_test_casted, self.X_test, decimalPlace, "X_test_casted != X_test")
        np.testing.assert_array_almost_equal(y_train_casted, self.y_train, decimalPlace, "y_train_casted != y_train")
        np.testing.assert_array_almost_equal(y_test_casted, self.y_test, decimalPlace, "y_test_casted != y_test")

    def test_Downcast_DowncastDataFrames_NoPrecisionLost(self):
        # arrange
        decimalPlace = 6

        # act
        X_train_casted = Downcasting.downcast(self.X_train)
        X_test_casted = Downcasting.downcast(self.X_test)
        y_train_casted = Downcasting.downcast(self.y_train)
        y_test_casted = Downcasting.downcast(self.y_test)

        # assert
        np.testing.assert_array_almost_equal(X_train_casted, self.X_train, decimalPlace, "X_train_casted != X_train")
        np.testing.assert_array_almost_equal(X_test_casted, self.X_test, decimalPlace, "X_test_casted != X_test")
        np.testing.assert_array_almost_equal(y_train_casted, self.y_train, decimalPlace, "y_train_casted != y_train")
        np.testing.assert_array_almost_equal(y_test_casted, self.y_test, decimalPlace, "y_test_casted != y_test")

    def test_Downcast_DowncastWholeNumpyArrays_SizeCastedArraysIsSmaller(self):
        # act
        X_train_casted = Downcasting.downcast(self.X_train)
        X_test_casted = Downcasting.downcast(self.X_test)

        # assert
        casted = sys.getsizeof(X_train_casted)
        orig = sys.getsizeof(self.X_train)
        self.assertLess(
            casted,
            orig,
            f"X_train_casted is not smaller than X_train: {casted} vs {orig}",
        )

        casted = sys.getsizeof(X_test_casted)
        orig = sys.getsizeof(self.X_test)
        self.assertLess(
            sys.getsizeof(X_test_casted),
            sys.getsizeof(self.X_test),
            f"X_test_casted is not smaller than X_test: {casted} vs {orig}",
        )
