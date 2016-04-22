Thermochemical Calculations
***************************

Preparing Thermochemical Data
=============================
The :py:mod:`auxi.tools.chemistry.thermochemistry` module provides a number of useful functions for doing thermochemical calculations that would otherwise have been quite cumbersome to do. To make these calculations possible, some thermochemical data is needed. The :py:mod:`auxi` distribution package currently contains data for around 80 compounds. This may, however, not be sufficient for your process calculations. FactSage data can be converted into auxi thermochemical data using the :py:func:`~.auxi.tools.chemistry.thermochemistry.convert_fact_file_to_auxi_thermo_file` function.

To prepare your own compound data files with FactSage, follow these steps:

* Open FactSage.
* Click on the "View Data" button.
* Select the "Compound" option, NOT "Solution".
* Select the database that you want to use. "FactPS" should be OK.
* Type the formula of the compound you need in the box at the bottom.
* Click OK.
* Click on the "Cp(T)" tab.
* Select "File" from the menu and then "Save As ...".
* Select the folder where you want to store all your thermochemical data files.
* The filename must have a specific format. Taking "Ar" as an example, use "Compound_Ar.txt" for the file name.
* Click "Save".

You will have to repeat this procedure for all the compounds that you need to include in your calculations.

To convert the factsage file to an auxi thermochemical file use the following code::

    from auxi.tools.chemistry import thermochemistry as thermo

    thermo.convert_fact_file_to_auxi_thermo_file("path/to/factsage_file", "path/to/new_auxi_thermo_file")


Loading Thermochemical Data
===========================
If you are going to use the default set of data provided with :py:mod:`auxi`, you do not need to do anything. The entire data set will be available by default. You can obtain a list of all the compounds and their phases by using the following code::

    from auxi.tools.chemistry import thermochemistry as thermo

    thermo.list_compounds()

Here are the first few lines of the result::

    Compounds currently loaded in the thermochemistry module:
    Ag ['G', 'L', 'S']
    Ag2O ['S']
    Al ['G', 'L', 'S']
    Al2O3 ['G', 'L', 'S1', 'S2', 'S3', 'S4']
    Al4C3 ['S1']
    C ['G', 'S1', 'S2']
    C2H2 ['G']
    CH4 ['Aq', 'G']
    CO ['G']
    CO2 ['G']
    ...

The result lists all the compounds with the phases for which data are available. Taking the compound SiO2 as an example, data are available for eight solid phases (S1 to S8), for the liquid phase and for the gas phase.

If you have decided to create you own data folder, you can force :py:mod:`auxi` to use the data in that folder. Here is the code for this::

    from auxi.tools.chemistry import thermochemistry as thermo

    thermo.load_data('/home/someuser/thermodata')
    thermo.list_compounds()

This example data folder only contains a small selection of files::

    Compounds currently loaded in the thermo module:
    Ag ['G', 'L', 'S']
    CaO ['G', 'L', 'S']
    Cr2O3 ['L', 'S']
    Cu ['G', 'L', 'S']
    CuO ['G', 'S']


Calculating Heat Capacity
=========================
The :py:func:`~.auxi.tools.chemistry.thermochemistry.Cp` function in the :py:mod:`auxi.tools.chemistry.thermochemistry` module can be used to calculate the heat capacity at constant pressure for a compound. This can be done as follows::

    from auxi.tools.chemistry import thermochemistry as thermo

    Cp_H2O = thermo.Cp("H2O[L]", 70.0)
    print("The Cp of 1 kg of water at 70 °C is", Cp_H2O, "kWh/K.")

    Cp_H2O = thermo.Cp("H2O[G]", 70.0)
    print("The Cp of 1 kg of water vapour at 70 °C is", Cp_H2O, "kWh/K.")

    m_ZrO2 = 2.34
    Cp_ZrO2 = thermo.Cp("ZrO2[S1]", 893.5, m_ZrO2)
    print("The Cp of 2.34 kg of ZrO2[S1] at 893.5 °C is", Cp_ZrO2, "kWh/K.")

Here are the results::

    The Cp of 1 kg of water at 70 °C is 0.0011634065724223574 kWh/K.
    The Cp of 1 kg of water vapour at 70 °C is 0.0005217114220395267 kWh/K.
    The Cp of 2.34 kg of ZrO2[S1] at 70 °C is 0.0004084615851157184 kWh/K.

The first parameter to the function must specify both the compound's formula and phase. If the phase is not specified it is impossible to calculate a result. The heat capacity of water is clearly significantly different from that of water vapour.

The last parameter of the :py:func:`~.auxi.tools.chemistry.thermochemistry.Cp` is mass and it is optional. If no value is specified, it is taken to be 1 kg. This was the case for the first two calculations above. A mass of 2.34 kg was specified in the last Cp calculation.


Calculating Enthalpy
====================
The :py:func:`~.auxi.tools.chemistry.thermochemistry.H` function in :py:mod:`~.auxi.tools.chemistry.thermochemistry` is used to calculate the enthalpy of a compound. This can be done as follows::

    from auxi.tools.chemistry import thermochemistry as thermo

    H_H2O = thermo.H("H2O[L]", 70.0)
    print("The enthalpy of 1 kg of water at 70 °C is", H_H2O, "kWh.")

    H_H2O = thermo.H("H2O[G]", 70.0)
    print("The enthalpy of 1 kg of water vapour at 70 °C is", H_H2O, "kWh.")

    m_ZrO2 = 2.34
    H_ZrO2 = thermo.H("ZrO2[S1]", 893.5, m_ZrO2)
    print("The enthalpy of 2.34 kg of ZrO2[S1] at 893.5 °C is", H_ZrO2, "kWh.")

Here are the results::

    The enthalpy of 1 kg of water at 70 °C is -4.35495670039936 kWh.
    The enthalpy of 1 kg of water vapour at 70 °C is -3.7054553712406264 kWh.
    The enthalpy of 2.34 kg of ZrO2[S1] at 893.5 °C is -5.463105585819936 kWh.

The parameters to the :py:func:`~.auxi.tools.chemistry.thermochemistry.H` function works the same as that of the :py:func:`~.auxi.tools.chemistry.thermochemistry.Cp` function. Both formula and phase are required in the first parameter, the second is temperature in °C and the third is mass, which is optional with a default value of 1 kg.


Calculating Entropy
===================
The :py:func:`~.auxi.tools.chemistry.thermochemistry.S` function in :py:mod:`~.auxi.tools.chemistry.thermochemistry` is used to calculate the entropy of a compound. This can be done as follows::

    from auxi.tools.chemistry import thermochemistry as thermo

    S_H2O = thermo.S("H2O[L]", 70.0)
    print("The entropy of 1 kg of water at 70 °C is", S_H2O, "kWh/K.")

    S_H2O = thermo.S("H2O[G]", 70.0)
    print("The entropy of 1 kg of water vapour at 70 °C is", S_H2O, "kWh/K.")

    m_ZrO2 = 2.34
    S_ZrO2 = thermo.S("ZrO2[S1]", 893.5, m_ZrO2)
    print("The entropy of 2.34 kg of ZrO2[S1] at 893.5 °C is", S_ZrO2, "kWh/K.")

Here are the results::

    The entropy of 1 kg of water at 70 °C is 0.0012418035680941087 kWh/K.
    The entropy of 1 kg of water vapour at 70 °C is 0.0029829908763826032 kWh/K.
    The entropy of 2.34 kg of ZrO2[S1] at 893.5 °C is 0.000762164298048799 kWh/K.

The parameters to the :py:func:`~.auxi.tools.chemistry.thermochemistry.S` function works the same as that of the :py:func:`~.auxi.tools.chemistry.thermochemistry.Cp` function. Both formula and phase are required in the first parameter, the second is temperature in °C and the third is mass, which is optional with a default value of 1 kg.


Calculating Gibbs Free Energy
=============================
The :py:func:`~.auxi.tools.chemistry.thermochemistry.G` function in :py:mod:`~.auxi.tools.chemistry.thermochemistry` is used to calculate the Gibbs free energy of a compound. This can be done as follows::

    from auxi.tools.chemistry import thermochemistry as thermo

    G_H2O = thermo.G("H2O[L]", 70.0)
    print("The Gibbs free energy of 1 kg of water at 70 °C is", G_H2O,
        "kWh.")

    G_H2O = thermo.G("H2O[G]", 70.0)
    print("The Gibbs free energy of 1 kg of water vapour at 70 °C is", G_H2O,
        "kWh.")

    m_ZrO2 = 2.34
    G_ZrO2 = thermo.G("ZrO2[S1]", 893.5, m_ZrO2)
    print("The Gibbs free energy of 2.34 kg of ZrO2[S1] at 893.5 °C is", G_ZrO2,
        "kWh.")

Here are the results::

    The Gibbs free energy of 1 kg of water at 70 °C is
        -4.781081594790853 kWh.
    The Gibbs free energy of 1 kg of water vapour at 70 °C is
        -4.729068690471317 kWh.
    The Gibbs free energy of 2.34 kg of ZrO2[S1] at 893.5 °C is
        -6.352284564138569 kWh.

The parameters to the :py:func:`~.auxi.tools.chemistry.thermochemistry.G` function works the same as that of the :py:func:`~.auxi.tools.chemistry.thermochemistry.Cp` function. Both formula and phase are required in the first parameter, the second is temperature in °C and the third is mass, which is optional with a default value of 1 kg.
