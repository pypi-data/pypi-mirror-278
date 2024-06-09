"""Tests for feature engineering module"""

import re

import pandas as pd

from orpheus.components.preprocessing.feature_adding import FeatureAdding
from orpheus.test_utils.stubs import get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase


class TestsFeatureAdding(TestCaseBase):
    """Tests for FeatureAdding class"""

    def setUp(self):
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(is_regression=False)
        self.feature_adding = FeatureAdding(self.y_train, type_estimator="classifier")

    def tearDown(self):
        self.feature_adding = None

    def test_AddLagsOrRollingStats_NonWorkableColumnsAreAddedAsAttributeThroughRegexPattern_ShouldPassOnAllFaultyColumnNames(
        self,
    ):
        """Test the Regex pattern for non-workable columns"""
        method = "lag"

        # arrange
        pattern = re.compile(rf".*_{method}_\d+$")
        data = {
            "valid_col_lag_1": [1, 2, 3],
            "valid_col_roll_2": [1, 2, 3],
            "invalid_col_something": [1, 2, 3],
            "valid_col_lag_10": [1, 2, 3],
        }

        df = pd.DataFrame(data)

        # act
        non_workable_columns = set(col for col in df.columns if pattern.match(col))

        # assert
        expected_non_workable_columns = {"valid_col_lag_1", "valid_col_lag_10"}
        self.assertEqual(
            non_workable_columns, expected_non_workable_columns, "Mismatch in columns identified as non-workable."
        )
