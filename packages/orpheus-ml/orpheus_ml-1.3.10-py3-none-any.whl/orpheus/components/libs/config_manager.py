"""Configmanager for creating and reading configuration files for the ComponentService class in YAML format."""


import os
from collections import OrderedDict
from copy import deepcopy
from functools import partial, reduce
from typing import Any, Dict, Iterable, List

import pandas as pd
import ruamel.yaml
import ruamel.yaml.comments
from ruamel.yaml.comments import CommentedMap

from orpheus.utils.constants import ADDITIONAL_METHOD_COMMENTS_FOR_CONFIG, CONFIG_COMMENTS
from orpheus.utils.custom_types import PredictorType
from orpheus.utils.helper_functions import get_default_args, get_obj_name
from orpheus.utils.logger import logger


class ConfigManager:
    """
    Class for creating and reading configuration files in YAML format.

    public static methods
    ----------
    create_config(config_path, *classes_to_create_config_for)
        Create a configuration file for the given classes. If the file already exists, the configuration is appended.

    load_config_from yaml(obj, config_path)
        Load configuration from a YAML file. Call this method in the `__init__` method of a class that accepts a 'config_path' parameter.

    """

    @staticmethod
    def create_config(config_path: str, *classes_to_create_config_for: Any) -> None:
        """Create a configuration file for the given classes. If the file already exists, the configuration is appended.

        Parameters
        ----------
        config_path : str
            Path to the configuration file. Must end with .yaml
        *classes_to_create_config_for : object
            Classes to create configuration for. These will be written to the configuration file.
        """
        for obj in classes_to_create_config_for:
            public_method_dict = ConfigManager._gather_public_methods_from_class(obj)
            ConfigManager.write_or_update_config(public_method_dict, config_path)

        ConfigManager._reload_config_to_add_comments(config_path)

        logger.notice(
            f"Created configuration {config_path} for {[get_obj_name(obj) for obj in classes_to_create_config_for]}.",
        )
        logger.notice("Run the program again to apply the configuration to the components.")

    @staticmethod
    def load_config_from_yaml(obj, config_path: str):
        """Load configuration from a YAML file. Call this method in the `__init__` method of a class that accepts a 'config_path' parameter.

        Parameters
        ----------
        obj : object
            Object to load the configuration for.
        config_path : str
            Path to the configuration file. Must end with .yaml
        """
        with open(config_path, "r", encoding="utf-8") as y:
            contents = ruamel.yaml.load(y)[get_obj_name(obj)]
            ConfigManager._set_methods(obj, contents)
            logger.notice(
                f"Loaded configuration {config_path} for {get_obj_name(obj)}.",
            )

    @staticmethod
    def write_or_update_config(entry: dict, path: str) -> None:
        """
        create and write a config to path if it does not exist, update the configpath if it does exist

        Parameters
        ----------
        entry : dict
            dictionary with the following structure:
            {class_name: {method_name: parameters}}

        path : str
            path to the config file
        """
        component_keys = ["Scaling", "FeatureAdding", "FeatureRemoving", "HyperTuner"]

        # write
        if not os.path.isfile(path):
            config = dict(OrderedDict.fromkeys(component_keys))
            config.update(entry)
            with open(path, mode="w", encoding="utf-8") as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping=4, sequence=4, offset=2)
                yaml.dump(config, file)
        # update
        else:
            with open(path, encoding="utf-8") as f:
                config = ruamel.yaml.round_trip_load(f)
            config.update(entry)
            with open(path, mode="w", encoding="utf-8") as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping=4, sequence=4, offset=2)
                yaml.dump(config, file)

    @staticmethod
    def write_dict_to_yaml(config_path: str, data: dict, add_comments: bool = True) -> None:
        """Writes a Python dictionary to a YAML file.

        Parameters
        ----------
        file_path : str
            The file path where the YAML file will be saved.
        data : dict
            The Python dictionary to be written to the YAML file.
        """
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=4, sequence=4, offset=2)
        with open(config_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(data, yaml_file)

        if add_comments:
            ConfigManager._reload_config_to_add_comments(config_path)

        logger.notice(f"Saved dictionary to YAML file {config_path}")

    @staticmethod
    def dicts_to_features(dicts: Iterable[dict]) -> pd.DataFrame:
        """
        Convert an Iterable with dictionaries to a pandas DataFrame with features as columns and parameters as rows,
        where each row represents a sample.
        """
        if not hasattr(dicts, "__iter__"):
            raise TypeError("dicts must be an Iterable")
        if not all(isinstance(d, dict) for d in dicts):
            raise TypeError("dicts must contain only dictionaries")
        df = pd.DataFrame()
        for d in dicts:
            flattened = flatten_dict(d)
            df = pd.concat([df, pd.DataFrame([flattened])], axis=0, ignore_index=True)

        return df

    @staticmethod
    def features_to_dicts(df: pd.DataFrame) -> List[dict]:
        """
        Convert a pandas DataFrame with features as columns and parameters as rows to a list of dictionaries,
        where each dictionary represents a row (sample) in the DataFrame.
        """
        nested_dicts = []
        for _, row in df.iterrows():
            flat_dict = row.to_dict()
            nested_dict = nested_dict_from_flat(flat_dict)
            nested_dicts.append(nested_dict)
        return nested_dicts

    @staticmethod
    def _reload_config_to_add_comments(config_path: str):
        with open(config_path, encoding="utf-8") as file:
            config = ruamel.yaml.round_trip_load(file)

        config = add_comments_to_config(config, CONFIG_COMMENTS)
        yaml = ruamel.yaml.YAML()
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file)

    @staticmethod
    def _set_methods(obj: Any, contents) -> None:
        """Set all public methods of an object through the contents read from a YAML file.

        Parameters
        ----------
        obj : object
            Object to set the methods for.
        contents : dict
            Contents read from a YAML file.
        """
        for method_name, parameters in contents.items():
            method = getattr(obj, method_name)
            method = partial(method, **parameters)
            setattr(obj, method_name, method)

    @staticmethod
    def _gather_public_methods_from_class(obj: Any) -> dict:
        """
        gather all public methods from a class.
        If a method starts with an underscore, it is ignored.

        returns:
        ---
            dict: {class_name: {method_name: parameters}}
        """
        public_method_list = [
            func
            for func in dir(obj)
            if callable(getattr(obj, func)) and not func.startswith(("_", "__")) and func not in {"load"}
        ]
        param_dict = {func: get_default_args(getattr(obj, func)) for func in public_method_list}
        param_dict_copy = deepcopy(param_dict)
        for method, params in param_dict_copy.items():
            for param, val in params.items():
                if (
                    not isinstance(val, (str, int, float, list, dict, bool, type(None)))
                    or (param.startswith("_"))
                    or (("estimator") in param)
                ):
                    if isinstance(val, PredictorType):
                        param_dict[method][param] = val.value
                    else:
                        del param_dict[method][param]

        return {get_obj_name(obj): param_dict}


def add_comments_to_config(config: CommentedMap, comments: dict):
    """Add comments to a YAML file. config must be loaded with ruamel.yaml.round_trip_load."""
    config.yaml_set_start_comment(
        "Configuration file for ComponentService or PipelineOrchestrator classes. Use in conjuction with `ComponentService.initialize()` or `PipelineOrchestrator.build()` methods. All steps are executed in the order they are defined in this file."
    )

    for component, methods in config.items():
        config.yaml_set_comment_before_after_key(component, before="\n")
        config.yaml_set_comment_before_after_key(component, before=f"{component} component")
        if isinstance(methods, CommentedMap):
            new_methods = CommentedMap()
            for key, value in methods.items():
                key_path = f"{component}.{methods}"
                method_str = f"{key} method."
                if key in ADDITIONAL_METHOD_COMMENTS_FOR_CONFIG:
                    method_str += f" {ADDITIONAL_METHOD_COMMENTS_FOR_CONFIG[key]}"
                new_methods.yaml_set_comment_before_after_key(key, before=method_str, indent=2)
        config[component] = new_methods
        for method, params in methods.items():
            if isinstance(params, CommentedMap):
                # If the parameter is a CommentedMap, create a new dictionary
                # with comments added
                new_params = CommentedMap()
                for param, value in params.items():
                    # Add a comment before each key in the CommentedMap
                    key_path = f"{component}.{method}.{param}"
                    comment = get_nested_value_with_dotted_key(comments, key_path)
                    new_params.yaml_set_comment_before_after_key(param, before=comment, indent=4)
                    # Add the value to the new dictionary. If None, the value
                    # is not added
                    new_params[param] = value
            else:
                raise ValueError("Parameter must be a CommentedMap or CommentedSeq")
            # Set the new parameter with comments added to the original
            # dictionary
            config[component][method] = new_params

    return config


def flatten_dict(d: dict, parent_key="", sep=".") -> dict:
    """Flatten a nested dictionary."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def set_nested_item(dct, keys, value):
    """Set a value in a nested dictionary."""
    for key in keys[:-1]:
        dct = dct.setdefault(key, {})
    dct[keys[-1]] = value


def nested_dict_from_flat(flat_dict):
    """Convert a flat dictionary with dot-separated keys to a nested dictionary."""
    nested_dict = {}  # Using a regular dict here
    for key, value in flat_dict.items():
        keys = key.split(".")
        set_nested_item(nested_dict, keys, value)
    return nested_dict


def get_nested_value_with_dotted_key(dictionary, keys, default=None):
    """Get a value from a nested dictionary with key passed as strings with dots."""
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def set_nested_value_with_dotted_key(data: Dict[str, Any], key: str, value: Any) -> None:
    """Set a value in a nested dictionary using dotted notation."""
    keys = key.split(".")
    d = data
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value
