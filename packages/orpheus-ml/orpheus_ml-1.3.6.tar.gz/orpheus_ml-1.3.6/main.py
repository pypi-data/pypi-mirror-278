"""This script is a proof of concept for a complete ML Pipeline, with the goal of automating the process of finding the best model for a given data set."""


import sys
import time

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, r2_score

from datasets.datasets import get_boston_housing_set

sys.path.append(".")
sys.path.append("src")
from src.orpheus import PipelineOrchestrator, PipelineOrchestratorProxy

# import faulthandler
# faulthandler.enable()
# faulthandler.dump_traceback_later(30, exit=True)

if __name__ == "__main__":

    def run_loop(CONFIG_PATH, VERBOSE, N_JOBS, METRIC, X, y, estimator_list):
        X = X.copy()
        y = y.copy()

        orchestrator: PipelineOrchestrator = PipelineOrchestratorProxy(
            PipelineOrchestrator(
                X,
                y,
                metric=METRIC,
                config_path=CONFIG_PATH,
                verbose=VERBOSE,
                n_jobs=N_JOBS,
                shuffle=True,
                stratify=False,
                ensemble_size=0.1,
                validation_size=0.1,
                log_file_path=None,
                log_file_mode="w+",
                estimator_list=estimator_list,
                use_sklearn_estimators_aside_estimator_list=True,
                n_splits_if_cv_obj_is_none=2,
                log_cpu_memory_usage=True,
            ),
            dataset_name=f"some_{'classifier' if not USE_REGRESSION_DATA else 'regressor'}_set",
        )

        pipe_dict = (
            orchestrator.build(
                scale=False,
                add_features=False,
                remove_features=False,
                generations=["base", "stacked", "evolved"],
                timeout_duration=None,
            )
            .refit_pipelines(
                on_test=True,
                on_validation=True,
                on_train=True,
            )
            .fortify(
                optimize_n_jobs=False,
                threshold_score=None,
                fraction_to_explain=0,
                plot_explaining=False,
            )
        )

        return orchestrator

    # STUB DATA. replace METRIC with the metric of your choice and X, y with your data
    CONFIG_PATH = "configurations"
    USE_REGRESSION_DATA = True
    VERBOSE = 3
    N_JOBS = 12

    METRIC = r2_score if USE_REGRESSION_DATA else accuracy_score

    X, y = (
        get_boston_housing_set()
        if USE_REGRESSION_DATA
        else make_classification(
            n_samples=10_000,
            n_features=10,
        )
    )
    X = pd.DataFrame(X)
    X.columns = [f"feature_{N}" for N in range(1, X.shape[1] + 1)]
    y = pd.Series(y)


    start = time.time()

    orchestrator: PipelineOrchestratorProxy = run_loop(
        CONFIG_PATH, VERBOSE, N_JOBS, METRIC, X, y, estimator_list=estimator_list
    )

    res_id = orchestrator.write_dto_to_db()
    # print("DTO written to disk:", res_id)
    # res = orchestrator._repository.get_dto_by_id(res_id)

    # print(orchestrator.pipelines["base"].score(orchestrator.X_test, orchestrator.y_test))
    # print(orchestrator.pipelines["base"].predict(orchestrator.X_test, n_jobs=2))
    # print(orchestrator.pipelines["base"].predict_proba(orchestrator.X_test, transform_discrete=True))

    # print(orchestrator.pipelines["stacked"].score(orchestrator.X_test, orchestrator.y_test))
    # print(orchestrator.pipelines["stacked"].predict(orchestrator.X_test, n_jobs=2))
    # print(orchestrator.pipelines["stacked"].predict_proba(orchestrator.X_test, transform_discrete=True))

    print(f"Time elapsed: {time.time() - start}")
