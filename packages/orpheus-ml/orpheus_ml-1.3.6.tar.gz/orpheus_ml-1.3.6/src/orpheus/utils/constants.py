"""Constants used in the package."""

import multiprocessing as mp

# colors for printing
COLOR_CODES = {
    "INFO": "\033[31;1m",  # Red, bright
    "NOTICE": "\033[34;1m",  # Blue, bright
    "ERROR": "\033[37;22m",  # White, normal
}


# Common parameters in the package
DEFAULT_VALUES = {
    "verbose": 3,
    "n_jobs": max(1, mp.cpu_count() // 2),
}


# prevent common estimator parameters without procedural use
# from being added to paramgrid in during HyperTuner.fit()
ARGS_TO_IGNORE_HYPERTUNER = {
    "cache_size",
    "random_state",
    "verbose",
    "verbos",
    "break_ties",
    "n_jobs",
    "input_dim",
    "output_dim",
    "device",
}

# order of adding for FeatureAdding class
ORDER_OF_ADDING = [
    "add_features",
    "add_lags",
    "add_rolling_stats",
]

# order of removing for FeatureRemoving class
ORDER_OF_REMOVING = [
    "remove_features_by_correlation",
    "remove_features_by_selection",
    "remove_features_by_top_n",
]

# weights for round 2 of HyperTuner.fit
R2_WEIGHTS = {"best_mean": 0.0, "lowest_stdev": 0.0, "amount_of_unique_vals": 0.0}


# used to link methods in the configfile to additional comments
ADDITIONAL_METHOD_COMMENTS_FOR_CONFIG = {
    "scale": "Compare multiple scaling methods per fold and select the best one.",
    "add_features": "Add recommended features to the dataset in an automated fashion.",
    "add_lags": "Add lagged features to the dataset. Special option for time series data. NOTE: If used, make sure that inputdata is at least 2 times the size of the largest lag.",
    "add_rolling_stats": "Add statistics of a rolling window to the dataset. Special option for time series data. NOTE: If used, make sure that inputdata is at least 2 times the size of the largest lag.",
    "sequential_order_of_adding": "Decide the order of adding features to the dataset.",
    "remove_features_by_correlation": "Removes both highly correlated features and features with a low correlation with the target variable. Relatively fast and accurate.",
    "remove_features_by_selection": "Remove features by a RFECV algorithm. Useful for getting insight in the importance of features. Slow, but very accurate.",
    "remove_features_by_top_n": "Keeps only the top N features by using a linear model. Very fast, but not very accurate if features have a non-linear relationship with the target variable.",
    "sequential_order_of_removing": "Decide the order of removing features from the dataset.",
    "fit": "Fit models to the dataset per fold through a three-round process through automated hyperparameter tuning",
}


min_features_to_keep = "This number of features which will always be left in the dataset as minimum, although more features may also remain."
top_n_features = "Top N number of features to keep in the dataset. Contrary to 'min_features_to_keep', amount of features is deducted until its exactly N. If -1, all features are kept."

# used to add comments to the yaml config file
CONFIG_COMMENTS = {
    "Scaling": {
        "scale": {
            "timeout": "Timeout for the scaling process in seconds. If null, no timeout is set. Note that the timeout is per fold.",
            "columns_to_scale": "Pass multiple columns in a list as groups to scale together. If null, all columns are scaled.",
            "compare_to_unscaled_data": "If True, unscaled data is also taken into scoring process.",
            "penalty_to_score_if_overfitting": "0.0 <= float <= 1.0. Apply a penalty to the score if overfitting occurs during classification. If 0.0, no penalty is applied.",
            "random_subset": "0.0 < float <= 1.0. Each estimator will be fitted on a random subset of the data during each iteration per round. This is useful to speed up fitting and prevent overfitting. If 1.0, no random subset is used.",
        },
    },
    "FeatureAdding": {
        "add_features": {
            "max_added_features": "Maximum number of features to add. If -1, all possible features are added. If N > 0, N features will be added randomly.",
            "ignore_columns": "List of columns to ignore when adding features.",
        },
        "add_lags": {
            "column_to_extract_lags_from": "Column to extract lags from. If null, the column with the highest correlation with y will be used. If 'all', all eligible columns will be used. Last 'upper_bound' rows will be automaticly dropped in each train and testset to prevent leakage of data. ",
            "lower_bound": "Lower bound of lags. Must be lower than 'upper_bound' and 0 or higher.",
            "upper_bound": "Upper bound of lags. Given inputdats is a timeseries, must be higher than lower_bound and at least 1 to have effect. upper_bound is inclusive.",
        },
        "add_rolling_stats": {
            "column_to_extract_stats_from": "Column to extract rolling stats from. If null, the column with the highest correlation with y will be used. If 'all', all eligible columns will be used. First 'upper_bound' rows will be automaticly dropped in each train and testset to prevent leakage of data.",
            "lower_bound": "Lower bound of rolling timeperiod. Must be lower than 'upper_bound' and 0 or higher.",
            "upper_bound": "Upper bound of rolling timeperiod. Given inputdats is a timeseries, must be higher than lower_bound and at least 1 to have effect. upper_bound is inclusive",
        },
        "sequential_order_of_adding": {
            "order": f"List of feature adding steps to be executed in sequential order. Turn on/off by adding/removing from {ORDER_OF_ADDING}."
        },
    },
    "FeatureRemoving": {
        "remove_features_by_correlation": {
            "n_steps": "Amount of steps to iterate in the search_space of the correlation-threshold between 1 downwards to 0.05. The higher the amount, the smaller the steps in the search-space will be.",
            "min_features_to_keep": min_features_to_keep,
            "early_stopping": "If True, iterations will be halted as soon as the current step has a worse score than the previous step.",
        },
        "remove_features_by_selection": {
            "n_steps_per_iter": "`n_steps_per_iter` corresponds to the (integer) number of features to remove at each iteration. Increase the amount to speed up the process.",
            "min_features_to_keep": min_features_to_keep,
            "top_n_features": top_n_features,
            "plotting": "If True, see plots about feature importance and cross-validation scores aqcuired during feature selection.",
        },
        "remove_features_by_top_n": {
            "top_n_features": top_n_features,
        },
        "sequential_order_of_removing": {
            "order": f"List of feature removal steps to be executed in sequential order. Turn on/off by adding/removing from {ORDER_OF_REMOVING}.",
            "use_scoring_for_random_forest_selection": "Use the scoring function for optimizing the RandomForest estimator in feature selection if no custom estimator is provided, defaulting to r2 or accuracy. Applies to steps: 'remove_features_by_selection', 'remove_features_by_correlation'.",
            "random_subset": "0.0 < float <= 1.0. Only a random subset will be removed during the entire process of feature removing. This is useful to speed up the whole process. If 1.0, no random subset is used.",
        },
    },
    "HyperTuner": {
        "fit": {
            "R1_timeout": "Timeout for the first round of hyperparameter tuning in seconds. If null, no timeout is set. Note that the timeout is per fold.",
            "R2_timeout": "Timeout for the second round of hyperparameter tuning in seconds. If null, no timeout is set. Note that the timeout is per fold.",
            "R3_timeout": "Timeout for the third round of hyperparameter tuning in seconds. If null, no timeout is set. Note that the timeout is per fold.",
            "R2_R3_max_iter": "Maximum number of iterations for the second and third round of hyperparameter tuning. If null, no maximum is set.",
            "R2_R3_amt_params": "Max amount of parameters to tune in the second and third round of hyperparameter tuning.",
            "R2_R3_exclude_params": "List of words of hyperparameters to exclude from the paramgrid in the second and third round of hyperparameter tuning. Words do not have to be exact matches, but can be substrings of hyperparameters.",
            "R2_n_vals_per_param": "Number of values to try for each parameter in the second round of hyperparameter tuning.",
            "R1_amt_surviving_models": "Amount of models to survive to the second round of hyperparameter tuning.",
            "R1_exclude_models": "List of models to exclude from the first round of hyperparameter tuning and directly move to the second round of hyperparameter tuning. If null, no models are excluded.",
            "R2_include_string_args": "If True, estimator-parameters which accept values of type string, are also included in the second round of hyperparameter tuning. NOTE: This option can be buggy. If you get unknown errors, try setting this to False.",
            "R2_weights": "Weights for the different metrics in the second round of hyperparameter tuning. Pass as dict with values of 3 floats, representing weights for:  1. best mean, 2. lowest standarddeviation and 3. amount of unique scores respectfully. If values are all 0.0, no weights are applied.",
            "R2_int_distance_factor": "Factor to determine the distance between integer values in the second round of hyperparameter tuning. It is recommended to keep this larger than `R3_int_distance_factor` to keep the searching space wide, because R2 is a random gridsearch.",
            "R2_float_distance_factor": "Factor to determine the distance between float values in the second round of hyperparameter tuning. It is recommended to keep this larger than `R3_float_distance_factor` to keep the searching space wide, because R2 is a random gridsearch.",
            "R3_min_correlation_to_best_score": "0.0 < float < 1.0. If correlation to best score of a parameter >= `R3_min_correlation_to_best_score`, every parameter with correlation equal or above this threshold will be used for R3_gridsearch. One percent of correlation equals 0.01.",
            "R3_int_distance_factor": "Factor to determine the distance between integer values in the third round of hyperparameter tuning. It is recommended to extensively narrow this value down in comparison to `R2_int_distance_factor`, because R3 will look for improvements in a small searchspace",
            "R3_float_distance_factor": "Factor to determine the distance between float values in the third round of hyperparameter tuning. It is recommended to extensively narrow this value down in comparison to `R2_float_distance_factor`, because R3 will look for improvements in a small searchspace.",
            "amt_top_models_saved_per_round": "Amount of top models to save per round. This is important, as all trained models which will be deployed in the end, derive from this metric. On the other hand, not using this properly can lead to excessive memory usage.",
            "penalty_to_score_if_overfitting": "0.0 <= float <= 1.0. Apply a penalty to the score if overfitting occurs during classification. If 0.0, no penalty is applied.",
            "random_subset": "0.0 < float <= 1.0. Each estimator will be fitted on a random subset of the data during each iteration per round. This is useful to speed up fitting and prevent overfitting. If 1.0, no random subset is used.",
            "random_subset_factor": "float >= 1.0. The size of the random subset is determined by multiplying the amount of samples in the dataset with this factor after each round. Only used between rounds if `random_subset` is less than 1.0.",
        },
    },
}
