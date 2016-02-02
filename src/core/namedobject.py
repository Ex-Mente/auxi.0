# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 05:34:00 2016

@author: johanz
"""

from auxi.core.object import Object


class NamedObject(Object):
    """
    Base class for all auxi classes containing a name and description.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
