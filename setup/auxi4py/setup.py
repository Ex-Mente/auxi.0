# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

from distutils.core import setup

# build the distribution
setup(name="auxi",
      version="0.0.0",
      description="auxi for Python",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core", "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*','*.so.1.54.0*'],
                    'auxi.tools.chemistry': ['*.so*','*.so.1.54.0*', r'data/*'],
                    'auxi' : [r'*.txt', r'doc/*.pdf', r'doc/*', r'doc/_static/*', r'doc/_sources/*']}
      )
