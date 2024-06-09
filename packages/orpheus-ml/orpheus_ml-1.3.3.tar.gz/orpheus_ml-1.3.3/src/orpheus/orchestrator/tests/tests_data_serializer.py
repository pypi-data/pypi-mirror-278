"""Tests for DataSerializer class."""

from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from orpheus.orchestrator.data_transfer.pipeline_metadata import PipelineMetadata
from orpheus.orchestrator.data_transfer.data_serializer import DataSerializer
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.test_utils.helper_functions import estimators_are_equal, scalers_are_equal
from orpheus.test_utils.stubs import get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.utils.generic_functions import generate_unique_id
from orpheus.orchestrator.data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO


class TestsDataSerializer(TestCaseBase):
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

    def tests_Serializepipeline_SerializeAndDeserializePipeline_PipelinesAreEqual(self):
        """Test if a serialized pipeline is equal to the original pipeline"""
        # arrange
        pipeline: MultiEstimatorPipeline = self.dto["metadata_dict"]["base"].pipeline
        pipeline.fit(self.X_train, self.y_train)

        # act
        serialized_pipeline: str = DataSerializer.serialize(pipeline)
        deserialized_pipeline: MultiEstimatorPipeline = DataSerializer.deserialize(serialized_pipeline)

        # assert
        for step in zip(self.pipeline.steps, deserialized_pipeline.steps):
            pipeline_item, deserialized_pipeline_item = step
            if isinstance(pipeline_item[1], StandardScaler):
                self.assertTrue(scalers_are_equal(pipeline_item[1], deserialized_pipeline_item[1]))
            elif isinstance(pipeline_item[1], MultiEstimatorWrapper):
                for est in zip(pipeline_item[1].estimators, deserialized_pipeline_item[1].estimators):
                    self.assertTrue(estimators_are_equal(est[0], est[1]))
        self.assertTrue(str(self.pipeline.__dict__), str(deserialized_pipeline.__dict__))

    def tests_DeserializePipeline_DeserializePipeline_PredictionsAreEqual(self):
        """Test if a deserialized pipeline gives the same predictions as the original pipeline"""
        # arrange
        self.pipeline.fit(self.X_train, self.y_train)
        serialized_pipeline = DataSerializer.serialize(self.pipeline)
        deserialized_pipeline = DataSerializer.deserialize(serialized_pipeline)

        # act
        predictions_pipeline = self.pipeline.predict(self.X_test)
        predictions_deserialized_pipeline = deserialized_pipeline.predict(self.X_test)

        # assert
        self.assertListEqual(predictions_pipeline.tolist(), predictions_deserialized_pipeline.tolist())
