"""Functions which are applicable to timeseries."""


import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_rolling_statistics(df: pd.DataFrame, col: str, window: int = 5) -> pd.DataFrame:
    """Add rolling statistics to a timeseries.

    Parameters
    ----------
    df : pd.DataFrame
        timeseries
    window : int, optional
        window size, by default 5

    Returns
    -------
    pd.DataFrame
        timeseries with rolling statistics
    """

    def autocorr(x: pd.Series) -> float:
        return x.autocorr()

    df_rolling = df.copy()

    df_rolling[f"{col}_mean_rolling_{window}"] = df[col].rolling(window=window).mean()
    df_rolling[f"{col}_std_rolling_{window}"] = df[col].rolling(window=window).std()
    df_rolling[f"{col}_sem_rolling_{window}"] = df[col].rolling(window=window).sem()
    df_rolling[f"{col}_min_rolling_{window}"] = df[col].rolling(window=window).min()
    df_rolling[f"{col}_25_quantile_rolling_{window}"] = df[col].rolling(window=window).quantile(0.25)
    df_rolling[f"{col}_50_quantile_rolling_{window}"] = df[col].rolling(window=window).quantile(0.5)
    df_rolling[f"{col}_75_quantile_rolling_{window}"] = df[col].rolling(window=window).quantile(0.75)
    df_rolling[f"{col}_max_rolling_{window}"] = df[col].rolling(window=window).max()
    df_rolling[f"{col}_skew_rolling_{window}"] = df[col].rolling(window=window).skew()
    df_rolling[f"{col}_kurt_rolling_{window}"] = df[col].rolling(window=window).kurt()
    df_rolling[f"{col}_var_rolling_{window}"] = df[col].rolling(window=window).var()
    df_rolling[f"{col}_sum_rolling_{window}"] = df[col].rolling(window=window).sum()
    df_rolling[f"{col}_autocorr_rolling_{window}"] = df[col].rolling(window=window).apply(autocorr, raw=False)

    return df_rolling


def plot_results_as_pdf(X_test, y_test, y_pred, pdf_name="output"):
    """
    plot results of a timeseries in a pdf. One image is plotted per page.
    """

    true_series = np.concatenate((X_test, y_test.reshape(-1, 1)), axis=1)
    pred_series = np.concatenate((X_test, y_pred.reshape(-1, 1)), axis=1)

    pdf = matplotlib.backends.backend_pdf.PdfPages(f"{pdf_name}.pdf")

    n_figs = len(true_series)
    plt.figure(1)  # create figure outside loop

    for j in range(n_figs):  # create all figures
        # plt.suptitle("figure {}" .format(j+1))
        plt.xticks(range(0, len(pred_series[0])))
        plt.plot(pred_series[j], label="predicted", ls="--", lw=2)
        plt.plot(true_series[j], label="true", lw=2.5)
        pdf.savefig(1)  # save on the fly
        plt.clf()  # clear figure once saved

    pdf.close()


def is_df_has_time_index(df: pd.DataFrame) -> bool:
    """check whether is dataframe and has a time index or not"""
    if isinstance(df, pd.DataFrame):
        if isinstance(df.index, pd.DatetimeIndex):
            return True
    return False
