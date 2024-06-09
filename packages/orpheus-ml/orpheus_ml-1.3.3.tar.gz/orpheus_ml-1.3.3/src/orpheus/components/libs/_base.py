from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional

from orpheus.components.libs.config_manager import ConfigManager
from orpheus.utils.constants import DEFAULT_VALUES


class _ComponentBase(ABC):
    """
    Base class for all components (Scaling, FeatureAdding, FeatureRemoving, HyperTuner, etc.)
    """

    @abstractmethod
    def __init__(
        self,
        scoring: Optional[Callable] = None,
        maximize_scoring: bool = True,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
        config_path: str = "",
    ) -> None:
        """
        scoring: Callable = None
            custom scoring function to be used in getting score.
            Use together with maximize_scoring to specify
            whether this function needs to be maximized or mimimized.
            if None, "score" method from estimator will be used.
            NOTE: Custom score functions should be imported from a seperate .py file!
            This is due to the nature of multiprocessing in python.

        maximize_scoring: bool = True
            use if custom `scoring` function is passed.
            Decide whether passed `scoring` function needs to be maximized or minimized.
            By default, 'scoring` function is maximized.

        estimator_list: list = None
            List of estimators. Provide a list with uncalled estimators,
            like for example: [RandomForestClassifier, LogisticRegression]

        type_estimator: str = None : {'None', 'regressor', 'classifier'}
            manually choose the estimatortype suited for the problem.
            By doing this, an estimator_list doesnt need to be provided.
            if None, type_estimator will be determined automatically.

        num_workers: int = DEFAULT_VALUES["n_jobs"]
            number of workers to be used for parallel processing processes.
            This will apply for every method in the HyperTuner class where parallel processing is possible.

        config_path : str = ""
            Load configurations from a .yaml file. If a path to a yaml file is provided,
            the configurations will be loaded from that file.
            If an empty string is provided, no configurations will be loaded.
        """
        self.scoring = scoring
        self.maximize_scoring = maximize_scoring
        self.type_estimator = type_estimator
        self.num_workers = num_workers

        if config_path:
            ConfigManager.load_config_from_yaml(self, config_path)
