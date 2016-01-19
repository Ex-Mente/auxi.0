# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

from distutils.core import setup

# build the distribution
setup(name="auxi",
      version="0.1.0rc14",
      description="A toolkit to help metallurgical process engineers to rapidly do day-to-day calculations.",
      long_description=open('README.txt').read(),
      author="Ex Mente (Pty) Ltd",
      author_email="dev@ex-mente.co.za",
      maintainer="Ex Mente (Pty) Ltd",
      maintainer_email="dev@ex-mente.co.za",
      url="https://github.com/Ex-Mente/auxi.0",
      download_url="https://pypi.python.org/pypi/auxi",
      license='LICENSE.txt',
      keywords="metallurgy,chemistry,modelling,simulation,thermochemistry,engineering,mass balance,energy balance",
      platforms="Ubunutu 14.04,Ubuntu 15.04,Windows 7 (For the stoichiometry and thermochemistry tools only.)",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core",
                "auxi.modelling", "auxi.modelling.financial", "auxi.simulation",
                "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*','*.so.1.54.0*', '*.a', '*.dll', '*.pyd'],
                    'auxi.modelling.financial': ['*.a', '*.so*', '*.dll', '*.pyd', '*_report.py'],
                    'auxi.modelling': ['*.a', '*.so*', '*.dll', '*.pyd', '*_report.py'],
                    'auxi.simulation': ['*.py', r'io/*'],
                    'auxi.tools.chemistry': ['*.so*', '*.a', '*.dll', '*.pyd','*.so.1.54.0*', r'data/*'],
                    'auxi' : [r'*.txt']}
      )
