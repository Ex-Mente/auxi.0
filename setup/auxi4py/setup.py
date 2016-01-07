# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

from distutils.core import setup

# build the distribution
setup(name="auxi",
      version="0.0.3",
      description="A toolkit to help metallurgical process engineers to rapidly do day-to-day calculations.",
      long_description="auxi is a toolkit to help metallurgical process engineers with their day-to-day tasks. Many of the calculations that we do require things like molar masses, conversion of one compound to another using stoichiometry, heat transfer calculations, mass balances, energy balances, etc. It is usually quite time consuming to get started with these calculations in a tool like Excel. auxi aims to save you time by making many of these calculations available from within python.\n We hope that auxi will help you spend less time focusing on searching for formulas and data, and setting up calculations, and more on thinking about the problems that you need to solve with these calculations. Enjoy!",
      author="Ex Mente (Pty) Ltd",
      author_email="dev@ex-mente.co.za",
      maintainer="Ex Mente (Pty) Ltd",
      maintainer_email="dev@ex-mente.co.za",
      url="https://github.com/Ex-Mente/auxi.0",
      keywords="metallurgy,chemistry,modelling,simulation,thermochemistry,engineering,mass balance,energy balance",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core", "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*','*.so.1.54.0*'],
                    'auxi.tools.chemistry': ['*.so*','*.so.1.54.0*', r'data/*'],
                    'auxi' : [r'*.txt']}
      )
