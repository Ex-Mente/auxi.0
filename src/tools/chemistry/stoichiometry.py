# -*- coding: utf-8 -*-
"""
This module provides a number of functions for doing stoichiometry
calculations.
"""
__version__ = "0.2.0"

import numpy
from auxi.tools.chemistry.element import Element


# =============================================================================
# Private functions.
# =============================================================================

def _formula_code(formula=str()):
    """Generate a unique formula code for a chemical compound.

    :param formula: The formula describing the chemical compound.

    :returns: The formula code for the chemical compouned.
    """

    result = str()
    if len(formula) == 0:
        return result

    codeSum = 0
    for i in range(len(formula)):
        c = formula[i:i+1]
        b = ord(c)
        result = result + str(b)
        codeSum = codeSum + b
    result = result + "_" + str(codeSum)

    return result


def _get_character(string, index=0):
    """Returns the character from a string at the index position, the integer
    ordinal of the character, and an incremented index.

    If index is at the end of the string, return an empty string, -1 for the \
    ordinal, and return index unchanged.

    :param string: String to search.
    :param index:  Index at which the character should be located.

    :returns: character at string[index]
    :returns: ordinal of character
    :returns: incremented index"""

    if index == len(string):
        return "", -1, index
    else:
        character = string[index:index+1]
        ordinal = ord(character)
        return character, ordinal, index + 1


def _get_formula(compound):
    """Remove the phase from a compound string if it exists and return only
    the formula.

    :param compound: Formula and phase of a chemical compound, e.g. \
    "Fe2O3[S1]".

    :returns: Chemical formula.
    """

    return compound.split("[")[0]


def _parse_element_for_mass(compound, index):
    """Determine the atomic mass of the element at the specified index of the
    chemical compound formula by parsing the formula.

    :param compound: Formula of a chemical compound, "Fe3O4".
    :param index:    Index from which the formula should be parsed.

    :returns: Atomic mass. [kg/kmol]
    """

    Element = compound[index:index+1]
    index = index + 1
    if index < len(compound):
        code = ord(compound[index:index+1])
    else:
        code = 0

    while code >= 97 and code <= 123:
        Element = Element + compound[index:index+1]
        index = index + 1
        if index == len(compound):
            code = 0
            break
        code = ord(compound[index:index+1])

    multiplier = str()
    while (code >= 48 and code <= 57) or code == 46:
        multiplier = multiplier + compound[index:index+1]
        index = index + 1
        if index == len(compound):
            break
        code = ord(compound[index:index+1])
    if multiplier == "":
        multiplier = "1"

    result = _element_dictionary[Element].molar_mass * float(multiplier)
    return (result, index)


def _parse_element_for_stoichiometry(compound, index):
    """Determine the stoichiometry coefficient of the element at the specified
    index of the formula by parsing the formula.

    :param compound: Formula of a chemical compound, "Fe3O4".
    :param index:    Index from which the formula should be parsed.

    :returns: Stoichiometric coefficient.
    """

    element_symbol = compound[index:index+1]
    index = index + 1
    if index < len(compound):
        c = compound[index:index+1]
        b = ord(c)
    else:
        b = 0

    while (b >= 97 and b <= 123):
        element_symbol = element_symbol + compound[index:index+1]
        index = index + 1
        if index >= len(compound):
            return (element_symbol, 1.0, index)
        c = compound[index:index+1]
        b = ord(c)

    stoichiometry_coefficient = ""

    while ((b >= 48 and b <= 57) or b == 46):
        stoichiometry_coefficient = stoichiometry_coefficient + compound[index:index+1]
        index = index + 1
        if index >= len(compound):
            break
        c = compound[index:index+1]
        b = ord(c)

    if stoichiometry_coefficient == "":
        stoichiometry_coefficient = "1.0"

    return (element_symbol, float(stoichiometry_coefficient), index)


def _parse_formula_for_elements(compound):
    """Determine the set of elements that occur in the specified formula.

    :param compound: Formula of a chemical compound.

    :returns: Set of elements.
    """

    # Initialise the search variables.
    result = set()
    i = 0              # The index of the current character in the string.

    # Do the search.
    while i < len(compound):
        c, b, i = _get_character(compound, i)
        if b >= 65 and b <= 90:  # Element found. Process it.
            j = i
            element = c
            c, b, j = _get_character(compound, j)
            while b >= 97 and b <= 122:
                element = element + c
                c, b, j = _get_character(compound, j)
            result.add(element)

    return result


def _parse_formula_for_mass(compound, index):
    """Determine the molar mass of the chemical compound by recursively
    parsing its formula from the specified index.

    :param compound: Formula of chemical compound.
    :param index:    Index from which the formula should be parsed.

    :returns: Molecular mass of the parsed portion of the formula.
    """
    result = 0.0

    c = str()
    while index < len(compound) and c != ")":
        c = compound[index:index+1]
        b = ord(c)

        if c == "(":
            index = index + 1
            dresult, index = _parse_formula_for_mass(compound, index)
            result = result + dresult
        elif b >= 65 and b <= 90:
            dresult, index = _parse_element_for_mass(compound, index)
            result = result + dresult

    if index >= len(compound):
        return result

    if c == ")":
        index = index + 1
    b = ord(compound[index:index+1])

    multiplier = str()
    while ((b >= 48 and b <= 57) or b == 46):
        multiplier = multiplier + compound[index:index+1]
        index = index + 1
        if index == len(compound):
            break
        c = compound[index:index+1]
        b = ord(c)

    if multiplier == "":
        multiplier = "1"

    result = result * float(multiplier)
    return (result, index)


def _parse_formula_for_stoichiometry(compound, index, stoich_dict):
    """Determine the stoichiometry of the formula by recursively parsing it
    from the specified index and storing the result in the specified dictionary.

    :param compound:    Formula of chemical compound.
    :param index:       Index from which the formula should be parsed.
    :param stoich_dict: Stoichiometry dictionary.
    """
    c = str()
    while index < len(compound) and c != ")":
        c = compound[index:index+1]
        b = ord(c)

        if c == "(":
            index = index + 1
            new_stoichiometry_records = {}
            _parse_formula_for_stoichiometry(compound, index, new_stoichiometry_records)
            for k, v in new_stoichiometry_records.items():
                if k in stoich_dict:
                    stoich_dict[k] = stoich_dict[k] + new_stoichiometry_records[k]
                else:
                    stoich_dict[k] = v
        else:
            if b >= 65 and b <= 90:
                element, coefficient, index = _parse_element_for_stoichiometry(compound, index)
                if element in stoich_dict:
                    stoich_dict[element] = stoich_dict[element] + coefficient
                else:
                    stoich_dict[element] = coefficient

    if index >= len(compound):
        return

    if c == ")":
        index = index + 1
    c = compound[index:index+1]
    b = ord(c)

    multplier_string = str()
    while ((b >= 48 and b <= 57) or b == 46):
        multplier_string = multplier_string + compound[index:index+1]
        index = index + 1
        if index == len(compound):
            return
        c = compound[index:index+1]
        b = ord(c)

    if multplier_string != "":
        multiplier = float(multplier_string)
        for k, v in stoich_dict.items():
            stoich_dict[k] = stoich_dict[k] * multiplier


def _populate_element_dictionary():
    """Create all the elements of the periodic table and add them to the
    element dictionary."""

    # period 1
    _element_dictionary["H"]   = Element(1,  1,   1, "H",    1.00794)
    _element_dictionary["He"]  = Element(1, 18,   2, "He",   4.002602)

    # period 2
    _element_dictionary["Li"]  = Element(2,  1,   3, "Li",   6.941)
    _element_dictionary["Be"]  = Element(2,  2,   4, "Be",   9.012182)
    _element_dictionary["B"]   = Element(2, 13,   5, "B",   10.811)
    _element_dictionary["C"]   = Element(2, 14,   6, "C",   12.0107)
    _element_dictionary["N"]   = Element(2, 15,   7, "N",   14.00674)
    _element_dictionary["O"]   = Element(2, 16,   8, "O",   15.9994)
    _element_dictionary["F"]   = Element(2, 17,   9, "F",   18.9984032)
    _element_dictionary["Ne"]  = Element(2, 18,  10, "Ne",  20.1797)

    # period 3
    _element_dictionary["Na"]  = Element(3,  1,  11, "Na",  22.98977)
    _element_dictionary["Mg"]  = Element(3,  2,  12, "Mg",  24.305)
    _element_dictionary["Al"]  = Element(3, 13,  13, "Al",  26.981538)
    _element_dictionary["Si"]  = Element(3, 14,  14, "Si",  28.0855)
    _element_dictionary["P"]   = Element(3, 15,  15, "P",   30.973762)
    _element_dictionary["S"]   = Element(3, 16,  16, "S",   32.066)
    _element_dictionary["Cl"]  = Element(3, 17,  17, "Cl",  35.4527)
    _element_dictionary["Ar"]  = Element(3, 18,  18, "Ar",  39.948)

    # period 4
    _element_dictionary["K"]   = Element(4,  1,  19, "K",   39.0983)
    _element_dictionary["Ca"]  = Element(4,  2,  20, "Ca",  40.078)
    _element_dictionary["Sc"]  = Element(4,  3,  21, "Sc",  44.95591)
    _element_dictionary["Ti"]  = Element(4,  4,  22, "Ti",  47.867)
    _element_dictionary["V"]   = Element(4,  5,  23, "V",   50.9415)
    _element_dictionary["Cr"]  = Element(4,  6,  24, "Cr",  51.9961)
    _element_dictionary["Mn"]  = Element(4,  7,  25, "Mn",  54.938049)
    _element_dictionary["Fe"]  = Element(4,  8,  26, "Fe",  55.845)
    _element_dictionary["Co"]  = Element(4,  9,  27, "Co",  58.9332)
    _element_dictionary["Ni"]  = Element(4, 10,  28, "Ni",  58.6934)
    _element_dictionary["Cu"]  = Element(4, 11,  29, "Cu",  63.546)
    _element_dictionary["Zn"]  = Element(4, 12,  30, "Zn",  65.39)
    _element_dictionary["Ga"]  = Element(4, 13,  31, "Ga",  69.723)
    _element_dictionary["Ge"]  = Element(4, 14,  32, "Ge",  72.61)
    _element_dictionary["As"]  = Element(4, 15,  33, "As",  74.9216)
    _element_dictionary["Se"]  = Element(4, 16,  34, "Se",  78.96)
    _element_dictionary["Br"]  = Element(4, 17,  35, "Br",  79.904)
    _element_dictionary["Kr"]  = Element(4, 18,  36, "Kr",  83.8)

    # period 5
    _element_dictionary["Rb"]  = Element(5,  1,  37, "Rb",  85.4678)
    _element_dictionary["Sr"]  = Element(5,  2,  38, "Sr",  87.62)
    _element_dictionary["Y"]   = Element(5,  3,  39, "Y",   88.90585)
    _element_dictionary["Zr"]  = Element(5,  4,  40, "Zr",  91.224)
    _element_dictionary["Nb"]  = Element(5,  5,  41, "Nb",  92.90638)
    _element_dictionary["Mo"]  = Element(5,  6,  42, "Mo",  95.94)
    _element_dictionary["Tc"]  = Element(5,  7,  43, "Tc",  98.0)
    _element_dictionary["Ru"]  = Element(5,  8,  44, "Ru",  101.07)
    _element_dictionary["Rh"]  = Element(5,  9,  45, "Rh",  102.9055)
    _element_dictionary["Pd"]  = Element(5, 10,  46, "Pd",  106.42)
    _element_dictionary["Ag"]  = Element(5, 11,  47, "Ag",  107.8682)
    _element_dictionary["Cd"]  = Element(5, 12,  48, "Cd",  112.411)
    _element_dictionary["In"]  = Element(5, 13,  49, "In",  114.818)
    _element_dictionary["Sn"]  = Element(5, 14,  50, "Sn",  118.71)
    _element_dictionary["Sb"]  = Element(5, 15,  51, "Sb",  121.76)
    _element_dictionary["Te"]  = Element(5, 16,  52, "Te",  127.6)
    _element_dictionary["I"]   = Element(5, 17,  53, "I",   126.90447)
    _element_dictionary["Xe"]  = Element(5, 18,  54, "Xe",  131.29)

    # period 6
    _element_dictionary["Cs"]  = Element(6,  1,  55, "Cs",  132.90545)
    _element_dictionary["Ba"]  = Element(6,  2,  56, "Ba",  137.327)
    _element_dictionary["La"]  = Element(6,  0,  57, "La",  138.9055)
    _element_dictionary["Ce"]  = Element(6,  0,  58, "Ce",  140.116)
    _element_dictionary["Pr"]  = Element(6,  0,  59, "Pr",  140.90765)
    _element_dictionary["Nd"]  = Element(6,  0,  60, "Nd",  144.24)
    _element_dictionary["Pm"]  = Element(6,  0,  61, "Pm",  145.0)
    _element_dictionary["Sm"]  = Element(6,  0,  62, "Sm",  150.36)
    _element_dictionary["Eu"]  = Element(6,  0,  63, "Eu",  151.964)
    _element_dictionary["Gd"]  = Element(6,  0,  64, "Gd",  157.25)
    _element_dictionary["Tb"]  = Element(6,  0,  65, "Tb",  158.92534)
    _element_dictionary["Dy"]  = Element(6,  0,  66, "Dy",  162.5)
    _element_dictionary["Ho"]  = Element(6,  0,  67, "Ho",  164.93032)
    _element_dictionary["Er"]  = Element(6,  0,  68, "Er",  167.26)
    _element_dictionary["Tm"]  = Element(6,  0,  69, "Tm",  168.93421)
    _element_dictionary["Yb"]  = Element(6,  0,  70, "Yb",  173.04)
    _element_dictionary["Lu"]  = Element(6,  0,  71, "Lu",  174.967)
    _element_dictionary["Hf"]  = Element(6,  4,  72, "Hf",  178.49)
    _element_dictionary["Ta"]  = Element(6,  5,  73, "Ta",  180.9479)
    _element_dictionary["W"]   = Element(6,  6,  74, "W",   183.84)
    _element_dictionary["Re"]  = Element(6,  7,  75, "Re",  186.207)
    _element_dictionary["Os"]  = Element(6,  8,  76, "Os",  190.23)
    _element_dictionary["Ir"]  = Element(6,  9,  77, "Ir",  192.217)
    _element_dictionary["Pt"]  = Element(6, 10,  78, "Pt",  195.078)
    _element_dictionary["Au"]  = Element(6, 11,  79, "Au",  196.96655)
    _element_dictionary["Hg"]  = Element(6, 12,  80, "Hg",  200.59)
    _element_dictionary["Tl"]  = Element(6, 13,  81, "Tl",  204.3833)
    _element_dictionary["Pb"]  = Element(6, 14,  82, "Pb",  207.2)
    _element_dictionary["Bi"]  = Element(6, 15,  83, "Bi",  208.98038)
    _element_dictionary["Po"]  = Element(6, 16,  84, "Po",  210.0)
    _element_dictionary["At"]  = Element(6, 17,  85, "At",  210.0)
    _element_dictionary["Rn"]  = Element(6, 18,  86, "Rn",  222.0)

    # period 7
    _element_dictionary["Fr"]  = Element(7,  1, 87, "Fr",   223.0)
    _element_dictionary["Ra"]  = Element(7,  2, 88, "Ra",   226.0)
    _element_dictionary["Ac"]  = Element(7,  0, 89, "Ac",   227.0)
    _element_dictionary["Th"]  = Element(7,  0, 90, "Th",   232.0381)
    _element_dictionary["Pa"]  = Element(7,  0, 91, "Pa",   231.03588)
    _element_dictionary["U"]   = Element(7,  0, 92, "U",    238.0289)
    _element_dictionary["Np"]  = Element(7,  0, 93, "Np",   237.0)
    _element_dictionary["Pu"]  = Element(7,  0, 94, "Pu",   244.0)
    _element_dictionary["Am"]  = Element(7,  0, 95, "Am",   243.0)
    _element_dictionary["Cm"]  = Element(7,  0, 96, "Cm",   247.0)
    _element_dictionary["Bk"]  = Element(7,  0, 97, "Bk",   247.0)
    _element_dictionary["Cf"]  = Element(7,  0, 98, "Cf",   251.0)
    _element_dictionary["Es"]  = Element(7,  0, 99, "Es",   252.0)
    _element_dictionary["Fm"]  = Element(7,  0, 100, "Fm",  257.0)
    _element_dictionary["Md"]  = Element(7,  0, 101, "Md",  258.0)
    _element_dictionary["No"]  = Element(7,  0, 102, "No",  259.0)
    _element_dictionary["Lr"]  = Element(7,  0, 103, "Lr",  262.0)
    _element_dictionary["Rf"]  = Element(7,  4, 104, "Rf",  261.0)
    _element_dictionary["Db"]  = Element(7,  5, 105, "Db",  262.0)
    _element_dictionary["Sg"]  = Element(7,  6, 106, "Sg",  266.0)
    _element_dictionary["Bh"]  = Element(7,  7, 107, "Bh",  264.0)
    _element_dictionary["Hs"]  = Element(7,  8, 108, "Hs",  269.0)
    _element_dictionary["Mt"]  = Element(7,  9, 109, "Mt",  268.0)
    _element_dictionary["Ds"]  = Element(7, 10, 110, "Ds",  269.0)
    _element_dictionary["Rg"]  = Element(7, 11, 111, "Rg",  272.0)
    # Cn missing
    # Uut missing
    # Fl missing
    # Uup missing
    # Lv missing
    # Uus missing
    # Uuo missing
    # actinides


# =============================================================================
# Public functions.
# =============================================================================

def amount(compound, mass):
    """Calculate the number of moles in the specified mass of a chemical
    compound.

    :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]". The \
    phase may be omitted.
    :param mass:     [kg]

    :returns: Amount. [kmol]
    """

    return mass / molar_mass(_get_formula(compound))


def mass(compound, amount):
    """Calculate the mass of the specified amount of a chemical compound.

    :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]". The \
phase may be omitted.
    :param amount:   [kmol]

    :returns: Mass. [kg]
    """

    return amount * molar_mass(_get_formula(compound))


def convert_compound(mass, source, target, element):
    """Convert the specified mass of the source compound to the target using
    element as basis.

    :param mass:    Mass of from_compound. [kg]
    :param source:  Formula and phase of the original compound, e.g. \
    "Fe2O3[S1]".
    :param target:  Formula and phase of the target compound, e.g. \
    "Fe[S1]".
    :param element: Element to use as basis for the conversion, e.g. \
    "Fe" or "O".

    :returns: Mass of to_compound. [kg]
    """

    # Convert compounds to formulas.
    source_formula = _get_formula(source)
    target_formula = _get_formula(target)

    # Perform the conversion.
    source_mass_fraction = element_mass_fraction(source_formula, element)
    target_mass_fraction = element_mass_fraction(target_formula, element)
    if target_mass_fraction == 0.0:
        # If target_formula does not contain element, just return 0.0.
        return 0.0
    else:
        return mass * source_mass_fraction / target_mass_fraction


def element_mass_fraction(compound, element):
    """Determine the mass fraction of an element in a chemical compound.

    :param compound: Formula of the chemical compound, "FeCr2O4".
    :param element: Element, e.g. "Cr".

    :returns: Element mass fraction."""

    elementStoichiometryCoefficient = stoichiometry_coefficient(compound, element)
    if elementStoichiometryCoefficient == 0.0:
        return 0.0
    else:
        formulaMass = molar_mass(compound)
        elementMass = molar_mass(element)
        return elementStoichiometryCoefficient * elementMass / formulaMass


def element_mass_fractions(compound, elements):
    """Determine the mass fractions of a list of elements in a chemical
    compound.

    :param compound: Formula and phase of a chemical compound, e.g. \
    "Fe2O3[S1]".
    :param elements: List of elements, ["Si", "O", "Fe"].

    :returns: Mass fractions."""

    formula = _get_formula(compound)
    result = numpy.array([])
    for i in range(0, len(elements)):
        result = numpy.append(result, element_mass_fraction(formula, elements[i]))
    return result


def elements(compounds):
    """Determine the set of elements present in a list of chemical compounds.

    The list of elements is sorted alphabetically.

    :param compounds: List of compound formulas and phases, e.g. \
    ["Fe2O3[S1]", "Al2O3[S1]"].

    :returns: List of elements.
    """

    result = set()
    for compound in compounds:
        formula = _get_formula(compound)
        result = result.union(_parse_formula_for_elements(formula))
    return result


def molar_mass(compound=""):
    """Determine the molar mass of a chemical compound.

    The molar mass is usually the mass of one mole of the substance, but here
    it is the mass of 1000 moles, since the mass unit used in pmpy is kg.

    :param compound: Formula of a chemical compound, e.g. "Fe2O3".

    :returns: Molar mass. [kg/kmol]"""

    result = 0.0
    compound = compound.strip()
    if len(compound) == 0:
        return result

    code = _formula_code(compound)
    if code not in _molar_mass_dictionary:
        index = 0
        _molar_mass_dictionary[code] = _parse_formula_for_mass(compound, index)
    result = _molar_mass_dictionary[code]

    return result


def stoichiometry_coefficient(compound, element):
    """Determine the stoichiometry coefficient of an element in a chemical
    compound.

    :param compound: Formula of a chemical compound, e.g. "SiO2".
    :param element:  Element, e.g. "Si".

    :returns: Stoichiometry coefficient."""

    compound = compound.strip()

    if compound not in _stoichiometry_dictionary:
        stoichiometry = {}
        _parse_formula_for_stoichiometry(compound, 0, stoichiometry)
        _stoichiometry_dictionary[_formula_code(compound)] = stoichiometry

    stoichiometry = _stoichiometry_dictionary[_formula_code(compound)]

    if element in stoichiometry:
        return stoichiometry[element]
    else:
        return 0.0


# TODO: Fix problem when there are brackets in the formula.
def stoichiometry_coefficients(compound, elements):
    """Determine the stoichiometry coefficients of the specified elements in
    the specified chemical compound.

    :param compound: Formula of a chemical compound, e.g. "SiO2".
    :param elements: List of elements, e.g. ["Si", "O", "C"].

    :returns: List of stoichiometry coefficients."""

    result = []
    for i in range(0, len(elements)):
        result.append(stoichiometry_coefficient(compound, elements[i]))
    return result


# =============================================================================
# Private variables.
# =============================================================================

_element_dictionary = {}
_molar_mass_dictionary = {}
_stoichiometry_dictionary = {}


# =============================================================================
# Module initialisation.
# =============================================================================

_populate_element_dictionary()
