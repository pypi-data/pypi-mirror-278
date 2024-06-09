"""Proxy class for PipelineOrchestrator that collects information about the configurations of the PipelineOrchestrator instance."""

from datetime import datetime
import traceback
import types
from typing import Any, Optional

import joblib
import ruamel.yaml

from orpheus.repository.pipeline_orchestrator_proxy_repository import PipelineOrchestratorProxyRepository
from orpheus.utils.generic_functions import generate_unique_id, get_args_from_function
from orpheus.utils.logger import logger

from .pipeline_orchestrator import PipelineOrchestrator
from .data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO


class PipelineOrchestratorProxy:
    """
    Proxy class for PipelineOrchestrator that collects information about the configurations of the PipelineOrchestrator instance.
    Has the exact same functionalities as PipelineOrchestrator, but also collects information about
    the configurations of the PipelineOrchestrator instance during runtime.

    Public attributes
    -----------------
    pipeline_orchestrator : PipelineOrchestrator
        The PipelineOrchestrator instance to proxy

    dataset_name : str
        Name of the dataset. Used to identify the dataset in the database.

    db_path : str
        Path to the database file

    id : str
        Unique id for this instance

    dto : PipelineOrchestratorProxyDTO
        Data Transfer Object containing the collected data of the results of a single run of the PipelineOrchestrator instance.

    Public methods
    --------------

    write_dto_to_disk(filename: Optional[str] = None) -> None
        Writes the dto of a single run of the PipelineOrchestrator instance to disk in a serialized format, using joblib.
    """

    def __init__(
        self,
        pipeline_orchestrator: PipelineOrchestrator,
        dataset_name: str,
        db_path: str = "orpheus_data.db",
        repository: Optional[PipelineOrchestratorProxyRepository] = None,
    ) -> None:
        """
        Proxy class for PipelineOrchestrator that collects information about the configurations of the PipelineOrchestrator instance.
        Has the exact same functionalities as PipelineOrchestrator, but also collects information about the configurations of the PipelineOrchestrator instance during runtime.


        Parameters
        ----------
        pipeline_orchestrator : PipelineOrchestrator
            The PipelineOrchestrator instance to proxy
        dataset_name : str
            Name of the dataset. Used to identify the dataset in the database.
        db_path : str, optional
            Path to the database file, by default "orpheus_data.db"
        repository : Optional[PipelineOrchestratorProxyRepository], optional
            The repository to write the dto to, by default None
            If none is given, a new repository is created with the given db_path
        """
        self._validate_orchestrator(pipeline_orchestrator)

        self.pipeline_orchestrator = pipeline_orchestrator
        self.dataset_name = dataset_name
        self.db_path = db_path
        self.config = self._load_config_from_yaml()

        self._id = generate_unique_id()
        if repository is None:
            self._repository = PipelineOrchestratorProxyRepository(db_path=self.db_path)
        else:
            self._repository = repository

        self.dto = PipelineOrchestratorProxyDTO(
            _id=self._id, dataset_name=self.dataset_name, config=self.config, call_order={}, metadata_dict={}
        )

        # only relevant parameters are added to the dto which can be used to recreate the PipelineOrchestrator instance
        self.dto["call_order"]["init"] = {
            "metadata_data": self.pipeline_orchestrator._data_metadata,  # pylint: disable=protected-access
            "metric": self.pipeline_orchestrator.metric,
            "n_jobs": self.pipeline_orchestrator.n_jobs,
            "ensemble_size": self.pipeline_orchestrator.ensemble_size,
            "validation_size": self.pipeline_orchestrator.validation_size,
            "shuffle": self.pipeline_orchestrator.shuffle,
            "stratify": self.pipeline_orchestrator.stratify,
            "cv_obj": self.pipeline_orchestrator.cv_obj,
            "estimator_list": self.pipeline_orchestrator.estimator_list,
            "random_state": self.pipeline_orchestrator.random_state,
            # next params should be False/None because the estimator_list is already set
            "use_sklearn_estimators_aside_estimator_list": False,
            "predict_proba_only": False,
            "exclude_estimators": None,
        }

    def __getattr__(self, attr) -> Any:
        attr_obj = getattr(self.pipeline_orchestrator, attr)

        # Check if it's a method
        if isinstance(attr_obj, types.MethodType):

            def wrapper(*args, _self=self, **kwargs):
                _self.dto["call_order"][attr] = get_args_from_function(
                    attr_obj, args, kwargs
                )  # pylint: disable=protected-access
                start_time = datetime.now()

                # run the method
                attr_obj(*args, **kwargs)

                end_time = datetime.now()
                _self.dto["call_order"][attr]["_execution_time"] = (end_time - start_time).total_seconds()

                # after fortify is called, the metadata of the pipelines is available
                if self._fortify_is_called() and not _self.dto["metadata_dict"]:  # pylint: disable=protected-access
                    metadata_dict = (
                        _self.pipeline_orchestrator.get_pipeline_metadata()
                    )  # pylint: disable=protected-access
                    # metadata_dict = {name: metadata.to_dict() for name, metadata in metadata_dict.items()}
                    _self.dto["metadata_dict"] = metadata_dict  # pylint: disable=protected-access
                return _self

            return wrapper

        return attr_obj

    def write_dto_to_disk(self, filename: Optional[str] = None) -> Any:
        """
        Writes the dto to disk in a serialized format, using joblib.
        The dto is based on the PipelineOrchestratorProxyDTO class and
        contains the collected data of a single run of the PipelineOrchestrator instance.

        Parameters
        ----------
        filename : str, optional
            Gives the file a name.
            If filename is None, The file name is {self.dataset_name}__{self._id}.joblib.

        Returns
        -------
        Any
            The return value of joblib.dump
        """
        if not filename:
            filename = f"{self.dataset_name}__{self._id}.joblib"
        return joblib.dump(self.dto, filename)

    def write_dto_to_db(self) -> str:
        """
        Writes the dto to the database

        Returns
        -------
        str
            The id of the dto
        """
        dto_id = self._repository.write_dto_to_db(self.dto)
        logger.notice(f"DTO with id {dto_id} succesfully written to database '{self.db_path}'")
        return dto_id

    def _fortify_is_called(self) -> bool:
        """Returns True if the fortify method is called, False otherwise"""
        return "fortify" in self.dto["call_order"]

    def _validate_orchestrator(self, pipeline_orchestrator) -> None:
        if not isinstance(pipeline_orchestrator, PipelineOrchestrator):
            raise TypeError(
                f"pipeline_orchestrator must be of type PipelineOrchestrator, but is of type {type(pipeline_orchestrator)}"
            )

    def _load_config_from_yaml(self) -> dict:
        try:
            with open(self.pipeline_orchestrator.config_path, encoding="utf-8") as file:
                config = ruamel.yaml.safe_load(file)
        except Exception:
            logger.critical(
                f"A critical error occurred while trying to read the config file {self.pipeline_orchestrator.config_path}:\n{traceback.format_exc()}"
            )
            raise

        return config
