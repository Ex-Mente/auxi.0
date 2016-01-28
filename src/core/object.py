# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 05:34:00 2016

@author: johanz
"""

import json
import jsonpickle


class Object(object):
    """
    Base class for all auxi classes.
    """

    def __str__(self):
        o = json.loads(jsonpickle.encode(self))
        result = json.dumps(o, sort_keys=True,
                            indent=4, separators=(',', ': '))
        return result

    def __hash__(self):
        return hash(str(self))

if __name__ == "__main__":
    o = Object()
    print(o)
    print(o.__hash__())

    str_o = str(o)
    new_o = jsonpickle.decode(str_o)
    print(new_o)
    print(type(new_o))
