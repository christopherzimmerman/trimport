# -*- coding: utf-8 -*-
"""
    tests constructors
    ~~~~~
    Tests helper functions
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import pytest

from trimport.core.functions.generic import FunctionPathFactory
from trimport.core.functions.generic import FunctionPath


class TestFunctionPathFactoryConstructor:
    """
    Tests FunctionPathFactory, primarily for
    issues with nonexistent files
    """

    def test_constructor_bad_directory(self):
        with pytest.raises(NotADirectoryError):
            FunctionPathFactory(path="/api2")

    @pytest.mark.parametrize(
        "path, extension, allowed_methods",
        ((3, ".py", ["foo"]), ("/api", None, ["foo"]), ("/api", ".py", object())),
    )
    def test_constructor_bad_arguments(self, path, extension, allowed_methods):
        with pytest.raises(TypeError):
            FunctionPathFactory(path, extension, allowed_methods)
