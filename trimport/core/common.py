# -*- coding: utf-8 -*-
"""
    common functions
    ~~~~~
    Helper functions only accessed by internal objects
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import glob
import importlib.util
import os
import re
from typing import Optional, List


def find_files_from_path(
    path: str, extension: str = ".py", recursive: bool = True
) -> [str]:
    """
    Parameters
    ----------
    path
    extension
    recursive

    Returns
    -------

    """
    if not os.path.isdir(path):
        raise NotADirectoryError("{} is not a directory".format(path))

    pathname = "{path}/**/*{extension}".format(path=path, extension=extension)

    return glob.glob(pathname=pathname, recursive=recursive)


def remove_base_path_from_file(base_path: str, filename: str) -> str:
    """
    Parameters
    ----------
    base_path
    filename

    Returns
    -------

    """
    return filename.replace(base_path, "", 1)


def extract_objects_from_path(
    path: str, allowed_methods: Optional[List[str]] = None
) -> dict:
    """
    Parameters
    ----------
    path
    allowed_methods

    Returns
    -------

    """
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    fns = set(dir(module))
    if allowed_methods is not None:
        fns &= set(allowed_methods)
    if allowed_methods is None:
        fns = {fn for fn in fns if not fn.startswith("__")}

    attrs = {fn: getattr(module, fn) for fn in fns}
    return {k: v for k, v in attrs.items() if callable(v)}


def convert_path_to_function(clipped_path: str, extension: str = ".py") -> str:
    """
    Parameters
    ----------
    clipped_path
    extension

    Returns
    -------

    """
    components = [comp for comp in clipped_path.split(os.sep) if comp]
    joined = "_".join(components)
    return re.sub(r"{}$".format(extension), "", joined)
