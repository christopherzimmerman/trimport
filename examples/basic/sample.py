# -*- coding: utf-8 -*-
"""
    examples.sample
    ~~~~~
    Tests helper functions
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""
import os
from trimport import FunctionPathFactory

fn_dir = os.path.dirname(os.path.realpath(__file__)) + "/path/"
factory = FunctionPathFactory(fn_dir)

fn, *rest = factory.function_paths

print(fn.clipped_path)
print(fn.fn_path)

print(fn.methods['hello_world']())
print(fn.methods['add_two_ints'](2, 2))
