"""Validate input of PipelineOrchestrator class."""

import pandas as pd

from orpheus.validations.input_checks import AttributeValidation


class PipelineOrchestratorValidator:
    @staticmethod
    def validate_parameters(X, y, ensemble_size: float, validation_size: float, verbose: int):
        PipelineOrchestratorValidator.validate_X_y(X, instance_must_be_dataframe=True)
        PipelineOrchestratorValidator.validate_X_y(y, instance_must_be_dataframe=False)
        PipelineOrchestratorValidator.validate_ensemble_validation_size(ensemble_size, validation_size)
        AttributeValidation.validate_verbose(verbose)

    @staticmethod
    def validate_X_y(data, instance_must_be_dataframe=True):
        available_types = (pd.DataFrame, pd.Series, tuple, list)
        if not isinstance(data, available_types):
            raise TypeError(f"X must be a of types {available_types}. Got {type(data)} instead.")

        enforced_type = pd.DataFrame if instance_must_be_dataframe else pd.Series
        collection_length_is_3 = len(data) == 3
        all_elements_are_right_type = all(isinstance(elem, enforced_type) for elem in data)
        is_single_unsplit_arraylike = isinstance(data, enforced_type) and not data.empty

        # Collection is considered split if it has exactly 3 dataframes
        is_splitted_collection = collection_length_is_3 and all_elements_are_right_type
        is_non_splitted_collection = is_single_unsplit_arraylike

        if not (is_splitted_collection or is_non_splitted_collection):
            raise ValueError(
                f"X must be a collection which contains exactly 3 {enforced_type} instances of split data or a single {enforced_type} instance of non-split data. Now got:\n{data}"
            )

    @staticmethod
    def validate_ensemble_validation_size(ensemble_size: float, validation_size: float):
        if not validation_size or not ensemble_size:
            raise ValueError(
                f"validation_size and ensemble_size cannot be None or 0.0. Got validation_size={validation_size} and ensemble_size={ensemble_size}"
            )
        
        if not isinstance(validation_size, float) or not isinstance(ensemble_size, float):
            raise TypeError(
                f"validation_size and ensemble_size must be of type float. Got validation_size={type(validation_size)} and ensemble_size={type(ensemble_size)}"
            )

        if validation_size < 0 or ensemble_size < 0:
            raise ValueError(
                f"validation_size and ensemble_size cannot be negative. Got validation_size={validation_size} and ensemble_size={ensemble_size}"
            )
        
        if validation_size + ensemble_size >= 1.0:
            raise ValueError(
                f"validation_size and ensemble_size together cannot be larger than 1. Got validation_size={validation_size} and ensemble_size={ensemble_size}"
            )
