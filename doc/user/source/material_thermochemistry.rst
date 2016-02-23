.. highlight:: python
   :linenothreshold: 5

.. _section_thermochemistry_material_calculations:

thermochemistry material Calculations
*************************************
The purpose of this section is to explain a number of concepts and demonstrate the use of the :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.Material` and :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.MaterialPackage` classes in the :py:mod:`auxi.modelling.process.materials.thermochemistry.material` module.


Material Description Files
==========================
You need to create one or more material description files (MDFs) before you can create a material object in Python. Material description data are stored in simple text files with ".txt" extensions. The most simple format of such a file is the "mix.txt" file shown here:

.. code-block:: none

    Compound
    Al2O3[S1]
    C[S1]
    CaO[S]
    Cr2O3[S]
    Fe2O3[S1]
    Fe3O4[S1]
    FeO[S]
    H2[G]
    K2O[S]
    MgO[S]
    MnO[S]
    Na2O[S1]
    N2[G]
    O2[G]
    P4O10[S]
    S[S1]
    SiO2[S1]
    TiO2[S1]
    V2O5[S]

The file contains a header row, which in this case only contains the word "Compound". All subsequent rows contain chemical compound phases. For example, the second line contains the S1 phase of Al2O3. When you consult FactSage, you will see that S1 refers to the gamma phase. The third line contains the graphite phase of carbon, and so forth. The purpose of this file is to tell :py:mod:`auxi` that materials based on this MDF will contain these compound phases, and nothing else.

Material description files can also contain material assays. The content of the "ilmenite.txt" MDF is shown here:

.. code-block:: none

    Compound   IlmeniteA  IlmeniteB  IlmeniteC
    Al2O3[S1]  0.01160    0.01550    0.00941
    CaO[S]     0.00022    0.00001    0.00017
    Cr2O3[S]   0.00008    0.00022    0.00011
    Fe2O3[S1]  0.20200    0.47300    0.49674
    Fe3O4[S1]  0.00000    0.00000    0.00000
    FeO[S]     0.27900    0.19100    0.00000
    K2O[S]     0.00004    0.00001    0.00005
    MgO[S]     0.01040    0.00580    0.01090
    MnO[S]     0.00540    0.00480    0.00525
    Na2O[S1]   0.00007    0.00005    0.00031
    P4O10[S]   0.00001    0.00032    0.00015
    SiO2[S1]   0.00850    0.00490    0.01744
    TiO2[S1]   0.47700    0.29400    0.45949
    V2O5[S]    0.00360    0.00800    0.00000

The first row still contains the word "Compound" as header for the list of compound phases. The subsequent words in the first row are assay names. **An assay name may not contain space or tab characters.** If it does, it will be interpreted as more than one name.

The first column of the file has the same meaning as the single column in the "mix.txt" file. It is a list of chemical compound phases that are allowed in materials based on this MDF. All subsequent columns contain assay information. Generally the numbers are mass fractions of the different component phases for the respective material assays. If you will be normalising your assays, the numbers can be masses, percentages or mass fractions, since they will be converted to mass fractions by normalisation.

There is more more twist in the MDF tale. You can add your own custom material properties to the file. The "ilmenite.txt" file was modified to include prices for the different ilmenites:

.. code-block:: none

    Compound        IlmeniteA  IlmeniteB  IlmeniteC
    Al2O3[S1]       0.01160    0.01550    0.00941
    CaO[S]          0.00022    0.00001    0.00017
    Cr2O3[S]        0.00008    0.00022    0.00011
    Fe2O3[S1]       0.20200    0.47300    0.49674
    Fe3O4[S1]       0.00000    0.00000    0.00000
    FeO[S]          0.27900    0.19100    0.00000
    K2O[S]          0.00004    0.00001    0.00005
    MgO[S]          0.01040    0.00580    0.01090
    MnO[S]          0.00540    0.00480    0.00525
    Na2O[S1]        0.00007    0.00005    0.00031
    P4O10[S]        0.00001    0.00032    0.00015
    SiO2[S1]        0.00850    0.00490    0.01744
    TiO2[S1]        0.47700    0.29400    0.45949
    V2O5[S]         0.00360    0.00800    0.00000
    #
    Price[USD/ton]  47.5000    32.2300    45.1400

The name of the property in this case is "Price" and its units are "USD/ton". **There may be no spaces in the string containing the property name and units.** In this case the string is "Price[USD/ton]", which serves the purpose of describing the custom property clearly.

**Be careful not to leave empty lines at the end of your material description file.** It tends to cause problems.


Materials
=========
Now that we have created a few material description files, we can create material objects in Python.

::

    from pmpy.materials.thermomaterial import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    print(ilmenite)

    reductant = Material("Reductant", "./materials/reductant.txt")
    print(reductant)

    mix = Material("Mix", "./materials/mix.txt")
    print(mix)

The :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.Material` class is imported on line 1. On line 3 a :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.Material` object is created, specifying the name of the object as the first parameter, and the location and name of the material description file as the second parameter. Two more :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.Material` objects are created on lines 6 and 9. The materials are preted out after creation, with the following result:

.. code-block:: none

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
    --------------------------------------------------------------------
    Custom Properties:
    --------------------------------------------------------------------
    Price[USD/ton]      4.75000000e+01   3.22300000e+01   4.51400000e+01
    ====================================================================

    ===================================================
    Material
    ===================================================
    Name                Reductant
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

    =======================
    Material
    =======================
    Name                Mix
    -----------------------
    Compound
    -----------------------
    Al2O3[S1]
    C[S1]
    CaO[S]
    Cr2O3[S]
    Fe2O3[S1]
    Fe3O4[S1]
    FeO[S]
    H2[G]
    K2O[S]
    MgO[S]
    MnO[S]
    Na2O[S1]
    N2[G]
    O2[G]
    P4O10[S]
    S[S1]
    SiO2[S1]
    TiO2[S1]
    V2O5[S]
    =======================

The material objects are now ready to create material packages.


Material Packages
=================

Creating Empty Packages
-----------------------
The simplest way to create material packages is to create empty ones.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    empty_ilmenite_package = ilmenite.create_package()
    print(empty_ilmenite_package)

    empty_reductant_package = reductant.create_package()
    print(empty_reductant_package)

    empty_mix_package = mix.create_package()
    print(empty_mix_package)

The empty packages are created by calling the "create_package" method of the :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.Material` objects without passing any parameters.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 0.00000000e+00 kg
    Amount               0.00000000e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy             0.00000000e+00 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Cr2O3[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    K2O[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MnO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Na2O[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    P4O10[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    TiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    V2O5[S]             0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Reductant
    Mass                 0.00000000e+00 kg
    Amount               0.00000000e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy             0.00000000e+00 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    C[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    H2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    O2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    N2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    S[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Mix
    Mass                 0.00000000e+00 kg
    Amount               0.00000000e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy             0.00000000e+00 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    C[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Cr2O3[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    H2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    K2O[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MnO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Na2O[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    N2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    O2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    P4O10[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    S[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    TiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    V2O5[S]             0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================


Creating Filled Packages
------------------------
It is just as easy to create packages that contain some mass. Let's do that with ilmenite.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    print(ilma_package)

The parameters to the "create_package" method are:

1. material assay name, "IlmeniteA"
2. mass, 300 kg
3. pressure, 1 atm
4. temperature, 25 °C

We therefore created 300 kg based on the composition specified by the IlmeniteA assay, at 1 atm pressure and 25 °C temperature. The resulting package is shown here.

.. code-block:: none

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


Adding Material to a Package - Another Package
==============================================
Now we create another ilmenite package with a different composition, mass and temperature, and add it to the first:

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    ilmb_package = ilmenite.create_package("IlmeniteB", 500.0, 1.0, 750.0)

    ilma_package += ilmb_package
    print(ilma_package)
    print(ilmb_package)

This changes the original "ilma_package", but the second "ilmb_package" remains the same. This is quite a powerful action, since one line of code does all of the following:

* Calculate the total mass of each component by adding up the component masses from the two packages.
* Calculate the mass fraction of each compound.
* Calculate the mole fraction of each compound.
* Calculate the total amount (in kmol) of compounds in the package.
* Calculate the total enthalpy by adding up the enthalpies of the two original packages.
* Calculate the temperature of the new package.

The resulting two packages are shown below:

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 8.00000000e+02 kg
    Amount               8.43715862e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          4.88474167e+02 °C
    Enthalpy            -1.59326344e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           1.12558204e+01  1.40697755e-02  1.30841549e-02
    CaO[S]              7.11495448e-02  8.89369310e-05  1.50379294e-04
    Cr2O3[S]            1.34313554e-01  1.67891942e-04  1.04738770e-04
    Fe2O3[S1]           2.97792900e+02  3.72241125e-01  2.21026985e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.79603251e+02  2.24504063e-01  2.96295501e-01
    K2O[S]              1.70369907e-02  2.12962383e-05  2.14370100e-05
    MgO[S]              6.03345073e+00  7.54181341e-03  1.77425932e-02
    MnO[S]              4.02912637e+00  5.03640796e-03  6.73192250e-03
    Na2O[S1]            4.61036642e-02  5.76295802e-05  8.81647712e-05
    P4O10[S]            1.63389569e-01  2.04236961e-04  6.82149359e-05
    SiO2[S1]            5.01118458e+00  6.26398073e-03  9.88514810e-03
    TiO2[S1]            2.90750440e+02  3.63438050e-01  4.31482633e-01
    V2O5[S]             5.09183399e+00  6.36479248e-03  3.31812755e-03
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


Adding Material to a Package - A Compound Mass
==============================================
Sometimes you need to add material to a package, one compound at a time.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    ilma_package += ("TiO2[S1]", 150.0)
    print(ilma_package)

This adds 150 kg of TiO2[S1] to ilma_package. The temperature of the added material is assumed to be the same as that of the original package, which means that ilma_package's temperature does not change. Here is the result:

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 4.50000000e+02 kg
    Amount               5.40632064e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -1.18069622e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  7.74945219e-03  6.32625154e-03
    CaO[S]              6.61375661e-02  1.46972369e-04  2.18151669e-04
    Cr2O3[S]            2.40500241e-02  5.34444979e-05  2.92683040e-05
    Fe2O3[S1]           6.07263107e+01  1.34947357e-01  7.03399852e-02
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  1.86387686e-01  2.15940951e-01
    K2O[S]              1.20250120e-02  2.67222489e-05  2.36130050e-05
    MgO[S]              3.12650313e+00  6.94778473e-03  1.43484374e-02
    MnO[S]              1.62337662e+00  3.60750361e-03  4.23293814e-03
    Na2O[S1]            2.10437710e-02  4.67639357e-05  6.28026001e-05
    P4O10[S]            3.00625301e-03  6.68056224e-06  1.95873232e-06
    SiO2[S1]            2.55531506e+00  5.67847790e-03  7.86650184e-03
    TiO2[S1]            2.93398268e+02  6.51996152e-01  6.79508511e-01
    V2O5[S]             1.08225108e+00  2.40500241e-03  1.10062984e-03
    ==================================================================


Adding Material to a Package - A Compound Mass with Specified Temperature
=========================================================================
We can also add a certain mass of a specified compound at a temperature different from the original package.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    ilma_package += ("TiO2[S1]", 150.0, 1000.0)
    print(ilma_package)

This action calculates a new total mass, component masses, mass fractions and mole fractions, as well as a new enthalpy and temperature.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 4.50000000e+02 kg
    Amount               5.40632064e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          3.84927151e+02 °C
    Enthalpy            -1.14449836e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  7.74945219e-03  6.32625154e-03
    CaO[S]              6.61375661e-02  1.46972369e-04  2.18151669e-04
    Cr2O3[S]            2.40500241e-02  5.34444979e-05  2.92683040e-05
    Fe2O3[S1]           6.07263107e+01  1.34947357e-01  7.03399852e-02
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  1.86387686e-01  2.15940951e-01
    K2O[S]              1.20250120e-02  2.67222489e-05  2.36130050e-05
    MgO[S]              3.12650313e+00  6.94778473e-03  1.43484374e-02
    MnO[S]              1.62337662e+00  3.60750361e-03  4.23293814e-03
    Na2O[S1]            2.10437710e-02  4.67639357e-05  6.28026001e-05
    P4O10[S]            3.00625301e-03  6.68056224e-06  1.95873232e-06
    SiO2[S1]            2.55531506e+00  5.67847790e-03  7.86650184e-03
    TiO2[S1]            2.93398268e+02  6.51996152e-01  6.79508511e-01
    V2O5[S]             1.08225108e+00  2.40500241e-03  1.10062984e-03
    ==================================================================


Adding Packages of Different Materials Together
===============================================
We very often need to add packages from different materials together. For example, ilmenite and reductant can be added together so that reduction reactions can be modelled.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    reda_package = reductant.create_package("ReductantA", 35.0, 1.0, 25.0)

    new_package = ilma_package + reda_package
    print(new_package)

This, however, does not work. See the last two lines of the error message below.

.. code-block:: none

    Traceback (most recent call last):
    File "test.py", line 10, in <module>
        new_package = ilma_package + reda_package
    File "thermochemistry.material.py", line 430, in __add__
        self.material.name + "'.")
    Exception: Packages of 'Reductant' cannot be added to packages of 'Ilmenite'.
        The compound 'C[S1]' was not found in 'Ilmenite'.

Let's try it by swopping the two material packages around.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    reda_package = reductant.create_package("ReductantA", 35.0, 1.0, 25.0)

    new_package = reda_package + ilma_package
    print(new_package)


.. code-block:: none

    Traceback (most recent call last):
    File "test.py", line 10, in <module>
        new_package = reda_package + ilma_package
    File "thermochemistry.material.py", line 430, in __add__
        self.material.name + "'.")
    Exception: Packages of 'Ilmenite' cannot be added to packages of 'Reductant'.
        The compound 'Cr2O3[S]' was not found in 'Reductant'.

Still no luck. These packages cannot be added together because their materials are not compatible. We need to use an intermediate material package from a compatible material that will allow us to add ilmenite and reductant together. This is the purpose of the "mix" material that we created early on.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    reda_package = reductant.create_package("ReductantA", 35.0, 1.0, 25.0)

    new_package = mix.create_package()
    new_package += ilma_package
    new_package += reda_package
    print(new_package)

Success at last! The mix material package is able to receive all the compound masses from both the ilmenite and reductant packages.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Mix
    Mass                 3.35000000e+02 kg
    Amount               6.30500835e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -6.92925041e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.52956294e+00  1.05360088e-02  5.49034965e-03
    C[S1]               2.94340853e+01  8.78629412e-02  3.88683906e-01
    CaO[S]              1.69100559e-01  5.04777788e-04  4.78268203e-04
    Cr2O3[S]            2.40500241e-02  7.17911166e-05  2.50965308e-05
    Fe2O3[S1]           6.34771555e+01  1.89484046e-01  6.30462073e-02
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  2.50371519e-01  1.85161693e-01
    H2[G]               4.82843151e-01  1.44132284e-03  3.79888138e-02
    K2O[S]              1.20250120e-02  3.58955583e-05  2.02473128e-05
    MgO[S]              3.17591590e+00  9.48034598e-03  1.24977222e-02
    MnO[S]              1.62337662e+00  4.84590037e-03  3.62959406e-03
    Na2O[S1]            2.10437710e-02  6.28172270e-05  5.38509982e-05
    N2[G]               2.13430742e-01  6.37106693e-04  1.20838199e-03
    O2[G]               1.73018862e+00  5.16474215e-03  8.57578913e-03
    P4O10[S]            3.00625301e-03  8.97388957e-06  1.67954337e-06
    S[S1]               7.17266865e-02  2.14109512e-04  3.54772799e-04
    SiO2[S1]            2.67751054e+00  7.99256877e-03  7.06780432e-03
    TiO2[S1]            1.43398268e+02  4.28054533e-01  2.84772072e-01
    V2O5[S]             1.08225108e+00  3.23060025e-03  9.43750984e-04
    ==================================================================


Adding Material Together - Package + Package
============================================
In the above three sections we demonstrated how material can be added to an existing package. Here we will add material together to create a new package.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)
    ilmb_package = ilmenite.create_package("IlmeniteB", 500.0, 1.0, 750.0)

    new_package = ilma_package + ilmb_package
    print(new_package)

This action performs all the calculations to create a new package with properties based on the two original packages. Specifically note that the temperature was automatically calculated.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 8.00000000e+02 kg
    Amount               8.43715862e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          4.88474167e+02 °C
    Enthalpy            -1.59326344e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           1.12558204e+01  1.40697755e-02  1.30841549e-02
    CaO[S]              7.11495448e-02  8.89369310e-05  1.50379294e-04
    Cr2O3[S]            1.34313554e-01  1.67891942e-04  1.04738770e-04
    Fe2O3[S1]           2.97792900e+02  3.72241125e-01  2.21026985e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.79603251e+02  2.24504063e-01  2.96295501e-01
    K2O[S]              1.70369907e-02  2.12962383e-05  2.14370100e-05
    MgO[S]              6.03345073e+00  7.54181341e-03  1.77425932e-02
    MnO[S]              4.02912637e+00  5.03640796e-03  6.73192250e-03
    Na2O[S1]            4.61036642e-02  5.76295802e-05  8.81647712e-05
    P4O10[S]            1.63389569e-01  2.04236961e-04  6.82149359e-05
    SiO2[S1]            5.01118458e+00  6.26398073e-03  9.88514810e-03
    TiO2[S1]            2.90750440e+02  3.63438050e-01  4.31482633e-01
    V2O5[S]             5.09183399e+00  6.36479248e-03  3.31812755e-03
    ==================================================================




Adding Material Together - Package + Compound Mass
==================================================
Now we add a package and specific mass of a compound together to produce a new package.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package + ("TiO2[S1]", 150.0)
    print(new_package)

The added compound mass is assumed to be at the same temperature as the original package. This results in the new package having the same temperature as the original package.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 4.50000000e+02 kg
    Amount               5.40632064e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -1.18069622e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  7.74945219e-03  6.32625154e-03
    CaO[S]              6.61375661e-02  1.46972369e-04  2.18151669e-04
    Cr2O3[S]            2.40500241e-02  5.34444979e-05  2.92683040e-05
    Fe2O3[S1]           6.07263107e+01  1.34947357e-01  7.03399852e-02
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  1.86387686e-01  2.15940951e-01
    K2O[S]              1.20250120e-02  2.67222489e-05  2.36130050e-05
    MgO[S]              3.12650313e+00  6.94778473e-03  1.43484374e-02
    MnO[S]              1.62337662e+00  3.60750361e-03  4.23293814e-03
    Na2O[S1]            2.10437710e-02  4.67639357e-05  6.28026001e-05
    P4O10[S]            3.00625301e-03  6.68056224e-06  1.95873232e-06
    SiO2[S1]            2.55531506e+00  5.67847790e-03  7.86650184e-03
    TiO2[S1]            2.93398268e+02  6.51996152e-01  6.79508511e-01
    V2O5[S]             1.08225108e+00  2.40500241e-03  1.10062984e-03
    ==================================================================


Adding Material Together - Package + Compound Mass at Specified Temperature
===========================================================================
Now we add the same compound mass as in the previous section, but at a different temperature.

::

    from auxi.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package + ("TiO2[S1]", 150.0, 1000.0)
    print(new_package)

The new package now has a different temperature, which is calculated based on the enthalpy of the original package and the enthalpy of the added compound mass.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 4.50000000e+02 kg
    Amount               5.40632064e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          3.84927151e+02 °C
    Enthalpy            -1.14449836e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  7.74945219e-03  6.32625154e-03
    CaO[S]              6.61375661e-02  1.46972369e-04  2.18151669e-04
    Cr2O3[S]            2.40500241e-02  5.34444979e-05  2.92683040e-05
    Fe2O3[S1]           6.07263107e+01  1.34947357e-01  7.03399852e-02
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  1.86387686e-01  2.15940951e-01
    K2O[S]              1.20250120e-02  2.67222489e-05  2.36130050e-05
    MgO[S]              3.12650313e+00  6.94778473e-03  1.43484374e-02
    MnO[S]              1.62337662e+00  3.60750361e-03  4.23293814e-03
    Na2O[S1]            2.10437710e-02  4.67639357e-05  6.28026001e-05
    P4O10[S]            3.00625301e-03  6.68056224e-06  1.95873232e-06
    SiO2[S1]            2.55531506e+00  5.67847790e-03  7.86650184e-03
    TiO2[S1]            2.93398268e+02  6.51996152e-01  6.79508511e-01
    V2O5[S]             1.08225108e+00  2.40500241e-03  1.10062984e-03
    ==================================================================


Extract Material from a Package - Mass
======================================
When we need to create a new package by extracting material from an existing material, we use the "extract" method. First of all we can simply specify the total mass to be extracted.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package.extract(75.0)
    print(ilma_package)
    print(new_package)

This removes 75 kg from the original package, and produces a new package of 75 kg. The new package has the same composition, temperature and pressure as the original one.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 2.25000000e+02 kg
    Amount               2.64612753e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -5.15859089e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           2.61544012e+00  1.16241783e-02  9.69390473e-03
    CaO[S]              4.96031746e-02  2.20458554e-04  3.34280337e-04
    Cr2O3[S]            1.80375180e-02  8.01667468e-05  4.48486990e-05
    Fe2O3[S1]           4.55447330e+01  2.02421036e-01  1.07784066e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              6.29058442e+01  2.79581530e-01  3.30892788e-01
    K2O[S]              9.01875902e-03  4.00833734e-05  3.61829148e-05
    MgO[S]              2.34487734e+00  1.04216771e-02  2.19865404e-02
    MnO[S]              1.21753247e+00  5.41125541e-03  6.48625791e-03
    Na2O[S1]            1.57828283e-02  7.01459035e-05  9.62343053e-05
    P4O10[S]            2.25468975e-03  1.00208434e-05  3.00142421e-06
    SiO2[S1]            1.91648629e+00  8.51771685e-03  1.20540764e-02
    TiO2[S1]            1.07548701e+02  4.77994228e-01  5.08901291e-01
    V2O5[S]             8.11688312e-01  3.60750361e-03  1.68652807e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 7.50000000e+01 kg
    Amount               8.82042511e-01 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -1.71953030e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           8.71813372e-01  1.16241783e-02  9.69390473e-03
    CaO[S]              1.65343915e-02  2.20458554e-04  3.34280337e-04
    Cr2O3[S]            6.01250601e-03  8.01667468e-05  4.48486990e-05
    Fe2O3[S1]           1.51815777e+01  2.02421036e-01  1.07784066e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              2.09686147e+01  2.79581530e-01  3.30892788e-01
    K2O[S]              3.00625301e-03  4.00833734e-05  3.61829148e-05
    MgO[S]              7.81625782e-01  1.04216771e-02  2.19865404e-02
    MnO[S]              4.05844156e-01  5.41125541e-03  6.48625791e-03
    Na2O[S1]            5.26094276e-03  7.01459035e-05  9.62343053e-05
    P4O10[S]            7.51563252e-04  1.00208434e-05  3.00142421e-06
    SiO2[S1]            6.38828764e-01  8.51771685e-03  1.20540764e-02
    TiO2[S1]            3.58495671e+01  4.77994228e-01  5.08901291e-01
    V2O5[S]             2.70562771e-01  3.60750361e-03  1.68652807e-03
    ==================================================================


Extract Material from a Package - Compound
==========================================
We can also extract all the mass of a single compound from an existing package into a new one.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package.extract("TiO2[S1]")
    print(ilma_package)
    print(new_package)

This modifies the original package's composition and enthalpy, and creates a new package of the same temperature consisting purely of the specified compound.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.56601732e+02 kg
    Amount               1.73267975e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -2.16620609e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  2.22682946e-02  1.97392185e-02
    CaO[S]              6.61375661e-02  4.22329724e-04  6.80678509e-04
    Cr2O3[S]            2.40500241e-02  1.53574445e-04  9.13231864e-05
    Fe2O3[S1]           6.07263107e+01  3.87775474e-01  2.19475361e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  5.35590878e-01  6.73780610e-01
    K2O[S]              1.20250120e-02  7.67872226e-05  7.36774791e-05
    MgO[S]              3.12650313e+00  1.99646779e-02  4.47701043e-02
    MnO[S]              1.62337662e+00  1.03662751e-02  1.32076460e-02
    Na2O[S1]            2.10437710e-02  1.34377640e-04  1.95957154e-04
    P4O10[S]            3.00625301e-03  1.91968057e-05  6.11165160e-06
    SiO2[S1]            2.55531506e+00  1.63172848e-02  2.45451193e-02
    TiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    V2O5[S]             1.08225108e+00  6.91085003e-03  3.43419366e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.43398268e+02 kg
    Amount               1.79549029e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -4.71191509e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Cr2O3[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    K2O[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MnO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Na2O[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    P4O10[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    TiO2[S1]            1.43398268e+02  1.00000000e+00  1.00000000e+00
    V2O5[S]             0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================


Extract Material from a Package - Compound Mass
===============================================
We may not want to extract all the mass of a specific compound. In this case we can specify the mass to extract.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package.extract(("TiO2[S1]", 110.0))
    print(ilma_package)
    print(new_package)

The existing package is modified appropriately and a new package containing only the specified mass of the required compound is produced.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.90000000e+02 kg
    Amount               2.15085961e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -3.26363778e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           3.48725349e+00  1.83539657e-02  1.59014304e-02
    CaO[S]              6.61375661e-02  3.48092453e-04  5.48337915e-04
    Cr2O3[S]            2.40500241e-02  1.26579074e-04  7.35677195e-05
    Fe2O3[S1]           6.07263107e+01  3.19612162e-01  1.76803968e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  4.41444520e-01  5.42781136e-01
    K2O[S]              1.20250120e-02  6.32895370e-05  5.93527704e-05
    MgO[S]              3.12650313e+00  1.64552796e-02  3.60656982e-02
    MnO[S]              1.62337662e+00  8.54408749e-03  1.06397557e-02
    Na2O[S1]            2.10437710e-02  1.10756690e-04  1.57858278e-04
    P4O10[S]            3.00625301e-03  1.58223842e-05  4.92339666e-06
    SiO2[S1]            2.55531506e+00  1.34490266e-02  1.97729462e-02
    TiO2[S1]            3.33982684e+01  1.75780360e-01  1.94424522e-01
    V2O5[S]             1.08225108e+00  5.69605833e-03  2.76650220e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 1.10000000e+02 kg
    Amount               1.37731044e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -3.61448340e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Cr2O3[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    K2O[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MnO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Na2O[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    P4O10[S]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    TiO2[S1]            1.10000000e+02  1.00000000e+00  1.00000000e+00
    V2O5[S]             0.00000000e+00  0.00000000e+00  0.00000000e+00
    ==================================================================


Extract Material from a Package - Material
==========================================
We may need to extract all the compounds that appear in a specific material into a new package.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    new_package = ilma_package.extract(reductant)
    print(ilma_package)
    print(new_package)

The existing package loses all the masses of components that appear in the specified material. The new package contains these masses and have the same temperature and pressure as the original material.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 2.30038480e+02 kg
    Amount               2.99240730e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -5.62518853e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    CaO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    Cr2O3[S]            2.40500241e-02  1.04547831e-04  5.28784420e-05
    Fe2O3[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              8.38744589e+01  3.64610559e-01  3.90136068e-01
    K2O[S]              1.20250120e-02  5.22739153e-05  4.26611298e-05
    MgO[S]              0.00000000e+00  0.00000000e+00  0.00000000e+00
    MnO[S]              1.62337662e+00  7.05697857e-03  7.64756215e-03
    Na2O[S1]            2.10437710e-02  9.14793518e-05  1.13464164e-04
    P4O10[S]            3.00625301e-03  1.30684788e-05  3.53880134e-06
    SiO2[S1]            0.00000000e+00  0.00000000e+00  0.00000000e+00
    TiO2[S1]            1.43398268e+02  6.23366440e-01  6.00015342e-01
    V2O5[S]             1.08225108e+00  4.70465238e-03  1.98848527e-03
    ==================================================================

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Reductant
    Mass                 6.99615200e+01 kg
    Amount               5.35762740e-01 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -1.25293265e+02 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    C[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    H2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    O2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    N2[G]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    S[S1]               0.00000000e+00  0.00000000e+00  0.00000000e+00
    Al2O3[S1]           3.48725349e+00  4.98453077e-02  6.38374820e-02
    CaO[S]              6.61375661e-02  9.45342042e-04  2.20134358e-03
    Fe2O3[S1]           6.07263107e+01  8.67995875e-01  7.09792759e-01
    MgO[S]              3.12650313e+00  4.46888965e-02  1.44788444e-01
    SiO2[S1]            2.55531506e+00  3.65245789e-02  7.93799718e-02
    ==================================================================


Multiplying a Package by a Scalar
=================================
It may sometimes be useful to multiply a package by a scalar.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    ilma_package *= 2.0
    print(ilma_package)

This doubles the package mass and enthalpy. Temperature, pressure and composition remain the same, since these are intensive properties.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 6.00000000e+02 kg
    Amount               7.05634009e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          2.50000000e+01 °C
    Enthalpy            -1.37562424e+03 kWh
    ------------------------------------------------------------------
    Compound Details
    Formula             Mass            Mass Fraction   Mole Fraction
    ------------------------------------------------------------------
    Al2O3[S1]           6.97450697e+00  1.16241783e-02  9.69390473e-03
    CaO[S]              1.32275132e-01  2.20458554e-04  3.34280337e-04
    Cr2O3[S]            4.81000481e-02  8.01667468e-05  4.48486990e-05
    Fe2O3[S1]           1.21452621e+02  2.02421036e-01  1.07784066e-01
    Fe3O4[S1]           0.00000000e+00  0.00000000e+00  0.00000000e+00
    FeO[S]              1.67748918e+02  2.79581530e-01  3.30892788e-01
    K2O[S]              2.40500241e-02  4.00833734e-05  3.61829148e-05
    MgO[S]              6.25300625e+00  1.04216771e-02  2.19865404e-02
    MnO[S]              3.24675325e+00  5.41125541e-03  6.48625791e-03
    Na2O[S1]            4.20875421e-02  7.01459035e-05  9.62343053e-05
    P4O10[S]            6.01250601e-03  1.00208434e-05  3.00142421e-06
    SiO2[S1]            5.11063011e+00  8.51771685e-03  1.20540764e-02
    TiO2[S1]            2.86796537e+02  4.77994228e-01  5.08901291e-01
    V2O5[S]             2.16450216e+00  3.60750361e-03  1.68652807e-03
    ==================================================================


Setting Package Temperature
===========================
Using the "T" property of a :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.MaterialPackage` object, it is easy to set the temperature of a package to a new value.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    ilma_package.T = 1000.0
    print(ilma_package)

This results in the temperature to be updated, as well as the package's enthalpy.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 3.00000000e+02 kg
    Amount               3.52817004e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          1.00000000e+03 °C
    Enthalpy            -6.18986580e+02 kWh
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


Setting Package Enthalpy
========================
We can use the "H" property of a :py:class:`~.auxi.modelling.process.materials.thermochemistry.material.MaterialPackage` object to add or subtract enthalpy, or to set it to a new value. This is very useful when building an energy balance.

::

    from auxi.modelling.process.materials.thermochemistry.material import Material

    ilmenite = Material("Ilmenite", "./materials/ilmenite.txt")
    reductant = Material("Reductant", "./materials/reductant.txt")
    mix = Material("Mix", "./materials/mix.txt")

    ilma_package = ilmenite.create_package("IlmeniteA", 300.0, 1.0, 25.0)

    ilma_package.H = ilma_package.H + 1.0
    print(ilma_package)

This updates the package's enthalpy and automatically re-calculates its temperature.

.. code-block:: none

    ==================================================================
    MaterialPackage
    ==================================================================
    Material            Ilmenite
    Mass                 3.00000000e+02 kg
    Amount               3.52817004e+00 kmol
    Pressure             1.00000000e+00 atm
    Temperature          4.22166385e+01 °C
    Enthalpy            -6.86812118e+02 kWh
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
