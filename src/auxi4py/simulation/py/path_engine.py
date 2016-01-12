# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:19:02 2015

Contains functions to help create paths and access values specified by a path.

@author: Christoff Kok
"""

from datetime import datetime
from auxi.modelling.business import NamedObject


def generate_parameter_paths(root_object):
    return generate_paths(root_object, True)


def generate_result_paths(root_object):
    return generate_paths(root_object, False)


def get_class_properties(cls):
    result = []
    for p in cls.__dict__.keys():
        if p[:2] != '__' and (isinstance(getattr(cls, p), property)
                              or (p in vars(cls) and p != "is_param"
                                  and not callable(p))):
            result.append(p)
    return result


def generate_paths(root_object, exclude_non_settable_props, path=""):
    result = {}
    if path == "":
        path = root_object.name

    for a in get_class_properties(type(root_object)):
        if a == "":
            raise ValueError("Could not create a path to the '%s' object. \
at path '%s'." % (type(root_object), a))
        if not root_object.is_param(a):
            continue
        prop = getattr(root_object, a)
        if type(prop) in (int, float, bool, str, datetime):
            result[(path, root_object, a)] = prop
        elif hasattr(prop, '__iter__'):
            for item in prop:
                item_path = path + "//" + item.name
                for r_path, r_prop in generate_paths(item,
                                                     exclude_non_settable_props,
                                                     item_path).items():
                    result[r_path] = r_prop
        elif isinstance(prop, NamedObject):
            prop_path = path + "//" + prop.name
            for r_path, r_prop in generate_paths(prop,
                                                 exclude_non_settable_props,
                                                 prop_path).items():
                result[r_path] = r_prop
    return result


def get_instance_value(root_object, prop_name):
    return getattr(root_object, prop_name)


def set_instance_value(root_object, prop_name, value):
    if value is None:
        val = ""
    else:
        if isinstance(value, datetime):
            val = value
        else:
            val = eval(str(value))
    try:
        setattr(root_object, prop_name, val)
    except AttributeError:
        pass
