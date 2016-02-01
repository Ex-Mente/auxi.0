auxi Installation
=================
Currently, auxi only runs on Linux.

Prerequisites
-------------
You need the following before starting your auxi Python package installation:

* Python 3.4
* pip3

  * sudo apt-get update
  * sudo apt-get install -y python3-pip

* tabulate

  * sudo pip3 install tabulate

Installation
------------

To install auxi::

  sudo pip3 install auxi

To uninstall auxi::

  sudo pip3 uninstall auxi


Importing auxi Components
==========================
If you want to use auxi in one of your python modules, you need to import its components in the same way that you do for any other python package. For example, to use the stoichiometry tool, you will have to do the following::

  from auxi.tools.chemistry import stoichiometry

The same method is used for all modules, functions and classes in auxi4py. Here are a few more import examples::

  from auxi.tools.chemistry.stoichiometry import molar_mass
  from auxi.tools.chemistry.stoichiometry import molar_mass as mm
  from auxi.tools.chemistry.stoichiometry import convert_compound
  from auxi.tools.chemistry.stoichiometry import convert_compound as cc

  from auxi.tools.chemistry import thermochemistry
  from auxi.tools.chemistry.thermochemistry import Compound

Getting Help
============
You can use Python's standard help function on any of auxi's components. For example::

  import auxi
  help(auxi)

  from auxi.tools.chemistry import stoichiometry

  help(stoichiometry)
  help(stoichiometry.molar_mass)
  help(stoichiometry.convert_compound)

All the help information that you are able to access in this way are also available through auxi's HTML documentation that is included in the auxi Python package distribution.
