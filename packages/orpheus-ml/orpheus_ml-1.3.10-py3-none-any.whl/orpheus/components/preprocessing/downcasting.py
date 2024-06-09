from typing import Optional, Union

import numpy as np
import pandas as pd
from numpy.typing import DTypeLike
from pandas.api.types import is_float_dtype


class Downcasting:
    @staticmethod
    def downcast(
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        dtype: Optional[DTypeLike] = None,
    ) -> Union[pd.DataFrame, pd.Series, np.ndarray]:
        """
        downcast data and y to smaller size for memory purposes.
        if dtype is None, the smallest possible dtype is used.
        """
        if isinstance(data, pd.DataFrame):
            return Downcasting.downcast_dataframe(data)
        elif isinstance(data, pd.Series):
            return (
                pd.to_numeric(data, downcast="float")
                if is_float_dtype(data.dtype)
                else pd.to_numeric(data, downcast="integer")
            )
        elif isinstance(data, np.ndarray):
            dtype = np.min_scalar_type(data.max())
            if is_float_dtype(dtype):
                dtype = np.float32
            return data.astype(dtype)
        else:
            raise TypeError(f"unsupported type: {type(data)}")

    @staticmethod
    def downcast_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        downcast dataframe for speed, performance and memory purposes.
        NOTE: this method is not meant to be used on categorical data. Also, precision loss is possible if data contains more than 6 decimals.

        Parameters:
        ---
        df: pd.DataFrame
            dataframe to be downcasted.

        returns
        ---
        downcasted dataframe.

        """
        fcols = df.select_dtypes("float").columns
        icols = df.select_dtypes("integer").columns

        df_f = df[fcols].apply(pd.to_numeric, downcast="float")
        df_i = df[icols].apply(pd.to_numeric, downcast="integer")
        return pd.concat([df_f, df_i], axis=1)
