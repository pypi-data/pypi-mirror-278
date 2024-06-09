"""Validations for sklearn transformers."""

from functools import partial
from types import FunctionType
from typing import Any, Union
from sklearn.base import TransformerMixin
from orpheus.utils.type_vars import TransformerType


def is_transformer_class(transformer: TransformerType) -> bool:
    return issubclass(type(transformer), TransformerMixin) and hasattr(transformer, "transform")


def is_transformer_function(transformer: Union[FunctionType, partial]) -> bool:
    return isinstance(transformer, (FunctionType, partial))


def is_transformer(transformer: Any) -> bool:
    return is_transformer_class(transformer) or is_transformer_function(transformer)
