"""
Class for rebuilding an iteration of a pipeline orchestrator from a dto stored in the database.
This is useful for resurfacing the best configuration from the database and then adjusting it based on the surrogate model.
"""

import os
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import schema
from sklearn.ensemble import RandomForestRegressor

from orpheus.components.libs.config_manager import (
    ConfigManager,
    get_nested_value_with_dotted_key,
    set_nested_value_with_dotted_key,
)
from orpheus.orchestrator.data_transfer.pipeline_orchestrator_proxy_dto import PipelineOrchestratorProxyDTO
from orpheus.orchestrator.helper_functions import create_multi_column_samples_infer_type
from orpheus.orchestrator.pipeline_manager import PipelineManager
from orpheus.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from orpheus.orchestrator.pipeline_orchestrator_proxy import PipelineOrchestratorProxy
from orpheus.repository.pipeline_orchestrator_proxy_repository import PipelineOrchestratorProxyRepository
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.utils.logger import logger
from orpheus.validations.config_schema import config_schema, validate_bounds_FeatureAdding


class PipelineOrchestratorRebuilder:
    """Class for rebuilding an iteration of a pipeline orchestrator from a dto stored in the database"""

    config_samples: List[dict] = []
    _config_samples_are_generated = False

    def __init__(self, dataset_name: str, db_path: str = "orpheus_data.db", verbose: int = 0, **random_forest_kwargs):
        """
        Class for rebuilding an iteration of a pipeline orchestrator from a dto stored in the database

        Parameters
        ----------
        dataset_name : str
            Name of the dataset. Used to identify the dataset in the database.
        db_path : str, optional
            Path to the database file, by default "orpheus_data.db"
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' does not exist")

        self.dataset_name = dataset_name
        self.db_path = db_path
        self._repository = PipelineOrchestratorProxyRepository(db_path)
        self.model = RandomForestRegressor(**random_forest_kwargs)

        self.dto: Optional[PipelineOrchestratorProxyDTO] = None
        self.numeric_features: Optional[List[str]] = None
        self.maximize_scoring: Optional[bool] = None
        self.generated_config_samples: Optional[List[dict]] = None

        # check if the dataset exists in the database
        dataset_id = self._repository.get_dataset_id(dataset_name)
        if dataset_id is None:
            raise ValueError(f"Dataset '{dataset_name}' does not exist in database '{self.db_path}' ")

        logger.set_verbose(verbose)

    def set_dto(self, dto_id: str) -> "PipelineOrchestratorRebuilder":
        """
        Fetch the PipelineOrchestratorProxyDTO object from the database and set it as the dto attribute.
        """
        dto = self._repository.get_dto_by_id(dto_id)
        self.dto = dto
        return self

    def set_dto_by_score(self) -> "PipelineOrchestratorRebuilder":
        """Fetch the PipelineOrchestratorProxyDTO object from the database with the best score and set it as the dto attribute."""
        dto = self._repository.get_dto_by_score(self.dataset_name, top_n=1)[0]
        self.dto = dto
        return self

    def set_dto_by_last(self) -> "PipelineOrchestratorRebuilder":
        """Fetch the PipelineOrchestratorProxyDTO object from the database with the most recent timestamp and set it as the dto attribute."""
        dto = self._repository.get_last_dto(self.dataset_name)
        self.dto = dto
        return self

    def set_dto_by_score_then_last(self) -> "PipelineOrchestratorRebuilder":
        """
        If the dto is None, set the dto by score. Otherwise, set the dto by most recent.
        This is useful if the PipelineOrchestratorRebuilder instance is used in a loop, as
        the dto will be set by score the first time, and then by most recent the next times,
        allowing the configuration to be adjusted based on the most recent iteration each time.

        The idea is that the config-yaml file should slowly converge to the best configuration.
        """
        if self.dto is None:
            self.set_dto_by_score()
        else:
            self.dto = self._repository.get_last_dto(self.dataset_name)
        return self

    def set_config_samples(
        self, col_min_max_samples: List[Tuple[str, np.number, np.number]], row_index: int, N: int = 60
    ) -> "PipelineOrchestratorRebuilder":
        """
        Generate new config samples for model training based on the config of the dto.
        During runtime, only one set of config samples can be generated.
        The generated config samples are stored in PipelineOrchestratorRebuilder.config_samples.

        If config samples are already present in the database self.db_path with a given dataset_name, the amount of config samples generated will be N - amt_in_db.

        Parameters
        ----------
        N : int, optional
            The number of samples to create, by default 100
        """
        if not PipelineOrchestratorRebuilder._config_samples_are_generated:
            amt_in_db = self._repository.get_all(
                by_dataset_name=self.dataset_name, columns_wanted=["metadata_id"]
            ).shape[0]
            N -= amt_in_db
            logger.notice(
                f"Generating {N} config samples for training, with {amt_in_db} samples already in the database..."
            )
            if self.dto is None:
                raise AttributeError("No dto set. Use self.set_dto() or self.set_dto_by_score() to set the dto first.")

            # get the config from the dto
            config = self.dto["config"]
            config_df = ConfigManager.dicts_to_features([config])

            # create new samples
            new_samples = create_multi_column_samples_infer_type(
                df=config_df,
                row_index=row_index,
                col_min_max_tuples=col_min_max_samples,
                N=N,
            )

            generated_config_samples = ConfigManager.features_to_dicts(new_samples)
            PipelineOrchestratorRebuilder.config_samples.extend(generated_config_samples)
            PipelineOrchestratorRebuilder._config_samples_are_generated = True

        else:
            logger.warning(
                f"only one set of config samples can be generated during runtime!\nUse PipelineOrchestratorRebuilder.config_samples to access the generated config samples, of which are left: {len(PipelineOrchestratorRebuilder.config_samples)}"
            )

        return self

    def get_data(self) -> pd.DataFrame:
        """
        Get all data from the database for the given dataset_name.
        Excludes the "dto" column to ensure faster loading times.
        """
        return self._repository.get_all(
            by_dataset_name=self.dataset_name,
            columns_wanted=[
                "metadata_id",
                "created",
                "score",
                "execution_time",
                "metric",
                "type_estimator",
                "maximize_scoring",
            ],
        )

    def get_best_dtos_by_score(self, top_n: int = 1) -> List[PipelineOrchestratorProxyDTO]:
        """
        Get the best dtos by score from the database for the given dataset_name.

        """
        return self._repository.get_dto_by_score(self.dataset_name, top_n=top_n)

    def get_best_pipelines_by_score(self, top_n: int = 1, sort_by_performance=True) -> List[MultiEstimatorPipeline]:
        """
        Get the best pipelines by score from the database for the given dataset_name.

        parameters
        ----------
        top_n : int
            The top number of dtos to extract pipelines from, by default 1.
            Each dto can contain up to 3 pipelines (base, stacked, evolved).

        sort_by_performance : bool
            Whether to sort the pipelines by performance after fetching them from the DTO's.
            By default True.
        """
        dtos = self._repository.get_dto_by_score(self.dataset_name, top_n=top_n)
        pipelines = []
        for dto in dtos:
            for name, metadata_obj in dto["metadata_dict"].items():
                pipeline = metadata_obj.pipeline
                pipelines.append(pipeline)

        if sort_by_performance:
            pipelines.sort(key=lambda x: x.performance, reverse=True)

        return pipelines

    def train_model(self) -> "PipelineOrchestratorRebuilder":
        """Train a model on the train data."""
        if self.dto is None:
            raise AttributeError("No dto set. Use self.set_dto() or self.set_dto_by_score() to set the dto first.")

        all_data: pd.DataFrame = self._repository.get_all(
            by_dataset_name=self.dataset_name, columns_wanted=["dto", "score", "metric", "maximize_scoring"]
        )
        config_dicts = list(map(lambda x: x["config"], all_data["dto"]))
        X = ConfigManager.dicts_to_features(config_dicts)

        # clean X with columns which are not numeric:
        if self.numeric_features is None:
            X = X.select_dtypes(include="number")
            self.numeric_features = X.columns
        else:
            X = X[self.numeric_features]

        y = all_data["score"]
        logger.notice(f"Training model {self.model} on {X.shape[0]} samples...")
        self.model.fit(X, y)

        return self

    def set_config_by_model_pred(self, threshold=0.0001) -> "PipelineOrchestratorRebuilder":
        """
        Make a decision about the config based on the surrogate model.

        Parameters
        ----------
        threshold: float
            The threshold for the feature weights, where 0.01 is 1%.
            If the absolute value of the weight is below the threshold, the configsetting is not considered decisive.
        """
        if self.dto is None:
            raise AttributeError("No dto set. Use self.set_dto() or self.set_dto_by_score() to set the dto first.")
        if not self._model_is_fitted():
            raise AttributeError("Model is not fitted. Use self.train_model() to fit the model first.")

        # get coefs of features from the surrogate model
        feature_importances = self.model.feature_importances_
        maximize_scoring = self.dto.maximize_scoring
        feature_weights = pd.Series(dict(zip(self.numeric_features, feature_importances)))
        non_zero_weights = feature_weights[feature_weights != 0]

        # reverse sign of weights if the scoring is minimized
        if not maximize_scoring:
            non_zero_weights *= -1

        decisive_weights = non_zero_weights[non_zero_weights.abs() > threshold]

        # transform the dotted access to dict access ion the index so that values can be mapped directly to the config
        # decisive_weights.index = decisive_weights.index.map(transform_to_dict_access)

        # sum with 1 so that the values can be mapped directly to the config
        decisive_weights += 1
        logger.notice(
            f"Weights which will be used for configfile to adjust new settings:\n{decisive_weights.to_string()}"
        )

        # update the config
        config = self.dto["config"]
        validator = schema.Schema(config_schema)

        for key, weight in decisive_weights.items():
            # validate new values:
            try:
                old_value = get_nested_value_with_dotted_key(config, key)
                new_value = old_value * weight
                set_nested_value_with_dotted_key(config, key, new_value)
                validator.validate(config)
                validate_bounds_FeatureAdding(config["FeatureAdding"])
            except (schema.SchemaError, ValueError) as e:
                logger.warning(f"New value {new_value} for {key} is not valid!:\n{e}")
                logger.warning(f"Trying to set a new value for {key} which is valid...")
                if isinstance(new_value, float) and isinstance(old_value, int):
                    new_value = (old_value + 1) if weight > 1 else (old_value - 1)
                # if sign changed, set to 0
                elif new_value * old_value < 0:
                    new_value = 0
                else:
                    set_nested_value_with_dotted_key(config, key, old_value)
                    logger.notice(
                        f"Could not find a valid value for {key} . Switching back to the old value {old_value}"
                    )
                    continue
                logger.notice(f"Switching {key} from {old_value} to {new_value}")

                try:
                    set_nested_value_with_dotted_key(config, key, new_value)
                    validator.validate(config)
                    validate_bounds_FeatureAdding(config["FeatureAdding"])
                except (schema.SchemaError, ValueError):
                    logger.error(f"Could not set a proper value for {key}. Switching back to {old_value}")
                    set_nested_value_with_dotted_key(config, key, old_value)

        self.dto["config"] = config

        return self

    def run(
        self,
        X: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]],
        y: Union[pd.Series, Tuple[pd.Series, pd.Series, pd.Series]],
        config_path: str,
        log_file_path: Optional[str] = None,
        log_file_mode: str = "a+",
        log_cpu_memory_usage: bool = False,
        **orchestrator_init_kwargs,
    ) -> PipelineManager:
        """
        Create a new PipelineOrchestrator instance from a PipelineOrchestratorProxyDTO object saved in the database.
        Then, insert the orchestrator instance in a PipelineOrchestratorProxy object so that metadata about the run can be collected.
        And run the methods of the PipelineOrchestratorProxy object.

        IMPORTANT: This method uses the current config in self.dto["config"] to run the methods of the PipelineOrchestratorProxy object.

        Parameters
        ----------
        X: Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]
            The feature matrix or a tuple of the train, test and validation feature matrices.
            This last option is useful when you want to preprocess the data before splitting it.
        y: Union[pd.Series, Tuple[pd.Series, pd.Series, pd.Series]]
            The target vector or a tuple of the train, test and validation target vectors.
        dto: PipelineOrchestratorProxyDTO
            The PipelineOrchestratorProxyDTO object. This object is loaded from the database.
        config_path: str
            The path to the configuration file of the components (scaling, adding/removing features and hyperparameter tuning).
            The settings
        verbose: int
            The verbosity level.
        log_file_path: Optional[str]
            The path to the log file. If None, messages will be printed to the console given verbose > 0.
        log_file_mode : str = "a+"
            Mode to open log file. Default is "a+" (append). Use "w+" to overwrite.
        log_cpu_memory_usage: bool
            Whether to also log the cpu and memory usage. This can be useful for debugging purposes.
        orchestrator_init_kwargs: dict
            Additional keyword arguments for the PipelineOrchestrator class.
            Examples: n_jobs, shuffle, stratify, ensemble_size, validation_size, estimator_list, use_sklearn_estimators_aside_estimator_list, n_splits_if_cv_obj_is_none

        Returns
        -------
        pipeline_orchestrator: PipelineOrchestrator
            The PipelineOrchestrator object.
        """
        if self.dto is None:
            raise AttributeError("No dto set. Use self.set_dto() or self.set_dto_by_score() to set the dto first.")

        # write the config to a yaml file
        if PipelineOrchestratorRebuilder.config_samples:
            logger.notice(
                f"Using generated config samples for self.run(). Config samples left: {len(PipelineOrchestratorRebuilder.config_samples)}"
            )
            config = PipelineOrchestratorRebuilder.config_samples.pop()
        else:
            logger.notice("Using config from self.dto for self.run()")
            config = self.dto["config"]
        if not config_path.endswith(".yaml"):
            config_path += ".yaml"
        ConfigManager.write_dict_to_yaml(config_path, config)

        init_params = self.dto["call_order"].pop("init")
        metadata_data = init_params.pop("metadata_data")

        if not isinstance(X, metadata_data["X"]["type"]):
            raise TypeError(f"X must be a {metadata_data['type']}, but is {type(X)}")
        if not isinstance(y, metadata_data["y"]["type"]):
            raise TypeError(f"y must be a {metadata_data['type']}, but is {type(y)}")

        if orchestrator_init_kwargs:
            init_params.update(orchestrator_init_kwargs)

        orchestrator = PipelineOrchestrator(
            X=X,
            y=y,
            config_path=config_path,
            verbose=logger.get_verbose(),
            log_file_path=log_file_path,
            log_file_mode=log_file_mode,
            log_cpu_memory_usage=log_cpu_memory_usage,
            **init_params,
        )

        # instantiate the orchestrator proxy to collect metadata about the new run.
        orchestrator_proxy = PipelineOrchestratorProxy(
            orchestrator,
            dataset_name=self.dataset_name,
            db_path=self.db_path,
            repository=self._repository,
        )

        # start the run
        for key, params in self.dto["call_order"].items():
            # skip parameters starting with an underscore:
            params = {k: v for k, v in params.items() if not k.startswith("_")}
            method = getattr(orchestrator_proxy, key, None)
            if method is None:
                raise AttributeError(f"Method {method} not found in PipelineOrchestrator class")
            method(**params)

        orchestrator_proxy.write_dto_to_db()

        return orchestrator_proxy.pipelines

    def _model_is_fitted(self) -> bool:
        try:
            _ = self.model.feature_importances_
            return True
        except AttributeError:
            return False
