import pandas as pd
from sklearn.metrics import accuracy_score, r2_score

from src.orpheus.evaluators.evaluator import Evaluator
from src.orpheus.evaluators.model_explainer import ModelExplainer
from src.orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from src.orpheus.services.performance_service import PerformanceService
from src.orpheus.utils.logger import logger


def pass_pipelines_for_testing(
    IS_REGRESSION: bool,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    pipeline_base: MultiEstimatorPipeline,
    pipeline_stacked: MultiEstimatorPipeline,
    pipeline_evolved: MultiEstimatorPipeline,
):
    """
    Pass the pipelines and execute as much as possible for the sake of testing functionality.
    """
    # Make predictions
    pred_pipeline_base = pipeline_base.predict(X_test)
    pred_pipeline_stacked = pipeline_stacked.predict(X_test)
    pred_evolved = pipeline_evolved.predict(X_test)

    # Evaluate robustness
    evaluator = Evaluator(r2_score if IS_REGRESSION else accuracy_score)
    for pipe_name, pipe in [
        ("pipeline_base", pipeline_base),
        ("pipeline_stacked", pipeline_stacked),
        ("pipeline_evolved", pipeline_evolved),
    ]:
        robustness_score = evaluator.evaluate_robustness(X_test, y_test, pipe)
        logger.notice(f"robustness {pipe_name}: \n{robustness_score}")

    # Explain feature importance
    explainer = ModelExplainer(pipeline_base, X_train, mode="regression" if IS_REGRESSION else "classification")
    explained_features = explainer.explain_all(X_test)
    logger.notice(f"explained features head: \n{explained_features.head()}")

    # Evaluate performance and distribution
    for pred_name, pred in [
        ("pred_pipeline_base", pred_pipeline_base),
        ("pred_pipeline_stacked", pred_pipeline_stacked),
        ("pred_evolved", pred_evolved),
    ]:
        performance_score = evaluator.evaluate_performance(y_test, pred)
        distribution = evaluator.get_distribution(y_test, pred)
        logger.notice(f"evaluate performance {pred_name}: \n{performance_score}")
        logger.notice(f"get distribution {pred_name}: \n{distribution}")

    # Optimize n_jobs
    for pipe_name, pipe in [
        ("pipeline_base", pipeline_base),
        ("pipeline_stacked", pipeline_stacked),
    ]:
        optimized_n_jobs = pipe.optimize_n_jobs(X_test)
        logger.notice(f"optimize n_jobs {pipe_name}: \n{optimized_n_jobs}")

    # Build robust pipelines
    for pipe_name, pipe in [
        ("pipeline_base", pipeline_base),
        ("pipeline_stacked", pipeline_stacked),
        ("pipeline_evolved", pipeline_evolved),
    ]:
        ps = PerformanceService(pipe, X_train, X_val, y_val, r2_score if IS_REGRESSION else accuracy_score)
        robust_pipeline = ps.stress_test_pipeline(
            overwrite_pipeline=True,
            threshold_score=-50,  # low threshold_score to prevent from raising PipelineNotRobustError
            pipeline_name=pipe_name,
        )
        logger.notice(f"weights {pipe_name}: \n{robust_pipeline.get_weights()}")
        logger.notice(f"scores {pipe_name}: \n{robust_pipeline.scores}")
        logger.notice(f"{pipe_name} succesfully build robust pipeline through PerformanceService")

        # Update scores
        scores = ps.get_scores()
        robust_pipeline.update_scores(scores)
        logger.notice(
            f"succesfully updated scores {pipe_name}: \n{robust_pipeline.scores}",
        )
        logger.notice(f"{robust_pipeline.get_name_by_index(0)}")
        logger.notice(f"{robust_pipeline.get_stats()}")
