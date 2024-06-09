import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.impute import SimpleImputer


def impute_nans(data: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing values in a DataFrame.

    For object dtype columns, use 'most_frequent' strategy.
    For numerical columns, use 'mean' strategy.

    Parameters:
        data (pd.DataFrame): DataFrame with missing values

    Returns:
        pd.DataFrame: DataFrame with missing values imputed
    """
    # Check total number of NaNs
    nan_amt = data.isna().sum().sum()

    if nan_amt > 0:
        for col in data.columns:
            if data[col].isna().sum() > 0:
                if is_numeric_dtype(data[col]):
                    strategy = "mean"
                else:  # non numerical type
                    strategy = "most_frequent"
                imputer = SimpleImputer(strategy=strategy)
                # Reshape to be a 2D array and impute
                data[col] = imputer.fit_transform(data[col].to_numpy().reshape(-1, 1)).iloc[:, 0].to_numpy()

    return data
