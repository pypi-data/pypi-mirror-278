"""Define the schema for the config file of the ComponentService class."""

from schema import And, Or
from featuretools import primitives

from orpheus.utils.constants import ORDER_OF_ADDING, ORDER_OF_REMOVING

valid_transformatives = set(primitives.get_transform_primitives().keys())
valid_transformatives.add("all")

config_schema = {
    "Scaling": {
        "scale": {
            "timeout": Or(
                And(
                    int,
                    lambda n: n >= 0,
                    error="timeout should be a positive integer or None",
                ),
                None,
            ),
            "columns_to_scale": Or(
                And(
                    [[str]],
                    error="columns_to_scale should be a list of inner lists, where each list represents a group of valid columnnames passed as strings.",
                ),
                None,
            ),
            "compare_to_unscaled_data": bool,
            "penalty_to_score_if_overfitting": And(
                float,
                lambda n: 0 <= n <= 1,
                error="penalty_to_score_if_overfitting should be a float between 0.0 and 1.0",
            ),
            "random_subset": And(
                float,
                lambda n: 0 < n <= 1,
                error="random_subset should be a float between 0.0 and 1.0(inclusive)",
            ),
        }
    },
    "FeatureAdding": {
        "add_features": {
            "max_added_features": And(
                int,
                lambda n: n >= -1 and n != 0,
                error="max_added_features should be a positive integer or -1",
            ),
            "ignore_columns": Or(
                And(
                    [str],
                    error="ignore_columns should be a list of strings with valid columnnames",
                ),
                None,
            ),
        },
        "add_lags": {
            "column_to_extract_lags_from": Or(str, None),
            "lower_bound": And(int, lambda n: n >= 0),
            "upper_bound": And(int, lambda n: n >= 0),
        },
        "add_rolling_stats": {
            "column_to_extract_stats_from": Or(str, None),
            "lower_bound": And(int, lambda n: n >= 0),
            "upper_bound": And(int, lambda n: n >= 0),
        },
        "sequential_order_of_adding": {
            "order": And(
                [str],
                lambda lst: len(lst) <= 3 and all(s in ORDER_OF_ADDING for s in lst),
                error=f"order of adding should be a list of max. 3 strings, being of values: {ORDER_OF_ADDING}",
            )
        },
    },
    "FeatureRemoving": {
        "remove_features_by_correlation": {
            "n_steps": And(
                int,
                lambda n: n > 1,
                error="n_steps should be a positive integer greater than 1. Range: n > 1. Type: int",
            ),
            "min_features_to_keep": And(
                int,
                lambda n: n >= 1,
                error="min_features_to_keep should be a positive integer. Range: n >= 1. Type: int",
            ),
            "early_stopping": bool,
        },
        "remove_features_by_selection": {
            "n_steps_per_iter": And(
                int,
                lambda n: n >= 1,
                error="n_steps_per_iter should be a positive integer. Range: n >= 1. Type: int",
            ),
            "min_features_to_keep": And(
                int,
                lambda n: n >= 1,
                error="min_features_to_keep should be a positive integer. Range: n >= 1. Type: int",
            ),
            "top_n_features": And(
                Or(int, And(float, lambda n: 0 <= n <= 1)),
                lambda n: n >= -1 and n != 0,
                error="top_n_features should be a positive integer, -1, or a float between 0 and 1. Range: n >= -1 and n != 0. Type: int or float",
            ),
            "plotting": bool,
        },
        "remove_features_by_top_n": {
            "top_n_features": And(
                Or(int, And(float, lambda n: 0 <= n <= 1)),
                lambda n: n >= -1 and n != 0,
                error="top_n_features should be a positive integer, -1, or a float between 0 and 1. Range: n >= -1 and n != 0. Type: int or float",
            )
        },
        "sequential_order_of_removing": {
            "order": And(
                [str],
                lambda lst: len(lst) <= 3 and all(s in ORDER_OF_REMOVING for s in lst),
                error=f"order of removing should be a list of max. 3 strings, being of values: {ORDER_OF_REMOVING}",
            ),
            "use_scoring_for_random_forest_selection": And(
                bool,
                error="use_scoring_for_random_forest_selection should be a boolean. Type: bool",
            ),
            "random_subset": And(
                float,
                lambda n: 0 < n <= 1,
                error="random_subset should be a float between 0.0 and 1.0(inclusive). Range: 0.0 < n <= 1.0. Type: float",
            ),
        },
    },
    "HyperTuner": {
        "fit": {
            "R1_timeout": Or(
                None,
                And(
                    int,
                    lambda n: n >= 0,
                    error="R1_timeout should be a positive integer or None. Range: n >= 0. Type: int or None",
                ),
            ),
            "R2_timeout": Or(
                None,
                And(
                    int,
                    lambda n: n >= 0,
                    error="R2_timeout should be a positive integer or None. Range: n >= 0. Type: int or None",
                ),
            ),
            "R3_timeout": Or(
                None,
                And(
                    int,
                    lambda n: n >= 0,
                    error="R3_timeout should be a positive integer or None. Range: n >= 0. Type: int or None",
                ),
            ),
            "R2_R3_max_iter": And(
                int,
                lambda n: n >= 1,
                error="R2_R3_max_iter should be a positive integer. Range: n >= 1. Type: int",
            ),
            "R2_R3_amt_params": And(
                int,
                lambda n: n >= 1,
                error="R2_R3_amt_params should be a positive integer. Range: n >= 1. Type: int",
            ),
            "R2_R3_exclude_params": Or(
                None,
                And(
                    [str],
                    lambda lst: all(isinstance(s, str) for s in lst),
                    error="R2_R3_exclude_params should be a list of string or None. Type: list or None",
                ),
            ),
            "R2_n_vals_per_param": And(
                int,
                lambda n: n >= 1,
                error="R2_n_vals_per_param should be a positive integer. Range: n >= 1. Type: int",
            ),
            "R1_amt_surviving_models": And(
                int,
                lambda n: n >= 1,
                error="R1_amt_surviving_models should be a positive integer. Range: n >= 1. Type: int",
            ),
            "R1_exclude_models": Or(
                None,
                And(
                    [str],
                    lambda lst: all(isinstance(s, str) for s in lst),
                    error="R1_exclude_models should be a list of string or None. Type: list or None",
                ),
            ),
            "R2_include_string_args": bool,
            "R2_weights": And(
                dict,
                lambda d: len(d) == 3 and all(0 <= w <= 1 for w in d.values()),
                error="R2_weights should be a dict of 3 positive floats between 0.0 and 1.0 as values. Range: 0.0 >= n >= 1.0. Type: dict[str, float]",
            ),
            "R2_int_distance_factor": And(
                float,
                lambda n: n > 1,
                error="R2_int_distance_factor should be a float greater than 1.0. Range: n > 1.0. Type: float",
            ),
            "R2_float_distance_factor": And(
                float,
                lambda n: n > 1,
                error="R2_float_distance_factor should be a float greater than 1.0. Range: n > 1.0. Type: float",
            ),
            "R3_min_correlation_to_best_score": And(
                float,
                lambda n: 0 < n < 1,
                error="R3_min_correlation_to_best_score should be a float between 0.0 and 1.0. Range: 0.0 < n < 1.0. Type: float",
            ),
            "R3_int_distance_factor": And(
                float,
                lambda n: n > 1,
                error="R3_int_distance_factor should be a float greater than 1.0. Range: n > 1.0. Type: float",
            ),
            "R3_float_distance_factor": And(
                float,
                lambda n: n > 1,
                error="R3_float_distance_factor should be a float greater than 1.0. Range: n > 1.0. Type: float",
            ),
            "amt_top_models_saved_per_round": And(
                int,
                lambda n: n >= 1,
                error="amt_top_models_saved_per_round should be a positive integer. Range: n >= 1. Type: int",
            ),
            "penalty_to_score_if_overfitting": And(
                float,
                lambda n: 0 <= n <= 1,
                error="penalty_to_score_if_overfitting should be a float between 0.0 and 1.0(inclusive). Range: 0.0 <= n <= 1.0. Type: float",
            ),
            "random_subset": And(
                float,
                lambda n: 0 < n <= 1,
                error="random_subset should be a float between 0.0 and 1.0(inclusive). Range: 0.0 < n <= 1.0. Type: float",
            ),
            "random_subset_factor": And(
                float,
                lambda n: n >= 1.0,
                error="random_subset_factor should be a 1.0 or higher. Range: n >= 1.0. Type: float",
            ),
        },
    },
}


def validate_bounds_FeatureAdding(d: dict) -> None:
    """Validate the bounds for the FeatureAdding class."""
    for k, v in d.items():
        if k in {"add_lags", "add_rolling_stats"}:
            lower_bound = v.get("lower_bound")
            upper_bound = v.get("upper_bound")
            if lower_bound != 0 and upper_bound != 0 and lower_bound >= upper_bound:
                raise ValueError(f"In {k}, lower_bound {lower_bound} must be less than upper_bound {upper_bound}.")
            elif upper_bound != 0 and upper_bound <= lower_bound:
                raise ValueError(f"In {k}, upper_bound {upper_bound} must be greater than lower_bound {lower_bound}.")
