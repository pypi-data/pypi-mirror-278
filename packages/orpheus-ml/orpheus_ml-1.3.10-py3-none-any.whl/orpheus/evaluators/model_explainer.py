"""ModelExplainer class for generating explanations of model predictions using LIME (Local Interpretable Model-agnostic Explanations)."""

from functools import partial
from typing import Callable, Dict, List, Literal, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from orpheus._vendor.lime import lime_tabular
from orpheus._vendor.lime.explanation import Explanation
from orpheus.services.additional_types.multi_estimator_pipeline import MultiEstimatorPipeline
from orpheus.utils.type_vars import EstimatorType
from orpheus.validations.input_checks import DataValidation
from orpheus.utils.logger import logger

# lime==0.2.0.1


class ModelExplainer:
    """
    A class for generating explanations of model predictions using LIME (Local Interpretable Model-agnostic Explanations).

    Public attributes:
    -----------
    model: The trained machine learning model.
    train_data (pd.DataFrame): The training data.
    class_names (Optional[List[str]]): List of class names for classification tasks.
    mode (str): The mode of the explainer ('classification' or 'regression').
    explainer (lime_tabular.LimeTabularExplainer): LIME explainer instance.
    """

    def __init__(
        self,
        model: Union[MultiEstimatorPipeline, EstimatorType],
        X_train: pd.DataFrame,
        mode: Literal["classification", "regression"],
        class_names: Optional[List[str]] = None,
        discretize_continuous: bool = True,
    ):
        """
        Initialize the ModelExplainer class.

        Parameters:
        -----------
        model: A trained machine learning model with a predict() or predict_proba() method.
        X_train (DataFrame): The training data used to train the model.
        mode (str, optional): The mode of the explainer. Must be either 'classification' or 'regression'. Default is 'classification'.
        class_names (Optional[List[str]], optional): List of class names for classification tasks. Not required for regression tasks.
        discretize_continuous (bool, optional): Flag to control whether continuous features should be discretized. Default is True.
        """
        if mode not in {"classification", "regression"}:
            raise ValueError("mode should be either 'classification' or 'regression'")

        if isinstance(model, MultiEstimatorPipeline):
            X_train = model.transform_only(X_train)

        DataValidation.validate_xy_types({"X_train": X_train})

        self.model = model
        self.train_data = X_train.to_numpy()
        self.feature_names = X_train.columns.to_list()
        self.class_names = class_names
        self.mode = mode
        self.explainer = self._create_explainer(
            categorical_features=None,
            categorical_names=None,
            discretize_continuous=discretize_continuous,
        )

    def __repr__(self):
        return f"ModelExplainer(model={self.model}, train_data={self.train_data}, feature_names={self.feature_names}, class_names={self.class_names}, mode={self.mode})"

    def explain_sample(
        self, sample: pd.Series, num_features: int = 10, plot=True, prob_func: Optional[Callable] = None, **kwargs
    ) -> Explanation:
        """
        Explain the model through LIME through a single sample.

        parameters
        ----------
        sample: np.ndarray
            Sample to explain. Should be a 1D array corresponding to a single row.
        num_features: int
            Number of features to include in the explanation.
        plot: bool
            Whether to plot the explanation.
        **kwargs:
            keyword arguments to pass to the explainer.
            See explanation here: https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_tabular.LimeTabularExplainer.explain_instance

        returns
        -------
        Returns:
            An Explanation object (see _vendor.lime.explanation.py) with the corresponding
            explanations.
            And the predicted value(s) of the model.
            For classification, this is the probability of the predicted class.
            For regression, this is the predicted value.


        """
        if not isinstance(sample, pd.Series):
            raise ValueError("sample should be a pd.Series")

        if prob_func is None:
            prob_func = self._get_prob_func()

        exp: Explanation = self.explainer.explain_instance(sample, prob_func, num_features=num_features, **kwargs)

        if plot:
            exp.as_pyplot_figure()
            plt.tight_layout()
            plt.show()

        return exp

    def explain_all(
        self,
        X: pd.DataFrame,
        fraction: float = 1.0,
        shuffle: bool = False,
        plot: bool = False,
        num_features: Optional[int] = None,
        random_state: Optional[int] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Explain the model through LIME for all *fraction*% samples in self.X_train
        Uses the explain_sample() method to explain each sample and takes the average of the feature importances.

        If self.model is a MultiEstimatorPipeline ,only the first (and normally leading) model in the pipeline is used for predictions.

        parameters
        ----------
        X: pd.DataFrame
            Samples to explain. Should be a pd.DataFrame.
        fraction: float
            Fraction of samples to explain. Default is 1.0.
        random_state: int
            Random state for sampling. If None, no random state is set.
        num_features: int
            Number of features to include in the explanation.
        **kwargs:
            keyword arguments to pass to the explainer.
            See explanation here: https://lime-ml.readthedocs.io/en/latest/lime.html

        returns
        -------
        pd.DataFrame:
            A DataFrame with the samples, explanations and predictions.
            Only the first (and normally leading) model in the pipeline is used for predictions.
        """
        prob_func = self._get_prob_func()

        if isinstance(self.model, MultiEstimatorPipeline):
            X = self.model.transform_only(X)
            prob_func = partial(prob_func, exclude_transformers=True)

        X_validated, num_features = self._validate_explain_all(X, fraction, shuffle, num_features, random_state)

        # get explanations for all samples
        explanations = self._gather_explanations(X_validated, num_features, kwargs, prob_func)
        explained_features = [exp.as_map()[1] for exp in explanations]
        explanation_dict: Dict[str, List] = {feat[0]: [] for feat in explained_features[0]}

        for feat in explained_features:
            for key, val in feat:
                explanation_dict[key].append(val)

        exp_df = pd.DataFrame.from_dict(explanation_dict)
        mapped_cols = {i: f"explanation_{col}" for i, col in enumerate(X_validated.columns)}
        exp_df = exp_df.rename(columns=mapped_cols)

        # get predictions for all samples
        model_index_0_preds = [
            exp.predict_proba if self.mode == "classification" else exp.predicted_value for exp in explanations
        ]
        if self.mode == "classification":
            pred_column_names = (
                self.class_names
                if self.class_names is not None
                else [f"prediction_class_{i}" for i in range(len(model_index_0_preds[0]))]
            )
        else:
            pred_column_names = ["prediction"]
        preds = pd.DataFrame(np.array(model_index_0_preds), columns=pred_column_names)

        # concat features, explanations and predictions
        df = pd.concat([X_validated.set_index(exp_df.index), exp_df, preds], axis=1)

        if plot:
            sorted_feat_results = exp_df.describe().sort_values(by="mean", ascending=False, axis=1)
            sorted_feat_results.columns = sorted_feat_results.columns.str.replace("explanation_", "")
            self._plot_feature_importance(sorted_feat_results)

        return df

    def _validate_explain_all(self, X, fraction, shuffle, num_features, random_state):
        """Validate the input for the explain_all() method and return the validated input."""
        assert set(X.columns) == set(
            self.feature_names
        ), f"X should have the same columns as the training data! Systematic difference: {set(X.columns) ^ set(self.feature_names)}"
        if num_features is None:
            num_features = X.shape[1]
        if not 0.0 < fraction <= 1.0:
            raise ValueError(f"fraction must be higher than 0 and lower than or equal to 1, but got {fraction}")
        if fraction < 1.0:
            X, _ = train_test_split(X, random_state=random_state, test_size=1 - fraction, shuffle=shuffle)

        return X, num_features

    def _gather_explanations(self, X, num_features, kwargs, prob_func) -> List[Explanation]:
        explanations = []
        total_samples = X.shape[0]

        for idx, (_, sample) in enumerate(X.iterrows(), start=1):
            logger.info(f"Explaining sample {idx}/{total_samples} through LIME, containing {num_features} features.")
            try:
                exp = self.explain_sample(sample, num_features=num_features, plot=False, prob_func=prob_func, **kwargs)
            except (NotImplementedError, ValueError, KeyError):
                prob_func = partial(prob_func, transform_discrete=True)
                exp = self.explain_sample(sample, num_features=num_features, plot=False, prob_func=prob_func, **kwargs)
            except Exception as e:
                raise e from None
            explanations.append(exp)

        return explanations

    def _plot_feature_importance(self, sorted_feat_results: pd.DataFrame) -> None:
        """Plot the feature importances from the explain_all() method."""
        mean_row = sorted_feat_results.loc["mean"][::-1]
        std_row = sorted_feat_results.loc["std"][::-1]

        # Combine them into a new DataFrame for plotting
        plot_df = pd.DataFrame({"mean": mean_row, "std": std_row})

        # Create the grouped bar chart
        ax = plot_df.plot(kind="barh", color=["g", "b"])

        # Generate colors based on mean values
        colors = ["g" if value > 0 else "r" for value in mean_row]

        # Manually set the colors for the 'mean' bars
        for i, bar in enumerate(ax.patches[: len(colors)]):
            bar.set_color(colors[i])

        plt.title("LIME Feature Importances")
        plt.tight_layout()
        plt.show()

    def _create_explainer(
        self, categorical_features, categorical_names, discretize_continuous
    ) -> lime_tabular.LimeTabularExplainer:
        """Create the LIME explainer instance."""
        explainer = lime_tabular.LimeTabularExplainer(
            self.train_data,
            feature_names=self.feature_names,
            class_names=self.class_names,
            categorical_features=categorical_features,
            categorical_names=categorical_names,
            discretize_continuous=discretize_continuous,
            mode=self.mode,
        )
        return explainer

    def _get_prob_func(self):
        """Get the predict or predict_proba method of the model, depending on the mode."""
        if self.mode == "classification":
            prob_func = self.model.predict_proba
        elif self.mode == "regression":
            prob_func = self.model.predict
        else:
            raise ValueError("Invalid mode. Choose 'classification' or 'regression'.")
        return prob_func
