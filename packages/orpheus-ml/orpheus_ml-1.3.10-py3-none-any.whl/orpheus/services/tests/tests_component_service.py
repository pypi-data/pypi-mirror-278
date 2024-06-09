"""Create a test suite for the component service"""


import numpy as np
import pandas as pd

from orpheus.services.component_service import ComponentService
from orpheus.services.utils.private_functions import _create_preprocessing_pipeline
from orpheus.test_utils.stubs import get_cv_obj, get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from tests.config.test_configurations import CONFIG


class TestsComponentService(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(random_state=0, is_regression=False)
        self.type_estimator = "classifier"
        self.estimator_list = get_estimator_list(random_state=0, is_regression=False)
        self.cv_obj = get_cv_obj()
        self.config_path = CONFIG["CONFIG_PATH"]
        # self.config_path = ""

    def tearDown(self):
        """Clean up the objects after running the test"""
        del self.X_train
        del self.X_test
        del self.y_train
        del self.y_test
        del self.type_estimator
        del self.estimator_list
        del self.cv_obj

    def test_CreatePreprocessingPipeline_ScalerShouldNotAlterBinaryColumns(self):
        self.X_train = pd.DataFrame(
            {
                "binary1": [0, 1, 1, 0, 1],
                "binary2": [1, 1, 0, 0, 1],
                "num1": [1.1, 2.2, 3.3, 4.4, 5.5],
                "num2": [6.1, 7.1, 8.2, 9.3, 10.4],
            }
        )
        self.y_train = pd.Series([0, 1, 0, 1, 1])

        pipeline, X_transformed = _create_preprocessing_pipeline(
            self.X_train,
            self.y_train,
            self.cv_obj,
            downcast=False,
            scale=True,
            add_features=False,
            remove_features=False,
            return_X=True,
            type_estimator=self.type_estimator,
            estimator_list=self.estimator_list,
        )

        # Verify that binary columns are included in the output and not scaled
        self.assertTrue("binary1" in X_transformed.columns)
        self.assertTrue("binary2" in X_transformed.columns)
        self.assertTrue(np.array_equal(self.X_train["binary1"], X_transformed["binary1"]))
        self.assertTrue(np.array_equal(self.X_train["binary2"], X_transformed["binary2"]))

    def test_DataIsNonNumerical_ShouldRaiseAssertionError(self):
        # arrange
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(
            random_state=0, is_regression=False, n_categorical_features=2
        )

        # act/assert
        with self.assertRaises(AssertionError):
            ComponentService(
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test,
                cv_obj=self.cv_obj,
                type_estimator=self.type_estimator,
                estimator_list=self.estimator_list,
                config_path=self.config_path,
            )

    def test_DataIsNonNumerical_ShouldPassIfCategoricalFeaturesArePassed(self):
        # Arrange
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(
            random_state=0, is_regression=False, n_categorical_features=2
        )
        categorical_features = ["col1", "col2"]

        # Act
        try:
            result = ComponentService(
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test,
                cv_obj=self.cv_obj,
                config_path=self.config_path,
                type_estimator=self.type_estimator,
                estimator_list=self.estimator_list,
                categorical_features=categorical_features,
            )
            exception_occurred = False
            exception_message = ""
        except Exception as e:
            exception_occurred = True
            exception_message = str(e)

        # Assert
        self.assertFalse(
            exception_occurred,
            f"ComponentService should not raise an exception for non-numerical data. Exception: {exception_message}",
        )
        # Assert
        self.assertFalse(exception_occurred, "ComponentService should not raise an exception for non-numerical data")
