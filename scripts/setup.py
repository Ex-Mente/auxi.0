# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command

# from distutils.core import setup

from setuptools import setup

# build the distribution
setup(name='auxi',
      version='0.3.0',
      description='A toolkit to help metallurgical process engineers to '
                  'rapidly do day-to-day calculations.',
      long_description=open('README.md').read(),
      author='Ex Mente (Pty) Ltd',
      author_email='dev@ex-mente.co.za',
      maintainer='Ex Mente (Pty) Ltd',
      maintainer_email='dev@ex-mente.co.za',
      url='https://github.com/Ex-Mente/auxi.0',
      download_url='https://pypi.python.org/pypi/auxi',
      license='LGPL v3.0',
      keywords='metallurgy,chemistry,modelling,simulation,thermochemistry,'
               'engineering,mass balance,energy balance',
      platforms='Ubunutu 14.04,Ubuntu 15.04,Windows 7 (For the stoichiometry '
                'and thermochemistry tools only.)',
      package_dir={'auxi': 'src'},
      packages=['auxi',
                'auxi.core',
                'auxi.modelling',
                'auxi.modelling.process',
                'auxi.modelling.process.materials',
                'auxi.modelling.financial',
                'auxi.modelling.business',
                'auxi.tools',
                'auxi.tools.chemistry',
                'auxi.tools.materialphysicalproperties',
                'auxi.tools.transportphenomena',
                'auxi.tools.transportphenomena.heattransfer'],
      package_data={'auxi.tools.chemistry': [r'data/*.json',
                                             r'data/rao/*.json',
                                             r'data/nist/*.json'],
                    'auxi.modelling.process.materials': [r'data/*.txt'],
                    'auxi.tools.materialphysicalproperties': [r'data/*.json',
                                                              r'data/*.csv'],
                    'auxi.examples': [],
                    'auxi': [r'../*.md', r'doc/*.pdf', 'examples/*',
                             'examples/temp', 'examples/data',
                             'examples/modelling/*', 'examples/tools/*',
                             'examples/tools/materialphysicalproperties/*',
                             'examples/tools/transportphenomena/*',
                             'examples/tools/transportphenomena/heattransfer/*'
                             ]},
      install_requires=['jsonpickle', 'tabulate', 'enum34', 'python-dateutil',
                        'cerberus', 'pandas', 'bibtexparser']
      )
