#!/usr/bin/env python3
"""
This module provides a number of functions for doing stoichiometry
calculations.
"""

import collections
import functools
import re

import parsimonious

from auxi.core.objects import Object



__version__ = '0.3.3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Element(Object):
    """
    An element in the periodic table.

    :param period: Period to which the element belongs.
    :param group: Group to which the element belongs.
    :param atomic_number: Number of protons in the element's nucleus.
    :param symbol: Element's symbol.
    :param molar_mass: [kg/kmol] Element's standard atomic mass.
    """

    # TODO: Add tests.
    # TODO: Implement validate method.

    def __init__(self, period, group, atomic_number, symbol, molar_mass):
        self.period = period
        self.group = group
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.molar_mass = molar_mass
        self._validate_()

    def count(self):
        return {self.symbol: 1}

    def _validate_(self):
        pass

    def __repr__(self):
        return "Element('{}')".format(self.element)


def count_with_multiplier(groups, multiplier):
    """ Update group counts with multiplier

    This is for handling atom counts on groups like (OH)2

    :param groups: iterable of Group/Element
    :param multiplier: the number to multiply by

    """
    counts = collections.defaultdict(float)
    for group in groups:
        for element, count in group.count().items():
            counts[element] += count*multiplier
    return counts


class Group:
    """ Represent a part of a compound formula

    :param group: iterable of Group/Element parts
    :param multiplier: multiplier in subscript or prefix of group
    :param dotted: True of the group is like '.2H2O'

    """

    def __init__(self, group, multiplier=1, dotted=False):
        self.group = group
        self.multiplier = multiplier
        self.dotted = dotted

    def count(self):
        return count_with_multiplier(self.group, self.multiplier)

    def __repr__(self):
        return "Group({}, multiplier={}, dotted={})".format(self.group, self.multiplier, self.dotted)


class Compound:
    """ Represents a full compound formula

    :param group: iterable of Group/Element
    :param dottedgroup: A Group if there is a .H2O part, None otherwise
    :param phase: The phase if there is a [phase] part, None otherwise

    """

    def __init__(self, group, dottedgroup=None, phase=None):
        self.group = [group]
        if dottedgroup:
            self.group.append(dottedgroup)
        self.phase = phase

    def count(self):
        return count_with_multiplier(self.group, multiplier=1)

    def molar_mass(self):
        return sum(_element_dictionary_[element].molar_mass*count
                   for element, count in self.count().items())

    def __repr__(self):
        return "Compound({}, {})".format(self.group, self.phase)


class CompoundVisitor(parsimonious.NodeVisitor):
    """ Visitor which takes parsed tree to useful groups.

        For parallels, check the grammar.
    """
    def visit_compound(self, node, compound):
        (group, dottedgroup, phase) = compound
        return Compound(group, dottedgroup, phase)

    def visit_group(self, node, group):
        return Group(group)

    def visit_phase(self, node, phase):
        (_, string, _) = node
        return string.text

    def visit_dottedgroup(self, node, dottedgroup):
        (_, number, group) = dottedgroup
        if not number:
            number = 1
        return Group([group], number, dotted=True)

    def visit_subscriptedgroup(self, node, subscriptedgroup):
        (_, group, _, number) = subscriptedgroup
        if not number:
            number = 1
        return Group([group], number)

    def visit_subscriptedelement(self, node, subscriptedelement):
        (element, number) = subscriptedelement
        return Group([element], number)

    def visit_element(self, node, element):
        return _element_dictionary_[node.text]

    def visit_number(self, node, element):
        return int(node.text)

    def generic_visit(self, node, other):
        try:
            return other[0]
        except:
            return other


grammar = parsimonious.grammar.Grammar(
    """
    compound = group dottedgroup? phase?
    group = (subscriptedgroup / subscriptedelement / element)+
    phase = "[" string "]"
    dottedgroup = "." number? group
    subscriptedgroup = "(" group ")" number?
    subscriptedelement = element number
    element = ~r"[A-Z][a-z]*"
    string = ~r"[A-Za-z]+"
    number = ~r"[0-9]+"
    """)

@functools.lru_cache()
def parse_compound(string):
    visitor = CompoundVisitor()
    parsed_tree = grammar.parse(string)
    return visitor.visit(parsed_tree)


def _populate_element_dictionary_():
    """
    Create all the elements of the periodic table and add them to the
    element dictionary.
    """

    # period 1
    _element_dictionary_['H'] = Element(1, 1, 1, 'H', 1.00794)
    _element_dictionary_['He'] = Element(1, 18, 2, 'He', 4.002602)

    # period 2
    _element_dictionary_['Li'] = Element(2, 1, 3, 'Li', 6.941)
    _element_dictionary_['Be'] = Element(2, 2, 4, 'Be', 9.012182)
    _element_dictionary_['B'] = Element(2, 13, 5, 'B', 10.811)
    _element_dictionary_['C'] = Element(2, 14, 6, 'C', 12.0107)
    _element_dictionary_['N'] = Element(2, 15, 7, 'N', 14.00674)
    _element_dictionary_['O'] = Element(2, 16, 8, 'O', 15.9994)
    _element_dictionary_['F'] = Element(2, 17, 9, 'F', 18.9984032)
    _element_dictionary_['Ne'] = Element(2, 18, 10, 'Ne', 20.1797)

    # period 3
    _element_dictionary_['Na'] = Element(3, 1, 11, 'Na', 22.98977)
    _element_dictionary_['Mg'] = Element(3, 2, 12, 'Mg', 24.305)
    _element_dictionary_['Al'] = Element(3, 13, 13, 'Al', 26.981538)
    _element_dictionary_['Si'] = Element(3, 14, 14, 'Si', 28.0855)
    _element_dictionary_['P'] = Element(3, 15, 15, 'P', 30.973762)
    _element_dictionary_['S'] = Element(3, 16, 16, 'S', 32.066)
    _element_dictionary_['Cl'] = Element(3, 17, 17, 'Cl', 35.4527)
    _element_dictionary_['Ar'] = Element(3, 18, 18, 'Ar', 39.948)

    # period 4
    _element_dictionary_['K'] = Element(4, 1, 19, 'K', 39.0983)
    _element_dictionary_['Ca'] = Element(4, 2, 20, 'Ca', 40.078)
    _element_dictionary_['Sc'] = Element(4, 3, 21, 'Sc', 44.95591)
    _element_dictionary_['Ti'] = Element(4, 4, 22, 'Ti', 47.867)
    _element_dictionary_['V'] = Element(4, 5, 23, 'V', 50.9415)
    _element_dictionary_['Cr'] = Element(4, 6, 24, 'Cr', 51.9961)
    _element_dictionary_['Mn'] = Element(4, 7, 25, 'Mn', 54.938049)
    _element_dictionary_['Fe'] = Element(4, 8, 26, 'Fe', 55.845)
    _element_dictionary_['Co'] = Element(4, 9, 27, 'Co', 58.9332)
    _element_dictionary_['Ni'] = Element(4, 10, 28, 'Ni', 58.6934)
    _element_dictionary_['Cu'] = Element(4, 11, 29, 'Cu', 63.546)
    _element_dictionary_['Zn'] = Element(4, 12, 30, 'Zn', 65.39)
    _element_dictionary_['Ga'] = Element(4, 13, 31, 'Ga', 69.723)
    _element_dictionary_['Ge'] = Element(4, 14, 32, 'Ge', 72.61)
    _element_dictionary_['As'] = Element(4, 15, 33, 'As', 74.9216)
    _element_dictionary_['Se'] = Element(4, 16, 34, 'Se', 78.96)
    _element_dictionary_['Br'] = Element(4, 17, 35, 'Br', 79.904)
    _element_dictionary_['Kr'] = Element(4, 18, 36, 'Kr', 83.8)

    # period 5
    _element_dictionary_['Rb'] = Element(5, 1, 37, 'Rb', 85.4678)
    _element_dictionary_['Sr'] = Element(5, 2, 38, 'Sr', 87.62)
    _element_dictionary_['Y'] = Element(5, 3, 39, 'Y', 88.90585)
    _element_dictionary_['Zr'] = Element(5, 4, 40, 'Zr', 91.224)
    _element_dictionary_['Nb'] = Element(5, 5, 41, 'Nb', 92.90638)
    _element_dictionary_['Mo'] = Element(5, 6, 42, 'Mo', 95.94)
    _element_dictionary_['Tc'] = Element(5, 7, 43, 'Tc', 98.0)
    _element_dictionary_['Ru'] = Element(5, 8, 44, 'Ru', 101.07)
    _element_dictionary_['Rh'] = Element(5, 9, 45, 'Rh', 102.9055)
    _element_dictionary_['Pd'] = Element(5, 10, 46, 'Pd', 106.42)
    _element_dictionary_['Ag'] = Element(5, 11, 47, 'Ag', 107.8682)
    _element_dictionary_['Cd'] = Element(5, 12, 48, 'Cd', 112.411)
    _element_dictionary_['In'] = Element(5, 13, 49, 'In', 114.818)
    _element_dictionary_['Sn'] = Element(5, 14, 50, 'Sn', 118.71)
    _element_dictionary_['Sb'] = Element(5, 15, 51, 'Sb', 121.76)
    _element_dictionary_['Te'] = Element(5, 16, 52, 'Te', 127.6)
    _element_dictionary_['I'] = Element(5, 17, 53, 'I', 126.90447)
    _element_dictionary_['Xe'] = Element(5, 18, 54, 'Xe', 131.29)

    # period 6
    _element_dictionary_['Cs'] = Element(6, 1, 55, 'Cs', 132.90545)
    _element_dictionary_['Ba'] = Element(6, 2, 56, 'Ba', 137.327)
    _element_dictionary_['La'] = Element(6, 0, 57, 'La', 138.9055)
    _element_dictionary_['Ce'] = Element(6, 0, 58, 'Ce', 140.116)
    _element_dictionary_['Pr'] = Element(6, 0, 59, 'Pr', 140.90765)
    _element_dictionary_['Nd'] = Element(6, 0, 60, 'Nd', 144.24)
    _element_dictionary_['Pm'] = Element(6, 0, 61, 'Pm', 145.0)
    _element_dictionary_['Sm'] = Element(6, 0, 62, 'Sm', 150.36)
    _element_dictionary_['Eu'] = Element(6, 0, 63, 'Eu', 151.964)
    _element_dictionary_['Gd'] = Element(6, 0, 64, 'Gd', 157.25)
    _element_dictionary_['Tb'] = Element(6, 0, 65, 'Tb', 158.92534)
    _element_dictionary_['Dy'] = Element(6, 0, 66, 'Dy', 162.5)
    _element_dictionary_['Ho'] = Element(6, 0, 67, 'Ho', 164.93032)
    _element_dictionary_['Er'] = Element(6, 0, 68, 'Er', 167.26)
    _element_dictionary_['Tm'] = Element(6, 0, 69, 'Tm', 168.93421)
    _element_dictionary_['Yb'] = Element(6, 0, 70, 'Yb', 173.04)
    _element_dictionary_['Lu'] = Element(6, 0, 71, 'Lu', 174.967)
    _element_dictionary_['Hf'] = Element(6, 4, 72, 'Hf', 178.49)
    _element_dictionary_['Ta'] = Element(6, 5, 73, 'Ta', 180.9479)
    _element_dictionary_['W'] = Element(6, 6, 74, 'W', 183.84)
    _element_dictionary_['Re'] = Element(6, 7, 75, 'Re', 186.207)
    _element_dictionary_['Os'] = Element(6, 8, 76, 'Os', 190.23)
    _element_dictionary_['Ir'] = Element(6, 9, 77, 'Ir', 192.217)
    _element_dictionary_['Pt'] = Element(6, 10, 78, 'Pt', 195.078)
    _element_dictionary_['Au'] = Element(6, 11, 79, 'Au', 196.96655)
    _element_dictionary_['Hg'] = Element(6, 12, 80, 'Hg', 200.59)
    _element_dictionary_['Tl'] = Element(6, 13, 81, 'Tl', 204.3833)
    _element_dictionary_['Pb'] = Element(6, 14, 82, 'Pb', 207.2)
    _element_dictionary_['Bi'] = Element(6, 15, 83, 'Bi', 208.98038)
    _element_dictionary_['Po'] = Element(6, 16, 84, 'Po', 210.0)
    _element_dictionary_['At'] = Element(6, 17, 85, 'At', 210.0)
    _element_dictionary_['Rn'] = Element(6, 18, 86, 'Rn', 222.0)

    # period 7
    _element_dictionary_['Fr'] = Element(7, 1, 87, 'Fr', 223.0)
    _element_dictionary_['Ra'] = Element(7, 2, 88, 'Ra', 226.0)
    _element_dictionary_['Ac'] = Element(7, 0, 89, 'Ac', 227.0)
    _element_dictionary_['Th'] = Element(7, 0, 90, 'Th', 232.0381)
    _element_dictionary_['Pa'] = Element(7, 0, 91, 'Pa', 231.03588)
    _element_dictionary_['U'] = Element(7, 0, 92, 'U', 238.0289)
    _element_dictionary_['Np'] = Element(7, 0, 93, 'Np', 237.0)
    _element_dictionary_['Pu'] = Element(7, 0, 94, 'Pu', 244.0)
    _element_dictionary_['Am'] = Element(7, 0, 95, 'Am', 243.0)
    _element_dictionary_['Cm'] = Element(7, 0, 96, 'Cm', 247.0)
    _element_dictionary_['Bk'] = Element(7, 0, 97, 'Bk', 247.0)
    _element_dictionary_['Cf'] = Element(7, 0, 98, 'Cf', 251.0)
    _element_dictionary_['Es'] = Element(7, 0, 99, 'Es', 252.0)
    _element_dictionary_['Fm'] = Element(7, 0, 100, 'Fm', 257.0)
    _element_dictionary_['Md'] = Element(7, 0, 101, 'Md', 258.0)
    _element_dictionary_['No'] = Element(7, 0, 102, 'No', 259.0)
    _element_dictionary_['Lr'] = Element(7, 0, 103, 'Lr', 262.0)
    _element_dictionary_['Rf'] = Element(7, 4, 104, 'Rf', 261.0)
    _element_dictionary_['Db'] = Element(7, 5, 105, 'Db', 262.0)
    _element_dictionary_['Sg'] = Element(7, 6, 106, 'Sg', 266.0)
    _element_dictionary_['Bh'] = Element(7, 7, 107, 'Bh', 264.0)
    _element_dictionary_['Hs'] = Element(7, 8, 108, 'Hs', 269.0)
    _element_dictionary_['Mt'] = Element(7, 9, 109, 'Mt', 268.0)
    _element_dictionary_['Ds'] = Element(7, 10, 110, 'Ds', 269.0)
    _element_dictionary_['Rg'] = Element(7, 11, 111, 'Rg', 272.0)
    # Cn missing
    # Uut missing
    # Fl missing
    # Uup missing
    # Lv missing
    # Uus missing
    # Uuo missing
    # actinides


def amount(compound, mass):
    """
    Calculate the number of moles in the specified mass of a chemical compound.

    :param compound: Formula and phase of a compound, e.g. 'Fe2O3[S1]'. The
      phase may be omitted.
    :param mass: [kg]

    :returns: Amount. [kmol]
    """

    return mass / molar_mass(compound)


def amounts(masses):
    """
    Calculate the amounts from the specified compound masses.

    :param masses: [kg] dictionary, e.g. {'SiO2': 3.0, 'FeO', 1.5}

    :returns: [kmol] dictionary
    """

    return {compound: amount(compound, masses[compound])
            for compound in masses.keys()}


def amount_fractions(masses):
    """
    Calculate the mole fractions from the specified compound masses.

    :param masses: [kg] dictionary, e.g. {'SiO2': 3.0, 'FeO', 1.5}

    :returns: [mole fractions] dictionary
    """

    n = amounts(masses)
    n_total = sum(n.values())
    return {compound: n[compound]/n_total for compound in n.keys()}


def mass(compound, amount):
    """
    Calculate the mass of the specified amount of a chemical compound.

    :param compound: Formula and phase of a compound, e.g. 'Fe2O3[S1]'. The
      phase may be omitted.
    :param amount: [kmol]

    :returns: Mass. [kg]
    """

    return amount * molar_mass(compound)


def masses(amounts):
    """
    Calculate the masses from the specified compound amounts.

    :param masses: [kmol] dictionary, e.g. {'SiO2': 3.0, 'FeO', 1.5}

    :returns: [kg] dictionary
    """

    return {compound: mass(compound, amounts[compound])
            for compound in amounts.keys()}


def mass_fractions(amounts):
    """
    Calculate the mole fractions from the specified compound masses.

    :param masses: [kg] dictionary, e.g. {'SiO2': 3.0, 'FeO', 1.5}

    :returns: [mass fractions] dictionary
    """

    m = masses(amounts)
    m_total = sum(m.values())
    return {compound: m[compound]/m_total for compound in m.keys()}


def convert_compound(mass, source, target, element):
    """
    Convert the specified mass of the source compound to the target using
    element as basis.

    :param mass: Mass of from_compound. [kg]
    :param source: Formula and phase of the original compound, e.g.
      'Fe2O3[S1]'.
    :param target: Formula and phase of the target compound, e.g. 'Fe[S1]'.
    :param element: Element to use as basis for the conversion, e.g. 'Fe' or
      'O'.

    :returns: Mass of target. [kg]
    """

    # Perform the conversion.
    target_mass_fraction = element_mass_fraction(target, element)
    if target_mass_fraction == 0.0:
        # If target_formula does not contain element, just return 0.0.
        return 0.0
    else:
        source_mass_fraction = element_mass_fraction(source, element)
        return mass * source_mass_fraction / target_mass_fraction


def element_mass_fraction(compound, element):
    """
    Determine the mass fraction of an element in a chemical compound.

    :param compound: Formula of the chemical compound, 'FeCr2O4'.
    :param element: Element, e.g. 'Cr'.

    :returns: Element mass fraction.
    """

    elementStoichiometryCoefficient = stoichiometry_coefficient(compound,
                                                                element)
    if elementStoichiometryCoefficient == 0.0:
        return 0.0
    else:
        formulaMass = molar_mass(compound)
        elementMass = molar_mass(element)
        return elementStoichiometryCoefficient * elementMass / formulaMass


def element_mass_fractions(compound, elements):
    """
    Determine the mass fractions of a list of elements in a chemical compound.

    :param compound: Formula and phase of a chemical compound, e.g.
      'Fe2O3[S1]'.
    :param elements: List of elements, ['Si', 'O', 'Fe'].

    :returns: Mass fractions.
    """

    return [element_mass_fraction(compound, element)
            for element in elements]


def elements(compounds):
    """
    Determine the set of elements present in a list of chemical compounds.

    The list of elements is sorted alphabetically.

    :param compounds: List of compound formulas and phases, e.g.
      ['Fe2O3[S1]', 'Al2O3[S1]'].

    :returns: List of elements.
    """

    elementlist = [parse_compound(compound).count().keys() for compound in compounds]
    return set().union(*elementlist)


def molar_mass(compound=''):
    """Determine the molar mass of a chemical compound.

    The molar mass is usually the mass of one mole of the substance, but here
    it is the mass of 1000 moles, since the mass unit used in pmpy is kg.

    :param compound: Formula of a chemical compound, e.g. 'Fe2O3'.

    :returns: Molar mass. [kg/kmol]
    """


    result = 0.0
    if compound is None or len(compound) == 0:
        return result

    compound = compound.strip()

    parsed = parse_compound(compound)

    return parsed.molar_mass()


def stoichiometry_coefficient(compound, element):
    """
    Determine the stoichiometry coefficient of an element in a chemical
    compound.

    :param compound: Formula of a chemical compound, e.g. 'SiO2'.
    :param element:  Element, e.g. 'Si'.

    :returns: Stoichiometry coefficient.
    """

    stoichiometry = parse_compound(compound.strip()).count()

    return stoichiometry[element]


def stoichiometry_coefficients(compound, elements):
    """
    Determine the stoichiometry coefficients of the specified elements in
    the specified chemical compound.

    :param compound: Formula of a chemical compound, e.g. 'SiO2'.
    :param elements: List of elements, e.g. ['Si', 'O', 'C'].

    :returns: List of stoichiometry coefficients.
    """

    stoichiometry = parse_compound(compound.strip()).count()

    return [stoichiometry[element] for element in elements]


# Initialise the module.
_element_dictionary_ = {}
_molar_mass_dictionary_ = {}
disallowed_chars = re.compile('[^0-9A-Za-z().]+')

_populate_element_dictionary_()


if __name__ == '__main__':
    import unittest
    from auxi.tools.chemistry.stoichiometry_test import StoichFunctionTester
    unittest.main()
