"""
This module provides utilities for handling relative paths in multi-structured frameworks.

Functions:
    rel2abs(path): Converts a relative path to an absolute path.

Usage:
    Whenever specifying a relative path, use `rel2abs`.

Example:
    from pydtl_relativepath import rel2abs, RelativePathType
    readmepath = rel2abs("README.txt", relative_to=RelativePathType.RELATIVE_TO_CURRENT_FILE)
    print(open(readmepath, mode="r", encoding="utf-8").read())

This function converts a specified relative path to an absolute path, relative to the current file's directory.
`readmepath` will contain the absolute path for the README.txt file. This function is compatible with os.PathLike objects.
"""

import inspect
import os
from pathlib import Path
from typing import Union

from .enums import RelativePathType


def rel2abs(
    *args,
    relative_type: Union[str, RelativePathType] = RelativePathType.RELATIVE_TO_WORKING_DIRECTORY,
    parent_dir_jump: int = 0,
):
    """
    Convert Relative Path to Absolute Path

    Args:
        *args: Specify each folder and destination files. Example: "folder1", "folder2", "file.txt"
        relative_type (str | RelativePathType): Specify the root location. Default is RelativePathType.RELATIVE_TO_WORKING_DIRECTORY.
        parent_dir_jump (int): Specify the number of folders to go up from the relative to location. Default is 0. Positive values are not allowed.

    Example:
        from pydtl_relativepath import rel2abs, RelativePathType
        readmepath = rel2abs("README.txt", relative_to=RelativePathType.RELATIVE_TO_CURRENT_FILE)
        print(open(readmepath, mode="r", encoding="utf-8").read())

    Returns:
        Path: The absolute path of the specified relative path.
    """

    root_path = ""

    if isinstance(relative_type, str):
        relative_type = RelativePathType(relative_type)

    if relative_type == RelativePathType.RELATIVE_TO_CURRENT_FILE:
        root_path = os.path.dirname(inspect.stack()[1].filename)  # current file's dir
    elif relative_type == RelativePathType.RELATIVE_TO_WORKING_DIRECTORY:
        root_path = os.path.abspath(os.curdir)  # current working dir
    else:
        raise ValueError(f"Invalid root option [{relative_type}]\nUse RelativePathType enum")

    if parent_dir_jump > 0 or not isinstance(parent_dir_jump, int):
        raise ValueError(
            "Invalid parent_dir_jump value. Only negative integers and zero are allowed."
        )
    else:
        no_of_dirs_to_jump = parent_dir_jump * -1  # convert to positive value
        for _ in range(no_of_dirs_to_jump):
            root_path = os.path.dirname(root_path)

    abs_path = os.path.join(root_path, *args)
    abs_path = os.path.normpath(abs_path)

    return Path(abs_path)
