"""Tests for multi_estimator_pipeline.py."""

import io
from contextlib import redirect_stdout
import timeit
import unittest.mock as mock

import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.test_utils.stubs import get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.test_utils.helper_functions import arr_equality_msg
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.validations.estimators import is_estimator
from orpheus.services.additional_types.utils import MultiEstimatorPipelineScoreTracker

# due to the complexity of overhead in parallelization, we allow a tolerance of a given pct for the time measurements.
TIME_TOLERANCE_PCT = 0.01


class TestsMultiEstimatorPipeline(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""
        self.steps = [("scaler", StandardScaler()), ("estimators", LogisticRegression())]
        self.type_estimator = "classifier"
        self.metric = accuracy_score
        self.maximize_scoring = True
        self.estimator_list = get_estimator_list(random_state=0, is_regression=False)
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(random_state=0, is_regression=False)
        self.pipeline = MultiEstimatorPipeline(
            steps=self.steps,
            metric=self.metric,
            maximize_scoring=self.maximize_scoring,
            type_estimator=self.type_estimator,
            verbose=0,
        )

    def tearDown(self):
        """Clean up the objects after running the test"""
        self.steps = None
        self.type_estimator = None
        self.maximize_scoring = None
        self.estimator_list = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.pipeline.set_verbose(0)
        self.pipeline = None

    def test_SetEstimators_SetSingleEstimator_ShouldBeSuccesful(self):
        estimator = LogisticRegression()
        self.pipeline.estimators = estimator
        self.assertEqual(self.pipeline.estimators, [estimator])

    def test_SetEstimators_SetListOfEstimators_ShouldBeSuccesful(self):
        # arrange
        estimator_list = [LogisticRegression()]

        # act
        self.pipeline.estimators = estimator_list

        # assert
        self.assertEqual(self.pipeline.estimators, estimator_list)

    def test_SetEstimators_SetListOfEstimatorsWithTransformer_ShouldThrowValueError(self):
        # arrange
        estimator_list = self.estimator_list + [StandardScaler()]

        # assert
        with self.assertRaises(ValueError):
            self.pipeline.estimators = estimator_list

    def test_SetEstimators_SetNone_ShouldThrowValueError(self):
        with self.assertRaises(ValueError):
            self.pipeline.estimators = None

    def test_GetEstimators_EstimatorsIsNotMultiEstimatorWrapper_GetsTransformedInMultiEstimatorWrapper(self):
        self.assertIsInstance(self.pipeline.estimators, list)
        self.assertTrue(is_estimator(self.pipeline.estimators[0]))
        self.assertIsInstance(self.pipeline.steps[-1][1], MultiEstimatorWrapper)

    def test_SetVerbose_SetVerboseTo1_ShouldPrintSomethingToConsole(self):
        # arrange
        self.pipeline.set_verbose(1)

        # redirect stdout to a StringIO object
        with io.StringIO() as buf, redirect_stdout(buf):
            # act
            self.pipeline.fit(self.X_train, self.y_train)
            self.pipeline.predict(self.X_test)

            # assert
            self.assertNotEqual(buf.getvalue(), "")

    def test_SetVerbose_SetVerboseTo0_ShouldPrintNothingToConsole(self):
        # arrange
        self.pipeline.set_verbose(0)

        # redirect stdout to a StringIO object
        with io.StringIO() as buf, redirect_stdout(buf):
            # act
            self.pipeline.fit(self.X_train, self.y_train)
            self.pipeline.predict(self.X_test)

            # assert
            self.assertEqual(buf.getvalue(), "")

    def test_Score_MetricIsNotNone_ShouldUpdateScoresAndReturnScore(self):
        # arrange
        self.pipeline.metric = accuracy_score

        # act
        with mock.patch.object(self.pipeline, "update_scores") as mock_update_scores:
            self.pipeline.fit(self.X_train, self.y_train)
            scores = self.pipeline.score(self.X_test, self.y_test, update_scores=True)

            # assert
            self.assertIsInstance(scores, np.ndarray)
            self.assertIsInstance(scores[0], float)
            self.assertEqual(len(scores), len(self.pipeline.estimators))
            mock_update_scores.assert_called_once()

    def test_Score_MetricIsNone_ShouldRaiseTypeErrorThroughSetter(self):
        with self.assertRaises(TypeError):
            # act
            self.pipeline.metric = None

    def test_OptimizeNJobs_ExcludeNothing_SecondPredictionShouldBeFasterThanFirstPrediction(self):
        # arrange
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(
            n_samples=1000, n_features=50, random_state=0, is_regression=False
        )
        N_ITER = 50

        # act
        self.pipeline.fit(self.X_train, self.y_train)
        first_prediction = self.pipeline.predict(self.X_test)
        first_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)
        results = self.pipeline.optimize_n_jobs(self.X_train, n_iter=N_ITER, exclude=None)
        second_prediction = self.pipeline.predict(self.X_test)
        second_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)

        # assert
        tolerance = TIME_TOLERANCE_PCT  # adjust this to the desired tolerance level
        difference = second_prediction_time - first_prediction_time
        self.assertLessEqual(difference, tolerance, "results optimize_n_jobs: {}".format(results))
        self.assertTrue(
            np.array_equal(first_prediction, second_prediction),
            msg=arr_equality_msg(first_prediction, second_prediction),
        )

    def test_OptimizeNJobs_ExcludeTransformers_SecondPredictionShouldBeFasterThanFirstPrediction(self):
        # arrange
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(
            n_samples=1000, n_features=50, random_state=0, is_regression=False
        )
        N_ITER = 50

        # act
        self.pipeline.fit(self.X_train, self.y_train)
        first_prediction = self.pipeline.predict(self.X_test)
        first_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)
        results = self.pipeline.optimize_n_jobs(self.X_train, n_iter=N_ITER, exclude="transformers")
        second_prediction = self.pipeline.predict(self.X_test)
        second_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)

        # assert
        tolerance = TIME_TOLERANCE_PCT  # adjust this to the desired tolerance level
        difference = second_prediction_time - first_prediction_time
        self.assertLessEqual(difference, tolerance, "results optimize_n_jobs: {}".format(results))
        self.assertTrue(
            np.array_equal(first_prediction, second_prediction),
            msg=arr_equality_msg(first_prediction, second_prediction),
        )

    def test_OptimizeNJobs_ExcludeEstimators_SecondPredictionShouldBeFasterThanFirstPrediction(self):
        # arrange
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(
            n_samples=1000, n_features=50, random_state=0, is_regression=False
        )
        N_ITER = 50

        # act
        self.pipeline.fit(self.X_train, self.y_train)
        first_prediction = self.pipeline.predict(self.X_test)
        first_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)
        results = self.pipeline.optimize_n_jobs(self.X_train, n_iter=N_ITER, exclude="estimators")
        second_prediction = self.pipeline.predict(self.X_test)
        second_prediction_time = timeit.timeit(lambda: self.pipeline.predict(self.X_test), number=N_ITER)

        # assert
        tolerance = TIME_TOLERANCE_PCT  # adjust this to the desired tolerance level
        difference = second_prediction_time - first_prediction_time
        self.assertLessEqual(difference, tolerance, "results optimize_n_jobs: {}".format(results))
        self.assertTrue(
            np.array_equal(first_prediction.flatten(), second_prediction.flatten()),
            msg=arr_equality_msg(first_prediction, second_prediction),
        )

    def test_Score_XisDataFrameAndYIsSeries_ShouldReturnFloat(self):
        # act
        self.pipeline.fit(self.X_train, self.y_train)
        score = self.pipeline.score(self.X_test, self.y_test)

        # assert
        self.assertIsInstance(score, np.ndarray)
        self.assertIsInstance(score[0], float)

    def test_Score_XAndYAreScalars_ShouldReturnEmptyArray(self):
        # arrange
        self.pipeline.metric = accuracy_score

        # act
        self.pipeline.fit(self.X_train, self.y_train)

        # assert
        with self.assertRaises(ValueError):
            scores = self.pipeline.score(4, 5)

    def test_Init_TypeEstimatorIsNonValidWord_ShouldRaiseAttributeError(self):
        # arrange
        type_estimator = "non-valid-word"

        with self.assertRaises(AttributeError):
            # act
            self.pipeline.type_estimator = type_estimator

    def test_Init_AttributesAreInitializedProperly(self):
        # arrange
        type_estimator = "classifier"
        generation = None
        leakage_prevention_slice = [0, 0]
        train_data_mean = None
        test_data_mean = None

        # assert
        self.assertEqual(self.pipeline.type_estimator, type_estimator)
        self.assertEqual(self.pipeline._type_estimator, type_estimator)
        self.assertEqual(self.pipeline.generation, generation)
        self.assertIsInstance(self.pipeline._score_tracker, MultiEstimatorPipelineScoreTracker)
        self.assertEqual(self.pipeline.leakage_prevention_slice, leakage_prevention_slice)
        self.assertEqual(self.pipeline.train_data_mean, train_data_mean)
        self.assertEqual(self.pipeline.test_data_mean, test_data_mean)
