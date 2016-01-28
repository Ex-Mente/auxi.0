# -*- coding: utf-8 -*-
"""
This module contains a single class that represents an element of the periodic
table.
"""
__version__ = "0.2.0"

from auxi.core.object import Object

class Element(Object):
    """An element in the periodic table.

    :param period:        Period to which the element belongs.
    :param group:         Group to which the element belongs.
    :param atomic_number: Number of protons in the element's nucleus.
    :param symbol:        Element's symbol.
    :param molar_mass:    [kg/kmol] Element's standard atomic mass.
    """

    def __init__(self, period, group, atomic_number, symbol, molar_mass):
        self.period = period
        self.group = group
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.molar_mass = molar_mass
