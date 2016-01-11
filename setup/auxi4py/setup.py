# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

from distutils.core import setup

# build the distribution
setup(name="auxi",
      version="0.0.4",
      description="A toolkit to help metallurgical process engineers to rapidly do day-to-day calculations.",
      long_description=open('README.txt').read(),
      author="Ex Mente (Pty) Ltd",
      author_email="dev@ex-mente.co.za",
      maintainer="Ex Mente (Pty) Ltd",
      maintainer_email="dev@ex-mente.co.za",
      url="https://github.com/Ex-Mente/auxi.0",
      download_url="https://pypi.python.org/pypi/auxi",
      license=open('LICENSE.txt').read(),
      keywords="metallurgy,chemistry,modelling,simulation,thermochemistry,engineering,mass balance,energy balance",
      platforms="Ubunutu 14.04,Ubuntu 15.04",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core", "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*','*.so.1.54.0*'],
                    'auxi.tools.chemistry': ['*.so*','*.so.1.54.0*', r'data/*'],
                    'auxi' : [r'*.txt']}
      )
