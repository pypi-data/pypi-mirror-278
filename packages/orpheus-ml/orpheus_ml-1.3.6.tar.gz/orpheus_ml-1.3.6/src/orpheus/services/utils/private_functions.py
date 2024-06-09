"""
Private functions which are essential for ComponentService class.
Organized here to keep ComponentService class clean.
"""

import multiprocessing as mp
import time
import traceback
from copy import deepcopy
from functools import partial
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, OrdinalEncoder

from orpheus.components.hypertuner.hypertuner import HyperTuner
from orpheus.components.hypertuner.hypertuner_stacked import HyperTunerStacked
from orpheus.components.preprocessing.constants import SCALERS
from orpheus.components.preprocessing.downcasting import Downcasting
from orpheus.components.preprocessing.feature_adding import FeatureAdding
from orpheus.components.preprocessing.feature_removing import FeatureRemoving
from orpheus.components.preprocessing.scaling import Scaling
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.utils.constants import DEFAULT_VALUES
from orpheus.utils.custom_estimators import MultiEstimatorWrapper, PredictFuncWrapper
from orpheus.utils.custom_transformers import FeatureTransformerWrapper, replace_special_chars_in_columns
from orpheus.utils.custom_types import PredictorType
from orpheus.utils.helper_functions import ensure_numpy, get_obj_name
from orpheus.utils.logger import logger
from orpheus.utils.type_vars import CrossValidatorType, EstimatorType, ScalerType


def _stacked_predict(
    hypertuner_stacked: HyperTunerStacked,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    top_n_per_tuner: Optional[int] = None,
    stacked: bool = True,
    stacked_unfit: bool = True,
    voting_hard: bool = True,
    voting_hard_unfit: bool = True,
    voting_soft: bool = True,
    voting_soft_unfit: bool = True,
    averaged: bool = True,
    averaged_weighted: bool = True,
    averaged_predictor: Optional[Union[PredictorType, int]] = None,
    stacked_final_estimator: Optional[EstimatorType] = None,
    timeout_duration: Optional[int] = None,
) -> Tuple[pd.DataFrame, Dict[str, HyperTunerStacked]]:
    df = pd.DataFrame()
    fitted_models_dict = dict.fromkeys(
        [
            "stacked",
            "stacked_unfit",
            "voting_hard",
            "voting_hard_unfit",
            "voting_soft",
            "voting_soft_unfit",
        ]
    )

    def succes_msg(s, top_n_per_tuner):
        logger.notice(f"Successfully finished {s} for top_n={top_n_per_tuner}")

    def error_msg(s, top_n_per_tuner):
        logger.error(f"Prediction for {s} with top_n={top_n_per_tuner} failed!")
        logger.error(traceback.format_exc())

    if stacked:
        try:
            fitted = hypertuner_stacked.fit_stacked(
                X_train,
                y_train,
                top_n_per_tuner=top_n_per_tuner,
                _final_estimator=stacked_final_estimator,
                timeout_duration=timeout_duration,
            )
            df["stacked"] = fitted.predict(X_test)
            fitted_models_dict["stacked"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("stacked", top_n_per_tuner)
        except Exception:
            error_msg("stacked", top_n_per_tuner)

    if stacked_unfit:
        try:
            fitted = hypertuner_stacked.fit_stacked(
                X_train,
                y_train,
                top_n_per_tuner=top_n_per_tuner,
                unfit=True,
                _final_estimator=stacked_final_estimator,
                timeout_duration=timeout_duration,
            )
            df["stacked_unfit"] = fitted.predict(X_test)
            fitted_models_dict["stacked_unfit"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("stacked_unfit", top_n_per_tuner)
        except Exception:
            error_msg("stacked_unfit", top_n_per_tuner)

    if voting_hard:
        try:
            fitted = hypertuner_stacked.fit_voting(
                X_train, y_train, voting="hard", top_n_per_tuner=top_n_per_tuner, timeout_duration=timeout_duration
            )
            df["voting_hard"] = fitted.predict(X_test)
            fitted_models_dict["voting_hard"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("voting_hard", top_n_per_tuner)
        except Exception:
            error_msg("voting_hard", top_n_per_tuner)

    if voting_hard_unfit:
        try:
            fitted = hypertuner_stacked.fit_voting(
                X_train,
                y_train,
                voting="hard",
                top_n_per_tuner=top_n_per_tuner,
                unfit=True,
                timeout_duration=timeout_duration,
            )
            df["voting_hard_unfit"] = fitted.predict(X_test)
            fitted_models_dict["voting_hard_unfit"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("voting_hard_unfit", top_n_per_tuner)
        except Exception:
            error_msg("voting_hard_unfit", top_n_per_tuner)

    if voting_soft:
        try:
            fitted = hypertuner_stacked.fit_voting(
                X_train, y_train, voting="soft", top_n_per_tuner=top_n_per_tuner, timeout_duration=timeout_duration
            )
            df["voting_soft"] = fitted.predict(X_test)
            fitted_models_dict["voting_soft"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("voting_soft", top_n_per_tuner)
        except Exception:
            error_msg("voting_soft", top_n_per_tuner)

    if voting_soft_unfit:
        try:
            fitted = hypertuner_stacked.fit_voting(
                X_train,
                y_train,
                voting="soft",
                top_n_per_tuner=top_n_per_tuner,
                unfit=True,
                timeout_duration=timeout_duration,
            )
            df["voting_soft_unfit"] = fitted.predict(X_test)
            fitted_models_dict["voting_soft_unfit"] = {f"top_n={top_n_per_tuner}": fitted}
            succes_msg("voting_soft_unfit", top_n_per_tuner)
        except Exception:
            error_msg("voting_soft_unfit", top_n_per_tuner)
    if averaged:
        try:
            df["averaged"] = hypertuner_stacked.predict_averaged(
                _data=X_test,
                top_n_per_tuner=top_n_per_tuner,
                predictor=averaged_predictor,
            )
            succes_msg("averaged", top_n_per_tuner)
        except Exception:
            error_msg("averaged", top_n_per_tuner)

    if averaged_weighted:
        try:
            df["averaged_weighted"] = hypertuner_stacked.predict_averaged(
                _data=X_test,
                weighted=True,
                top_n_per_tuner=top_n_per_tuner,
                predictor=averaged_predictor,
            )
            succes_msg("averaged_weighted", top_n_per_tuner)
        except Exception:
            error_msg("averaged_weighted", top_n_per_tuner)

    return df, fitted_models_dict


def _stacked_predict_range(
    hypertuner_stacked: HyperTunerStacked,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    top_n_per_tuner_range: Union[List[Union[int, int]], Tuple[Union[int, int]]] = [
        1,
        5,
    ],
    stacked: bool = True,
    stacked_unfit: bool = True,
    voting_hard: bool = True,
    voting_hard_unfit: bool = True,
    voting_soft: bool = True,
    voting_soft_unfit: bool = True,
    averaged: bool = True,
    averaged_weighted: bool = True,
    averaged_predictor: Optional[Union[PredictorType, int]] = None,
    stacked_final_estimator: Optional[EstimatorType] = None,
    timeout_duration: Optional[int] = None,
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, HyperTunerStacked]]]:
    """
    Predicts a range of top_n_per_tuner values for a `HyperTunerStacked` object.
    Basicly a wrapper for stacked_predict with a custom range of
    `top_n_per_tuner` (top models per fold) values.

    Parameters
    ----------
    hypertuner_stacked : HyperTunerStacked
        The HyperTunerStacked object to predict from.

    X_train : np.ndarray
        The training data to fit the stacked model.

    X_test : np.ndarray
        The test data to check performance of the stacked model.

    y_train : np.ndarray
        The training labels to fit the stacked model.

    top_n_per_tuner_range : Union[List[Union[int, int]], Tuple[Union[int, int]]], optional
        The range of top_n_per_tuner values to predict, by default [1, 5]
        second number is exclusive.

    timeout_duration : Optional[int], optional
        The max timeout duration in seconds for each model to fit, by default None.
        If None, no timeout will be used.

    Returns:
    --------
    pred_df : pd.DataFrame
        DataFrame containing the predictions for each
        `top_n_per_tuner` value and each predictionmethod.

    fitted_models_dict : Dict[str, Dict[str, HyperTunerStacked]]
        Dictionary containing the fitted models for
        each top_n_per_tuner value and each predictionmethod.
        These fitted models can be used to predict new data and
        needed to be saved if you want to use the
        fitted models for prediction later.
    """

    pred_df = pd.DataFrame()

    if not isinstance(top_n_per_tuner_range, (list, tuple)) or not isinstance(top_n_per_tuner_range[0], int):
        raise TypeError(f"top_n_per_tuner_range must be a list or tuple of integers, not {type(top_n_per_tuner_range)}")

    if not 1 <= top_n_per_tuner_range[0] < top_n_per_tuner_range[1]:
        raise ValueError(
            f"top_n_per_tuner_range must be a list or tuple of length 2 where the first value is greater than or equal to 1 and less than to the second value, not {top_n_per_tuner_range}"
        )

    fitted_models: Dict[str, Dict] = dict.fromkeys(
        [
            "stacked",
            "stacked_unfit",
            "voting_hard",
            "voting_hard_unfit",
            "voting_soft",
            "voting_soft_unfit",
        ],
        dict(),
    )

    for N in range(*top_n_per_tuner_range):
        logger.notice(f"Predicting stacked models on testdata for top_n_per_tuner={N}")
        pred_df_temp, fitted_models_dict = _stacked_predict(
            hypertuner_stacked,
            X_train,
            X_test,
            y_train,
            top_n_per_tuner=N,
            stacked=stacked,
            stacked_unfit=stacked_unfit,
            voting_hard=voting_hard,
            voting_hard_unfit=voting_hard_unfit,
            voting_soft=voting_soft,
            voting_soft_unfit=voting_soft_unfit,
            averaged=averaged,
            averaged_weighted=averaged_weighted,
            averaged_predictor=averaged_predictor,
            stacked_final_estimator=stacked_final_estimator,
            timeout_duration=timeout_duration,
        )

        fitted_models = {
            k: {**v, **(fitted_models_dict[k] if fitted_models_dict[k] is not None else {})}
            for k, v in fitted_models.items()
        }

        pred_df_temp.columns = [
            pred_df_temp.columns,
            [f"top_n={N}" for i in range(len(pred_df_temp.columns))],
        ]
        pred_df = pd.concat([pred_df, pred_df_temp], axis=1)

    pred_df.columns = pred_df.columns.sort_values()

    return pred_df, fitted_models


def _deploy_pipeline_of_stacked_models(
    hypertuner_stacked: HyperTunerStacked,
    pred_df: pd.DataFrame,
    fitted_models: dict,
    y_test: np.ndarray,
    return_top_n_models: int,
    round_floats_in_pred_if_classifier: bool,
) -> Union[Callable, MultiEstimatorPipeline]:
    """
    Deploys a pipeline of the best models from a `HyperTunerStacked` object.
    Insert the dataframe with the predictions from
    the `_stacked_predict_range` function.

    Parameters
    ----------
    hypertuner_stacked : HyperTunerStacked
        The HyperTunerStacked object to predict from.

    pred_df : pd.DataFrame
        The dataframe with the predictions from the stacked_predict_range function.

    fitted_models : dict
        The fitted models from the stacked_predict_range function.

    y_test : np.ndarray
        The test data to predict.

    return_top_n_models : int
        The top number of models to return.

    Returns
    -------
    MultiEstimatorPipeline
        A pipeline object containing multiple estimators.

    """
    maximize_scoring = hypertuner_stacked.maximize_scoring
    scoring = (
        hypertuner_stacked.scoring
        if hypertuner_stacked.scoring is not None
        else r2_score
        if hypertuner_stacked.type_estimator == "regressor"
        else accuracy_score
    )

    def return_valid_scores(y_true, y_pred, current_column: str, round_floats_in_pred_if_classifier: bool):
        """Returns the score if it is valid, else returns np.nan"""
        y_true = ensure_numpy(y_true)
        y_pred = ensure_numpy(y_pred)
        if (
            round_floats_in_pred_if_classifier
            and hypertuner_stacked.type_estimator == "classifier"
            and not all(isinstance(i, int) for i in y_pred)
        ):
            logger.notice(f"Rounding floats in {current_column} up to integers")
            y_pred = np.round(y_pred)
        try:
            return scoring(y_true, y_pred)
        except ValueError as e:
            logger.error(
                f"Scoring failed for y_true and y_pred in {current_column}, where first values are: {y_true[0] if y_true.any() else None, y_pred[0] if y_pred.any() else None} because of a ValueError: {e}",
            )
            return np.nan

    scores = pred_df.apply(
        lambda x: return_valid_scores(
            y_test,
            x,
            current_column=x.name,
            round_floats_in_pred_if_classifier=round_floats_in_pred_if_classifier,
        )
    ).sort_values(ascending=not maximize_scoring)
    logger.notice(
        f"Scores generate_pipeline_for_stacked_models on testdata:\n{scores.to_string(index=True, header=True)}",
    )
    if scores.isnull().all():
        raise ValueError(
            "All scores are NaN. This is probably because the predictions are not valid for the scoring function."
        )

    # Only keep the top_n models with valid scores
    top_n_models_scores = scores[:return_top_n_models].dropna()
    estimators = []

    for (model_type, top_n), score in top_n_models_scores.items():
        if model_type in [
            "stacked",
            "stacked_unfit",
            "voting_hard",
            "voting_hard_unfit",
            "voting_soft",
            "voting_soft_unfit",
        ]:
            try:
                est = fitted_models[model_type][top_n]["estimator"]
            except KeyError:
                logger.error(traceback.format_exc())
                continue
        else:
            est = PredictFuncWrapper(
                partial(
                    hypertuner_stacked.predict_averaged,
                    top_n_per_tuner=int(top_n.split("=")[-1]) if isinstance(top_n, str) else top_n,
                    pipeline=hypertuner_stacked.pipeline,
                    weighted="averaged_weighted" in model_type,
                    use_pipeline=False,
                )
            )
        estimators.append(est)

    # DEPLOY PIPELINE:
    pipeline: MultiEstimatorPipeline = deepcopy(hypertuner_stacked.pipeline)
    estimators_wrapper = MultiEstimatorWrapper(estimators)
    pipeline.steps.append(("estimators", estimators_wrapper))

    scores = top_n_models_scores.to_numpy()
    pipeline.update_scores(scores)

    return pipeline


def _create_preprocessing_pipeline(
    X: pd.DataFrame,
    y: pd.DataFrame,
    cv_obj: CrossValidatorType,
    downcast: bool,
    scale: bool,
    add_features: bool,
    remove_features: bool,
    type_estimator: Literal["regressor", "classifier"],
    estimator_list: List[EstimatorType],
    config_path: str = "",
    return_X: bool = False,
    scoring: Optional[Callable] = None,
    maximize_scoring: bool = True,
    num_workers: int = DEFAULT_VALUES["n_jobs"],
    remove_features_estimator: Optional[EstimatorType] = None,
    ordinal_features: Optional[Dict[str, List[str]]] = None,
    categorical_features: Optional[List[str]] = None,
    categorical_features_pca_variance_threshold: Optional[float] = None,
) -> Union[Tuple[MultiEstimatorPipeline, pd.DataFrame], MultiEstimatorPipeline]:
    """
    Return complete preprocessing pipeline.
    Exclude non-scalable columns from scaling and feature_adding, then add them back before feature_removing.
    For excluding non-scalable columns, there is a seperate pipeline, called 'preprocessing_pipe' .
    This pipeline is later added to the end_to_end pipeline under the step `preprocessing_scalable_cols`.

    Parameters
    ----

    X : array-like of shape (n_samples, n_features)
    y : array-like of shape (n_samples,)
    cv_obj : instantiated Sklearn cross-validation object, imported from sklearn.model_selection
        Examples are KFold, StratifiedKfold, TimeSeriesSplit, etc.
        n_splits must be equal to the number of `HyperTuner` instances
        in list_of_tuners and n_splits must already be set.
    return_X : bool = False
        If True, next to the fitted pipeline, the transformed X will be returned.
    config_path : str = ""
        Load configurations from a .yaml file. If a path to a yaml file is provided,
        the configurations will be loaded from that file.
        If an empty string is provided, no configurations will be loaded.
    downcast : bool = False
        If True, the data will be downcasted to the smallest possible data type.
    add_features : bool = False
        If True, the data will be augmented with new features.
    remove_features : bool = False
        If True, the data will be reduced by removing features.
    scale : bool = False
        If True, the data will be scaled.
    type_estimator: Literal["regressor", "classifier"]
        Type of estimator to be used. Options are 'regressor' and 'classifier'.
    estimator_list : List[EstimatorType]
        List of estimators to be used.
    scoring : Callable = None
        objective function to be used during scaling.
    maximize_scoring : bool = True
        If True, the objective function will be maximized.
        else, it will be minimized.
    num_workers : int = mp.cpu_count()
        Number of workers to be uswd.
    verbose : int = 1
        Verbosity level.
    remove_features_estimator : EstimatorType = None
        Estimator to be used for recursive feature elimination.
    ordinal_features : List[str] = None
        List of ordinal features.
    categorical_features : List[str] = None
        List of categorical features.
    categorical_features_pca_variance_threshold : float = None
        Variance threshold to be used for PCA on categotical features.
        Only active if categorical_features are provided.
        Should be a float between 0 and 1.

    returns
    ---
    preprocessing pipe: pipeline object
    """
    VERBOSE_SKLEARN_OBJECTS: bool = logger.get_verbose() >= 3
    end_to_end_pipe = MultiEstimatorPipeline(
        [],
        metric=scoring,
        maximize_scoring=maximize_scoring,
        type_estimator=type_estimator,
        verbose=logger.get_verbose(),
    )

    # create seperate preprocessing pipeline for non-scalable columns
    preprocessing_pipe = Pipeline(
        [],
        verbose=VERBOSE_SKLEARN_OBJECTS,
    )

    X, end_to_end_pipe = _encode_non_numerical_features(
        X,
        categorical_features=categorical_features,
        categorical_features_pca_variance_threshold=categorical_features_pca_variance_threshold,
        ordinal_features=ordinal_features,
        verbosity_col_transformer=VERBOSE_SKLEARN_OBJECTS,
        end_to_end_pipe=end_to_end_pipe,
    )

    # downcast
    if downcast:
        X = Downcasting.downcast(X)
        y = Downcasting.downcast(y)

        downcast_step = FunctionTransformer(Downcasting.downcast)
        end_to_end_pipe.steps.append(("downcasting", downcast_step))

    # seperate columns which should be untouched by scaling and feature_adding
    # these columns are either binary or ordinal, as categorical columns are already encoded to binary columns
    non_scalable_columns = X.columns[X.nunique() == 2]
    if ordinal_features:
        non_scalable_columns = non_scalable_columns.union(ordinal_features)

    scalable_columns = X.columns[~X.columns.isin(non_scalable_columns)]
    if non_scalable_columns.any():
        non_scalable_X = X[non_scalable_columns]
        X = X[scalable_columns]

    if scale:
        X, scaler_transformer = _create_scaling_transformer_for_pipeline(
            X,
            y,
            cv_obj,
            config_path,
            scoring,
            maximize_scoring,
            estimator_list,
            type_estimator,
            num_workers,
        )
        if scaler_transformer:
            preprocessing_pipe.steps.append(("scaler", scaler_transformer))
        else:
            logger.notice("No scaler was selected, no scaler will be applied to the data")

    if add_features:
        (X, fitted_feature_adding_obj, feature_adding_transformer,) = _create_feature_adding_transformer_for_pipeline(
            X,
            y,
            downcast,
            add_features,
            config_path,
            scoring,
            maximize_scoring,
            num_workers,
            type_estimator,
        )
        preprocessing_pipe.steps.append(("feature_adding", feature_adding_transformer))

        # we need to add the leakage_prevention_slice to the end_to_end_pipe so that it is available in the ComponentService class
        end_to_end_pipe.leakage_prevention_slice = fitted_feature_adding_obj.leakage_prevention_slice

    # replace special characters in columnnames
    X = replace_special_chars_in_columns(X)
    preprocessing_pipe.steps.append(
        (
            "feature_name_cleaner",
            FunctionTransformer(
                replace_special_chars_in_columns,
            ),
        )
    )

    # only apply feature adding and scaling to scalable columns.
    # non-scalable columns will be left untouched by setting remainder="passthrough" in the ColumnTransformer.
    # after this, we will add the non-scalable columns back to X.
    if non_scalable_columns.any():
        X = pd.concat([X, non_scalable_X], axis=1)
        logger.notice(
            f"Added non-scalable columns {non_scalable_X.columns.to_list()} to ColumnTransformer. Amount of columns in X: {X.shape[1]}",
        )
        scalable_col_transformer = ColumnTransformer(
            transformers=[
                (
                    "scalable_col_transformer",
                    preprocessing_pipe,
                    scalable_columns,
                )
            ],
            remainder="passthrough",
            verbose=0 if logger.get_verbose() < 1 else logger.get_verbose(),
            verbose_feature_names_out=False,
        )
        end_to_end_pipe.steps.append(("preprocessing_scalable_cols", scalable_col_transformer))
    else:
        end_to_end_pipe.steps.append(("preprocessing_scalable_cols", preprocessing_pipe))

    if remove_features:
        (X, feature_removing_transformer,) = _create_feature_removing_transformer_for_pipeline(
            X,
            y,
            cv_obj,
            downcast,
            remove_features,
            config_path,
            scoring,
            maximize_scoring,
            num_workers,
            type_estimator,
            remove_features_estimator,
        )

        end_to_end_pipe.steps.append(("feature_removing", feature_removing_transformer))

    if return_X:
        return end_to_end_pipe, X
    return end_to_end_pipe


def _create_scaling_transformer_for_pipeline(
    X,
    y,
    cv_obj,
    config_path,
    scoring,
    maximize_scoring,
    estimator_list,
    type_estimator,
    num_workers,
):
    scaler_scores = {}
    for train_index, test_index in cv_obj.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        scaler_obj = Scaling(
            X_train,
            X_test,
            y_train,
            y_test,
            config_path=config_path,
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            estimator_list=estimator_list,
            type_estimator=type_estimator,
            num_workers=num_workers,
        )
        scores = scaler_obj.scale()
        if not scores:
            raise ValueError(
                "no scaler_scores were returned after scaler_obj.scale()! Please check your configuration file if timeouts are set correctly."
            )

        columns_are_passed = isinstance(list(scores.keys())[0], tuple)
        if columns_are_passed:  # if specific features are passed to scale()
            for feats, scores_temp in scores.items():
                if feats not in scaler_scores:
                    scaler_scores[feats] = {}
                scaler_scores[feats].update(scores_temp)
        else:
            scaler_scores.update(scores)

    best_scaler = _get_best_scaler(scaler_scores, scaler_obj, columns_are_passed)

    if best_scaler:
        logger.notice(f"Best scaler is {best_scaler} and will be applied to the data")

        if isinstance(best_scaler, dict):
            transformers = [
                (f"scaler{idx}", scaler, list(columns))
                for idx, (columns, scaler) in enumerate(best_scaler.items(), start=1)
                if scaler is not None
            ]
            scaler_transformer = ColumnTransformer(transformers, remainder="passthrough")
        else:
            scaler_transformer = best_scaler

        X = scaler_transformer.fit_transform(X)
    else:
        logger.notice("No scaler was selected, no scaler will be applied to the data")
        scaler_transformer = None

    return X, scaler_transformer


def _create_feature_adding_transformer_for_pipeline(
    X,
    y,
    downcast,
    add_features,
    config_path,
    scoring,
    maximize_scoring,
    num_workers,
    type_estimator,
):
    feature_adding_obj = FeatureAdding(
        y=y,
        scoring=scoring,
        config_path=config_path,
        maximize_scoring=maximize_scoring,
        num_workers=num_workers,
        type_estimator=type_estimator,
        downcast=downcast,
    )

    fitted_feature_adding_obj, X = _feature_adding_fit(
        X=X,
        feature_adding_obj=feature_adding_obj,
        add_features=add_features,
    )

    feature_adding_transformer = FeatureTransformerWrapper(fitted_feature_adding_obj, n_jobs=num_workers)

    return X, fitted_feature_adding_obj, feature_adding_transformer


def _create_feature_removing_transformer_for_pipeline(
    X,
    y,
    cv_obj,
    downcast,
    remove_features,
    config_path,
    scoring,
    maximize_scoring,
    num_workers,
    type_estimator,
    remove_features_estimator,
):
    feature_removing_obj = FeatureRemoving(
        scoring=scoring,
        config_path=config_path,
        maximize_scoring=maximize_scoring,
        num_workers=num_workers,
        type_estimator=type_estimator,
        downcast=downcast,
    )

    fitted_feature_removing_obj, X = _feature_removing_fit(
        X=X,
        y=y,
        remove_features=remove_features,
        cv_obj=cv_obj,
        feature_removing_obj=feature_removing_obj,
        remove_features_estimator=remove_features_estimator,
    )

    feature_removing_transformer = FeatureTransformerWrapper(fitted_feature_removing_obj, n_jobs=num_workers)

    return X, feature_removing_transformer


def _feature_adding_fit(
    X,
    feature_adding_obj: FeatureAdding,
    add_features: bool,
) -> Tuple[FeatureAdding, pd.DataFrame]:
    """Fit the FeatureAdding object on X and return X and the fitted object."""
    assert isinstance(
        X, pd.DataFrame
    ), f"in self._pipeline in the FeatureAdding class, data should be a pd.DataFrame, but is {type(X)}.\nError: {traceback.print_stack()}"

    if add_features:
        X = feature_adding_obj.sequential_order_of_adding(_X=X)

    return feature_adding_obj, X


def _feature_removing_fit(
    X,
    y,
    remove_features: bool,
    cv_obj,
    feature_removing_obj: FeatureRemoving,
    remove_features_estimator: Optional[EstimatorType] = None,
) -> Tuple[FeatureRemoving, pd.DataFrame]:
    """Fit the FeatureRemoving object on X and return X and the fitted object."""
    assert isinstance(
        X, pd.DataFrame
    ), f"in self._pipeline in the FeatureRemoving class, data should be a pd.DataFrame, but is {type(X)}.\nError: {traceback.print_stack()}"

    if remove_features:
        X = feature_removing_obj.sequential_order_of_removing(
            _X=X, _y=y, _cv_obj=cv_obj, _estimator=remove_features_estimator
        )
    return feature_removing_obj, X


def _create_hypertuners(
    X: np.ndarray,
    y: np.ndarray,
    cv_obj: CrossValidatorType,
    leakage_prevention_slice=List[Union[int, int]],
    config_path: str = "",
    scoring: Optional[Callable] = None,
    maximize_scoring: bool = True,
    estimator_list: Optional[List[EstimatorType]] = None,
    num_workers: int = DEFAULT_VALUES["n_jobs"],
    type_estimator: Optional[Literal["regressor", "classifier"]] = None,
    random_state: Optional[int] = None,
) -> Union[np.ndarray, np.ndarray, List[HyperTuner]]:
    """
    Fit models on N cross-validations and return list of HyperTuner instances.
    ---
    HyperTuner.tuner_list: list[HyperTuner]
        List of all HyperTuner instances used for cross-validation.
    """
    X = ensure_numpy(X)
    y = ensure_numpy(y)
    # Clearing the tuner_list variable resolves issues caused by
    # using an older hyperTuner instance with trained models that have a
    # different shape, which can cause input data shape mismatches.
    if HyperTuner.tuner_list:
        HyperTuner.tuner_list = []

    # fitting and tuning:
    for fold_idx, (train_index, test_index) in enumerate(cv_obj.split(X, y), start=1):
        if leakage_prevention_slice[0]:
            logger.notice(
                f"Data leakage prevention applied on test and traindata in fold {fold_idx}. First {leakage_prevention_slice[0]} rows removed."
            )
            train_index = train_index[leakage_prevention_slice[0] :]
            test_index = test_index[leakage_prevention_slice[0] :]
        if leakage_prevention_slice[1]:
            logger.notice(
                f"Data leakage prevention applied on test and traindata in fold {fold_idx}. Last {leakage_prevention_slice[1]} rows removed."
            )
            train_index = train_index[: -leakage_prevention_slice[1]]  # pylint: disable=E1130
            test_index = test_index[: -leakage_prevention_slice[1]]  # pylint: disable=E1130
        logger.notice(f"Starting HyperTuner for fold {fold_idx} of {cv_obj.n_splits}")
        if any(leakage_prevention_slice):
            logger.notice(f"Train indexes: {[train_index[0], train_index[-1]]}")
            logger.notice(f"Test indexes: {[test_index[0], test_index[-1]]}")
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        logger.notice(f"Train shape: {X_train.shape}")
        logger.notice(f"Test shape: {X_test.shape}")
        tuner = HyperTuner(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            config_path=config_path,
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            estimator_list=estimator_list,
            random_state=random_state,
            type_estimator=type_estimator,
            num_workers=num_workers,
        )
        tuner.fit()

    return HyperTuner.tuner_list


def _get_best_scaler(
    scaler_scores: Union[dict, None],
    scaler_obj: Scaling,
    columns_are_passed: bool,
) -> Union[dict, ScalerType, None]:
    if not scaler_scores:
        return None

    if columns_are_passed:
        best_scalers = {}
        for feats, scores_temp in scaler_scores.items():
            score_overview = _get_scaler_score_overview(scaler_scores[feats], scaler_obj)
            logger.notice(f"Scaler scores for {feats}:\n{score_overview.to_string()}")
            best_scaler_repr = score_overview.index[0]
            best_scaler = next(
                (i() for i in SCALERS if best_scaler_repr == (get_obj_name(i) + "()")),
                None,
            )
            best_scalers[feats] = best_scaler
        return best_scalers

    score_overview = _get_scaler_score_overview(scaler_scores, scaler_obj)
    logger.notice(f"Scaler scores:\n{score_overview.to_string()}")
    best_scaler_repr = score_overview.index[0]
    best_scaler = next((i() for i in SCALERS if best_scaler_repr == (get_obj_name(i) + "()")), None)
    return best_scaler


def _get_scaler_score_overview(scaler_scores, scaler_obj) -> pd.Series:
    scaler_scores = pd.DataFrame.from_dict(scaler_scores)
    scaler_scores.index = scaler_scores.index.map(str)
    scaler_scores.columns = scaler_scores.columns.map(str)
    score_overview = scaler_scores.groupby(lambda x: x, axis=1).mean().groupby(scaler_scores.index).mean()
    # drop scalers where nan is 40% or more of the values
    score_overview = score_overview.dropna(thresh=score_overview.shape[0] * 0.6, axis=1)
    score_overview = score_overview.mean().sort_values(ascending=not scaler_obj.maximize_scoring)
    return score_overview


def _calculate_time_per_estimator(
    estimator: EstimatorType,
    X: pd.DataFrame,
    y: pd.Series,
) -> Tuple[EstimatorType, Union[float, str]]:
    """
    use in _optimize_estimator_list() to calculate time per estimator
    if succeeds, returns estimator and time it took to fit.
    if fails, returns estimator and traceback as str.
    """
    start_time = time.time()
    try:
        estimator().fit(X, y)
    except Exception:
        return estimator, traceback.format_exc()
    end_time = time.time()
    return estimator, end_time - start_time


def _calculate_time_per_estimator(
    estimator: EstimatorType,
    X: pd.DataFrame,
    y: pd.Series,
) -> Union[float, str]:
    start_time = time.time()
    try:
        estimator().fit(X, y)
    except Exception:
        return traceback.format_exc()
    end_time = time.time()
    return end_time - start_time


def _optimize_estimator_list_order(
    estimator_list: List[EstimatorType],
    X: pd.DataFrame,
    y: pd.Series,
    num_processes: int,
    timeout: Optional[int] = None,
    func: Callable = _calculate_time_per_estimator,
) -> pd.Series:
    estimator_list_copy = deepcopy(estimator_list)
    calc_worker = partial(func, X=X, y=y)
    results: Dict[EstimatorType, Union[float, str]] = {}

    with mp.Pool(num_processes) as pool:
        for est in estimator_list_copy:
            result = pool.apply_async(calc_worker, args=(est,))
            try:
                results[est] = result.get(timeout=timeout)
                logger.info(f"Finished {est} in {_optimize_estimator_list_order.__name__}")
            except mp.TimeoutError:
                results[est] = f"Timed out after {timeout} seconds"
                logger.error(f"{est} timed out during {_optimize_estimator_list_order.__name__}")

    if any(isinstance(result, str) for result in results.values()):
        logger.error(
            f"Some estimators failed to fit during {_optimize_estimator_list_order.__name__} and will be removed from the estimator_list. See below for traceback:"
        )
        for estimator, traceback_str in results.items():
            if isinstance(traceback_str, str):
                logger.error(
                    "------------------------------------------------------------------------------------------------------------------"
                )
                logger.error(f"{estimator}:\n{traceback_str}")

    result_series = pd.Series(results).apply(lambda x: np.nan if isinstance(x, str) else x).dropna().sort_values()
    if result_series.empty:
        raise ValueError(
            f"All estimators failed to fit during {_optimize_estimator_list_order.__name__}. See above for traceback."
        )
    return result_series


def _encode_non_numerical_features(
    X: pd.DataFrame,
    ordinal_features: Optional[Dict[str, List[str]]] = None,
    categorical_features: Optional[List[str]] = None,
    categorical_features_pca_variance_threshold: Optional[float] = None,
    verbosity_col_transformer: bool = False,
    end_to_end_pipe: MultiEstimatorPipeline = None,
) -> Tuple[pd.DataFrame, Optional[MultiEstimatorPipeline]]:
    """
    Separate non-numerical features and encode them to numerical features.

    Parameters
    ----------
    X : pd.DataFrame
        The dataframe to encode.
    ordinal_features: Optional[Dict[str, List[str]]] = None
        Dict of ordinal features, where the key is the column name and the value is a list of ordered values.
        Values which are not in the list will be encoded as -1 in the data.
        If None, assumes no ordinal features will be used.
    categorical_features : Optional[List[str]] = None
        List of categorical features to encode.
    categorical_features_pca_variance_threshold : Optional[float] = None
        Threshold to determine whether to use PCA or not on categorical features.
        If None, PCA will not be used.
        if float between 0 and 1, PCA will be used if the explained variance is above the threshold.
    verbosity_col_transformer : bool = False
        Verbosity level for the ColumnTransformer.
    end_to_end_pipe : MultiEstimatorPipeline = None
        The pipeline to add the encoders to.

    Returns
    -------
    pd.DataFrame
        The encoded dataframe.
    Optional[MultiEstimatorPipeline]
        The pipeline with the encoders added to it.
        Returns None if end_to_end_pipe is None.
    """

    def get_encoder(name, encoder, features):
        return ColumnTransformer(
            transformers=[(name, encoder, features)],
            remainder="passthrough",
            verbose=verbosity_col_transformer,
            verbose_feature_names_out=False,
        )

    if categorical_features_pca_variance_threshold is not None:
        if not 0 < categorical_features_pca_variance_threshold < 1:
            raise ValueError("categorical_features_pca_variance_threshold must be between 0 and 1")

    new_features = []

    if ordinal_features:
        # sort the keys of ordinal_features by the column index:
        ordinal_features = {
            k: ordinal_features[k] for k in sorted(ordinal_features, key=lambda k: X.columns.get_loc(k))
        }
        ordinal_features_cols = list(ordinal_features.keys())
        logger.notice(f"Encoding ordinal features: {ordinal_features_cols}")
        ordinal_transformer = get_encoder(
            "ordinal_encoder",
            OrdinalEncoder(
                categories=list(ordinal_features.values()), handle_unknown="use_encoded_value", unknown_value=-1
            ),
            ordinal_features_cols,
        )
        X = ordinal_transformer.fit_transform(X)

        if end_to_end_pipe is not None:
            end_to_end_pipe.steps.append(("ordinal_transformer", ordinal_transformer))

    if categorical_features:
        logger.notice(f"Encoding categorical features: {categorical_features}")
        categorical_transformer = get_encoder(
            "categorical_encoder", OneHotEncoder(sparse_output=False), categorical_features
        )
        cols_before_transform = X.columns
        X = categorical_transformer.fit_transform(X)
        cat_new_features = [col for col in X.columns if col not in cols_before_transform]
        logger.warning(
            f"After encoding categorical features, amount of columns increased from {len(cols_before_transform)} to {len(X.columns)}"
        )
        new_features.extend(cat_new_features)
        if end_to_end_pipe is not None:
            end_to_end_pipe.steps.append(("categorical_transformer", categorical_transformer))

    if categorical_features_pca_variance_threshold is not None and new_features:
        logger.notice("applying PCA on categorical features")
        pca = PCA()
        _ = pca.fit_transform(X.loc[:, new_features])

        # first find the number of components to use for PCA based on the variance threshold
        # Determine number of components needed to capture N% variance
        explained_var_ratio = np.cumsum(pca.explained_variance_ratio_)
        n_components = np.argmax(explained_var_ratio >= categorical_features_pca_variance_threshold) + 1
        logger.notice(
            f"PCA will reduce the amount of encoded categorical features from {len(new_features)} to {n_components} with max. variance_threshold {categorical_features_pca_variance_threshold}"
        )

        pca_transformer = get_encoder("pca_encoder", PCA(n_components=n_components), new_features)
        X = pca_transformer.fit_transform(X)
        if end_to_end_pipe is not None:
            end_to_end_pipe.steps.append(("pca_transformer_categorical_features", pca_transformer))

    return X, end_to_end_pipe
