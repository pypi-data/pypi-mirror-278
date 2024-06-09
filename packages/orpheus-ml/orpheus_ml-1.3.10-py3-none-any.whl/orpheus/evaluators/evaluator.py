"""Evaluator class for checking evaluation of model performance."""

from typing import Callable, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from orpheus.evaluators.model_evaluators import (
    ClassificationEvaluator,
    RegressionEvaluator,
)
from orpheus.metrics.metric_converter import MetricConverter
from orpheus.services.additional_types.multi_estimator_pipeline import (
    MultiEstimatorPipeline,
)
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger


class Evaluator:
    """Evaluator class for checking evaluation of model performance."""

    def __init__(self, metric: Callable):
        """
        Evaluator class for checking evaluation of model performance and distribution of predicted values.

        Parameters
        ----------
        metric: Callable
            Scoring function.

        Attributes
        ----------
        metric: Callable
            The scoring function.
        name: str
            The name of the scoring function.
        maximize_scoring: bool
            Whether the score should be maximized or minimized.
        type_estimator: str
            The type of estimator ("classifier" or "regressor").

        public methods
        --------------
        evaluate(y_true, y_pred)
            Evaluate the model performance.
        get_distribution(y_true, y_pred, plot=False)
            Evaluate the model performance and plot the distribution of predicted values.


        """
        self.metric: Callable = metric
        self.name: str = get_obj_name(metric)
        self._metric_converter: MetricConverter = MetricConverter(self.metric)
        self.type_estimator: str = self._metric_converter.type_estimator
        self.maximize_scoring: bool = self._metric_converter.maximize_scoring

    def __repr__(self):
        return f"Evaluator({self.name})"

    def evaluate_performance(self, y_true: np.ndarray, y_pred: np.ndarray) -> Union[float, pd.Series]:
        """
        Evaluate the model performance. Can accept a list of predictions.

        Parameters
        ----------
        y_true: array-like
            True values.
        y_pred: array-like or a list of arrays.
            Predicted values.

        Returns
        -------
        score: float
            Score of the model.
        """
        results = {}
        for model_idx, pred in enumerate(y_pred):
            try:
                result = self.metric(y_true, pred)
                results[model_idx] = result

            except ValueError as e:
                logger.error(f"Model with index {model_idx} failed: {e}")
                results[model_idx] = np.nan
        return pd.Series(results)

    def evaluate_robustness(
        self,
        X_val: np.ndarray,
        y_val: np.ndarray,
        pipeline: MultiEstimatorPipeline,
        clf_max_occurance_pct: float = 0.8,
        reg_trials: int = 5,
    ) -> List[int]:
        """
        Evaluate the robustness of models by performing some robustness checks.
        Then, return the indexes of the models that passed the checks.

        Parameters
        ----------
        X_val: array-like
            Validation data.
        y_val: array-like
            Validation labels.
        pipeline: MultiEstimatorPipeline
            Pipeline of which the models will be evaluated.
            Predict method must return a list of multiple predictions.
        clf_max_occurance_pct: float
            Maximum percentage of occurance of a value in the predicted values.
            NOTE: Only used for classification.
        reg_trials: int
            Number of trials to perform for the robustness check.
            NOTE: Only used for regression.

        Returns
        -------
        indexes_to_keep: list
            List of indexes of the models that passed the robustness check.
            If no models passed the check, the list will be empty.
        """
        if self.type_estimator == "classifier":
            y_pred = pipeline.predict(X_val)
            clf_evaluator = ClassificationEvaluator()
            indexes_to_keep = clf_evaluator.evaluate_classifier(y_pred, clf_max_occurance_pct)
        elif self.type_estimator == "regressor":
            reg_evaluator = RegressionEvaluator(X_val, y_val, self.metric, self.maximize_scoring)
            indexes_to_keep = reg_evaluator.evaluate_regressor(pipeline, reg_trials)
        else:
            raise ValueError(
                f"Type of estimator {self.type_estimator} not supported. "
                "Only 'classifier' and 'regressor' are supported."
            )

        return list(indexes_to_keep)

    def get_distribution(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        plot: bool = False,
    ):
        """
        get the distribution of predicted and true values.

        Parameters
        ----------
        y_true: array-like
            True values.
        y_pred: array-like or a list of arrays.
            Predicted values.
        plot: bool
            Whether to plot a distribution of predicted values.

        Returns
        -------
        pred_distribution: pd.DataFrame
            DataFrame with the distribution of predicted values.
            If y_pred is a list of arrays, the DataFrame will have a column for each array,
            with the index of the model as the column name.
            Else, the DataFrame will have a column for the predicted values.
        """
        if self.type_estimator == "regressor":
            if plot:
                self._plot_dist_regression(y_true, y_pred)
            bins_true = np.histogram(y_true, bins="auto")[1]
            true_distribution = dict(zip(bins_true, np.histogram(y_true, bins=bins_true)[0]))
            bins_pred = np.histogram(y_pred, bins=bins_true)[1]
            pred_distribution = self._get_pred_dist_regression(y_pred, bins_true, bins_pred)
        elif self.type_estimator == "classifier":
            if plot:
                self._plot_dist_classification(y_true, y_pred)
            unique_classes, class_counts = np.unique(y_true, return_counts=True)
            true_distribution = dict(zip(unique_classes, class_counts))

            pred_distribution = self._get_pred_dist_classification(y_pred, unique_classes)
        else:
            raise ValueError(
                f"Type of estimator {self.type_estimator} not supported. "
                "Only 'classifier' and 'regressor' are supported."
            )

        if all(isinstance(v, dict) for v in pred_distribution.values()):
            dist_df = pd.DataFrame({**{"True": true_distribution}, **pred_distribution})
        else:
            dist_df = pd.DataFrame({"True": true_distribution, "Predicted": pred_distribution})

        return dist_df

    def _get_pred_dist_classification(self, y_pred: np.ndarray, unique_classes: np.ndarray):
        pred_gen = map(
            lambda x: dict(zip(unique_classes, np.unique(x, return_counts=True)[1])),
            y_pred,
        )
        pred_distribution = {model_idx: pred for model_idx, pred in enumerate(pred_gen)}

        return pred_distribution

    def _get_pred_dist_regression(self, y_pred, bins_true, bins_pred):
        pred_gen = map(
            lambda x: dict(zip(bins_pred, np.histogram(x, bins=bins_true)[0])),
            y_pred,
        )
        pred_distribution = {model_idx: pred for model_idx, pred in enumerate(pred_gen)}

        return pred_distribution

    def _plot_dist_regression(self, y_true: np.ndarray, y_pred_list: np.ndarray):
        """Plot the distribution of predicted values for regression."""
        y_colors = ["red", "blue"]
        num_plots, fig, axs = self._get_fig_and_axs(y_pred_list)

        if isinstance(axs, np.ndarray) and axs.ndim != 1:
            axs = axs.flatten()

        for idx, (ax, y_pred) in enumerate(zip(axs, y_pred_list)):
            self._plot_scatter(y_true, y_pred, y_colors, ax)
            ax.set_title(f"Model index {idx}")
        fig.suptitle(f"Multi-plot distribution {self.name}")
        plt.subplots_adjust(top=0.9, hspace=0.4)  # Adjust top and hspace parameters
        plt.show()

    def _plot_dist_classification(self, y_true: np.ndarray, y_pred: np.ndarray):
        """Plot the distribution of predicted values for classification."""
        self._multi_plot_dist_classification(y_true, y_pred)

    def _multi_plot_dist_classification(self, y_true, y_pred_list):
        num_plots, fig, axs = self._get_fig_and_axs(y_pred_list)

        colors = ["green", "blue"]  # Set colors for true and predicted values

        for idx, (ax, y_pred) in enumerate(zip(axs.flatten(), y_pred_list)):
            if idx < num_plots:
                self._plot_histogram(ax, y_true, y_pred, colors)
                ax.set_title(f"Model index {idx}")
                ax.set_xlabel("Class")
                ax.set_ylabel("Count")
                n_classes = max(np.max(y_true), np.max(y_pred)) + 1
                ax.set_xticks(np.arange(n_classes) + 0.5)
                ax.set_xticklabels(np.arange(n_classes))
                ax.legend(loc="upper left", fontsize="small")
            else:
                fig.delaxes(ax)  # Remove unused subplots

        fig.suptitle(f"Multi-plot distribution {self.name}")
        plt.subplots_adjust(top=0.9, hspace=0.4)  # Adjust top and hspace parameters
        plt.show()

    def _plot_histogram(self, ax, y_true, y_pred, colors):
        n_classes = max(np.max(y_true), np.max(y_pred)) + 1
        for label in np.unique(y_true):
            ax.hist(
                y_true[y_true == label],
                bins=np.arange(n_classes + 1),
                color=colors[0],
                label="True values" if label == 0 else None,
                histtype="step",
                lw=3,
            )
            ax.hist(
                y_pred[y_pred == label],
                bins=np.arange(n_classes + 1),
                alpha=0.5,
                color=colors[1],
                label="Predicted values" if label == 0 else None,
                linewidth=2,
            )

    def _plot_scatter(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_colors: List[str],
        ax: plt.Axes,
    ):
        ax.scatter(range(len(y_true)), y_true, color=y_colors[0], label="True values")
        ax.scatter(
            range(len(y_pred)),
            y_pred,
            color=y_colors[1],
            label="Predicted values",
        )
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.legend(loc="upper left", fontsize="small")

    def _get_fig_and_axs(self, y_pred_list: np.ndarray) -> Tuple[int, plt.Figure, np.ndarray]:
        num_plots = len(y_pred_list)
        n_rows = (num_plots - 1) // 4 + 1
        n_cols = min(num_plots, 4)
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True)

        if not isinstance(axs, np.ndarray):
            axs = np.array([axs])

        return num_plots, fig, axs
