# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# NOTE: setup.py MUST exist in the `root` directory, not in the `script`
#   directory. readthedocs.org expects it to be in the root directory.

from setuptools import setup


# build the distribution
setup(name='auxi',
      version='0.3.6',
      description='A toolkit to help metallurgical process engineers to '
                  'rapidly do day-to-day calculations.',
      long_description=open('README.rst').read(),
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
      package_dir={'auxi': 'auxi'},
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
                    'auxi': [r'../*.md', r'doc/*.pdf',
                             'examples/*.ipynb', 'examples/*.py',
                             'examples/readme',
                             'examples/temp/*.csv',
                             'examples/modelling/readme',
                             'examples/tools/readme',
                             'examples/tools/materialphysicalproperties/*.ipynb',
                             'examples/tools/materialphysicalproperties/data/readme',
                             'examples/tools/transportphenomena/heattransfer/*.ipynb'
                             ]},
      install_requires=['jsonpickle', 'tabulate', 'python-dateutil',
                        'cerberus<=0.9.2', 'pandas', 'bibtexparser', 'parsimonious'],
      test_suite='auxi.tests'
      )
