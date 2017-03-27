#!/usr/bin/env python3
"""
This module contains helper functions to ease various tasks.
"""


import os
from datetime import datetime


def get_path_relative_to_module(module_file_path, relative_target_path):
    """
    Calculate a path relative to the specified module file.

    :param module_file_path: The file path to the module.
    """
    module_path = os.path.dirname(module_file_path)
    path = os.path.join(module_path, relative_target_path)
    path = os.path.abspath(path)
    return path


def get_date(date):
    """
    Get the date from a value that could be a date object or a string.

    :param date: The date object or string.

    :returns: The date object.
    """
    if type(date) is str:
        return datetime.strptime(date, '%Y-%m-%d').date()
    else:
        return date


if __name__ == "__main__":
    import unittest
    from helpers_test import HelpersUnitTester
    unittest.main()
