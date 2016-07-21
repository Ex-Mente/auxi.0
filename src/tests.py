#!/usr/bin/env python3
"""
This module runs all the tests of the auxi package at once.
"""

import unittest

from auxi.core.objects_test import ObjectUnitTester
from auxi.core.objects_test import NamedObjectUnitTester
from auxi.core.time_test import ClockUnitTester

from auxi.tools.chemistry.stoichiometry_test import StoichFunctionTester
from auxi.tools.chemistry.thermochemistry_test import ThermoFunctionTester
from auxi.tools.materialphysicalproperties.core_test import DataSetTester
from auxi.tools.materialphysicalproperties.idealgas_test \
    import BetaTTester, RhoTTester, RhoTPTester, RhoTPxTester
from auxi.tools.materialphysicalproperties.polynomial_test \
    import PolynomialModelTTester
from auxi.tools.transportphenomena.heattransfer.naturalconvection_test \
    import IsothermalFlatSurface_RegionTester, IsothermalFlatSurfaceTester
from auxi.tools.transportphenomena.dimensionlessquantities_test \
    import DimensionlessQiantitiesTester

from auxi.modelling.process.materials.chem_test \
    import ChemMaterialUnitTester, ChemMaterialPackageUnitTester
from auxi.modelling.process.materials.thermo_test \
    import ThermoMaterialUnitTester
# from auxi.modelling.process.materials.thermo_test \
#   import ThermoMaterialPackageUnitTester
from auxi.modelling.process.materials.psd_test \
    import PsdMaterialUnitTester, PsdMaterialPackageUnitTester
from auxi.modelling.process.materials.slurry_test \
    import SlurryMaterialUnitTester, SlurryMaterialPackageUnitTester


# MODELLING.FINANCIAL

from auxi.modelling.financial.des_test import GeneralLedgerAccountUnitTester
from auxi.modelling.financial.des_test import TransactionUnitTester
from auxi.modelling.financial.des_test import TransactionTemplateUnitTester
from auxi.modelling.financial.des_test import GeneralLedgerStructureUnitTester
from auxi.modelling.financial.des_test import GeneralLedgerUnitTester

from auxi.modelling.financial.reporting_test import GeneralLedgerStructureUnitTester
from auxi.modelling.financial.reporting_test import TransactionListUnitTester


# MODELLING.BUSINESS

from auxi.modelling.business.structure_test import ActivityUnitTester
from auxi.modelling.business.structure_test import ComponentUnitTester
from auxi.modelling.business.structure_test import EntityUnitTester

from auxi.modelling.business.basic_test import BasicActivityUnitTester
from auxi.modelling.business.basic_test import BasicLoanActivityUnitTester

from auxi.modelling.business.models_test import TimeBasedModelUnitTester


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


if __name__ == '__main__':
    unittest.main()
