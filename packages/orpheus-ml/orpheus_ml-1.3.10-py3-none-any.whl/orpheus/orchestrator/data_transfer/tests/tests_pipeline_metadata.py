"""Tests for PipelineMetadata class."""
from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from orpheus.orchestrator.data_transfer.pipeline_metadata import PipelineMetadata
from orpheus.orchestrator.data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.test_utils.stubs import get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.utils.generic_functions import generate_unique_id


class TestsPipelineMetadata(TestCaseBase):
    """Tests for DataSerializer class."""

    def setUp(self):
        """Initialize objects for testing"""
        estimators = MultiEstimatorWrapper([LogisticRegression(), DecisionTreeClassifier()])
        self.steps = [
            ("scaler", StandardScaler()),
            ("estimators", estimators),
        ]
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
        self.medatata_obj = PipelineMetadata(
            pipeline_name="base",
            pipeline=self.pipeline,
            is_robust=True,
        )
        self.dto = PipelineOrchestratorProxyDTO(
            _id=generate_unique_id(),
            dataset_name="test",
            config={},
            call_order={},
            metadata_dict={
                "base": self.medatata_obj,
            },
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

    def test_init(self):
        """Test the initialization of PipelineMetadata object"""
        # Arrange
        pipeline_name = "base"
        is_robust = True

        # Act
        metadata_obj = PipelineMetadata(
            pipeline_name=pipeline_name,
            pipeline=self.pipeline,
            is_robust=is_robust,
        )

        # Assert
        self.assertEqual(metadata_obj.pipeline_name, pipeline_name)
        self.assertEqual(metadata_obj.pipeline, self.pipeline)
        self.assertIsNone(metadata_obj.explained_features)
        self.assertIsNone(metadata_obj.explained_distribution)
        self.assertEqual(metadata_obj.is_robust, is_robust)

    # def test_ToDict_ReturnsDictWithPipelineMetadata_ShouldMatchFromDictInstance(self):
    #     """Test if a dictionary is returned with the pipeline metadata"""
    #     # Arrange
    #     self.pipeline.fit(self.X_train, self.y_train)
    #     pipeline_name = "base"
    #     is_robust = True
    #     metadata_obj = PipelineMetadata(
    #         pipeline_name=pipeline_name,
    #         pipeline=self.pipeline,
    #         is_robust=is_robust,
    #     )

    #     # Act
    #     metadata_dict = metadata_obj.to_dict()
    #     metadata_obj_new = PipelineMetadata.from_dict(metadata_dict)

    #     # Assert
    #     self.assertIsInstance(metadata_dict, dict)
    #     self.assertIsInstance(metadata_obj_new, PipelineMetadata)
    #     self.assertEqual(metadata_obj_new.pipeline_name, pipeline_name)
    #     self.assertIsNone(metadata_obj_new.explained_features)
    #     self.assertIsNone(metadata_obj_new.explained_distribution)
    #     self.assertEqual(metadata_obj_new.is_robust, is_robust)
    #     self.assertEqual(metadata_obj_new.metric, self.metric)
    #     self.assertEqual(metadata_obj_new.maximize_scoring, self.maximize_scoring)
    #     self.assertEqual(metadata_obj_new.type_estimator, self.type_estimator)

    #     # compare pipelines for equality
    #     pred1 = metadata_obj_new.pipeline.predict(self.X_test)
    #     pred2 = self.pipeline.predict(self.X_test)
    #     self.assertTrue(np.array_equal(pred1, pred2))
    #     for estimator1, estimator2 in zip(metadata_obj_new.pipeline.estimators, self.pipeline.estimators):
    #         self.assertTrue(estimators_are_equal(estimator1, estimator2))

    # def test_ToJson_ReturnsJsonWithPipelineMetadata_ShouldMatchFromDictInstance(self):
    #     """Test if a dictionary is returned with the pipeline metadata"""
    #     # Arrange
    #     self.pipeline.fit(self.X_train, self.y_train)
    #     pipeline_name = "base"
    #     is_robust = True
    #     metadata_obj = PipelineMetadata(
    #         pipeline_name=pipeline_name,
    #         pipeline=self.pipeline,
    #         is_robust=is_robust,
    #     )

    #     # Act
    #     metadata_json = metadata_obj.to_json()
    #     metadata_obj_new = PipelineMetadata.from_json(metadata_json)

    #     # Assert
    #     self.assertIsInstance(metadata_json, str)
    #     self.assertIsInstance(metadata_obj_new, PipelineMetadata)
    #     self.assertEqual(metadata_obj_new.pipeline_name, pipeline_name)
    #     self.assertIsNone(metadata_obj_new.explained_features)
    #     self.assertIsNone(metadata_obj_new.explained_distribution)
    #     self.assertEqual(metadata_obj_new.is_robust, is_robust)
    #     self.assertEqual(metadata_obj_new.metric, self.metric)
    #     self.assertEqual(metadata_obj_new.maximize_scoring, self.maximize_scoring)
    #     self.assertEqual(metadata_obj_new.type_estimator, self.type_estimator)

    #     # compare pipelines for equality
    #     pred1 = metadata_obj_new.pipeline.predict(self.X_test)
    #     pred2 = self.pipeline.predict(self.X_test)
    #     self.assertTrue(np.array_equal(pred1, pred2))
    #     for estimator1, estimator2 in zip(metadata_obj_new.pipeline.estimators, self.pipeline.estimators):
    #         self.assertTrue(estimators_are_equal(estimator1, estimator2))
