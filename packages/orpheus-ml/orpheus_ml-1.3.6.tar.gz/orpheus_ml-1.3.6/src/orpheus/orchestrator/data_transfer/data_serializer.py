"""A module for serializing and deserializing data."""

import base64
from io import BytesIO
from typing import Any

import joblib

from orpheus.utils.helper_functions import get_obj_name


class DataSerializer:
    """A class to serialize and deserialize data."""

    @staticmethod
    def serialize(obj: Any) -> str:
        """Serializes an object to a base64 string."""
        buffer = BytesIO()
        joblib.dump(obj, buffer)
        buffer.seek(0)
        obj_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return obj_base64

    @staticmethod
    def deserialize(base64_str: str) -> Any:
        """Deserializes an object from a base64 string."""
        buffer = BytesIO(base64.b64decode(base64_str))
        obj = joblib.load(buffer)
        return obj

    @staticmethod
    def make_serializable(obj: Any) -> Any:
        """Recursively convert non-serializable types into serializable base64 strings."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = DataSerializer.make_serializable(value)
        elif isinstance(obj, list):
            obj = [DataSerializer.make_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            obj = tuple([DataSerializer.make_serializable(item) for item in obj])
        elif isinstance(obj, set):
            obj = set([DataSerializer.make_serializable(item) for item in obj])
        elif not isinstance(obj, (str, int, float, bool)):
            try:
                obj = DataSerializer.serialize(obj)
            except Exception as e:
                obj = f"Non-serializable object of type {get_obj_name(obj)}: {e}"
        return obj

    @staticmethod
    def make_deserializable(obj: Any) -> Any:
        """Recursively convert base64 strings into deserialized objects."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = DataSerializer.make_deserializable(value)
        elif isinstance(obj, list):
            obj = [DataSerializer.make_deserializable(item) for item in obj]
        elif isinstance(obj, tuple):
            obj = tuple([DataSerializer.make_deserializable(item) for item in obj])
        elif isinstance(obj, set):
            obj = set([DataSerializer.make_deserializable(item) for item in obj])
        elif isinstance(obj, str):
            try:
                # Try to deserialize if it's a base64 string
                obj = DataSerializer.deserialize(obj)
            except Exception:
                pass  # If deserialization fails, leave the string as is
        return obj
