import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from tests.config.test_configurations import CONFIG

from orpheus.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.test_utils.stubs import get_X_y_train_test, get_estimator_list
from orpheus.utils.helper_functions import get_obj_name


class TestsPipelineOrchestrator(TestCaseBase):
    def setUp(self):
        """Initialize objects for testing"""
        self.X_train, self.X_test, self.y_train, self.y_test = get_X_y_train_test(random_state=0, is_regression=False)
        self.metric = accuracy_score
        self.config_path = CONFIG["CONFIG_PATH"]
        self.verbose = 0

    def tearDown(self):
        """Clean up the objects after running the test"""
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def test_Init_UnsplitXy_SplittedDataShouldMatchOriginalXy(self):
        # arrange
        orchestrator = PipelineOrchestrator(
            self.X_train, self.y_train, self.metric, self.config_path, verbose=self.verbose
        )
        X = pd.concat([orchestrator.X_train, orchestrator.X_test, orchestrator.X_val], axis=0)
        y = pd.concat([orchestrator.y_train, orchestrator.y_test, orchestrator.y_val], axis=0)

        # act
        self.assertTrue(np.array_equal(X, self.X_train))
        self.assertTrue(np.array_equal(y, self.y_train))

    def test_Init_SplitXy_SplitDataShouldMatchProvidedXy(self):
        # arrange
        X_train = self.X_train.iloc[:100]
        X_test = self.X_test.iloc[:50]
        X_val = self.X_test.iloc[:20]
        y_train = self.y_train.iloc[:100]
        y_test = self.y_test.iloc[:50]
        y_val = self.y_test.iloc[:20]

        # act
        orchestrator = PipelineOrchestrator(
            (X_train, X_test, X_val), (y_train, y_test, y_val), self.metric, self.config_path, verbose=self.verbose
        )

        # assert
        self.assertTrue(np.array_equal(orchestrator.X_train, X_train))
        self.assertTrue(np.array_equal(orchestrator.X_test, X_test))
        self.assertTrue(np.array_equal(orchestrator.X_val, X_val))
        self.assertTrue(np.array_equal(orchestrator.y_train, y_train))
        self.assertTrue(np.array_equal(orchestrator.y_test, y_test))
        self.assertTrue(np.array_equal(orchestrator.y_val, y_val))

    def test_Init_InvalidMetric_ShouldRaiseValueError(self):
        # arrange
        invalid_metric = "accuracy"

        # act/assert
        with self.assertRaises(ValueError):
            PipelineOrchestrator(self.X_train, self.y_train, invalid_metric, self.config_path, verbose=self.verbose)

    def test_Init_TestSizeValidationSize_SplitSizeShouldMatch(self):
        # arrange
        ensemble_size = 0.2
        validation_size = 0.1

        # act
        orchestrator = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            ensemble_size=ensemble_size,
            validation_size=validation_size,
            verbose=self.verbose,
        )

        # assert
        self.assertEqual(orchestrator.ensemble_size, ensemble_size)
        self.assertEqual(orchestrator.validation_size, validation_size)

    def test_Init_ShuffleStratify_ShuffleStratifyFlagsShouldMatch(self):
        # arrange
        shuffle = True
        stratify = True

        # act
        orchestrator = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            shuffle=shuffle,
            stratify=stratify,
            verbose=self.verbose,
        )

        # assert
        self.assertEqual(orchestrator.shuffle, shuffle)
        self.assertEqual(orchestrator.stratify, stratify)

    def test_Init_EstimatorList_DoNotUseSklearnEstimatorsAsideEstimatorList_EstimatorListFlagsShouldMatch(self):
        # arrange
        estimator_list = get_estimator_list(random_state=0)
        use_sklearn_estimators_aside_estimator_list = False

        # act
        orchestrator = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            estimator_list=estimator_list,
            use_sklearn_estimators_aside_estimator_list=use_sklearn_estimators_aside_estimator_list,
            verbose=self.verbose,
        )

        # assert
        self.assertEqual(orchestrator.component_service.estimator_list, estimator_list)

    def test_Init_ExcludeEstimators_ExcludeEstimatorsListShouldMatch(self):
        # arrange
        exclude_estimators = ["RandomForestClassifier", "SVC"]

        # act
        orchestrator_with_excluded_estimators = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            exclude_estimators=exclude_estimators,
            verbose=self.verbose,
        )
        orchestrator_without_excluded_estimators = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            verbose=self.verbose,
        )
        difference = set(orchestrator_without_excluded_estimators.component_service.estimator_list) - set(
            orchestrator_with_excluded_estimators.component_service.estimator_list
        )
        excluded_estimator_names = [get_obj_name(c) for c in difference]

        # assert
        list_to_pop = excluded_estimator_names.copy()

        for estimator_name in exclude_estimators:
            for excluded_estimator_name in excluded_estimator_names:
                if estimator_name in excluded_estimator_name:
                    list_to_pop.remove(excluded_estimator_name)
                    continue
        self.assertEqual([], list_to_pop)

    def test_Init_PredictProbaOnly_PredictProbaOnlyFlagShouldMatch(self):
        # arrange
        predict_proba_only = True

        # act
        orchestrator = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            predict_proba_only=predict_proba_only,
            verbose=self.verbose,
        )

        # assert
        self.assertTrue(
            all(est for est in orchestrator.component_service.estimator_list if hasattr(est, "predict_proba"))
        )

    def test_Init_RandomState_RandomStateShouldMatch(self):
        # arrange
        random_state = 42

        # act
        orchestrator = PipelineOrchestrator(
            self.X_train,
            self.y_train,
            self.metric,
            self.config_path,
            random_state=random_state,
            shuffle=True,
            verbose=self.verbose,
        )

        # assert
        self.assertEqual(orchestrator.random_state, random_state)
