# -*- coding: utf-8 -*-
"""
    tests constructors
    ~~~~~
    Tests helper functions
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import pytest

from trimport.core import FunctionPathFactory
from trimport.core import FunctionPath


EMPTY_FILE_CONTENT = "# empty"

GET_FILE_CONTENT = """
# simple get
def get():
    return 'Hello World'
"""


class TestFunctionPathFactoryConstructor:
    """
    Tests FunctionPathFactory, primarily for
    issues with nonexistent files
    """
    def test_constructor_bad_directory(self):
        with pytest.raises(NotADirectoryError):
            FunctionPathFactory(path='/api2')
