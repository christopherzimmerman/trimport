# -*- coding: utf-8 -*-
"""
    core
    ~~~~~
    Core functionality
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import os
from typing import Optional, List

from trimport.testing.utils import _validate_dtype

from trimport.core.common import (
    extract_objects_from_path,
    remove_base_path_from_file,
    convert_path_to_function,
    find_files_from_path,
)


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

    def __init__(
        self,
        filename: str,
        base_path: str,
        extension: str = ".py",
        allowed_methods: Optional[List[str]] = None,
    ):
        if not isinstance(filename, str):
            _validate_dtype("filename", type(filename), str)

        if not isinstance(base_path, str):
            _validate_dtype("base_path", type(filename), str)

        if not isinstance(extension, str):
            _validate_dtype("extension", type(extension), str)

        if not isinstance(allowed_methods, (list, type(None))):
            _validate_dtype("allowed_methods", type(allowed_methods), str)

        self._filename = filename
        self._base_path = base_path
        self._extension = extension
        self.methods = extract_objects_from_path(self._filename, allowed_methods)
        self._clipped_path = remove_base_path_from_file(self._base_path, self._filename)
        self._fn_path = convert_path_to_function(self._clipped_path)

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

    def __init__(
        self,
        path: str,
        extension: str = ".py",
        allowed_methods: Optional[List[str]] = None,
    ):
        if not isinstance(path, str):
            _validate_dtype("path", type(path), str)

        if not isinstance(extension, str):
            _validate_dtype("extension", type(extension), str)

        if not isinstance(allowed_methods, (list, type(None))):
            _validate_dtype("extension", type(allowed_methods), (list, type(None)))

        self.path = path
        self.norm_path = os.path.normpath(self.path)
        self.extension = extension
        self.allowed_methods = allowed_methods
        self.function_paths = self._compute_structure()

    def _compute_structure(self) -> [FunctionPath]:
        """uses a helper function to find files
        from a given path.  Currently uses glob
        in virtually a one line function, but in
        case that implementation changes it's easier
        to wrap it here
        Returns
        -------
        m : [FunctionPath] -- List of base routes for each found file
        """
        path = self.norm_path
        return [
            FunctionPath(file, path, self.extension, self.allowed_methods)
            for file in find_files_from_path(self.norm_path)
        ]
