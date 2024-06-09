"""convertions changing the input to the desired format"""

import multiprocessing as mp
import os


def convert_n_jobs_to_num_workers(n_jobs: int):
    """Convert n_jobs commonly used in sklearn libs to num_workers for multiprocessing.Pool."""
    if n_jobs > 0:
        n_jobs = min(n_jobs, mp.cpu_count())
    elif n_jobs < 0:
        n_jobs = max(1, mp.cpu_count() + (n_jobs + 1))
    else:
        raise ValueError("n_jobs must be a different number than 0")
    return n_jobs


def convert_cross_platform_path(path: str):
    """Converts a path to a cross platform path."""
    parts = os.path.normpath(path).split(os.sep)
    return os.path.join(*parts)
