.. auxi documentation master file, created by
   sphinx-quickstart on Tue May 12 07:52:59 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to auxi' user manual!
*****************************

Introduction
============
auxi is a toolkit to help metallurgical process engineers with their day-to-day tasks. Many of the calculations that we do require things like molar masses, conversion of one compound to another using stoichiometry, heat transfer calculations, mass balances, energy balances, etc. It is usually quite time consuming to get started with these calculations in a tool like Excel. auxi aims to save you time by making many of these calculations available from within python.

We hope that auxi will help you spend less time focusing on searching for formulas and data, and setting up calculations, and more on thinking about the problems that you need to solve with these calculations. Enjoy!

For video tutorials on using auxi visit `auxi youtube <https://www.youtube.com/channel/UCdklSCJ8S9wFyayLAO7iINQ>`_ .


Getting Started
===============

.. toctree::
   :maxdepth: 2

   gettingstarted


Structure
=========
auxi is a python package that packages modules containing functions and classes that the engineers will ultimately use to help with their day-to-day tasks.
auxi consists of python packages that are divided into two packages, the modelling framework package and the tools package.


Modelling Frameworks
--------------------
This package contains modules, functions and classes for developing different types of computational models.

.. toctree::
   :maxdepth: 1

   process_modelling
   business_modelling

Tools
-----
This package contains modules, functions and classes used to provide tools to aid the engineer with calculations.

.. toctree::
   :maxdepth: 1

   chemistry_tools


auxi Reference
==============

.. toctree::
    :maxdepth: 1

   auxi_api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`