# -*- coding: utf-8 -*-
"""
    core
    ~~~~~
    Core functionality
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import os

from .helpers import _extract_objects_from_path
from .helpers import _find_files_from_path
from .helpers import _convert_path_to_function
from .helpers import _remove_base_path_from_file


class FunctionPath(object):
    """ Takes an arbitrary filename and wraps convenient
    functions to convert it to valid functions
    Parameters
    ----------
    filename : str,
        filename to use to construct a BaseRoute
    base_path: str,
        base_path to be clipped for route generation
    """

    def __init__(self, filename, base_path):
        self._filename = filename
        self._base_path = base_path
        self.methods = _extract_objects_from_path(self._filename)
        self._clipped_path = _remove_base_path_from_file(
            self._base_path, self._filename
        )
        self._fn_path = _convert_path_to_function(self._clipped_path)

    @property
    def clipped_path(self):
        return self._clipped_path

    @property
    def fn_path(self):
        return self._fn_path


class FunctionPathFactory(object):
    """ Takes a path and finds functions and objects from
    nested files contained in the route.
    Parameters
    ----------
    path : str
        path to begin searching for routes
    """

    def __init__(self, path):
        self._path = path
        self._norm_path = os.path.normpath(self._path)
        self._function_paths = self._compute_structure()

    @property
    def function_paths(self):
        return self._function_paths

    def _compute_structure(self):
        """uses a helper function to find files
        from a given path.  Currently uses glob
        in virtually a one line function, but in
        case that implementation changes it's easier
        to wrap it here
        Returns
        -------
        m : [FunctionPath] -- List of base routes for each found file
        """
        return [
            FunctionPath(file, self._norm_path)
            for file in _find_files_from_path(self._norm_path)
        ]
