"""helperfunctions for orchestrator module"""
from typing import Tuple

import numpy as np
import pandas as pd


def create_multi_column_samples_infer_type(
    df: pd.DataFrame, row_index: int, col_min_max_tuples: Tuple[str, np.number, np.number], N: int
) -> pd.DataFrame:
    """
    Create N new samples based on an existing row in a DataFrame with random values in multiple columns.
    The data type of each random value is inferred from the original value in the DataFrame.

    Parameters
    ----------
    - df (DataFrame): The original DataFrame
    - row_index (int): The index of the row to use for creating new samples
    - col_min_max_tuples (list of tuples): List of tuples containing column name, min value, and max value
      Example: [("col1", 5, 10), ("col2", 3, 7)]
    - N (int): The number of new samples to create

    Returns
    ------
    - DataFrame: A DataFrame containing the new samples

    Example
    -------
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4.0, 5.0, 6.0],
        'C': [True, False, True]
    })

    new_samples = create_multi_column_samples_infer_type(
        df,
        row_index=1,
        col_min_max_tuples=[("A", 1, 5), ("B", 2, 10), ("C", 0, 1)],
        N=5
    )
    """
    # Validate the inputs
    if row_index not in df.index:
        raise ValueError("Invalid row index")
    for col, min_val, max_val in col_min_max_tuples:
        if col not in df.columns:
            raise ValueError(f"Invalid column name: {col}")
        if min_val > max_val:
            raise ValueError(f"min_value should be less than or equal to max_value for column {col}")
    if N <= 0:
        raise ValueError("N should be greater than 0")

    # Extract the row to be duplicated
    original_row = df.loc[row_index]

    # Create N new samples
    new_samples = pd.DataFrame([original_row] * N)

    # Replace the values in the specified columns with random values between min_value and max_value
    for col, min_val, max_val in col_min_max_tuples:
        original_value = original_row[col]
        if isinstance(original_value, bool):
            new_samples[col] = np.random.choice([True, False], N)
        elif isinstance(original_value, (int, float)):
            new_samples[col] = np.random.uniform(min_val, max_val, N)
            if isinstance(original_value, int):
                new_samples[col] = new_samples[col].astype(int)

    return new_samples
