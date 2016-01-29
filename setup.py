# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

from distutils.core import setup

# build the distribution
setup(name="auxi",
      version="0.2.0rc1",
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
      package_dir={'auxi': 'src'},
      packages=["auxi",
                "auxi.core",
                "auxi.modeling",
                "auxi.modeling.process",
                "auxi.modeling.process.materials",
                "auxi.modeling.process.materials.chemistry",
                "auxi.modeling.process.materials.psd",
                "auxi.modeling.process.materials.thermochemistry",
                "auxi.tools",
                "auxi.tools.chemistry"],
      package_data={'auxi.tools.chemistry': [r'data/thermo/*.txt'],
                    'auxi': [r'*.txt']}
      )
