# -*- coding: utf-8 -*-
"""
@title:
@author: Johan Zietsman
@organisation: University of Pretoria
@course: NWM780 Metallurgical Modelling
@date:   April 2014
"""
__version__ = "0.0.2"

import os


class Material:
    """A very simple class."""
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return "Material: name='" + self.name + "'"
    
    def create_package(self, mass):
        """This creates a new package.\n
        Usage: """
        result = MaterialPackage(self, mass)
        return result


class MaterialPackage:
    def __init__(self, material, mass):
        self._material = material
        self._mass = mass
        
    def __str__(self):
        return "MaterialPackage: material='" + self._material.name + "' mass=" + str(self._mass)
        
    def __add__(self, other):
        if type(other) is MaterialPackage:
            return MaterialPackage(self._material, \
            self.mass() + other.mass())
        else:
            raise Exception("Invalid addition argument.")
    
    def __sub__(self, other):
        if type(other) is float:
            if other > self._mass:
                raise Exception("Cannot subtract more than what is in the package.")
            self._mass = self._mass - other
            return MaterialPackage(self._material, other)
        elif type(other) is MaterialPackage:
            if other.mass() > self._mass:
                raise Exception("Cannot subtract more than what is in the package.")
            self._mass = self._mass - other.mass()
            return MaterialPackage(self._material, other.mass())
        else:
            raise Exception("Invalid subtraction argument.")

    def __mul__(self, other):
        if type(other) is float:
            if other < 0.0:
                raise Exception("Cannot multiply package with negative number.")
            return MaterialPackage(self._material, self._mass * other)
        else:
            raise Exception("Invalid multiplication argument.")

    def mass(self):
        return self._mass
        
    def material(self):
        return self._material


# =============================================================================
# Main Program
# =============================================================================

#os.system("cls")
#ilmenite = Material("ilmenite")
#p1 = ilmenite.create_package(123.456)
#p2 = ilmenite.create_package(234.567)
#p3 = p1 + p2
#p4 = p3 - 100.0
#p5 = p4 * 2.0

