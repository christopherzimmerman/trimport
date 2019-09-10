# -*- coding: utf-8 -*-
"""
    helpers
    ~~~~~
    Helper functions only accessed by internal objects
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import glob
import importlib.util
import os
import re


def _find_files_from_path(path):
    """
    Parameters
    ----------
    path : str
        path to search for files
    Returns
    -------
    paths : list of paths for an application
    """

    # python file extension
    glob_opts = {"pathname": path + "/**/*.py", "recursive": True}

    return glob.glob(**glob_opts)


def _remove_base_path_from_file(base_path, filename):
    """
    Turn a file into a route.  This will probably get more
    complicated to account for multiple OS and strange
    file names
    Parameters
    ----------
    base_path : str
        normalized base path
    filename : str
        filename to remove base_path from
    Returns
    -------
    s : filename with base_path removed
    """
    return filename.replace(base_path, "", 1)


def _extract_objects_from_path(path, allowed_methods=None):
    """
    Extract methods from a given path.  This imports
    an absolute path, although I don't see how this
    is any more dangerous than executing other code
    since you define the path that is imported
    Parameters
    ----------
    path : str
        absolute path to import
    Returns
    -------
    d : dictionary of methods
    """
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    fns = set(dir(module))
    if allowed_methods is not None:
        fns &= set(allowed_methods)
    if allowed_methods is None:
        fns = {fn for fn in fns if not fn.startswith('__')}

    return {fn: getattr(module, fn) for fn in fns}


def _convert_path_to_function(clipped_path):
    """
    Parameters
    ----------
    clipped_path : str
        api route with absolute path clipped
    Returns
    -------
    fn : str -- function name
    """
    components = [comp for comp in clipped_path.split(os.sep) if comp]
    return "_".join(components)[:-3]
