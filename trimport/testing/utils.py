# -*- coding: utf-8 -*-
"""
    testing utils
    ~~~~~
    Tests helper functions
    :copyright: 2019 Chris Zimmerman
    :license: BSD-3-Clause
"""


def _validate_dtype(parameter, type_, dt):
    """
    Parameters
    ----------
    parameter
    type_
    dt

    Returns
    -------

    """
    raise TypeError(
        "Parameter {} received {}, expected {}.".format(parameter, type_, dt)
    )
