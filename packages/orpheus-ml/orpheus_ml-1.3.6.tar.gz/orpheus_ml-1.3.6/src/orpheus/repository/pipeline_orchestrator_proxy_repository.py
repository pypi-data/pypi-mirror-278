"""This module contains the PipelineOrchestratorProxyRepository class, which is responsible for storing and retrieving PipelineOrchestratorProxyDTOs"""

import sqlite3
from typing import List, Optional, Tuple, Union

import pandas as pd

from orpheus.orchestrator.data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger


class PipelineOrchestratorProxyRepository:
    """Pipeline Repository class. This class is responsible for storing and retrieving PipelineOrchestratorProxyDTOs to and from the database."""

    def __init__(self, db_path: str = "orpheus_data.db"):
        self.db_path = db_path
        self.conn, self.cur = self._initialize_db()
        # Define the base columns and their mapping to the database fields
        self.base_columns = {
            "metadata_id": "metadata.id",
            "created": "metadata.created",
            "dto": "metadata.dto",
            "score": "metadata.score",
            "execution_time": "metadata.execution_time",
            "dataset": "dataset.name",
            "metric": "metrics.name",
            "type_estimator": "metrics.type_estimator",
            "maximize_scoring": "metrics.maximize_scoring",
        }

    def write_dto_to_db(self, dto: Union[PipelineOrchestratorProxyDTO, dict]) -> str:
        """Write the PipelineOrchestratorProxyDTO to the database as a serialized json-string."""
        tables_are_created = self._create_tables()
        if not tables_are_created:
            raise RuntimeError("Could not create tables in the database. Aborting...")

        if isinstance(dto, dict) and not isinstance(dto, PipelineOrchestratorProxyDTO):
            dto = PipelineOrchestratorProxyDTO.from_dict(dto)

        if not isinstance(dto, PipelineOrchestratorProxyDTO):
            raise TypeError(f"dto should be a PipelineOrchestratorProxyDTO, not {type(dto)}")

        metadata_id = dto["id"]
        dataset_name = dto["dataset"]
        metric = get_obj_name(dto.metric) if not isinstance(dto.metric, str) else dto.metric
        score = dto.score
        execution_time = dto.execution_time
        type_estimator = dto.type_estimator
        maximize_scoring = dto.maximize_scoring
        dto = dto.to_json()

        try:
            with self.conn:
                # Insert new dataset if not exists
                self.cur.execute("INSERT OR IGNORE INTO dataset (name) VALUES (?)", (dataset_name,))
                dataset_id = self.get_dataset_id(dataset_name)  # Fetch the existing or new dataset id

                # Insert new metrics if not exists
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO metrics
                    (name, type_estimator, maximize_scoring)
                    VALUES (?, ?, ?)
                    """,
                    (metric, type_estimator, maximize_scoring),
                )
                metrics_id = self.get_metric_id(metric)  # Fetch the existing or new metric id

                # Insert data into metadata table
                self.cur.execute(
                    """
                    INSERT OR IGNORE INTO metadata
                    (id, dto, score, dataset_id, metrics_id, execution_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (metadata_id, dto, score, dataset_id, metrics_id, execution_time),
                )
                return metadata_id

        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error: {e}")
            self.close_db()
            raise
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            self.close_db()
            raise

    def get_all(
        self, by_dataset_name: Optional[str] = None, columns_wanted: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Get selected records and columns from the database joined on metadata, dataset, and metrics and transform it into a DataFrame."""

        # If no columns are specified, use all base columns
        if columns_wanted is None:
            columns_wanted = list(self.base_columns.keys())
        else:
            if not all(column in self.base_columns for column in columns_wanted):
                invalid_columns = [column for column in columns_wanted if column not in self.base_columns]
                raise ValueError(
                    f"Invalid column name(s) in: {invalid_columns}. Valid column names are: {list(self.base_columns.keys())}"
                )

        # Filter the base_columns dictionary to include only columns wanted
        columns_to_query = [f"{self.base_columns[col]} AS {col}" for col in columns_wanted if col in self.base_columns]

        # Generate the SQL query string
        query = (
            "SELECT "
            + ", ".join(columns_to_query)
            + """
        FROM metadata
        JOIN dataset ON metadata.dataset_id = dataset.id
        JOIN metrics ON metadata.metrics_id = metrics.id
        """
        )

        if by_dataset_name is not None:
            query += "WHERE dataset.name = ?"
            df = pd.read_sql_query(query, self.conn, params=[by_dataset_name])
        else:
            df = pd.read_sql_query(query, self.conn)

        # Apply any necessary transformations based on the columns that were actually queried
        if "dto" in columns_wanted:
            df["dto"] = df["dto"].apply(PipelineOrchestratorProxyDTO.from_json)

        if "maximize_scoring" in columns_wanted:
            df["maximize_scoring"] = df["maximize_scoring"].astype(bool)

        return df

    def get_dto_by_score(self, dataset_name: str, top_n: int = 1) -> List[PipelineOrchestratorProxyDTO]:
        """Get the records from the database with the best score(s) and transform them into a list of PipelineOrchestratorProxyDTOs."""
        query = """
        SELECT 
            metadata.dto AS dto
         FROM metadata
        JOIN dataset ON metadata.dataset_id = dataset.id
        JOIN metrics ON metadata.metrics_id = metrics.id
        WHERE dataset.name = ?
        ORDER BY 
            CASE WHEN maximize_scoring THEN metadata.score END DESC,
            CASE WHEN NOT maximize_scoring THEN metadata.score END ASC
        LIMIT ?
        """
        self.cur.execute(query, (dataset_name, top_n))
        rows = self.cur.fetchall()

        if not rows:
            raise ValueError(f"No record found for dataset {dataset_name}")

        dtos = [PipelineOrchestratorProxyDTO.from_json(row[0]) for row in rows]

        return dtos

    def get_dto_by_id(self, metadata_id: str) -> PipelineOrchestratorProxyDTO:
        """Get the dto from the database with the given metadata_id and transform it into a PipelineOrchestratorProxyDTO."""
        query = """
        SELECT 
            metadata.dto AS dto
        FROM metadata
        WHERE metadata.id = ?
        """
        self.cur.execute(query, (metadata_id,))
        row = self.cur.fetchone()
        if not row:
            raise ValueError(f"No record found with metadata_id {metadata_id}")
        dto = PipelineOrchestratorProxyDTO.from_json(row[0])
        return dto

    def get_last_dto(self, dataset_name: str) -> PipelineOrchestratorProxyDTO:
        """Get the last dto from the database with the given dataset_name and transform it into a PipelineOrchestratorProxyDTO."""
        query = """
        SELECT 
            metadata.dto AS dto
        FROM metadata
        JOIN dataset ON metadata.dataset_id = dataset.id
        WHERE dataset.name = ?
        ORDER BY metadata.created DESC
        LIMIT 1
        """
        self.cur.execute(query, (dataset_name,))
        row = self.cur.fetchone()
        if not row:
            raise ValueError(f"No record found for dataset {dataset_name}")
        dto = PipelineOrchestratorProxyDTO.from_json(row[0])
        return dto

    def delete_by_id(self, metadata_id: str) -> bool:
        """Delete a record by its metadata_id."""
        try:
            with self.conn:
                self.cur.execute("DELETE FROM metadata WHERE id = ?", (metadata_id,))
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return False

    def get_column_names(self, table_name: str) -> List[str]:
        """Get the column names for a given table."""
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cur.fetchall()]
        return columns

    def get_dataset_id(self, dataset_name: str) -> Optional[int]:
        """Get the dataset ID from the database."""
        self.cur.execute("SELECT id FROM dataset WHERE name = ?", (dataset_name,))
        row = self.cur.fetchone()
        return row[0] if row else None

    def get_metric_id(self, metric_name: str) -> Optional[int]:
        """Get the metric ID from the database."""
        self.cur.execute("SELECT id FROM metrics WHERE name = ?", (metric_name,))
        row = self.cur.fetchone()
        return row[0] if row else None

    def close_db(self):
        """Close the database connection."""
        if self.conn:
            self.cur.close()
            self.conn.close()

    def _create_tables(self) -> bool:
        """
        Create the tables in the database and indexes.

        Returns
        -------
        bool
            True if the tables are created, False if not.
        """
        try:
            with self.conn:
                # Creating tables
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS dataset (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    );
                    """
                )
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        type_estimator TEXT,
                        maximize_scoring INTEGER
                    );
                    """
                )
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS metadata (
                        id TEXT PRIMARY KEY,
                        created DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                        dto TEXT NOT NULL,
                        score REAL,
                        execution_time INTEGER,
                        dataset_id INTEGER NOT NULL,
                        metrics_id INTEGER NOT NULL,
                        FOREIGN KEY (dataset_id) REFERENCES dataset (id),
                        FOREIGN KEY (metrics_id) REFERENCES metrics (id)
                    );
                    """
                )

                return True
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            self.close_db()
            return False

    def _initialize_db(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Initialize the database connection and return the connection and cursor."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur
