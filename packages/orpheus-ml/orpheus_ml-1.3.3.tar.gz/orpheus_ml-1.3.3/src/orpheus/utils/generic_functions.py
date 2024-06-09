"""generic useful helper-functions which could possibly be used in any project"""

import ast
import builtins
import inspect
import os
import sys
import time
import types
from typing import List, Optional, Union
import uuid

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_parent_dirs_to_path(num_parents=1):
    """
    Adds the parent directories of the current file to the sys.path variable.
    This is needed to import modules from the parent directory.

    Args:
        num_parents (int): The number of parent directories to add. Defaults to 1.
    """
    parent_dir = os.path.abspath(__file__)
    for _ in range(num_parents):
        parent_dir = os.path.dirname(parent_dir)
        sys.path.append(parent_dir)


def tableize(df: pd.DataFrame) -> Union[str, None]:
    """pretty print of dataframe"""
    if not isinstance(df, pd.DataFrame):
        return None
    df_columns = df.columns.to_list()

    def max_len_in_lst(lst):
        return len(sorted(lst, reverse=True, key=len)[0])

    def align_center(st, sz):
        return "{0}{1}{0}".format(" " * (1 + (sz - len(st)) // 2), st)[:sz] if len(st) < sz else st

    def align_right(st, sz):
        return "{0}{1} ".format(" " * (sz - len(st) - 1), st) if len(st) < sz else st

    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = dict(
        [(col, max_len_in_lst(df.iloc[:, idx].astype("str"))) for idx, col in enumerate(df_columns)]
    )
    col_sizes = dict([(col, 2 + max(max_val_len_for_col.get(col, 0), max_col_len)) for col in df_columns])

    def build_hline(row):
        return "+".join(["-" * col_sizes[col] for col in row]).join(["+", "+"])

    def build_data(row, align):
        return "|".join([align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join(["|", "|"])

    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]
    for _, row in df.iterrows():
        out.append(build_data(row.tolist(), align_right))
    out.append(hline)
    return "\n".join(out)


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(get_size(v, seen) for v in obj.values())
        size += sum(get_size(k, seen) for k in obj.keys())
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(i, seen) for i in obj)
    return size


def list_files(startpath: str, exclude: List[str] = []):
    """list all files in a directory recursively"""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        if any(excluded in root for excluded in exclude):
            continue
        print("{}{}/".format(indent, os.path.basename(root)))
        dirs[:] = [d for d in dirs if not any(excluded in d for excluded in exclude)]
        subindent = " " * 4 * (level + 1)
        for f in files:
            if any(excluded in f for excluded in exclude):
                continue
            print("{}{}".format(subindent, f))


def find_circular_imports(root_directory):
    """Find circular imports in a Python project."""

    dependencies = {}

    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()

                module = os.path.relpath(filepath, root_directory)
                module = os.path.splitext(module)[0].replace(os.path.sep, ".")

                tree = ast.parse(code)

                imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
                imports = [module for module in imports if module not in ("__future__", "builtins")]

                if module not in dependencies:
                    dependencies[module] = []

                dependencies[module].extend(imports)

    circular_imports = []
    for module, dep_list in dependencies.items():
        for dep in dep_list:
            dep_chain = [module]
            while dep in dependencies:
                if dep in dep_chain:
                    circular_imports.append(dep_chain + [dep])
                    break
                dep_chain.append(dep)
                dep = dependencies[dep][0]

    return circular_imports


def find_dependencies(root_directory):
    """Find all dependencies of a module"""
    dependencies = {}

    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()

                module = os.path.relpath(filepath, root_directory)
                module = os.path.splitext(module)[0].replace(os.path.sep, ".")

                tree = ast.parse(code)

                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    if isinstance(node, ast.ImportFrom):
                        module_name = node.module
                        for alias in node.names:
                            imported_module = module_name + "." + alias.name if module_name else alias.name
                            imports.append(imported_module)

                if module not in dependencies:
                    dependencies[module] = []

                dependencies[module].extend(imports)

    return dependencies


def best_fit_line(
    arr: Union[pd.Series, np.ndarray, list],
    plot: bool = False,
    plot_title: Optional[str] = None,
) -> Union[pd.Series, float]:
    """returns best fit line (aka least squares regression)."""
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    y = range(len(arr))
    bf_line = pd.Series(np.poly1d(np.polyfit(y, arr, 1))(y))

    if plot:
        plt.plot(arr)
        plt.plot(bf_line)
        plt.legend([plot_title or "array", "best fit line"])
        plt.show()

    return bf_line


def draw_coffee_cup() -> str:
    return """
                            (
                          )     (
                   ___...(-------)-....___
               .-\"       )    (          \"-.
         .-'``'|-._             )         _.-|
        /  .--.|   `\"---...........---\"`     |
       /  /    |                             |
       |  |    |                             |
        \\  \\   |                             |
         `\\ `\\ |                             |
           `\\ `|                             |
           _/ /\\                             /
          (__/  \\                           /
       _..---\"` \\                         /`\"---.._
    .-'           \\                       /          '-.
   :               `-.__             __.-'              :
   :                  ) \"---...---\" (                 :
    '._               `\"--...___...--\"`              _.'
      \\\"--..__                              __..--\"/
       '._     \"\"----.....______.....----\"\"     _.'
          `\\\"--..,,_____            _____,,..--\"`
    """


def prompt_console(N: int):
    """Prompt the console to wait for N seconds."""
    for remaining in range(N, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"Program will continue in{remaining}")
        sys.stdout.flush()
        time.sleep(1)


def list_python_imports(directory: str, exclude_dirs: Optional[List[str]] = None, indent: int = 0) -> None:
    """List all Python imports in a directory"""
    if exclude_dirs is None:
        exclude_dirs = []

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            if filename not in exclude_dirs:
                print("  " * indent + f"📁 {filename}")  # Print directory name
                list_python_imports(path, exclude_dirs, indent=indent + 1)
        elif filename.endswith(".py"):
            print("  " * indent + f"📄 {filename}")
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("import") or line.startswith("from"):
                        print("  " * (indent + 1) + f"📦 {line}")


def analyze_directory(directory, top_n=10):
    """
    Analyzes a directory of Python files and prints the top n most used functions and their docstrings.
    """

    def get_functions_and_docstrings(directory):
        functions_and_docstrings = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                                if node.name not in dir(builtins):
                                    docstring = ast.get_docstring(node)
                                    name = node.name
                                    functions_and_docstrings[name] = docstring
        return functions_and_docstrings

    def get_usage_counts(directory):
        counts = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if (
                                isinstance(node, ast.Call)
                                and isinstance(node.func, ast.Name)
                                and node.func.id not in dir(builtins)
                            ):
                                counts[node.func.id] = counts.get(node.func.id, 0) + 1
        return counts

    usage_counts = get_usage_counts(directory)
    functions_and_docstrings = get_functions_and_docstrings(directory)

    results = []
    for func, docstring in functions_and_docstrings.items():
        usage_count = usage_counts.get(func, 0)
        results.append((func, usage_count, docstring))

    # Sort the results by usage_count, descending
    results.sort(key=lambda x: -x[1])

    # Print the top n results
    for i, (func, usage_count, docstring) in enumerate(results[:top_n]):
        print(f"Rank {i + 1}: {func} (used {usage_count} times)")
        print(f"Docstring: {docstring}\n")


def get_args_from_function(attr_obj, args, kwargs) -> dict:
    """Get the names of the arguments the function takes and return a dictionary with the arguments and their values."""
    arg_names = list(inspect.signature(attr_obj).parameters.keys())

    final_args_dict = {}

    # Add default arguments
    default_values = attr_obj.__defaults__ if attr_obj.__defaults__ is not None else []
    default_args = dict(zip(arg_names[-len(default_values) :], default_values))

    # Update final_args_dict with default argument values
    final_args_dict.update(default_args)

    # Update final_args_dict with positional argument values
    for name, value in zip(arg_names, args):
        final_args_dict[name] = value

    # Update final_args_dict with keyword argument values
    final_args_dict.update(kwargs)

    return final_args_dict


def generate_unique_id() -> str:
    return str(uuid.uuid4())


def assert_builtin_types(obj):
    """
    Assert that the object and all its nested objects are built-in Python types.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            assert isinstance(
                key, (int, str, float, bool, bytes, types.NoneType)
            ), f"Key {key} is not a built-in type, but {type(key)}"
            assert_builtin_types(value)
    elif isinstance(obj, list):
        for item in obj:
            assert_builtin_types(item)
    elif isinstance(obj, tuple):
        for item in obj:
            assert_builtin_types(item)
    else:
        assert isinstance(
            obj, (int, str, float, bool, bytes, types.NoneType)
        ), f"{obj} is not a built-in type, but {type(obj)}"
