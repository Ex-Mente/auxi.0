#!/usr/bin/env python3
"""
This module contains helper functions to ease various tasks.
"""


import os


def get_path_relative_to_module(module_file_path, directory):
    """
    Calculate a path relative to the specified module file.
    """
    module_path = os.path.dirname(module_file_path)
    path = os.path.join(module_path, directory)
    path = os.path.abspath(path)
    return path
