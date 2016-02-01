Concepts
********

Motivation
==========
The material, material assay and material package concepts used in :py:mod:`auxi.modeling.process.materials` may initially seem somewhat foreign to new users. These concepts were developed to assist process engineers when doing metallurgical calculations, and while developing process models. It aims to reduce the complexity and time involved in performing these important but sometimes tedious tasks. Once these concepts have been mastered, they become incredibly powerful in the hands of a metallurgical process engineer.


Materials, Material Assays and Material Packages
================================================
:py:mod:`auxi.modeling.process.materials` includes a number of different representations of materials, material assays and material packages, each of which is contained in a separate Python module. The different modules cater for different situations as follows:

* :py:mod:`auxi.modeling.process.materials.psd.material` describes materials using particle size distributions. It can be used for processes in which particle size is the most important material property, such as a comminution circuit.
* :py:mod:`auxi.modeling.process.materials.psd.slurrymaterial` adds water to :py:mod:`~.auxi.modeling.process.materials.psd.material`. It can describe the solid and liquid portion of a particulate process such as a comminution circuit.
* :py:mod:`auxi.modeling.process.materials.chemistry.material` can be used for doing mass balances in chemically reactive processes such as leaching, precipitation, direct reduction and smelting. Its material class describes a material using its chemical composition. This module cannot perform any energy balance calculations.
* :py:mod:`auxi.modeling.process.materials.thermochemistry.material` adds thermochemistry to :py:mod:`~.auxi.modeling.process.materials.chemistry.material`. It can be used to do mass and energy balances in chemically reactive system such as smelting furnaces, direct reduction kilns, etc.

The :py:mod:`auxi.modeling.process.materials.thermochemistry.material` module will be used to illustrate the concepts here.

Material
--------
A Material class is used to represent a "type of material". Examples are ilmenite, iron ore, coal, ferrochrome alloy, etc. These terms are fairly abstract and generic, since they don't refer to something specific. The :py:mod:`~.auxi.modeling.process.materials.thermochemistry.material` module's :py:class:`~.auxi.modeling.process.materials.thermochemistry.material.Material` class uses uses a list of specific phases of chemical compounds to describe a "type of material". Here are some examples::

    ============================             ========================
    Material                                 Material
    ============================             ========================
    Name                Ilmenite             Name                Coal
    ----------------------------             ------------------------
    Compound                                 Compound
    ----------------------------             ------------------------
    Al2O3[S1]                                C[S1]
    CaO[S]                                   H2[G]
    Cr2O3[S]                                 O2[G]
    Fe2O3[S1]                                N2[G]
    Fe3O4[S1]                                S[S1]
    FeO[S]                                   Al2O3[S1]
    K2O[S]                                   CaO[S]
    MgO[S]                                   Fe2O3[S1]
    MnO[S]                                   MgO[S]
    Na2O[S1]                                 SiO2[S1]
    P4O10[S]                                 ========================
    SiO2[S1]
    TiO2[S1]
    V2O5[S]
    ============================

With the Ilmenite material we are specifying that, in our model or calculation, ilmenites will consist of the 14 compounds inluded in the first list. In the case of Coal, different coals will consist of the 10 compounds listed in the second list.


Material Assay
--------------
When we need to develop a model or do some calculations, it is not sufficient to simply know that a "type of material", such as ilmenite or coal, can consist of a specified list of compound phases. We need to know what the composition of a "specific material" is. With this composition we will be able to get started on some calculations. This is where material assays come in. In the next example, assays were added to the two materials defined above::

    ====================================================================
    Material
    ====================================================================
    Name                Ilmenite
    --------------------------------------------------------------------
    Composition Details (mass fractions)
    Compound            IlmeniteA        IlmeniteB        IlmeniteC
    --------------------------------------------------------------------
    Al2O3[S1]           1.16000000e-02   1.55000000e-02   9.41000000e-03
    CaO[S]              2.20000000e-04   1.00000000e-05   1.70000000e-04
    Cr2O3[S]            8.00000000e-05   2.20000000e-04   1.10000000e-04
    Fe2O3[S1]           2.02000000e-01   4.73000000e-01   4.96740000e-01
    Fe3O4[S1]           0.00000000e+00   0.00000000e+00   0.00000000e+00
    FeO[S]              2.79000000e-01   1.91000000e-01   0.00000000e+00
    K2O[S]              4.00000000e-05   1.00000000e-05   5.00000000e-05
    MgO[S]              1.04000000e-02   5.80000000e-03   1.09000000e-02
    MnO[S]              5.40000000e-03   4.80000000e-03   5.25000000e-03
    Na2O[S1]            7.00000000e-05   5.00000000e-05   3.10000000e-04
    P4O10[S]            1.00000000e-05   3.20000000e-04   1.50000000e-04
    SiO2[S1]            8.50000000e-03   4.90000000e-03   1.74400000e-02
    TiO2[S1]            4.77000000e-01   2.94000000e-01   4.59490000e-01
    V2O5[S]             3.60000000e-03   8.00000000e-03   0.00000000e+00
    ====================================================================


    ===================================================
    Material
    ===================================================
    Name                Coal
    ---------------------------------------------------
    Composition Details (mass fractions)
    Compound            ReductantA       ReductantB
    ---------------------------------------------------
    C[S1]               8.40973866e-01   1.00000000e+00
    H2[G]               1.37955186e-02   0.00000000e+00
    O2[G]               4.94339606e-02   0.00000000e+00
    N2[G]               6.09802120e-03   0.00000000e+00
    S[S1]               2.04933390e-03   0.00000000e+00
    Al2O3[S1]           1.20884160e-03   0.00000000e+00
    CaO[S]              2.94179980e-03   0.00000000e+00
    Fe2O3[S1]           7.85955656e-02   0.00000000e+00
    MgO[S]              1.41179360e-03   0.00000000e+00
    SiO2[S1]            3.49129950e-03   0.00000000e+00
    ===================================================

Our Ilmenite material now has three assays associated with it, and they are named IlmeniteA, IlmeniteB and IlmeniteC. Ilmenite therefore refers to a "type of material", and IlmeniteA, IlmeniteB and IlmeniteC refer to "specific materials".

Two assays were added to our Coal material. The first, ReductantA, refers to a coal with 84 % carbon and roughly 8.5 % ash. Reductant B is pure graphite.


Material Packages
-----------------
Using :py:mod:`auxi.modeling.process` we can now create a certain quantity of a "specific material" that is identified by a material and material assay. When we do this with the :py:mod:`~.auxi.modeling.process.materials.thermochemistry.material` :py:class:`~.auxi.modeling.process.materials.thermochemistry.material.Material` class, we also have to specify pressure and temperature. The result of creating 1000 kg of IlmeniteB at 1 atm pressure and 500 °C temperature is the following::

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.00000000e+03 kg
    Amount               9.81797715e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          5.00000000e+02 °C
    Enthalpy            -1.87069549e+03 kWh
    ------------------------------------------------------------------
    Compound Details:
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           1.55371337e+01  1.55371337e-02  1.55207829e-02
    CaO[S]              1.00239573e-02  1.00239573e-05  1.82066196e-05
    Cr2O3[S]            2.20527060e-01  2.20527060e-04  1.47782739e-04
    Fe2O3[S1]           4.74133178e+02  4.74133178e-01  3.02416515e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.91457584e+02  1.91457584e-01  2.71429867e-01
    K2O[S]              1.00239573e-02  1.00239573e-05  1.08388880e-05
    MgO[S]              5.81389521e+00  5.81389521e-03  1.46923993e-02
    MnO[S]              4.81149948e+00  4.81149948e-03  6.90848565e-03
    Na2O[S1]            5.01197863e-02  5.01197863e-05  8.23650657e-05
    P4O10[S]            3.20766632e-01  3.20766632e-04  1.15084949e-04
    SiO2[S1]            4.91173906e+00  4.91173906e-03  8.32630400e-03
    TiO2[S1]            2.94704343e+02  2.94704343e-01  3.75840583e-01
    V2O5[S]             8.01916581e+00  8.01916581e-03  4.49078466e-03
    ==================================================================

In the above result some of the useful work that :py:mod:`auxi.modeling.process.materials` does behind the scenes is already evident. The amount in kmol and the enthalpy in kWh of the material package was calculated, as were the masses and mole fractions of the compounds. You will notice that the mass fractions in the material package is slightly different from those in the IlmeniteB material assay. This is because the assay was automatically normalised to add up to 1.0. You can switch of normalisation if that is more appropriate.


Summary
-------
The :py:mod:`auxi.modeling.process.materials` concepts described above can be summarised as follows:

* A material provides a list of properties that describes a "type of material".
* A material assay describes a "specific material" by providing values for the listed properties.
* A material package describes a "specific quantity of material" belonging to a certain "type of material".

You may be wondering what the use of all this is. Why go through all the effort of defining materials, material assays and material packages? The next section demonstrates the power of these concepts.


Material Package Calculations
=============================
The use of materials and material packages are demonstrated here through the use of code snippets and the results produce by that code. We will be using ilmenite in the example. Firstly, let us import the :py:class:`auxi.modeling.process.materials.thermochemistry.material.Material`class, create a material object and print it out::

    from auxi.modeling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    print(ilmenite)

The material looks as follows::

    ====================================================================
    Material
    ====================================================================
    Name                Ilmenite
    --------------------------------------------------------------------
    Composition Details (mass fractions)
    Compound            IlmeniteA        IlmeniteB        IlmeniteC
    --------------------------------------------------------------------
    Al2O3[S1]           1.16000000e-02   1.55000000e-02   9.41000000e-03
    CaO[S]              2.20000000e-04   1.00000000e-05   1.70000000e-04
    Cr2O3[S]            8.00000000e-05   2.20000000e-04   1.10000000e-04
    Fe2O3[S1]           2.02000000e-01   4.73000000e-01   4.96740000e-01
    Fe3O4[S1]           0.00000000e+00   0.00000000e+00   0.00000000e+00
    FeO[S]              2.79000000e-01   1.91000000e-01   0.00000000e+00
    K2O[S]              4.00000000e-05   1.00000000e-05   5.00000000e-05
    MgO[S]              1.04000000e-02   5.80000000e-03   1.09000000e-02
    MnO[S]              5.40000000e-03   4.80000000e-03   5.25000000e-03
    Na2O[S1]            7.00000000e-05   5.00000000e-05   3.10000000e-04
    P4O10[S]            1.00000000e-05   3.20000000e-04   1.50000000e-04
    SiO2[S1]            8.50000000e-03   4.90000000e-03   1.74400000e-02
    TiO2[S1]            4.77000000e-01   2.94000000e-01   4.59490000e-01
    V2O5[S]             3.60000000e-03   8.00000000e-03   0.00000000e+00
    ====================================================================

Creating, Adding and Extracting
-------------------------------
Next we can use the material object (called ilmenite) to create a material package using each of the ilmenite assays::

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    print(ilma_package)
    ilmb_package = ilmenite.create_package("IlmeniteB", 500.0, 1.0, 750.0)
    print(ilmb_package)
    ilmc_package = ilmenite.create_package("IlmeniteC", 250.0, 1.0, 1200.0)
    print(ilmc_package)

Different masses were created from each assay (300 kg of IlmeniteA, 500.0 kg of IlmeniteB and 250.0 kg of IlmeniteC). All three packages were assigned a pressure of 1 atm, which is of no consequence. The packages were assigned temperatures of 25, 750 and 1200 °C respectively. In three short lines of code, :py:mod:`auxi.modeling.process.materials` did the following for us:

* Normalise the specified assay so that the mass fractions add up to 1.0. (We can choose not to do this.)
* Calculate the mass of each compound by multiplying the component mass fraction by the total package mass.
* Calculate the mass fraction of each compound.
* Calculate the mole fraction of each compound.
* Calculate the total amount (in kmol) of components in the package.
* Calculate the total enthalpy of the package by calculating the enthalpy of each compound and adding it together.

The result is as follows::

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 3.00000000e+02 kg
    Amount               3.52817004e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -6.87812118e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  1.16241783e-02  9.69390473e-03
    CaO[S]              6.61375661e-02  2.20458554e-04  3.34280337e-04
    Cr2O3[S]            2.40500241e-02  8.01667468e-05  4.48486990e-05
    Fe2O3[S1]           6.07263107e+01  2.02421036e-01  1.07784066e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  2.79581530e-01  3.30892788e-01
    K2O[S]              1.20250120e-02  4.00833734e-05  3.61829148e-05
    MgO[S]              3.12650313e+00  1.04216771e-02  2.19865404e-02
    MnO[S]              1.62337662e+00  5.41125541e-03  6.48625791e-03
    Na2O[S1]            2.10437710e-02  7.01459035e-05  9.62343053e-05
    P4O10[S]            3.00625301e-03  1.00208434e-05  3.00142421e-06
    SiO2[S1]            2.55531506e+00  8.51771685e-03  1.20540764e-02
    TiO2[S1]            1.43398268e+02  4.77994228e-01  5.08901291e-01
    V2O5[S]             1.08225108e+00  3.60750361e-03  1.68652807e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 5.00000000e+02 kg
    Amount               4.90898858e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          7.50000000e+02 °C
    Enthalpy            -9.05451326e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           7.76856687e+00  1.55371337e-02  1.55207829e-02
    CaO[S]              5.01197863e-03  1.00239573e-05  1.82066196e-05
    Cr2O3[S]            1.10263530e-01  2.20527060e-04  1.47782739e-04
    Fe2O3[S1]           2.37066589e+02  4.74133178e-01  3.02416515e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              9.57287918e+01  1.91457584e-01  2.71429867e-01
    K2O[S]              5.01197863e-03  1.00239573e-05  1.08388880e-05
    MgO[S]              2.90694760e+00  5.81389521e-03  1.46923993e-02
    MnO[S]              2.40574974e+00  4.81149948e-03  6.90848565e-03
    Na2O[S1]            2.50598931e-02  5.01197863e-05  8.23650657e-05
    P4O10[S]            1.60383316e-01  3.20766632e-04  1.15084949e-04
    SiO2[S1]            2.45586953e+00  4.91173906e-03  8.32630400e-03
    TiO2[S1]            1.47352172e+02  2.94704343e-01  3.75840583e-01
    V2O5[S]             4.00958290e+00  8.01916581e-03  4.49078466e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 2.50000000e+02 kg
    Amount               2.40014670e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          1.20000000e+03 °C
    Enthalpy            -5.25247309e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           2.35245295e+00  9.40981180e-03  9.61275553e-03
    CaO[S]              4.24991500e-02  1.69996600e-04  3.15758164e-04
    Cr2O3[S]            2.74994500e-02  1.09997800e-04  7.53824179e-05
    Fe2O3[S1]           1.24182516e+02  4.96730065e-01  3.24003606e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    K2O[S]              1.24997500e-02  4.99990000e-05  5.52880254e-05
    MgO[S]              2.72494550e+00  1.08997820e-02  2.81687499e-02
    MnO[S]              1.31247375e+00  5.24989500e-03  7.70863128e-03
    Na2O[S1]            7.74984500e-02  3.09993800e-04  5.20968045e-04
    P4O10[S]            3.74992500e-02  1.49997000e-04  5.50346434e-05
    SiO2[S1]            4.35991280e+00  1.74396512e-02  3.02328445e-02
    TiO2[S1]            1.14870203e+02  4.59480810e-01  5.99250982e-01
    V2O5[S]             0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================

We can now add these three packages of ilmenite together::

    total_package = ilma_package + ilmb_package + ilmc_package
    print(total_package)

In one line of code we did the following:

* Calculate the total mass of each component by adding up the component masses from the three original packages.
* Calculate the mass fraction of each compound.
* Calculate the mole fraction of each compound.
* Calculate the total amount (in kmol) of compounds in the package.
* Calculate the total enthalpy of the package by adding up the enthalpies from the three original packages.
* Calculate the temperature of the new package.

This new package (total_package) looks like this::

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.05000000e+03 kg
    Amount               1.08373053e+01 kmol
    Pressure             1.00000000e+00 atm
    Temperature          6.61513374e+02 °C
    Enthalpy            -2.11851075e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           1.36082733e+01  1.29602603e-02  1.23153413e-02
    CaO[S]              1.13648695e-01  1.08236852e-04  1.87005885e-04
    Cr2O3[S]            1.61813004e-01  1.54107623e-04  9.82371950e-05
    Fe2O3[S1]           4.21975416e+02  4.01881349e-01  2.43833300e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.79603251e+02  1.71050715e-01  2.30674699e-01
    K2O[S]              2.95367407e-02  2.81302292e-05  2.89340215e-05
    MgO[S]              8.75839623e+00  8.34132975e-03  2.00516825e-02
    MnO[S]              5.34160012e+00  5.08723821e-03  6.94823498e-03
    Na2O[S1]            1.23602114e-01  1.17716299e-04  1.84018059e-04
    P4O10[S]            2.00888819e-01  1.91322685e-04  6.52958859e-05
    SiO2[S1]            9.37109739e+00  8.92485465e-03  1.43915687e-02
    TiO2[S1]            4.05620643e+02  3.86305374e-01  4.68638424e-01
    V2O5[S]             5.09183399e+00  4.84936570e-03  2.58325918e-03
    ==================================================================

We can easily extract a part of a material package into a new one. Let us remove 30 kg from the new package and store it in a new package::

    dust_package = total_package.extract(30.0)
    print(dust_package)
    print(total_package)

By using one line of code we subtracted 30 kg of material from the original package and created a new one containing the subtracted 30 kg. All the other properties (e.g component masses, total amount and enthalpy) of the two packages were also recalculated. The extracted 30 kg package looks like this::

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 3.00000000e+01 kg
    Amount               3.09637295e-01 kmol
    Pressure             1.00000000e+00 atm
    Temperature          6.61513374e+02 °C
    Enthalpy            -6.05288787e+01 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.88807809e-01  1.29602603e-02  1.23153413e-02
    CaO[S]              3.24710557e-03  1.08236852e-04  1.87005885e-04
    Cr2O3[S]            4.62322868e-03  1.54107623e-04  9.82371950e-05
    Fe2O3[S1]           1.20564405e+01  4.01881349e-01  2.43833300e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              5.13152145e+00  1.71050715e-01  2.30674699e-01
    K2O[S]              8.43906876e-04  2.81302292e-05  2.89340215e-05
    MgO[S]              2.50239892e-01  8.34132975e-03  2.00516825e-02
    MnO[S]              1.52617146e-01  5.08723821e-03  6.94823498e-03
    Na2O[S1]            3.53148898e-03  1.17716299e-04  1.84018059e-04
    P4O10[S]            5.73968055e-03  1.91322685e-04  6.52958859e-05
    SiO2[S1]            2.67745640e-01  8.92485465e-03  1.43915687e-02
    TiO2[S1]            1.15891612e+01  3.86305374e-01  4.68638424e-01
    V2O5[S]             1.45480971e-01  4.84936570e-03  2.58325918e-03
    ==================================================================

The original package, which now contains 30 kg less, now looks like this::

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.02000000e+03 kg
    Amount               1.05276680e+01 kmol
    Pressure             1.00000000e+00 atm
    Temperature          6.61513374e+02 °C
    Enthalpy            -2.05798187e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           1.32194655e+01  1.29602603e-02  1.23153413e-02
    CaO[S]              1.10401589e-01  1.08236852e-04  1.87005885e-04
    Cr2O3[S]            1.57189775e-01  1.54107623e-04  9.82371950e-05
    Fe2O3[S1]           4.09918976e+02  4.01881349e-01  2.43833300e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.74471729e+02  1.71050715e-01  2.30674699e-01
    K2O[S]              2.86928338e-02  2.81302292e-05  2.89340215e-05
    MgO[S]              8.50815634e+00  8.34132975e-03  2.00516825e-02
    MnO[S]              5.18898297e+00  5.08723821e-03  6.94823498e-03
    Na2O[S1]            1.20070625e-01  1.17716299e-04  1.84018059e-04
    P4O10[S]            1.95149139e-01  1.91322685e-04  6.52958859e-05
    SiO2[S1]            9.10335175e+00  8.92485465e-03  1.43915687e-02
    TiO2[S1]            3.94031481e+02  3.86305374e-01  4.68638424e-01
    V2O5[S]             4.94635301e+00  4.84936570e-03  2.58325918e-03
    ==================================================================


Summary
-------
All the other capabilities of the :py:class:`auxi.modeling.process.materials.thermomaterial.MaterialPackage` class are not demonstrated here, since the purpose of this section is simply to introduce you to the material, material assay and material package concepts in :py:mod:`auxi.modeling.process.materials`. For full details on how to use the different Material and MaterialPackage classes and objects, refer to the following section:

* :ref:`section_chemistry_material_calculations`
* :ref:`section_psd_material_calculations`
* :ref:`section_psd_slurry_material_calculations`
* :ref:`section_thermochemistry_material_calculations`

The final point to make is that the classes in :py:mod:`auxi.modeling.process.materials` can assist you in perming large numbers of metallurgical calculations with very few lines of code. The purpose of this is to focus you on the process concepts rather than entagle you in the detail of tens or hundreds of stoichiometry and thermochemical calculations. This should keep your code clean and your mind clear, getting the job done well in a short space of time.
