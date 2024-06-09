import random
from typing import List, Literal, Tuple

import pandas as pd
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import KFold, train_test_split

from orpheus.components.hypertuner.utils.helper_functions import all_estimators_extended
from orpheus.utils.type_vars import CrossValidatorType, EstimatorType


def get_X_y(
    random_state: int = 0,
    is_regression: bool = False,
    n_samples: int = 100,
    n_features: int = 5,
    n_categorical_features: int = 0,
) -> tuple:
    """Get X and y."""
    if n_categorical_features > n_features:
        raise ValueError("n_categorical_features cannot be larger than n_features")

    if is_regression:
        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=3,
            shuffle=False,
            random_state=random_state,
        )
    else:
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=3,
            n_redundant=0,
            n_repeated=0,
            shuffle=False,
            random_state=random_state,
        )

    # Convert to DataFrame for easier manipulation
    X = pd.DataFrame(X, columns=[f"col{i}" for i in range(1, n_features + 1)])

    # Convert the first 'n_categorical_features' columns to categorical
    for i in range(1, n_categorical_features + 1):
        col_name = f"col{i}"
        X[col_name] = pd.cut(X[col_name], bins=3, labels=["low", "medium", "high"])

    return X, y


def get_cv_obj() -> CrossValidatorType:
    """get cross-validation object."""
    return KFold(n_splits=2)


def get_X_y_train_test(
    random_state: int = 0,
    n_samples: int = 100,
    n_features: int = 5,
    n_categorical_features: int = 0,
    test_size=0.33,
    is_regression: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    get X_train, X_test, y_train, y_test.

    parameters
    ----------
    random_state: int = 0
        random state
    n_samples: int = 100
        number of samples in X and y
    n_features: int = 5
       total number of features in X.
       These will be called col1, col2, etc.
    n_categorical_features: int = 0
        number of categorical features in X.
        These will be called col1, col2 and will overwrite the first features.
    test_size: float = 0.33
        test size

    """
    X, y = get_X_y(
        random_state=random_state,
        is_regression=is_regression,
        n_samples=n_samples,
        n_features=n_features,
        n_categorical_features=n_categorical_features,
    )
    y = pd.Series(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test


def get_estimator_list(random_state: int = 0, is_regression: bool = False) -> List[EstimatorType]:
    """get all sklearn estimators in a list and randomly shuffle the list."""
    type_estimator: Literal["classifier", "regressor"] = "regressor" if is_regression else "classifier"
    estimator_list = [e[1] for e in all_estimators_extended(type_filter=type_estimator)][:7]
    random.seed(random_state)
    random.shuffle(estimator_list)
    return estimator_list
