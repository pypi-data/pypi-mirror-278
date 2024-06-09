import threading
import time
import psutil
import matplotlib.pyplot as plt
from functools import wraps
import pandas as pd
from datetime import datetime


import threading
import time
from functools import wraps


def performance_monitor(interval: int) -> callable:
    """
    Decorator to monitor the memory and CPU usage of a system.

    Parameters
    ----------
    interval : int
        The interval (in seconds) at which the memory and CPU usage will be monitored.

    Returns
    -------
    function
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            mem_usage = []
            cpu_usage = []
            time_points = []

            def monitor():
                while True:
                    mem_usage.append(psutil.virtual_memory().percent)  # Total memory usage
                    cpu_usage.append(psutil.cpu_percent(interval=None))  # Total CPU usage
                    time_points.append(datetime.now())
                    time.sleep(interval)
                    if stop_event.is_set():
                        break

            stop_event = threading.Event()
            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()

            try:
                result = function(*args, **kwargs)
            finally:
                stop_event.set()
                monitor_thread.join()

            # Plot memory usage
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.plot(time_points, mem_usage)
            plt.gcf().autofmt_xdate()  # for better date label formatting
            plt.xlabel("Time (H:M:S)")
            plt.ylabel("Memory usage (%)")

            # Plot CPU usage
            plt.subplot(1, 2, 2)
            plt.plot(time_points, cpu_usage)
            plt.gcf().autofmt_xdate()  # for better date label formatting
            plt.xlabel("Time (H:M:S)")
            plt.ylabel("CPU usage (%)")

            plt.tight_layout()
            plt.show()

            return result

        return wrapper

    return decorator


def check_memory_df(df: pd.DataFrame) -> None:
    """Check the memory usage of a Pandas DataFrame as a percentage of the total memory available in the system."""
    df_memory_bytes = df.memory_usage(deep=True).sum()

    # Get the total memory available in the system (in bytes)
    total_memory_bytes = psutil.virtual_memory().total

    # Calculate the percentage
    percentage_memory_used = (df_memory_bytes / total_memory_bytes) * 100

    print(f"DataFrame consumes {percentage_memory_used:.2f}% of the total memory.")
