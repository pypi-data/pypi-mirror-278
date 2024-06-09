"""DTO for PipelineOrchestratorProxy object."""

import json
import traceback
from typing import Any, Dict, Union

import numpy as np

from orpheus.orchestrator.data_transfer.pipeline_metadata import PipelineMetadata
from orpheus.utils.generic_functions import assert_builtin_types
from orpheus.utils.logger import logger

from .data_serializer import DataSerializer


class PipelineOrchestratorProxyDTO(dict):
    """
    Class that represents a PipelineOrchestratorProxyDTO object.
    Specifically, it is a DTO for PipelineOrchestratorProxy.dto attribute.
    It contains all relevant data of a single run of a PipelineOrchestrator instance.
    """

    def __init__(
        self,
        _id: str,
        dataset_name: str,
        config: Dict[str, Any],
        call_order: Dict[str, Any],
        metadata_dict: Dict[str, PipelineMetadata],
    ):
        self._validate_params(_id, dataset_name, config, call_order, metadata_dict)

        super().__init__(
            {
                "id": _id,
                "dataset": dataset_name,
                "config": config,
                "call_order": call_order,
                "metadata_dict": metadata_dict,
            }
        )

    @property
    def metric(self) -> str:
        """Returns the metric parameter."""
        return self._get_attr_from_metadata("metric")

    @property
    def maximize_scoring(self) -> Union[bool, None]:
        """Returns the maximize_scoring parameter."""
        return self._get_attr_from_metadata("maximize_scoring")

    @property
    def score(self) -> float:
        """Returns the score from the mean of all metadata.performance values."""
        performances = [
            getattr(metadata, "performance", None) or metadata.get("performance", None)
            for metadata in self["metadata_dict"].values()
        ]
        performances = [p for p in performances if p is not None]
        return np.mean(performances)

    @property
    def type_estimator(self) -> str:
        """Returns the type_estimator parameter."""
        return self._get_attr_from_metadata("type_estimator")

    @property
    def dataset(self) -> str:
        """Returns the dataset name."""
        return self["dataset"]

    @property
    def execution_time(self) -> int:
        """Returns the total execution time of a PipelineOrchestrator-run in seconds."""
        return round(sum(v.get("_execution_time", 0) for k, v in self["call_order"].items()))

    @property
    def id(self) -> str:
        """Returns the id."""
        return self["id"]

    def __repr__(self) -> str:
        return f"PipelineOrchestratorProxyDTO(id={self.id}, dataset={self.dataset}, maximize_scoring={self.maximize_scoring}, score={self.score}, type_estimator={self.type_estimator}, keys={self.keys()})"

    @classmethod
    def from_dict(cls, _dict: dict) -> "PipelineOrchestratorProxyDTO":
        """Creates a PipelineOrchestratorProxyDTO object from a dictionary with similar keys as the constructor."""
        if not isinstance(_dict, dict):
            raise TypeError(f"_dict should be a dictionary, not {type(_dict)}")
        keys = ["id", "dataset", "config", "call_order", "metadata_dict"]
        if not all(key in _dict for key in keys):
            raise ValueError(f"Keys {keys} should be in dto_dict, but are not. Keys in dto_dict: {_dict.keys()}")

        _dict = DataSerializer.make_deserializable(_dict)

        return cls(
            _id=_dict["id"],
            dataset_name=_dict["dataset"],
            config=_dict["config"],
            call_order=_dict["call_order"],
            metadata_dict=_dict["metadata_dict"],
        )

    def to_dict(self) -> dict:
        """Returns the PipelineOrchestratorProxyDTO object as a dictionary with only builtin python types."""
        d = {
            "id": self.id,
            "dataset": self.dataset,
            "config": self["config"],
            "call_order": self["call_order"],
            "metadata_dict": self["metadata_dict"],
        }

        d = DataSerializer.make_serializable(d)
        assert_builtin_types(d)

        return d

    def to_json(self) -> str:
        """Returns the PipelineOrchestratorProxyDTO object as a json string."""
        try:
            d = self.to_dict()
            return json.dumps(d)
        except Exception:
            logger.error(f"Could not serialize {self} to json string:\n {traceback.format_exc()}")
            raise

    @classmethod
    def from_json(cls, json_str: str) -> "PipelineOrchestratorProxyDTO":
        """Parse a json string to a PipelineOrchestratorProxyDTO object."""
        try:
            d = json.loads(json_str)
            return cls.from_dict(d)
        except Exception:
            logger.error(f"Could not parse json string:\n{traceback.format_exc()}")
            raise

    def _validate_params(self, _id, dataset_name, config, call_order, metadata_dict):
        """Validates the parameters of the constructor."""
        if not isinstance(_id, str):
            raise TypeError(f"_id should be a string, not {type(_id)}")
        if not isinstance(dataset_name, str):
            raise TypeError(f"dataset_name should be a string, not {type(dataset_name)}")
        if not isinstance(config, dict):
            raise TypeError(f"config should be a dictionary, not {type(config)}")
        if not isinstance(call_order, dict):
            raise TypeError(f"call_order should be a dictionary, not {type(call_order)}")
        if not isinstance(metadata_dict, dict):
            raise TypeError(f"metadata should be a dictionary, not {type(metadata_dict)}")
        if not all(isinstance(key, str) for key in metadata_dict.keys()):
            raise TypeError(f"metadata keys should be strings, not {type(metadata_dict.keys())}")
        if not all(isinstance(value, (PipelineMetadata, dict)) for value in metadata_dict.values()):
            raise TypeError(
                f"metadata values should be PipelineMetadata objects or dicts, not {type(metadata_dict.values())}"
            )

    def _get_attr_from_metadata(self, attr: str) -> Union[Any, None]:
        """Returns the attr from the metadata_dict."""
        for metadata in self["metadata_dict"].values():
            found_attr = getattr(metadata, attr, None) or metadata.get(attr, None)
            if found_attr is not None:
                return found_attr
        raise AttributeError(f"{attr} not found in metadata_dict")
