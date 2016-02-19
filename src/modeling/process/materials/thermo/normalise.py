# -*- coding: utf-8 -*-
"""
This module provides a class that converts raw assays for use in calculations
by normalising.

@author: Ex Mente Technologies (Pty) Ltd
"""
__version__ = "0.2.0"

from assayconversionaction import AssayConversionAction

class Normalise(AssayConversionAction):
    def run(self, material):
        pass


conversion = [Normalise(), ]
mat = Material()
