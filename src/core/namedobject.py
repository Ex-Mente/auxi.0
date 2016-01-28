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

if __name__ == "__main__":
    import jsonpickle

    n = NamedObject()
    print(n)
    print(n.__hash__())

    str_n = str(n)
    new_n = jsonpickle.decode(str_n)
    print(new_n)
    print(type(new_n))
