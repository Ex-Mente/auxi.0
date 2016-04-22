Stoichiometry Calculations
**************************

Warning
=======
:py:mod:`auxi.tools.chemistry.stoichiometry` is not yet able to successfully parse compound formulae that contain parentheses. It is therefore suggested that a formula such as "Fe2(SO4)3" rather be expressed as "Fe2S3O12".


Calculating Molar Mass
======================
Determining the molar mass of a substance is done countless times in mass and energy balance models and other process models. It usually requires you to create your own little database or list that you look up the values from. Once you have that, you can perform the required calculations. The :py:mod:`auxi.tools.chemistry.stoichiometry` module provides the :py:func:`~.auxi.tools.chemistry.stoichiometry.molar_mass` function for this purpose.


Standard Approach
-----------------
The normal way of getting the molar mass of one or more compounds is as follows::

    from auxi.tools.chemistry import stoichiometry

    molarmass_FeO = stoichiometry.molar_mass("FeO")
    molarmass_CO2 = stoichiometry.molar_mass("CO2")
    molarmass_FeCr2O4 = stoichiometry.molar_mass("FeCr2O4")

    print("Molar mass of FeO    :", molarmass_FeO, "kg/kmol")
    print("Molar mass of CO2    :", molarmass_CO2, "kg/kmol")
    print("Molar mass of FeCr2O4:", molarmass_FeCr2O4, "kg/kmol")

The result of this should be::

    Molar mass of FeO    : 71.8444 kg/kmol
    Molar mass of CO2    : 44.0095 kg/kmol
    Molar mass of FeCr2O4: 223.8348 kg/kmol


Compact Approach
----------------
One of Python's strengths is its ability to make code very compact. You may not always want to use a lengthy "stoichiometry.molar_mass" reference to the function. Rather than importing the :py:mod:`~.auxi.tools.chemistry.stoichiometry` module, we can import the :py:func:`~.auxi.tools.chemistry.stoichiometry.molar_mass` function directly, and give it another name. Here is how you can make it short and sweet::

    from auxi.tools.chemistry.stoichiometry import molar_mass as mm

    molarmass_FeO = mm("FeO")

    print("Molar mass of FeO    :", molarmass_FeO, "kg/kmol")
    print("Molar mass of CO2    :", mm("CO2"), "kg/kmol")
    print("Molar mass of FeCr2O4:", mm("FeCr2O4"), "kg/kmol")

The result is still the same::

    Molar mass of FeO    : 71.8444 kg/kmol
    Molar mass of CO2    : 44.0095 kg/kmol
    Molar mass of FeCr2O4: 223.8348 kg/kmol


More Examples
-------------
Here are some more examples of molar mass calculations::

    from auxi.tools.chemistry.stoichiometry import molar_mass as mm

    def print_molar_mass(compound):
        print("Molar mass of", compound, "is", mm(compound), "kg/kmol.")

    print_molar_mass("FeO1.5")
    print_molar_mass("Fe2O3")
    print_molar_mass("FeOTiO2")
    print_molar_mass("FeTiO3")
    print_molar_mass("Fe2(CO3)3")
    print_molar_mass("Fe2C3O9")
    print_molar_mass("H2O")
    print_molar_mass("H")
    print_molar_mass("He")
    print_molar_mass("Au")

And the results are::

    Molar mass of FeO1.5 is 79.8441 kg/kmol.
    Molar mass of Fe2O3 is 159.6882 kg/kmol.
    Molar mass of FeOTiO2 is 151.7102 kg/kmol.
    Molar mass of FeTiO3 is 151.7102 kg/kmol.
    Molar mass of Fe2(CO3)3 is 291.7167 kg/kmol.
    Molar mass of Fe2C3O9 is 291.7167 kg/kmol.
    Molar mass of H2O is 18.01528 kg/kmol.
    Molar mass of H is 1.00794 kg/kmol.
    Molar mass of He is 4.002602 kg/kmol.
    Molar mass of Au is 196.96655 kg/kmol.


Calculating Compound Amount
===========================
Sometimes you need to convert the mass of a compound (kg) to the equivalent amount (kmol). The :py:mod:`~.auxi.tools.chemistry.stoichiometry` module provides the :py:func:`~.auxi.tools.chemistry.stoichiometry.amount` function to do this.

The amount is calculated as follows:

.. math::
    n_{\text{compound}} = \frac{m_{\text{compound}}}{mm_{\text{compound}}}

where

* :math:`n_{\text{compound}}` is the compound amount in kmol.
* :math:`m_{\text{compound}}` is the compound mass in kg.
* :math:`mm_{\text{compound}}` is the compound molar mass in kg/kmol.


Standard Approach
-----------------
The normal way of calculating the amount of a compound is as follows::

    from auxi.tools.chemistry import stoichiometry

    m_FeO = 10.0
    n_FeO = stoichiometry.amount("FeO", m_FeO)
    print("There is", n_FeO, "kmol of FeO in", m_FeO , "kg of the compound.")

    m_CO2 = 12.3
    n_CO2 = stoichiometry.amount("CO2", m_CO2)
    print("There is", n_CO2, "kmol of CO2 in", m_CO2 , "kg of the compound.")

    m_FeCr2O4 = 453.0
    n_FeCr2O4 = stoichiometry.amount("FeCr2O4", m_FeCr2O4)
    print("There is", n_FeCr2O4, "kmol of FeCr2O4 in",
          m_FeCr2O4 , "kg of the compound.")

The result of this should be::

    There is 0.1391896932815919 kmol of FeO in 10.0 kg of the compound.
    There is 0.2794851111691794 kmol of CO2 in 12.3 kg of the compound.
    There is 2.0238139913900786 kmol of FeCr2O4 in 453.0 kg of the compound.


Compact Approach
----------------
To make the code more compact, we can import the function instead of the module and get the same result like this::

    from auxi.tools.chemistry.stoichiometry import amount

    m_FeO = 10.0
    n_FeO = amount("FeO", m_FeO)
    print("There is", n_FeO, "kmol of FeO in", m_FeO , "kg of the compound.")

    m_CO2 = 12.3
    n_CO2 = amount("CO2", m_CO2)
    print("There is", n_CO2, "kmol of CO2 in", m_CO2 , "kg of the compound.")

    m_FeCr2O4 = 453.0
    n_FeCr2O4 = amount("FeCr2O4", m_FeCr2O4)
    print("There is", n_FeCr2O4, "kmol of FeCr2O4 in",
          m_FeCr2O4 , "kg of the compound.")

The result is still the same::

    There is 0.1391896932815919 kmol of FeO in 10.0 kg of the compound.
    There is 0.2794851111691794 kmol of CO2 in 12.3 kg of the compound.
    There is 2.0238139913900786 kmol of FeCr2O4 in 453.0 kg of the compound.


Calculating Compound Mass
===========================
You often have the amount (kmol) of a compound and then need to calculate its mass. The :py:mod:`~.auxi.tools.chemistry.stoichiometry` module provides the :py:func:`~.auxi.tools.chemistry.stoichiometry.mass` function for this. The mass is calculate with this formula:

.. math::
    m_{\text{compound}} = n_{\text{compound}} \cdot mm_{\text{compound}}

where

* :math:`m_{\text{compound}}` is the compound mass in kg.
* :math:`n_{\text{compound}}` is the compound amount in kmol.
* :math:`mm_{\text{compound}}` is the compound molar mass in kg/kmol.


From this point forward the standard and compact approaches are not both demonstrated. Only the standard method, which imports the module, is used below since it is more explicit::

    from auxi.tools.chemistry import stoichiometry

    n_FeO = 10.0
    m_FeO = stoichiometry.mass("FeO", n_FeO)
    print("There is", m_FeO, "kg of FeO in", n_FeO , "kmol of the compound.")

    m_CO2 = 12.3
    n_CO2 = stoichiometry.mass("CO2", m_CO2)
    print("There is", m_CO2, "kg of CO2 in", n_CO2 , "kmol of the compound.")

    m_FeCr2O4 = 453.0
    n_FeCr2O4 = stoichiometry.mass("FeCr2O4", m_FeCr2O4)
    print("There is", m_FeCr2O4, "kg of FeCr2O4 in",
          n_FeCr2O4 , "kmol of the compound.")

The restuls are::

    There is 718.444 kg of FeO in 10.0 kmol of the compound.
    There is 12.3 kg of CO2 in 541.31685 kmol of the compound.
    There is 453.0 kg of FeCr2O4 in 101397.1644 kmol of the compound.


Identifying Elements in Compounds
=================================
The list of elements present in one or more compounds can be used when calculating element balances. Determining this list is often done manually. :py:mod:`~.auxi.tools.chemistry.stoichiometry` has the :py:func:`~.auxi.tools.chemistry.stoichiometry.elements` function to automate this task. This is how you use it::

    from auxi.tools.chemistry import stoichiometry

    elements_Fe2O3 = stoichiometry.elements(["Fe2O3"])
    print("Fe2O3 contains these elements:", elements_Fe2O3)

    elements_CO2 = stoichiometry.elements(["CO2"])
    print("CO2 contains these elements:", elements_CO2)

    elements_Fe2Cr2O4 = stoichiometry.elements(["Fe2Cr2O4"])
    print("Fe2Cr2O4 contains these elements:", elements_Fe2Cr2O4)

    elements_Al2S3O12 = stoichiometry.elements(["Al2(SO4)3"])
    print("Al2(SO4)3 contains these elements:", elements_Al2S3O12)

    elements_all = stoichiometry.elements(["Fe2O3", "CO2", "Fe2Cr2O4", "Al2(SO4)3"])
    print("Fe2O3, CO2, Fe2Cr2O4 and Al2(SO4)3 contain these elements:",
          elements_all)

Here are the results::

    Fe2O3 contains these elements: {'Fe', 'O'}
    CO2 contains these elements: {'O', 'C'}
    Fe2Cr2O4 contains these elements: {'Fe', 'O', 'Cr'}
    Al2(SO4)3 contains these elements: {'Al', 'O', 'S'}
    Fe2O3, CO2, Fe2Cr2O4 and Al2(SO4)3 contain these elements:
        {'Al', 'Fe', 'O', 'C', 'S', 'Cr'}


Calculating Stoichiometry Coefficients
======================================
The :py:func:`~.auxi.tools.chemistry.stoichiometry.stoichiometry_coefficient` and :py:func:`~.auxi.tools.chemistry.stoichiometry.stoichiometry_coefficients` functions in :py:mod:`~.auxi.tools.chemistry.stoichiometry` determine the stoichiometry coefficients of elements in chemical compounds automatically. If we are only interested in the coefficient for a single element, we use :py:func:`~.auxi.tools.chemistry.stoichiometry.stoichiometry_coefficient` like this::

    from auxi.tools.chemistry import stoichiometry

    coeff_Fe2O3_Fe = stoichiometry.stoichiometry_coefficient("Fe2O3", "Fe")
    print("Stoichiometry coefficient of Fe in Fe2O3:", coeff_Fe2O3_Fe)

    coeff_Fe2O3_O = stoichiometry.stoichiometry_coefficient("Fe2O3", "O")
    print("Stoichiometry coefficient of O in Fe2O3:", coeff_Fe2O3_O)

    coeff_Fe2O3_C = stoichiometry.stoichiometry_coefficient("Fe2O3", "C")
    print("Stoichiometry coefficient of C in Fe2O3:", coeff_Fe2O3_C)

The results are::

    Stoichiometry coefficient of Fe in Fe2O3: 2.0
    Stoichiometry coefficient of O in Fe2O3: 3.0
    Stoichiometry coefficient of C in Fe2O3: 0.0

We can determine the coefficients for a list of elements using the :py:func:`~.auxi.tools.chemistry.stoichiometry.stoichiometry_coefficients` function::

    from auxi.tools.chemistry import stoichiometry

    elements = ["Fe", "O", "C", "Ar"]
    st_Fe2O3 = stoichiometry.stoichiometry_coefficients("Fe2O3", elements)
    print("Stoichiometry coefficient of", elements, "in Fe2O3:",
          st_Fe2O3)

    elements = ["Al", "Ca", "Fe", "Si", "O", "C", "H"]
    st_Lawsonite = stoichiometry.stoichiometry_coefficients("CaAl2Si2O7O2H2H2O",
                                                     elements)
    print("Stoichiometry coefficient of", elements,
          "in Lawsonite (CaAl2(Si2O7)(OH)2·H2O):", st_Lawsonite)

This produces these results::

    Stoichiometry coefficient of ['Fe', 'O', 'C', 'Ar'] in Fe2O3:
        [2.0, 3.0, 0.0, 0.0]
    Stoichiometry coefficient of ['Al', 'Ca', 'Fe', 'Si', 'O', 'C', 'H']
    in Lawsonite (CaAl2(Si2O7)(OH)2·H2O):
        [2.0, 1.0, 0.0, 2.0, 10.0, 0.0, 4.0]


Calculating Element Mass Fractions
==================================
Another two useful tools in the calculation of element balances are the :py:func:`~.auxi.tools.chemistry.stoichiometry.element_mass_fraction` and :py:func:`~.auxi.tools.chemistry.stoichiometry.element_mass_fractions` functions in :py:mod:`~.auxi.tools.chemistry.stoichiometry`. They are similar to the stoichiometry coefficient functions, but calculate the mass fraction of an element or list of elements in a chemical compound. The calculations are done with the following equation:

.. math::
    y_{\text{compound,element}} = \frac{n_{\text{compound,element}} \cdot mm_{\text{element}}}{mm_{\text{compound}}}

where

* :math:`y_{\text{compound,element}}` is the mass fraction of the specified element in the compound.
* :math:`n_{\text{compound,element}}` is the stoichiometry coefficient of the specified element in the compound.
* :math:`mm_{\text{element}}` is the element's molar mass in kg/kmol.
* :math:`mm_{\text{compound}}` is the compound's molar mass in kg/kmol.

For determining the mass fraction of a single element we can use :py:func:`~.auxi.tools.chemistry.stoichiometry.element_mass_fraction` as follows::

    from auxi.tools.chemistry import stoichiometry

    y_Fe2O3_Fe = stoichiometry.element_mass_fraction("Fe2O3", "Fe")
    print("Mass fraction of Fe in Fe2O3:", y_Fe2O3_Fe)

    y_Fe2O3_O = stoichiometry.element_mass_fraction("Fe2O3", "O")
    print("Mass fraction of O in Fe2O3:", y_Fe2O3_O)

    y_Fe2O3_C = stoichiometry.element_mass_fraction("Fe2O3", "C")
    print("Mass fraction of C in Fe2O3:", y_Fe2O3_C)

This produces these results::

    Mass fraction of Fe in Fe2O3: 0.699425505453753
    Mass fraction of O in Fe2O3: 0.300574494546247
    Mass fraction of C in Fe2O3: 0.0

Similarly, we can use :py:func:`~.auxi.tools.chemistry.stoichiometry.element_mass_fractions` to perform the calculation for a list of elements::

    from auxi.tools.chemistry import stoichiometry

    elements = ["Fe", "O", "C", "Ar"]
    y_Fe2O3 = stoichiometry.element_mass_fractions("Fe2O3", elements)
    print("Mass fractions of", elements, "in Fe2O3:", y_Fe2O3)

    elements = ["Al", "Ca", "Fe", "Si", "O", "C", "H"]
    y_Lawsonite = stoichiometry.element_mass_fractions("CaAl2Si2O7O2H2H2O", elements)
    print("Mass fractions of", elements,
          "in Lawsonite (CaAl2(Si2O7)(OH)2·H2O):",
          y_Lawsonite)

This results in::

    Mass fractions of ['Fe', 'O', 'C', 'Ar'] in Fe2O3:
        [ 0.69942551  0.30057449  0.0  0.0 ]
    Mass fractions of ['Al', 'Ca', 'Fe', 'Si', 'O', 'C', 'H']
    in Lawsonite (CaAl2(Si2O7)(OH)2·H2O):
        [ 0.17172686  0.12754034  0.0  0.17875314  0.50914938  0.0  0.01283028 ]


Converting Compounds
====================
Sometimes it is needed to convert the mass of one compound to an equivalent mass of another compound. For example, how much Fe will I get when I reduce a certain mass of Fe2O3? :py:mod:`~.auxi.tools.chemistry.stoichiometry` has the :py:func:`~.auxi.tools.chemistry.stoichiometry.convert_compound` function to help out. The function calculates the result as follows:

.. math::
    m_{\text{target}} = m_{\text{source}} \cdot \frac{y_{\text{source,element}}}{y_{\text{target,element}}}

where

* :math:`m_{\text{target}}` is the target compound mass in kg.
* :math:`m_{\text{source}}` is the source compound mass in kg.
* :math:`y_{\text{target,element}}` is the mass fraction of the specified base element in the target compound.
* :math:`y_{\text{source,element}}` is the mass fraction of the specified base element in the source compound.

Here are some simple examples of how to use :py:func:`~.auxi.tools.chemistry.stoichiometry.convert_compound`::

    from auxi.tools.chemistry import stoichiometry

    m_Fe2O3 = 10.0
    m_Fe = stoichiometry.convert_compound(m_Fe2O3, "Fe2O3", "Fe", "Fe")
    print("From", m_Fe2O3, "kg of Fe2O3,", m_Fe ,
          "kg of Fe can be produced.")

    m_Fe = 10.0
    m_Fe2O3 = stoichiometry.convert_compound(m_Fe, "Fe", "Fe2O3", "Fe")
    print("When", m_Fe, "kg of Fe is oxidised completely,", m_Fe2O3 ,
          "kg of Fe2O3 will be produced.")

The results are::

    From 10.0 kg of Fe2O3, 6.994255054537531 kg of Fe can be produced.
    When 10.0 kg of Fe is oxidised completely, 14.297448294386246 kg of
        Fe2O3 will be produced.

