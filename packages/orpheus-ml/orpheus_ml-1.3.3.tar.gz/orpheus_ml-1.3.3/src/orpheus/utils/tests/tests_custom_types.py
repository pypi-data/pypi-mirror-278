"""Tests for custom_types.py."""


import pandas as pd
import numpy as np
from sklearn.exceptions import NotFittedError

from orpheus.utils.custom_types import PreprocessTransformerChainerX
from orpheus.services.additional_types.multi_estimator_pipeline import (
    MultiEstimatorPipeline,
)
from sklearn.metrics import accuracy_score
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.test_utils.stubs import get_X_y_train_test


def log_transform(X: pd.DataFrame) -> pd.DataFrame:
    """log transform X"""
    X = np.log(X)
    return X


def reduce_columns(X: pd.DataFrame) -> pd.DataFrame:
    """reduce number of columns"""
    X = X.iloc[:, 0:3]
    return X


def change_dtype_columns(X: pd.DataFrame) -> pd.DataFrame:
    """change dtype of columns"""
    X = X.astype("float32")
    return X


class TestsCustomTypes(TestCaseBase):
    def setUp(self):
        """initialize objects for testing"""
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(is_regression=False)
        self.transformer_chain = [log_transform, reduce_columns, change_dtype_columns]
        self.preprocess_transformer_chainer = PreprocessTransformerChainerX(self.transformer_chain)
        self.metric = accuracy_score

    def tearDown(self):
        """clean up the objects after running the test"""
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.transformer_chain = None
        self.preprocess_transformer_chainer = None

    def test_PreprocessTransformerChainerX_CallTransformOnData_ShouldThrowRuntimeError(self):
        # act and assert
        self.assertFalse(self.preprocess_transformer_chainer.is_fitted)
        with self.assertRaises(NotFittedError):
            self.preprocess_transformer_chainer.transform(self.X_train)

    def test_PreprocessTransformerChainerX_FitTransformXTrain_TransformXTestShouldHaveSameProperties(
        self,
    ):
        # act
        X_train_transformed = self.preprocess_transformer_chainer.fit_transform(self.X_train)
        X_test_transformed = self.preprocess_transformer_chainer.transform(self.X_test)

        # assert
        self.assertEqual(X_train_transformed.shape[1], X_test_transformed.shape[1])
        self.assertEqual(X_train_transformed.columns.tolist(), X_test_transformed.columns.tolist())
        self.assertEqual(X_train_transformed.dtypes.tolist(), X_test_transformed.dtypes.tolist())
        self.assertTrue(self.preprocess_transformer_chainer.is_fitted)

    def test_PreprocessTransformerChainerX_FitTransformXTrainWithtransformerWhichDoesNothing_ShouldRaiseRuntimeError(
        self,
    ):
        # act
        transformer_which_does_nothing = lambda X: X
        transformer_chain = [log_transform, reduce_columns, transformer_which_does_nothing]
        self.preprocess_transformer_chainer.transformers = transformer_chain

        # assert
        with self.assertRaises(RuntimeError):
            self.preprocess_transformer_chainer.fit_transform(self.X_train)
        self.assertTrue(self.preprocess_transformer_chainer.is_fitted)

    def test_PreprocessTransformerChainerX_Fittransformers_IsFittedIsTrue(self):
        # act
        self.preprocess_transformer_chainer.fit(self.X_train)

        # assert
        self.assertTrue(self.preprocess_transformer_chainer.is_fitted)

    def test_PreprocessTransformerChainerX_PassEmptyList_ShouldRaiseTypeError(self):
        # act and assert
        with self.assertRaises(TypeError):
            self.preprocess_transformer_chainer.transformers = []
        self.assertFalse(self.preprocess_transformer_chainer.is_fitted)

    def test_PreprocessTransformerChainerX_FitListWithCallablesAndNone_ShouldRaiseTypeError(
        self,
    ):
        # act and assert
        transformer_chain = [log_transform, reduce_columns, change_dtype_columns, None]
        with self.assertRaises(TypeError):
            self.preprocess_transformer_chainer.transformers = transformer_chain
        self.assertFalse(self.preprocess_transformer_chainer.is_fitted)

    def test_PreprocessTransformerChainerX_MetadataUpdatedCorrectly(self):
        # act
        self.preprocess_transformer_chainer.fit_transform(self.X_train)

        # assert
        self.assertIn("input", self.preprocess_transformer_chainer.metadata)
        self.assertIn("log_transform", self.preprocess_transformer_chainer.metadata)
        self.assertIn("reduce_columns", self.preprocess_transformer_chainer.metadata)
        self.assertIn("change_dtype_columns", self.preprocess_transformer_chainer.metadata)

    def test_PreprocessTransformerChainerX_AddedToMultiEstimatorPipeline_XTestTransformedCorrectly(
        self,
    ):
        # act
        X_train_transformed = self.preprocess_transformer_chainer.fit_transform(self.X_train)
        pipeline = MultiEstimatorPipeline(
            [("preprocess", self.preprocess_transformer_chainer)],
            metric=self.metric,
            maximize_scoring=True,
            type_estimator="classifier",
        )
        X_test_transformed: pd.DataFrame = pipeline.transform(self.X_test)

        # assert
        self.assertEqual(X_train_transformed.shape[1], X_test_transformed.shape[1])
        self.assertEqual(X_train_transformed.columns.tolist(), X_test_transformed.columns.tolist())
        self.assertEqual(X_train_transformed.dtypes.tolist(), X_test_transformed.dtypes.tolist())
        self.assertTrue(pipeline.steps[0][1].is_fitted)
