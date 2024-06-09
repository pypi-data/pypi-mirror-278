"""
HyperTuner class.

Aims to automate/aid the process of tuning hyperparameters and
fitting estimators. Hyperparameters are tuned and the estimators
fitted by a process of three consecutive rounds with optional timeouts.
Each HyperTuner-instance represents a single fold of a cross-validation.
"""

from copy import deepcopy
import functools
import random
import re
import traceback
import warnings
from itertools import islice
from typing import Any, Callable, Dict, Generator, List, Literal, Optional, Tuple, Union

import numpy as np
import pandas as pd
from orpheus.components.hypertuner.utils.custom_types import (
    DefaultArgsDict,
    ErrorDict,
    ParamGridDict,
)
from orpheus.components.hypertuner.utils.helper_functions import (
    _collect_bound_errors,
    _create_paramgrid_from_distance_factors,
    fit_estimators_parallel,
    get_estimator_scores,
    get_numerical_defaultargs_from_estimator,
    get_uncalled_estimator,
    instantiate_estimator,
    exclude_hyperparameters_from_paramgrid,
    pretty_print_errors,
)
from orpheus.utils.custom_types import EstimatorErrorInfo
from orpheus.utils.type_vars import EstimatorType
from orpheus.utils.logger import logger
from orpheus.utils.helper_functions import (
    dict_product_R2,
    dict_product_R3,
    ensure_numpy,
    get_string_args_from_estimator,
    get_obj_name,
)
from orpheus.components.libs._base import _ComponentBase
from orpheus.utils.constants import R2_WEIGHTS
from orpheus.utils.constants import DEFAULT_VALUES

warnings.filterwarnings("ignore")


class HyperTuner(_ComponentBase):
    """
    HyperTuner class.

    Aims to automate/aid the process of tuning hyperparameters and fitting estimators.
    Hyperparameters are tuned and the estimators fitted by a process of three consecutive rounds with optional timeouts.

    Each HyperTuner-object represents a single fold of a cross-validation.

    Public methods:
    ---
    fit : Most important method. Find the best estimators with tuned hyperparameters through
        a three-round process with optional timeouts.
    """

    tuner_list: List["HyperTuner"] = []

    def __init__(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        scoring: Optional[Callable[[pd.Series, pd.Series], float]],
        maximize_scoring: bool = True,
        estimator_list: Optional[List[EstimatorType]] = None,
        type_estimator: Optional[Literal["regressor", "classifier"]] = None,
        num_workers: int = DEFAULT_VALUES["n_jobs"],
        random_state: Optional[int] = None,
        config_path: str = "",
    ) -> None:
        # no docstring for __init__ because it is inherited from _ComponentBase.
        # missing parameters are in docs: y_train, y_test, X_train, X_test, random_state
        super().__init__(
            scoring=scoring,
            maximize_scoring=maximize_scoring,
            type_estimator=type_estimator,
            num_workers=num_workers,
            config_path=config_path,
        )
        HyperTuner.tuner_list.append(self)
        self.X_train = ensure_numpy(X_train)
        self.X_test = ensure_numpy(X_test)
        self.y_train = ensure_numpy(y_train).ravel()
        self.y_test = ensure_numpy(y_test).ravel()

        self.train_shape = self.X_train.shape
        self.test_shape = self.X_test.shape

        self._random_state = random_state
        self.estimator_list = estimator_list

        DefaultArgsDict.set(self.estimator_list)

    def __repr__(self) -> str:
        estimatorflag = self.best_estimator_ if hasattr(self, "best_estimator_") else False
        return f"(best_estimator={estimatorflag}, trainshape={self.train_shape}, testshape={self.test_shape})"

    def fit(
        self,
        R1_timeout: Optional[int] = 60,
        R2_timeout: Optional[int] = 30,
        R3_timeout: Optional[int] = 30,
        R2_R3_max_iter: int = 10000,
        R2_R3_amt_params: int = 5,
        R2_R3_exclude_params: Optional[List[str]] = None,
        R2_n_vals_per_param: int = 10,
        R1_amt_surviving_models: int = 10,
        R1_exclude_models: Optional[List[str]] = None,
        R2_include_string_args: bool = False,
        R2_weights: Dict[str, float] = R2_WEIGHTS,
        R2_int_distance_factor: float = 2.0,
        R2_float_distance_factor: float = 10.0,
        R3_min_correlation_to_best_score: float = 0.01,
        R3_int_distance_factor: float = 1.01,
        R3_float_distance_factor: float = 1.01,
        amt_top_models_saved_per_round: int = 10,
        penalty_to_score_if_overfitting: float = 0.0,
        random_subset: float = 1.0,
        random_subset_factor: float = 1.0,
        params_for_estimators: Optional[Dict] = None,
    ) -> Union["HyperTuner", EstimatorType]:
        """
        Find the best fitting estimator with tuned hyperparameters.
        This happens through a process of three rounds:

        ROUND 1:
        ---
        Find the best N estimators (an amount decided by `R1_amt_surviving_models`)
        from estimator_list wihout any parameters added.
        Optional timeout to force a result after N seconds.

        ROUND 2:
        ---
        Find the best hyperparameters from best N estimators,
        which are decided by `R1_amt_surviving_models`.
        This is done by creating a parametergrid, based on the numerical
        default values of estimator-parameters.

        Then, perform a randomised gridsearch with aprox. int(`R2_R3_max_iter` / `R1_amt_surviving_models`)
        amount of iterations per estimator.

        Then, all scores are compared per estimator.
        The best estimator is chosen depending on 3 criteria.
        These criteria were chosen to prevent overfitting and are weighted per estimator-population,
        according to `R2_weights`:
        1. best mean (depending on "self.maximize_scoring")
        2. lowest standarddeviation from all scores.
        3. amount of unique scores

        Optional timeout to force a result after N seconds.

        ROUND 3:
        ---
        Perform a non-randomised gridsearch based on the best hyperparamers found in ROUND 2 and
        hyperparameters which show correlation with the best score.
        The process of creating a paramgrid is automated, just like before ROUND 2.
        Usually, this allows to squeeze a better score out than ROUND 2.
        Optional timeout to force a result after N seconds.


        creates attributes
        --------------
        best_estimator_ : EstimatorType
            best estimator found after all rounds finished.

        best_score_ : float
            best score found after all rounds finished.

        scores_R1_ : Tuple[EstimatorType, float]
            best estimators with their respective score from ROUND 1.
            Use parameter "amt_top_models_saved_per_round" for
            amount of scores assigned to this attribute.

        scores_R2_WEIGHTED : Tuple[EstimatorType, float]
            This attribute is only created if `R2_weights` is active (not [0.0, 0.0, 0.0] ).
            Best estimators with their respective score from each estimator-population after ROUND 2.
            Estimators per population are those chosen with
            `R1_amt_surviving_models` which survived R1.
            Thus, the variaty of estimators is much bigger than in the other `scores_Rx` attributes.
            Use parameter "R1_amt_surviving_models" for amount of
            distinct estimators assigned to this attribute.

        scores_R2_ : Tuple[EstimatorType, float]
            best estimators with their respective score from ROUND 2.
            Use parameter `amt_top_models_saved_per_round` for
            amount of scores assigned to this attribute.

        scores_R3_ : Tuple[EstimatorType, float]
            best estimators with their respective score from ROUND 3.
            Use parameter `amt_top_models_saved_per_round` for amount of scores
            assigned to this attribute.

        Parameters
        ----------
        R1_timeout: Optional[int] = 60
            Only applies to ROUND 1. N amount of seconds after which
            a result will be forced.
            Use if you want to have control of amount time the process will take.

        R2_timeout: Optional[int] = 30
            Only applies to ROUND 2. N amount of seconds after which a
            result will be forced.
            Use if you want to have control of amount of time the process will take.
            if None: `R2_R3_max_iter` amount of iterations will be finished until the end.
            if 0: skip round.

        R3_timeout: Optional[int] = 30
            Only applies to ROUND 3. N amount of seconds after which
            a result will be forced.
            Use if you want to have control of amount of time the process will take.
            if None: `R2_R3_max_iter` amount of iterations
            will be finished until the end.
            if 0: skip round.

        amt_top_models_saved_per_round: int = 10
            amount of top scoring estimators per round which
            will be assigned to `self.scores_Rx_` attributes.
            WARNING: Do not use a too high number, as estimators
            assigned to self.scores_Rx_ attributes can get very large!
            NOTE: This parameter is very important for later use,
            as it decides the amount of fitted estimators which will be saved!
            This is essential for using multiple estimators for
            predicting in HyperTunerStacked.

        R2_R3_max_iter: int = 5000
            Applies both to ROUND 2 and ROUND 3.
            Amount of iterations during random gridsearch.

        R2_R3_amt_params: int = 5
            Applies both to ROUND 2 and ROUND 3.
            Amount of parameters to be used in gridsearch.

        R2_R3_exclude_params: Optional[List[str]] = None
            Applies both to ROUND 2 and ROUND 3.
            List of parameters to be excluded from gridsearch.

        R2_n_vals_per_param: int = 10
            Only applies to ROUND 2.
            Amount of values per parameter to be used in gridsearch.
            In round 2, `R2_R3_amt_params` ** `R2_n_vals_per_param` combinations are possible.

        R1_exclude_models: Optional[List[str]] = None
            Only applies to ROUND 1.
            List of models to be excluded from ROUND 1 and directly proceed to ROUND 2.

        R1_amt_surviving_models: int = 10
            Only applies to ROUND 2. amount of distinct best estimators
            from ROUND 1 to go to ROUND 2.

        R2_include_string_args: bool = False
            Only applies to ROUND 2. Optionally include stringarguments,
            next to numerical arguments, from estimators in random gridsearch during ROUND 2.
            NOTE: This option is very unpredictable and it may take
            a lot longer to produce meaningful results!

        R2_weights: Dict[str, float]  = {
                                    "best_mean": 0.0,
                                    "lowest_stdev": 0.0,
                                    "amount_of_unique_scores": 0.0
                                    }
            Only applies to ROUND 2.
            If None, best estimator from all populations will proceed to ROUND 3.
            Optionally, a list with 3 floats as weights can be given to
            estimator-populations through best mean, lowest standarddeviation and
            amount of unique scores respectfully.
            Points are given to each estimator-population according to `R2_weights`.
            This is done during the scoring process after R2. From the best ranking population,
            the best scoring estimator proceeds to ROUND 3.
            NOTE: Passing weights is a good way of reducing overfitting.
            A good starting point would be: [0.9, 0.3, 0.3]

        R2_int_distance_factor: float = 2.0
            Only applies to ROUND 2. Factor of distance from default value of a parameter through
            which new values will be generated in `R2_n_vals_per_param` if parameter expects int values.
            Recommended: `R2_int_distance_factor` > `R3_int_distance_factor` > 1.

        R2_float_distance_factor: float = 10.0
            Only applies to ROUND 2. factor of distance from default value of a parameter
            through which new values will be generated in `R2_n_vals_per_param` if
            parameter expects float values.
            Recommended: `R2_float_distance_factor` > `R3_float_distance_factor` > 1.

        R3_min_correlation_to_best_score : float = 0.01
            Interval between [0, 1] (inclusive). If correlation to best score of a
            parameter >= `R3_min_correlation_to_best_score`,
            every parameter with correlation equal or above this threshold
            will be used for R3_gridsearch.

        R3_int_distance_factor: float = 1.5
            Only applies to ROUND 3. Factor of distance from default value of a parameter through which
            new values will be generated in "R2_n_vals_per_param" if parameter expects int values.
            Recommended: `R2_int_distance_factor` > `R3_int_distance_factor` > 1.

        R3_float_distance_factor: float = 1.5
            Only applies to ROUND 3. factor of distance from default value of a parameter through which
            new values will be generated in `R2_n_vals_per_param` if parameter expects float values.
            Recommended: `R2_float_distance_factor` > `R3_float_distance_factor` > 1.

        penalty_to_score_if_overfitting: float = 0.0
        NOTE: Using this parameter is only recommended for classification problems!

            It may happen that a specific value is overrepresented in y_pred, compared to self.y_test.
            This usually indicates overfitting and is especially a
            big problem in for example binary classification models,
            which may overfit to predict only one binary value, instead of two.
            To combat this problem, this parameter can be used.

            Interval between [0, 1] (inclusive) to penalize score if ratio of unique values
            in y_pred diverges too much from self.y_test.
            The bigger the difference, the more the penalty exponentially grows and will punish
            bigger divergances from ratio of values in self.y_test.
        Raises:
            ValueError: if value not between 0 and 1

        random_subset: float = 1.0
            Each estimator will be fitted on a random subset of the data during each iteration per round.
            This is useful for reducing overfitting and speeding up the process.
            random_subset must be a value between 0 and 1 (inclusive).
            iF 1.0, no random subset will be used.
            NOTE: Indexes will be shuffled before each iteration.

        random_subset_factor: float = 1.0
            The factor by which the random_subset will be multiplied after each of the three rounds.
            If 1.0, the random_subset will stay the same.
            Else, the random_subset will be multiplied by this factor after each round.
            For example: if random_subset_factor = 1.5 and random_subset 0.2,
            the random_subset in the three rounds will be:
            ROUND 1: 0.2
            ROUND 2: 0.3
            ROUND 3: 0.45

        params_for_estimators: Optional[dict] = None
            pass a dictionary of optional arguments which will be evaluated by each single estimator.


        returns
        ---
        self

        ---
        mainsource for timeout w/ multiprocessing mechanism: https://stackoverflow.com/questions/66051638/set-a-time-limit-on-the-pool-map-operation-when-using-multiprocessing
        """
        logger.notice("----------------------ROUND 1----------------------")

        estimator_list: List[EstimatorType] = [
            est for est, _ in map(instantiate_estimator, self.estimator_list) if est is not None
        ]

        excluded_estimators_R1: List[EstimatorType] = []
        if R1_exclude_models is not None:
            R1_exclude_models = [model.lower() for model in R1_exclude_models]
            excluded_estimators_R1 = [
                est
                for est in estimator_list
                if any(exclude_model in get_obj_name(est).lower() for exclude_model in R1_exclude_models)
            ]
            estimator_list = [est for est in estimator_list if est not in excluded_estimators_R1]
            logger.notice(f"Excluded estimators from ROUND 1: {excluded_estimators_R1}")

        if not estimator_list:
            raise ValueError("estimator_list is empty! Did you pass a valid estimator_list?")

        returned_results = fit_estimators_parallel(
            estimator_list=estimator_list,
            timeout=R1_timeout,
            num_workers=self.num_workers,
            X_train=self.X_train,
            y_train=self.y_train,
            random_subset=random_subset,
        )

        returned_estimators = [i for i in returned_results if not isinstance(i, list)]
        returned_errors = [i for i in returned_results if isinstance(i, list)]

        if returned_errors:
            pretty_print_errors(returned_errors)

        if not returned_estimators:
            raise ValueError("No finished estimators were found after R1! Did you make R1_timeout too short?")

        sorted_scores, best_estimator_R1, best_score_R1 = self._scoring_process_R1(
            amt_top_models_saved_per_round,
            penalty_to_score_if_overfitting,
            returned_estimators,
        )

        logger.notice(
            f"Total amount of succesful iterations in ROUND 1: {len(returned_estimators)}",
        )
        logger.notice(
            f"Percentage of errors in ROUND 1: {len(returned_errors)/len(returned_results) * 100:.2f} %",
        )

        if R2_timeout == 0:
            self.best_estimator_ = best_estimator_R1
            self.best_score_ = best_score_R1
            logger.notice(
                f"ended fit, because R2_timeout is 0.\nbest estimator: {self.best_estimator_}\nbest score: {self.best_score_}"
            )

            return self

        logger.notice("----------------------CREATING PARAMGRID ROUND 2----------------------")
        estimators_R2 = [i[0] for i in tuple(islice(sorted_scores.items(), 0, R1_amt_surviving_models))]

        if R1_exclude_models is not None:
            estimators_R2 = estimators_R2[: -len(excluded_estimators_R1)] + excluded_estimators_R1

        logger.notice(
            f"Amount of estimators which advance to ROUND 2: {len(estimators_R2)}",
        )
        n_iter_R2_per_estimator = int(R2_R3_max_iter / len(estimators_R2))

        # create paramgrid for ROUND 2.
        estimators_R2_keys = []

        for estimator in estimators_R2:
            estimator_str = get_obj_name(estimator)
            estimators_R2_keys.append(estimator_str)

            # if estimator is already in ParamGridDict, skip it.
            if estimator_str in ParamGridDict.get_all():
                continue
            else:
                paramgrid_R2_for_single_estimator = self._get_paramgrid_for_R2(
                    estimator=estimator,
                    n_vals_per_param=R2_n_vals_per_param,
                    amt_params=R2_R3_amt_params,
                    int_distance_factor=R2_int_distance_factor,
                    float_distance_factor=R2_float_distance_factor,
                    include_string_args=R2_include_string_args,
                )

                # check if there are any upper or lower bound errors.
                # if so, add them to ErrorDict.
                upper_bound_errors, lower_bound_errors = self._bound_error_scout_R2(
                    estimator, paramgrid_R2_for_single_estimator
                )

                if upper_bound_errors:
                    logger.error(f"Found upper bound errors for {estimator_str}: {upper_bound_errors}")
                    ErrorDict.set("upper_bound", estimator_str, upper_bound_errors)

                if lower_bound_errors:
                    logger.error(f"Found lower bound errors for {estimator_str}: {lower_bound_errors}")
                    ErrorDict.set("lower_bound", estimator_str, lower_bound_errors)

                # add the paramgrid to ParamGridDict:
                ParamGridDict.set(estimator_str, paramgrid_R2_for_single_estimator)

        # grab the matching estimators from ParamGridDict.
        # These are the paramgrids which were already scanned for errors in
        # previous runs.
        paramgrid_R2 = {}
        for key in estimators_R2_keys:
            paramgrid_R2[key] = self._get_new_paramgrid_without_errors(ParamGridDict.get(key), key)

        if R2_R3_exclude_params is not None:
            paramgrid_R2 = exclude_hyperparameters_from_paramgrid(paramgrid_R2, R2_R3_exclude_params)

        estimator_list = self._get_estimatorlist_for_R2(
            paramgrid_R2=paramgrid_R2,
            estimators_R2=estimators_R2,
            n_iter_R2_per_estimator=n_iter_R2_per_estimator,
            params_for_estimators=params_for_estimators,
        )

        logger.notice("----------------------ROUND 2----------------------")
        estimator_list = [j for i in estimator_list for j in i if j is not None]

        random.seed(self._random_state)
        random.shuffle(estimator_list)

        if random_subset < 1.0:
            random_subset = random_subset * random_subset_factor

        returned_results = fit_estimators_parallel(
            estimator_list=estimator_list,
            timeout=R2_timeout,
            num_workers=self.num_workers,
            X_train=self.X_train,
            y_train=self.y_train,
            random_subset=random_subset,
        )

        returned_estimators = [i for i in returned_results if not isinstance(i, list)]
        returned_errors = [i for i in returned_results if isinstance(i, list)]
        if returned_errors:
            self._process_returned_errors(returned_errors)

        if not returned_estimators:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator_R1, best_score_R1, "ended fit, because no estimators were returned after R2"
            )

            return self

        amt_iters_R2 = len(returned_estimators)

        (
            returned_estimators,
            sorted_scores,
            best_estimator_R2,
            best_score_R2,
            best_estimator,
            best_score,
        ) = self._scoring_process_R2(
            R2_weights,
            amt_top_models_saved_per_round,
            penalty_to_score_if_overfitting,
            best_estimator_R1,
            best_score_R1,
            estimators_R2,
            returned_estimators,
        )

        logger.notice(f"best estimator after R2: {best_estimator}")
        logger.notice(f"best score R1: {best_score_R1:.6f}")
        logger.notice(f"best score R2: {best_score_R2:.6f}")
        logger.notice(f"Total amount of succesful iterations in ROUND 2: {amt_iters_R2}")
        logger.notice(
            f"Percentage of errors in ROUND 2: {len(returned_errors)/len(returned_results) * 100:.2f} %",
        )

        if R3_timeout == 0:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator, best_score, "ended fit, because R3_timeout is 0"
            )

            return self

        logger.notice("----------------------CREATING PARAMGRID ROUND 3----------------------")

        paramgrid_R3, default_params_R3 = self._get_paramgrid_for_R3(
            best_estimator,
            DefaultArgsDict.get(get_obj_name(best_estimator)),
            sorted_scores,
            R3_min_correlation_to_best_score,
            R3_int_distance_factor,
            R3_float_distance_factor,
            R2_R3_max_iter,
        )

        if not paramgrid_R3:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator, best_score, "ended fit, because no suitable hyperparameters were found for R3"
            )
            return self

        # default_params_R3 are default values found in best_estimator after R2,
        # should not raise errors in R3 and are excluded here.
        paramgrid_R3 = self._get_new_paramgrid_without_errors(paramgrid_R3, get_obj_name(best_estimator))

        if R2_R3_exclude_params is not None:
            paramgrid_R3 = exclude_hyperparameters_from_paramgrid(paramgrid_R3, R2_R3_exclude_params)

        if not paramgrid_R3:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator, best_score, "ended fit, because no suitable hyperparameters were found for R3"
            )

            return self

        # add default_params_R3 to params_for_estimators so that they will be
        # included as default estimator-params in R3.
        params_for_estimators = (
            {**default_params_R3} if params_for_estimators is None else {**params_for_estimators, **default_params_R3}
        )

        paramlist_generator = self._get_paramgen_for_R3(
            R2_R3_max_iter,
            params_for_estimators,
            paramgrid_R3,
        )

        # remove duplicates from paramlist_R3:
        paramlist_R3 = []
        try:
            for d in paramlist_generator:
                if d not in paramlist_R3:
                    paramlist_R3.append(d)
        except ValueError:
            logger.error(traceback.format_exc())
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator,
                best_score,
                "ended fit, because a ValueError was raised during attempt to remove duplicates from paramlist_R3",
            )

            return self

        estimator_list: List[EstimatorType] = [
            instantiate_estimator(get_uncalled_estimator(best_estimator), **params)[0] for params in paramlist_R3
        ]

        logger.notice("----------------------ROUND 3----------------------")

        if random_subset < 1.0:
            random_subset = random_subset * random_subset_factor

        returned_results = fit_estimators_parallel(
            estimator_list=estimator_list,
            timeout=R3_timeout,
            num_workers=self.num_workers,
            X_train=self.X_train,
            y_train=self.y_train,
            random_subset=random_subset,
        )

        returned_estimators = [i for i in returned_results if not isinstance(i, list)]
        returned_errors = [i for i in returned_results if isinstance(i, list)]

        if returned_errors:
            self._process_returned_errors(returned_errors)

        if not returned_estimators:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator, best_score, "ended fit, because no estimators were returned after R3"
            )

            return self

        try:
            best_estimator, best_score, best_score_R3 = self._scoring_process_R3(
                amt_top_models_saved_per_round,
                penalty_to_score_if_overfitting,
                returned_estimators,
                best_estimator_R1,
                best_score_R1,
                best_estimator_R2,
                best_score_R2,
                best_estimator,
                best_score,
            )
        except ValueError:
            self._end_fit_and_instantiate_best_estimator_best_score(
                best_estimator, best_score, "ended fit, because a ValueError was raised during scoring process of R3"
            )

            return self

        logger.notice(
            f"Total amount of succesful iterations in ROUND 3: {len(returned_estimators)}",
        )
        logger.notice(
            f"Percentage of errors in ROUND 3: {len(returned_errors)/len(returned_results) * 100:.2f} %",
        )
        logger.notice(
            f"paramgrid R3: { {k: v[:3] + [('...')] + v[-3:] for k, v in paramgrid_R3.items()} }",
        )
        logger.notice(f"best score R3: {best_score_R3:.6f}")

        self._end_fit_and_instantiate_best_estimator_best_score(
            best_estimator, best_score, "ended fit, because R3 ended succesfully"
        )

        return self

    @functools.lru_cache
    def _get_all_fitted_estimators(self, sort_scores: bool = True, top_n: Optional[int] = None) -> dict:
        """
        get all estimators and scores from self.scores_Rx.

        Parameters
        ----------
        sort_scores : bool, default=True
            if True, the returned dict will be sorted by the scores.

        top_n : int, default=None
            if not None, only the top_n estimators will be returned.
        """
        estimators_and_scores = {i[0]: i[1] for k, v in vars(self).items() if k.startswith("scores_R") for i in v}
        if not estimators_and_scores:
            raise ValueError("No estimators have been fitted yet!")
        if top_n:
            estimators_and_scores = dict(islice(estimators_and_scores.items(), top_n))
            if len(estimators_and_scores) < top_n:
                logger.warning(
                    f"Only {len(estimators_and_scores)} scored estimators were saved in this HyperTuner instance, "
                    f"but top_n is {top_n}.\nConsider increasing 'amt_top_models_saved_per_round' to at least {top_n} in the configurationfile!",
                )
        if sort_scores:
            return dict(
                sorted(
                    estimators_and_scores.items(),
                    key=lambda d: d[1],
                    reverse=bool(self.maximize_scoring),
                )
            )
        return estimators_and_scores

    def _get_new_paramgrid_without_errors(self, old_paramgrid: Dict[str, List], estimator_str: str) -> Dict[str, List]:
        """
        Update old paramgrid with ErrorDict.get().
        Return the updated paramgrid without previous found errors.

        Parameters
        ----------
        old_paramgrid : Dict[str, List]
            The paramgrid of the estimator

        estimator_str : str
            The key of the estimator
        """
        new_paramgrid = deepcopy(old_paramgrid)

        if estimator_str in ErrorDict.get("lower_bound"):
            errors = ErrorDict.get("lower_bound", estimator_str)
            faulty_params = set(error_info.parameter for error_info in errors)
            faulty_params = [p for p in faulty_params if p in old_paramgrid]
            for param in faulty_params:
                edited_paramgrid = list(
                    filter(
                        lambda val, p=param: val >= DefaultArgsDict.get(estimator_str, p),
                        old_paramgrid[param],
                    )
                )
                try:
                    if edited_paramgrid != new_paramgrid[param]:
                        new_paramgrid[param] = edited_paramgrid
                    else:
                        del new_paramgrid[param]
                        logger.error(f"deleted {param} from paramgrid because of lower_bound error")
                except KeyError:
                    logger.error(f"KeyError: {param} not in {new_paramgrid}")

        if estimator_str in ErrorDict.get("upper_bound"):
            errors = ErrorDict.get("upper_bound", estimator_str)
            faulty_params = set(error_info.parameter for error_info in errors)
            faulty_params = [p for p in faulty_params if p in old_paramgrid]
            for param in faulty_params:
                edited_paramgrid = list(
                    filter(
                        lambda val, p=param: val <= DefaultArgsDict.get(estimator_str, p),
                        old_paramgrid[param],
                    )
                )
                try:
                    if edited_paramgrid != new_paramgrid[param]:
                        new_paramgrid[param] = edited_paramgrid
                    else:
                        del new_paramgrid[param]
                        logger.error(f"deleted {param} from paramgrid because of upper_bound error")

                except KeyError:
                    logger.error(f"KeyError: {param} not in {new_paramgrid}")

        if estimator_str in ErrorDict.get("unknown"):
            errors = ErrorDict.get("unknown", estimator_str)
            # here, there can be multiple params with different faulty values!
            for error_info in errors:
                faulty_param = error_info.parameter
                if faulty_param in new_paramgrid:
                    del new_paramgrid[faulty_param]
                    logger.error(f"deleted {faulty_param} from paramgrid because of unknown error")

        return new_paramgrid

    def _process_returned_errors(self, returned_errors: List[List[Union[EstimatorType, Exception, str]]]) -> None:
        """
        Process the errors returned by the parallel fit process

        This includes:
        - printing the errors
        - finding the faulty parameter values
        - setting and/or updating the ErrorDict
        """
        pretty_print_errors(returned_errors)

        bound_error_dict, unknown_error_dict = self._find_faulty_param_values_in_errors(returned_errors)

        if unknown_error_dict:
            for estimator_str, error_value in unknown_error_dict.items():
                ErrorDict.set("unknown", estimator_str, error_value)

        ErrorDict.update(bound_error_dict)

    def _pretty_print_errors(self, returned_errors: List[List[Union[EstimatorType, Exception, str]]]) -> None:
        """Print the errors returned by the parallel fit process."""
        logger.warning(f"{len(returned_errors)} estimators failed during fit:")
        for est, err, _traceback in returned_errors:
            logger.error(f"estimator: {est}\n{_traceback}")

    def _bound_error_scout_R2(
        self, estimator: EstimatorType, sorted_paramgrid_R2: Dict
    ) -> Tuple[List[Union[EstimatorErrorInfo, None]], List[Union[EstimatorErrorInfo, None]]]:
        """
        Collect errors from the bound values of the paramgrid before start of R2.
        The goal is to reduce the amount of errors that are raised during R2.

        Parameters
        ----------
        estimator : estimator object
            The estimator to be fitted.

        sorted_paramgrid_R2 : dict
            The paramgrid for R2.

        Returns
        -------
        upper_bound_errors, lower_bound_errors
        """
        default_args = DefaultArgsDict.get(get_obj_name(estimator))
        default_floats = {k: v for k, v in default_args.items() if isinstance(v, (float)) and not np.isinf(v)}
        default_ints = {k: v for k, v in default_args.items() if isinstance(v, (int))}

        bounds_paramgrid_R2 = {}
        for param, val in sorted_paramgrid_R2.items():
            if param in {**default_floats, **default_ints}:
                bounds_paramgrid_R2[param] = [min(val), max(val)]
            else:
                bounds_paramgrid_R2[param] = val

        bounds_paramgrid_R2 = [{param: val} for param, vals in bounds_paramgrid_R2.items() for val in vals]
        instantiated_estimators_bound_scout: List[EstimatorType, Dict[str, Any]] = [
            instantiate_estimator(get_uncalled_estimator(estimator), **params)
            for params in deepcopy(bounds_paramgrid_R2)
        ]

        if not instantiated_estimators_bound_scout:
            instantiated_estimators, found_errors_in_bound_scout = [], []
        else:
            instantiated_estimators, found_errors_in_bound_scout = zip(*instantiated_estimators_bound_scout)

        # fit estimators to see if an error is raised
        returned_errors = []
        for est in instantiated_estimators:
            # only insert a fraction of the data to see if an error is raised
            possible_error = self._fit_estimator_bound_scount(est, X=self.X_train[:10], y=self.y_train[:10])
            if isinstance(possible_error, Exception):
                returned_errors.append(possible_error)

        if returned_errors:
            upper_bound_errors, lower_bound_errors = _collect_bound_errors(
                estimator, returned_errors, bounds_paramgrid_R2
            )
        else:
            upper_bound_errors, lower_bound_errors = [], []

        for idx, error in enumerate(found_errors_in_bound_scout):
            if error:
                # if idx is even, the error is a lower bound error.
                # if idx is odd, the error is an upper bound error.
                if idx % 2 == 0:
                    lower_bound_errors.extend(error)
                else:
                    upper_bound_errors.extend(error)

        return upper_bound_errors, lower_bound_errors

    def _find_faulty_param_values_in_errors(
        self, returned_errors: List[List[List[Union[EstimatorType, Exception, str]]]]
    ) -> Tuple[Dict[str, List[EstimatorErrorInfo]], Dict[str, List[EstimatorErrorInfo]]]:
        """
        The algorithm tries to find the faulty hyperparameter value in the error message.
        Estimator, error, parameter and value are added to the EstimatorErrorInfo object if the error is found.

        This happens through two searches:
        1. level one match: the hyperparameter name has an exact match in the error message
        2. level two match: the hyperparameter name has a match in a phrase of the error message

        level-one matches will be added to bound_error_dict in a special EstimatorErrorInfo object,
        because the faulty hyperparameter value is known.

        level-two matches will be added to unknown_error_dict in a special EstimatorErrorInfo object,
        becausethe faulty hyperparameter value either a
        string (making it unfeasible for bound_error_dict) or not known.

        Parameters
        ----------
        returned_errors : list
            The errors returned by the parallel fit process.

        Returns
        -------
        bound_error_dict, unknown_error_dict
        """
        bound_error_dict = {}
        unknown_error_dict: Dict[str, List[EstimatorErrorInfo]] = {}
        match_pattern = re.compile(r"[\w]+")

        for error_item in returned_errors:
            estimator, error, _ = error_item
            estimator_str = get_obj_name(estimator)
            splitted_error_str = str(error).replace("'", "").split()
            try:
                possible_params = estimator.get_params()
            except AttributeError:
                possible_params = estimator.__dict__
            found = False
            level_two_matches = []
            for word in splitted_error_str:
                for param_name, param_val in possible_params.items():
                    if param_name in word:
                        level_two_matches.append(EstimatorErrorInfo(estimator, error, param_name, param_val))
                    str1 = "".join(match_pattern.findall(word))
                    str2 = "".join(match_pattern.findall(param_name))
                    if str1 == str2:
                        level_one_match = EstimatorErrorInfo(estimator, error, param_name, param_val)
                        bound_error_dict.setdefault(estimator_str, []).append(level_one_match)
                        found = True
                        break
            if not found:
                if len(level_two_matches) > 0:
                    level_two_match = level_two_matches[0]
                else:
                    level_two_match = EstimatorErrorInfo(estimator, error, None, None)
                unknown_error_dict.setdefault(estimator_str, []).append(level_two_match)

        return bound_error_dict, unknown_error_dict

    def _scoring_process_R1(
        self,
        amt_top_models_saved_per_round: int,
        penalty_to_score_if_overfitting: float,
        returned_estimators: List[EstimatorType],
    ) -> Tuple[dict, EstimatorType, float]:
        sorted_scores = get_estimator_scores(
            estimator_list=returned_estimators,
            X_test=self.X_test,
            y_test=self.y_test,
            scoring_func=self.scoring,
            maximize_scoring=self.maximize_scoring,
            penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
        )
        self.scores_R1_ = tuple(islice(sorted_scores.items(), 0, amt_top_models_saved_per_round))
        best_estimator_R1 = (
            max(sorted_scores, key=sorted_scores.get)
            if self.maximize_scoring
            else min(sorted_scores, key=sorted_scores.get)
        )
        best_score_R1 = sorted_scores[best_estimator_R1]
        return sorted_scores, best_estimator_R1, best_score_R1

    # TODO: refactor this function. It works, but is too long and complex
    def _scoring_process_R2(
        self,
        R2_weights: Dict[str, float],
        amt_top_models_saved_per_round: int,
        penalty_to_score_if_overfitting: float,
        best_estimator_R1: EstimatorType,
        best_score_R1: float,
        estimators_paramgrid_R2: list,
        returned_estimators: List[EstimatorType],
    ):
        if len(estimators_paramgrid_R2) > 1:
            sorted_scores = []
            for i in estimators_paramgrid_R2:
                estimators = [j for j in returned_estimators if i.__class__ == j.__class__]
                if estimators:
                    scores = get_estimator_scores(
                        estimator_list=estimators,
                        X_test=self.X_test,
                        y_test=self.y_test,
                        scoring_func=self.scoring,
                        maximize_scoring=self.maximize_scoring,
                        penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
                    )
                    sorted_scores.append(scores)
            if {} in sorted_scores:
                sorted_scores = [i for i in sorted_scores if i]

            if any(R2_weights.values()):
                (
                    mean_and_stdev,
                    mean_and_stdev_results,
                ) = self._get_R2_weights_ranking(R2_weights, sorted_scores)

                best_estimator_R2_class = mean_and_stdev_results.index[0]
                idx_sorted_scores = mean_and_stdev.loc[
                    mean_and_stdev.index == best_estimator_R2_class,
                    "idx_in_sorted_scores",
                ][0]
                sorted_scores = sorted_scores[idx_sorted_scores]
                logger.notice(f"\nresults R2:\n{mean_and_stdev}\n")
                logger.notice(
                    f"ranking R2:\n\n{mean_and_stdev_results.to_string()}",
                )
            else:
                best_score_per_population = [
                    max(population.values()) if self.maximize_scoring else min(population.values())
                    for population in sorted_scores
                ]
                if self.maximize_scoring:
                    best_score_index = np.argmax(best_score_per_population)
                else:
                    best_score_index = np.argmin(best_score_per_population)
                sorted_scores = sorted_scores[best_score_index]
        else:
            sorted_scores = get_estimator_scores(
                estimator_list=returned_estimators,
                X_test=self.X_test,
                y_test=self.y_test,
                scoring_func=self.scoring,
                maximize_scoring=self.maximize_scoring,
                penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
            )

        self.scores_R2_ = tuple(islice(sorted_scores.items(), 0, amt_top_models_saved_per_round))
        best_estimator_R2 = (
            max(sorted_scores, key=sorted_scores.get)
            if self.maximize_scoring
            else min(sorted_scores, key=sorted_scores.get)
        )
        best_score_R2 = sorted_scores[best_estimator_R2]

        if (get_uncalled_estimator(best_estimator_R1) == get_uncalled_estimator(best_estimator_R2)) or (
            not any(R2_weights.values())
        ):
            if self.maximize_scoring:
                best_estimator = best_estimator_R2 if best_score_R2 > best_score_R1 else best_estimator_R1
                best_score = best_score_R2 if best_score_R2 > best_score_R1 else best_score_R1
            else:
                best_estimator = best_estimator_R2 if best_score_R2 < best_score_R1 else best_estimator_R1
                best_score = best_score_R2 if best_score_R2 < best_score_R1 else best_score_R1
        else:
            logger.notice("best_estimator_R2 is different than best_estimator_R1!")
            logger.notice(
                f"change best_estimator from {best_estimator_R1} with score {best_score_R1:.6f} to {best_estimator_R2} with score {best_score_R2:.6f}"
            )
            best_estimator = best_estimator_R2
            best_score = best_score_R2

        return (
            returned_estimators,
            sorted_scores,
            best_estimator_R2,
            best_score_R2,
            best_estimator,
            best_score,
        )

    def _scoring_process_R3(
        self,
        amt_top_models_saved_per_round: int,
        penalty_to_score_if_overfitting: float,
        returned_estimators: List[EstimatorType],
        best_estimator_R1: EstimatorType,
        best_score_R1: float,
        best_estimator_R2: EstimatorType,
        best_score_R2: float,
        best_estimator: EstimatorType,
        best_score: float,
    ) -> Tuple[EstimatorType, float, float]:
        sorted_scores = get_estimator_scores(
            estimator_list=returned_estimators,
            X_test=self.X_test,
            y_test=self.y_test,
            scoring_func=self.scoring,
            maximize_scoring=self.maximize_scoring,
            penalty_to_score_if_overfitting=penalty_to_score_if_overfitting,
        )
        sorted_scores = sorted(sorted_scores.items(), key=lambda x: x[1], reverse=self.maximize_scoring)
        self.scores_R3_ = sorted_scores[:amt_top_models_saved_per_round]
        best_estimator_R3, best_score_R3 = sorted_scores[0]

        if self.maximize_scoring:
            best_estimator = best_estimator if best_score > best_score_R3 else best_estimator_R3
            best_score = best_score if best_score > best_score_R3 else best_score_R3
        else:
            best_estimator = best_estimator_R2 if best_score_R2 < best_score_R1 else best_estimator_R1
            best_score = best_score if best_score < best_score_R3 else best_score_R3

        return best_estimator, best_score, best_score_R3

    def _get_estimatorlist_for_R2(
        self,
        paramgrid_R2: Dict[str, list],
        estimators_R2: List[EstimatorType],
        n_iter_R2_per_estimator: int,
        params_for_estimators: Dict,
    ) -> Tuple[List, Dict, Dict]:
        """Create a list of instantiated estimators with
        parameters for R2 with the given paramgrid.

        Parameters
        ----------
        paramgrid_R2 : dict[str, list]
            The parameter grid for R2.

        estimators : List[EstimatorType]
            The estimators to use for R2.

        n_iter_R2_per_estimator : int
            The number of iterations for each estimator.

        params_for_estimators : dict
            The parameters to use for all estimators.

        Returns
        -------
        list with instantiated estimators
        """
        estimator_list = []
        estimators_R2_dict = {get_obj_name(est): est for est in estimators_R2}

        for est_str, param_grid in paramgrid_R2.items():
            # Create generator with parameters for the estimator:
            paramlist_gen = dict_product_R2(param_grid, n_iter_R2_per_estimator)
            if params_for_estimators is not None:
                paramlist_gen = ({**p, **params_for_estimators} for p in paramlist_gen)

            instantiated_estimators = [
                instantiate_estimator(get_uncalled_estimator(estimators_R2_dict[est_str]), **params)[0]
                for params in paramlist_gen
            ]

            estimator_list.append(instantiated_estimators)

        return estimator_list

    def _get_paramgen_for_R3(
        self,
        R2_R3_max_iter,
        params_for_estimators,
        paramgrid_R3,
    ) -> Generator:
        """Convert a dictionary of lists of parameters into a list of dictionaries of parameters,
        one per iteration."""
        paramlist_generator = dict_product_R3(paramgrid_R3, R2_R3_max_iter)

        if params_for_estimators is not None:
            paramlist_generator = ({**p, **params_for_estimators} for p in paramlist_generator)

        return paramlist_generator

    def _get_paramgrid_for_R2(
        self,
        estimator: EstimatorType,
        n_vals_per_param: int,
        amt_params: int,
        int_distance_factor: float = 2,
        float_distance_factor: float = 10,
        include_string_args: bool = False,
    ) -> Tuple[dict, list, list]:
        """
        return new_paramgrid for an estimator in ROUND 2.
        This assumes:
        - first parameters in docstring of an estimator are the most important hyperparameters.
        - it is wise to only use hyperparameters with numeric values,
        as changing categorical hyperparameters likely produces compatibility-errors.

        returns
        ---
        dict -> paramgrid for the estimator
        """
        # get all default values of parameters of the estimator:
        default_values = DefaultArgsDict.get(get_obj_name(estimator))
        default_ints = {k: v for k, v in default_values.items() if isinstance(v, (int))}
        default_floats = {k: v for k, v in default_values.items() if isinstance(v, (float)) and not np.isinf(v)}

        if not default_ints and not default_floats:
            return {}

        # create a paramgrid from the default values and distance factors:
        paramgrid = _create_paramgrid_from_distance_factors(
            n_vals_per_param,
            int_distance_factor,
            float_distance_factor,
            default_values,
            default_ints,
            default_floats,
        )

        # sort the paramgrid according to the order of the default values:
        used_default_args = {**default_ints, **default_floats}
        if include_string_args:
            default_strings = get_string_args_from_estimator(get_uncalled_estimator(estimator))
            paramgrid = {**paramgrid, **default_strings}
            used_default_args = {**used_default_args, **default_strings}

        param_hierarchy = [param for param in default_values if param in used_default_args]

        sorted_paramgrid = {param: paramgrid[param] for param in param_hierarchy}
        sorted_paramgrid = dict(islice(sorted_paramgrid.items(), 0, amt_params))
        sorted_paramgrid = {
            param: sorted(list(set(val))) if param in {**default_floats, **default_ints} else list(set(val))
            for param, val in sorted_paramgrid.items()
        }

        return sorted_paramgrid

    def _get_paramgrid_for_R3(
        self,
        estimator: EstimatorType,
        best_estimator_default_grid: Dict,
        sorted_scores_R2: Dict[EstimatorType, float],
        R3_min_correlation_to_best_score: float,
        int_distance_factor: float,
        float_distance_factor: float,
        max_iter: int,
    ) -> Tuple[Dict, Dict]:
        """return new_paramgrid for ROUND 3.

        Get the correlations between the parameters and the score.
        if there is some significant relationship or negative relationship,
        these parameters will be used further to extend a gridsearch in ROUND 3.

        Produce new ranges for paramgrid if values are found as first or
        last values in their range within the passed (and thus previous) paramgrid-parameter.
        Why? Because this signifies that expanding the range from this value
        might make it more likely to achieve better estimatorscores.
        """
        paramgrid_R3 = {}

        d = {}

        for idx, (estimator, score) in enumerate(sorted_scores_R2.items()):
            (
                default_ints,
                default_floats,
            ) = get_numerical_defaultargs_from_estimator(estimator)

            estimator_score = {
                **{
                    p: getattr(estimator, p)
                    for p in best_estimator_default_grid
                    if p in {**default_ints, **default_floats}
                },
                **{"score": score},
            }

            d.update({idx: estimator_score})
        paramgrid_df = pd.DataFrame.from_dict(d).T
        paramgrid_df = paramgrid_df if self.maximize_scoring else paramgrid_df[::-1]
        # take params which best score:
        corr_with_score = paramgrid_df.corr()["score"].drop("score")
        best_params = paramgrid_df.iloc[0].drop("score").to_dict()
        default_ints, default_floats = get_numerical_defaultargs_from_estimator(estimator)
        best_params = {k: int(v) if k in default_ints else v for k, v in best_params.items()}

        # if correlation of a parameter with score is equal to or higher than x
        # percent, use it for paramgrid_R3:
        parameters_which_show_correlation = corr_with_score.loc[
            (abs(corr_with_score) >= R3_min_correlation_to_best_score)
        ]
        # params which do not show correlation, will be used as default values for the estimator in R3:
        logger.notice(
            f"parameters of {get_obj_name(estimator)} which show higher correlation than absolute threshold of {R3_min_correlation_to_best_score}:\n{parameters_which_show_correlation.to_string()}",
        )
        default_params_R3 = {k: v for k, v in best_params.items() if k not in parameters_which_show_correlation.index}
        logger.notice(
            f"params which will be used as default values for estimator in R3 because they where NAN or not reach correlation threshold:\n{default_params_R3}"
        )

        if parameters_which_show_correlation.empty:
            return {}, {}
        n_vals_per_param = int(max_iter / parameters_which_show_correlation.shape[0])

        for param, corr in parameters_which_show_correlation.items():
            start_val = best_params[param]
            up = corr >= 0
            if start_val != 0:
                new_grid = self._get_gridrange_for_single_param(
                    int_distance_factor,
                    float_distance_factor,
                    n_vals_per_param,
                    start_val,
                    up=up,
                )
                paramgrid_R3.update({param: new_grid})

        return paramgrid_R3, default_params_R3

    def _get_gridrange_for_single_param(
        self,
        int_distance_factor,
        float_distance_factor,
        n_vals_per_param,
        start_val,
        up,
    ):
        d = [start_val]

        def zero_is_passed(x):
            return x <= 0 if start_val > 0 else x >= 0

        for n in range(1, n_vals_per_param):
            if isinstance(start_val, int):
                val = int(self._get_paramgrid_range_helper(start_val, int_distance_factor, n, up))
            else:
                val = self._get_paramgrid_range_helper(start_val, float_distance_factor, n, up)

            if zero_is_passed(val):
                break

            if up:
                d.append(val)
            else:
                d.insert(0, val)

        d = list(set(d))  # remove duplicate values
        new_grid = sorted(d, reverse=not up)

        return new_grid

    @functools.lru_cache
    def _get_paramgrid_range_helper(self, start_val, distance_factor, n, up=True):
        return (
            start_val + (((distance_factor - 1) * n) * start_val)
            if up
            else start_val - (((distance_factor - 1) * n) * start_val)
        )

    def _get_R2_weights_ranking(
        self, R2_weights: Dict[str, float], sorted_scores: Dict
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        mean_and_stdev = {}

        for idx, scores in enumerate(sorted_scores):
            scores_R2 = np.array(list(scores.values()))
            amt_unique_scores = len(np.unique(scores_R2))
            scores_R2_std = np.inf if scores_R2.std() == 0 else scores_R2.std()
            estimator = get_obj_name(list(scores.keys())[0])
            mean_and_stdev[estimator] = [
                scores_R2.mean(),
                scores_R2_std,
                amt_unique_scores,
                idx,
            ]

        mean_and_stdev = pd.DataFrame.from_dict(
            mean_and_stdev,
            orient="index",
            columns=["mean", "stdev", "amt_unique_scores", "idx_in_sorted_scores"],
        )

        s = pd.Series(mean_and_stdev["mean"].sort_values(ascending=self.maximize_scoring).index)
        mean_and_stdev["ranking_mean"] = pd.Series(s.index.values, index=s)

        s = pd.Series(mean_and_stdev.sort_values("stdev", ascending=False).index)
        mean_and_stdev["ranking_stdev"] = pd.Series(s.index.values, index=s)

        s = pd.Series(mean_and_stdev.sort_values("amt_unique_scores", ascending=True).index)
        mean_and_stdev["ranking_unique_scores"] = pd.Series(s.index.values, index=s)

        mean_and_stdev_results = mean_and_stdev[[col for col in mean_and_stdev if col.startswith("ranking")]]

        mean_and_stdev_weights = [w * 3 for w in R2_weights.values()]
        mean_and_stdev_results = (
            mean_and_stdev_results.mul(mean_and_stdev_weights).sum(axis=1).sort_values(ascending=False)
        )

        self.scores_R2_WEIGHTED = [i for scores in sorted_scores for i in islice(scores.items(), 0, 1)]
        self.scores_R2_WEIGHTED = [
            j
            for i in mean_and_stdev_results.index.to_list()
            for j in self.scores_R2_WEIGHTED
            if get_obj_name(j[0]) == i
        ]

        return mean_and_stdev, mean_and_stdev_results

    def _fit_estimator_bound_scount(
        self, estimator: EstimatorType, X: np.ndarray, y: np.ndarray
    ) -> Union[EstimatorType, Exception]:
        """collect information about lower/upper bounds in paramgrid between R1 and gridsearch,
        as well as already return some successful fitted estimators for R2."""
        try:
            estimator.fit(X, y)
            return estimator
        except Exception as e:
            return e

    def _end_fit_and_instantiate_best_estimator_best_score(
        self, best_estimator: EstimatorType, best_score: float, end_reason_msg: str
    ) -> None:
        self.best_estimator_ = best_estimator
        self.best_score_ = best_score
        logger.notice(f"{end_reason_msg}.\n{self.best_estimator_}\nbest score: {self.best_score_}")
