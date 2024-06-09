from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression, LinearRegression
import pandas as pd


def find_optimal_n_splits(
    X,
    y,
    type_estimator,
    cv_obj,
    estimator=None,
    min_splits=2,
    max_splits=10,
    scoring=None,
    n_jobs=None,
    verbose=0,
    **cv_obj_kwargs,
) -> pd.Series:
    """
    Analyzes the data using cross-validation and finds the optimal number of splits
    based on the average accuracy, R-squared score or custom scoring function across all splits.

    A simple regression algorithm is used to find the optimal number of splits.

    Parameters:
    X (numpy array or pandas DataFrame): Input data
    y (numpy array or pandas Series): Target values
    estimator (estimator object): Scikit-learn estimator object
    cv_obj (cross-validation object): Scikit-learn cross-validation object
    max_splits (int): Maximum number of splits to test. Last value is inclusive.

    Returns:
    optimal_splits (int): Optimal number of splits
    scores (list of floats): List of scores for each split
    """

    # Determine the score function based on the type of the target variable
    if estimator is None:
        if type_estimator == "regressor":
            estimator = LinearRegression()
        else:
            estimator = LogisticRegression()
    else:
        # check if estimator is instantiated:
        if isinstance(estimator, type):
            raise TypeError(f"{estimator} was passed uninstantiated. Please pass instantiated estimator!")

    # Initialize variables
    results_dict = {n: None for n in range(min_splits, max_splits + 1)}
    scoring = make_scorer(scoring) if scoring is not None else None

    # Loop through each number of splits
    for n_splits in range(min_splits, max_splits + 1):
        # Set the number of splits in the cross-validation object
        cv_obj_init = cv_obj(n_splits=n_splits, **cv_obj_kwargs) if cv_obj_kwargs else cv_obj(n_splits=n_splits)

        # Calculate cross-validation score
        score = cross_val_score(
            estimator,
            X,
            y,
            cv=cv_obj_init,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=0 if verbose < 1 else verbose,
        ).mean()

        # Save the score and check if it's the best so far
        results_dict[n_splits] = score

    # Convert the results to a pandas Series
    return pd.Series(results_dict)
