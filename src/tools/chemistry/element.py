#!/usr/bin/env python3
from auxi.core.object import Object


__version__ = "0.2.0rc3"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman"
__credits__ = ["Christoff Kok", "Johan Zietsman"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


class Element(Object):
    """
    An element in the periodic table.

    :param period: Period to which the element belongs.
    :param group: Group to which the element belongs.
    :param atomic_number: Number of protons in the element's nucleus.
    :param symbol: Element's symbol.
    :param molar_mass: [kg/kmol] Element's standard atomic mass.
    """

    def __init__(self, period, group, atomic_number, symbol, molar_mass):
        self.period = period
        self.group = group
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.molar_mass = molar_mass
        self._validate_()

    def _validate_(self):
        pass


#TODO: Add test file.
#TODO: Implement validate method.
