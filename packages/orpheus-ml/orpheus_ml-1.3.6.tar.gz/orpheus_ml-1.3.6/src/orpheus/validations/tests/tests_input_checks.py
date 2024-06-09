from functools import partial
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from orpheus.test_utils.stubs import get_estimator_list
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.validations.input_checks import AttributeValidation


class TestsAttributeValidation(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""

    def tearDown(self):
        """Clean up the objects after running the test"""

    def test_ValidateTypeEstimator_WhenTypeEstimatorIsRegressor_ReturnsTrue(self):
        # Arrange
        type_estimator = "regressor"

        # Act/Assert
        self.assertIsNone(AttributeValidation.validate_type_estimator(type_estimator))

    def test_ValidateTypeEstimator_WhenTypeEstimatorIsIncorrect_RaiseValueError(self):
        # Arrange
        type_estimator = "some_value"

        # Act/Assert
        with self.assertRaises(ValueError):
            AttributeValidation.validate_type_estimator(type_estimator)

    def test_ValidateEstimatorList_WhenEstimatorContainsUninstantiatedEstimatorsAndPartial_ReturnsTrue(self):
        # Arrange
        estimator_list = get_estimator_list(is_regression=False)
        new_estimators = [
            partial(RandomForestClassifier, n_estimators=100, criterion="gini"),
            partial(RandomForestClassifier, n_estimators=100, criterion="entropy"),
        ]

        estimator_list.extend(new_estimators)

        # Act/Assert
        self.assertIsNone(AttributeValidation.validate_estimator_list(estimator_list))

    def test_ValidateEstimatorList_WhenEstimatorListContainsRandomValue_RaiseTypeError(self):
        # Arrange
        estimator_list = ["some_value"]

        # Act/Assert
        with self.assertRaises(TypeError):
            AttributeValidation.validate_estimator_list(estimator_list)

    def test_ValidateEstimatorList_WhenEstimatorListContainsInstantietedEstimator_RaiseTypeError(self):
        # Arrange
        estimator_list = [RandomForestClassifier()]

        # Act/Assert
        with self.assertRaises(TypeError):
            AttributeValidation.validate_estimator_list(estimator_list)

    def test_ValidateExcludeEstimators_WhenAllStringsInList_ReturnsTrue(self):
        # Arrange
        exclude_estimators = ["RandomForest", "SVM", "LogisticRegression"]

        # Act/Assert
        self.assertIsNone(AttributeValidation.validate_exclude_estimators(exclude_estimators))

    def test_ValidateExcludeEstimators_WhenNonStringInList_RaisesTypeError(self):
        # Arrange
        exclude_estimators = ["RandomForest", "SVM", 1]

        # Act/Assert
        with self.assertRaises(TypeError):
            AttributeValidation.validate_exclude_estimators(exclude_estimators)

    def test_ValidateCategoricalFeatures_WhenAllStringsInListAndInDF_ReturnsTrue(self):
        # Arrange
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
        features = ["A", "B"]

        # Act/Assert
        self.assertIsNone(AttributeValidation.validate_categorical_features(df, features))

    def test_ValidateCategoricalFeatures_WhenNonStringInList_RaisesTypeError(self):
        # Arrange
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
        features = ["A", 1]

        # Act/Assert
        with self.assertRaises(TypeError):
            AttributeValidation.validate_categorical_features(df, features)

    def test_ValidateCategoricalFeatures_WhenFeatureNotInDF_RaisesValueError(self):
        # Arrange
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
        features = ["A", "Z"]

        # Act/Assert
        with self.assertRaises(ValueError):
            AttributeValidation.validate_categorical_features(df, features)

    def test_ValidateOrdinalFeatures_WhenAllValid_ReturnsTrue(self):
        # Arrange
        df = pd.DataFrame({"A": ["a", "b"], "B": ["x", "y"]})
        ordinal_features = {"A": ["a", "b"], "B": ["x", "y"]}

        # Act/Assert
        self.assertIsNone(AttributeValidation.validate_ordinal_features(df, ordinal_features))

    def test_ValidateOrdinalFeatures_WhenNonStringKeyInDict_RaisesTypeError(self):
        # Arrange
        df = pd.DataFrame({"A": ["a", "b"], "B": ["x", "y"]})
        ordinal_features = {1: ["a", "b"], "B": ["x", "y"]}

        # Act/Assert
        with self.assertRaises(TypeError):
            AttributeValidation.validate_ordinal_features(df, ordinal_features)

    def test_ValidateOrdinalFeatures_WhenFeatureNotInDF_RaisesValueError(self):
        # Arrange
        df = pd.DataFrame({"A": ["a", "b"], "B": ["x", "y"]})
        ordinal_features = {"A": ["a", "b"], "Z": ["x", "y"]}

        # Act/Assert
        with self.assertRaises(ValueError):
            AttributeValidation.validate_ordinal_features(df, ordinal_features)

    def test_ValidateOrdinalFeatures_WhenValueNotInDFColumn_RaisesValueError(self):
        # Arrange
        df = pd.DataFrame({"A": ["a", "b"], "B": ["x", "y"]})
        ordinal_features = {"A": ["a", "b"], "B": ["x", "z"]}

        # Act/Assert
        with self.assertRaises(ValueError):
            AttributeValidation.validate_ordinal_features(df, ordinal_features)
