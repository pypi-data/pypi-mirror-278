from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split


def get_boston_housing_set() -> Tuple[pd.DataFrame, pd.Series]:
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
    X = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    y = raw_df.values[1::2, 2]

    columns = [f"feature_{i}" for i in range(X.shape[1])]
    X = pd.DataFrame(X, columns=columns)
    y = pd.Series(y, name="target")

    return X, y


def get_titanic_dataset(
    test_size=0.25, random_state=42, stratify=True
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """return titanic dataset"""

    X, y = fetch_openml("titanic", version=1, as_frame=True, return_X_y=True)
    X.drop(["boat", "body", "home.dest"], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y if stratify else None, test_size=test_size, random_state=random_state
    )

    X_train.drop(["cabin"], axis=1, inplace=True)
    X_test.drop(["cabin"], axis=1, inplace=True)

    for dataset in [X_train, X_test]:
        dataset["family_size"] = dataset["parch"] + dataset["sibsp"]
        dataset.drop(["parch", "sibsp"], axis=1, inplace=True)
        dataset["is_alone"] = 1
        dataset["is_alone"].loc[dataset["family_size"] > 1] = 0

    for dataset in [X_train, X_test]:
        dataset["title"] = dataset["name"].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]
        dataset.drop(["name"], axis=1, inplace=True)

    X_comb = pd.concat([X_train, X_test])
    rare_titles = X_comb["title"].value_counts() < 10
    for dataset in [X_train, X_test]:
        dataset.title.loc[dataset.title == "Miss"] = "Mrs"
        dataset["title"] = dataset.title.apply(lambda x: "rare" if rare_titles[x] else x)

    for dataset in [X_train, X_test]:
        dataset.drop("ticket", axis=1, inplace=True)

    X_train["fare"].fillna(X_train["fare"].median(), inplace=True)
    X_test["fare"].fillna(X_train["fare"].median(), inplace=True)
    X_test["age"].fillna(X_train["age"].mean(), inplace=True)
    X_train["age"].fillna(X_train["age"].mean(), inplace=True)

    y_train = y_train.astype(int)
    y_test = y_test.astype(int)

    return X_train, X_test, y_train, y_test
