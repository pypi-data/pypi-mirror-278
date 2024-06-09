"""Tests for multi_estimator_pipeline.py."""


import os
import sqlite3
from unittest.mock import MagicMock

from sklearn.discriminant_analysis import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from orpheus.repository.pipeline_orchestrator_proxy_repository import PipelineOrchestratorProxyRepository
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.test_utils.stubs import get_estimator_list, get_X_y_train_test
from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.utils.custom_estimators import MultiEstimatorWrapper
from orpheus.utils.generic_functions import generate_unique_id
from orpheus.orchestrator.data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO


# Constants
SCORE = 0.5
TYPE_ESTIMATOR = "classifier"
MAXIMIZE_SCORING = True
METRIC = "accuracy_score"
EXECUTION_TIME = 100


def create_mock_dto(dataset_name, data_id) -> PipelineOrchestratorProxyDTO:
    """Creates a mock PipelineOrchestratorProxyDTO object"""
    dto = MagicMock(spec=PipelineOrchestratorProxyDTO)
    dto.__str__.return_value = "mocked dto"
    dto.maximize_scoring = MAXIMIZE_SCORING
    dto.score = SCORE
    dto.metric = METRIC
    dto.execution_time = EXECUTION_TIME
    dto.type_estimator = TYPE_ESTIMATOR
    dto["dataset"] = dataset_name
    dto["id"] = data_id
    dto.__getitem__.side_effect = lambda x: dataset_name if x == "dataset" else data_id
    dto.to_json = lambda: str(dto)
    return dto


class TestsPipelineOrchestratorProxyRepository(TestCaseBase):
    """Tests for PipelineOrchestratorProxyRepository class."""

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
        self.temp_db_path = "temp.db"
        self.repository = PipelineOrchestratorProxyRepository(db_path=self.temp_db_path)

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
        if self.repository.conn:
            self.repository.close_db()
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)
        self.repository = None

    def test_CreateTables_CreatesExpectedTables(self):
        """Test if the _create_tables method creates the expected tables"""
        # Arrange
        tables_are_created = self.repository._create_tables()  # pylint: disable=protected-access

        # Act/Assert
        self.assertTrue(tables_are_created)
        try:
            with self.repository.conn:
                # Checking if table dataset exists
                self.repository.cur.execute("PRAGMA table_info(dataset)")
                columns = self.repository.cur.fetchall()

                # Checking if table has columns dataset_id and name
                expected_columns = ["id", "name"]
                actual_columns = [column[1] for column in columns]

                for expected_column in expected_columns:
                    self.assertIn(expected_column, actual_columns)

        except sqlite3.Error as e:
            self.fail(f"SQLite error: {e}")

    def test_WriteDataToDb_WriteDataToDatabase_DataIsWrittenToDatabase(self):
        """Test if the write_dto_to_db method writes the data to the database"""
        # Arrange
        dataset_name1 = "test_dataset1"
        dataset_name2 = "test_dataset2"
        data_id1 = generate_unique_id()
        data_id2 = generate_unique_id()
        data_id3 = generate_unique_id()

        dto1 = create_mock_dto(dataset_name1, data_id1)
        dto2 = create_mock_dto(dataset_name2, data_id2)
        dto3 = create_mock_dto(dataset_name2, data_id3)

        # Act
        self.repository.write_dto_to_db(dto1)
        self.repository.write_dto_to_db(dto2)
        self.repository.write_dto_to_db(dto3)

        try:
            # Ensure the database connection is active
            if self.repository.conn is None:
                self.repository.conn, self.repository.cur = self.repository.initialize_db(self.temp_db_path)

            # Query to fetch data
            with self.repository.conn:
                self.repository.cur.execute("SELECT id, name FROM dataset")
                datasets = self.repository.cur.fetchall()
                self.repository.cur.execute("SELECT id, name, type_estimator, maximize_scoring FROM metrics")
                metrics = self.repository.cur.fetchall()
                self.repository.cur.execute(
                    "SELECT id, dto, score, execution_time, dataset_id, metrics_id FROM metadata"
                )
                metadata = self.repository.cur.fetchall()

            # Assert
            expected_dataset_table = [(1, dataset_name1), (2, dataset_name2)]
            expected_metric_table = [(1, METRIC, TYPE_ESTIMATOR, MAXIMIZE_SCORING)]
            expected_metadata_table = [
                (data_id1, str(dto1), SCORE, EXECUTION_TIME, 1, 1),
                (data_id2, str(dto2), SCORE, EXECUTION_TIME, 2, 1),
                (data_id3, str(dto3), SCORE, EXECUTION_TIME, 2, 1),
            ]
            self.assertListEqual(datasets, expected_dataset_table)
            self.assertListEqual(metrics, expected_metric_table)
            self.assertListEqual(metadata, expected_metadata_table)

        except sqlite3.Error as e:
            self.fail(f"SQLite error: {e}")
