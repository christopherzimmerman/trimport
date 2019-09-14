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

FILE_CONTENT = """
# simple get
def hello_world():
    return 'Hello World'
"""


def create_directory(tmpdir):
    base = tmpdir.mkdir("files")
    f1 = base.join("index.py")
    f2 = base.mkdir("foo").join("index.py")
    f3 = base.mkdir("bar").join("_variable.py")
    f1.write(FILE_CONTENT)
    f2.write(FILE_CONTENT)
    f3.write(FILE_CONTENT)


def create_single_file(tmpdir):
    f1 = tmpdir.mkdir("files").join("index.py")
    f1.write(FILE_CONTENT)


class TestFunctionFactoryFindFiles:
    """
    """

    @pytest.mark.parametrize(
        "fn, num_routes", [(create_directory, 3), (create_single_file, 1)]
    )
    def test_nested_files(self, fn, num_routes, tmpdir):
        fn(tmpdir)
        factory = FunctionPathFactory(tmpdir.strpath)
        assert len(factory.function_paths) == num_routes


class TestFunctionPathFiles:
    """
    """

    @pytest.mark.parametrize(
        "function, names",
        [
            (
                create_directory,
                ["/files/index.py", "/files/foo/index.py", "/files/bar/_variable.py"],
            ),
            (create_single_file, ["/files/index.py"]),
        ],
    )
    def test_file_clipped_names(self, function, names, tmpdir):
        function(tmpdir)
        factory = FunctionPathFactory(tmpdir.strpath)
        clipped = [fp.clipped_path for fp in factory.function_paths]
        assert clipped == names

    def test_file_method_count(self, tmpdir):
        create_single_file(tmpdir)
        factory = FunctionPathFactory(tmpdir.strpath)
        fp, *rest = factory.function_paths
        assert len(fp.methods.keys()) == 1

    def test_file_method_callable(self, tmpdir):
        create_single_file(tmpdir)
        factory = FunctionPathFactory(tmpdir.strpath)
        fp, *rest = factory.function_paths
        assert all(callable(fn) for fnn, fn in fp.methods.items())

    def test_file_method_output(self, tmpdir):
        create_single_file(tmpdir)
        factory = FunctionPathFactory(tmpdir.strpath)
        fp, *rest = factory.function_paths
        print(fp.methods)
        assert fp.methods["hello_world"]() == "Hello World"
