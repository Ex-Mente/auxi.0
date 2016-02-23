#!/usr/bin/env python3
"""
This module runs all the tests of the auxi package at once.
"""

import unittest

from auxi.core.objects_test import ObjectUnitTester
from auxi.core.objects_test import NamedObjectUnitTester

from auxi.tools.chemistry.stoichiometry_test import StoichFunctionTester
#from auxi.tools.chemistry.thermochemistry_test import ThermoFunctionTester

from auxi.modelling.process.materials.chem_test import ChemMaterialUnitTester
from auxi.modelling.process.materials.chem_test import ChemMaterialPackageUnitTester
#from auxi.modelling.process.materials.thermo_test import ThermoMaterialUnitTester
#from auxi.modelling.process.materials.thermo_test import ThermoMaterialPackageUnitTester
from auxi.modelling.process.materials.psd_test import PsdMaterialUnitTester
from auxi.modelling.process.materials.psd_test import PsdMaterialPackageUnitTester
from auxi.modelling.process.materials.slurry_test import SlurryMaterialUnitTester
from auxi.modelling.process.materials.slurry_test import SlurryMaterialPackageUnitTester
#
#from auxi.modelling.financial.des.transactiontemplate_test import *
#from auxi.modelling.financial.des.transaction_test import *
#from auxi.modelling.financial.des.generalledgeraccount_test import *
#from auxi.modelling.financial.des.generalledgerstructure_test import *
#from auxi.modelling.financial.des.generalledger_test import *
#from auxi.modelling.financial.des.currency_test import *
#from auxi.modelling.financial.des.currencytable_test import *
#
#from auxi.modelling.financial.tax.rule_test import *
#from auxi.modelling.financial.tax.ruleset_test import *
#from auxi.modelling.financial.tax.salesrule_test import *
#from auxi.modelling.financial.tax.incomerule_test import *
#from auxi.modelling.financial.tax.capitalgainsrule_test import *
#
#from auxi.modelling.business.clock_test import *
#from auxi.modelling.business.activity_test import *
#from auxi.modelling.business.basicactivity_test import *
#from auxi.modelling.business.component_test import *
#from auxi.modelling.business.entity_test import *
#from auxi.modelling.business.timebasedmodel_test import *


__version__ = "0.2.0rc4"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman"
__credits__ = ["Christoff Kok", "Johan Zietsman"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


if __name__ == '__main__':
    unittest.main()
