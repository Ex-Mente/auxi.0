#!/usr/bin/env python3
"""
This module runs all the tests of the auxi package at once.
"""

import unittest

from auxi.core.object_test import ObjectUnitTester
from auxi.core.namedobject_test import NamedObjectUnitTester

from auxi.tools.chemistry.stoichiometry_test import StoichFunctionTester
from auxi.tools.chemistry.thermochemistry_test import ThermoFunctionTester

from auxi.modeling.process.materials.chem import ChemMaterialUnitTester
#from auxi.modeling.process.materials.chem.materialpackage_test import *
#from auxi.modeling.process.materials.thermo.material_test import *
#from auxi.modeling.process.materials.thermo.materialpackage_test import *
#from auxi.modeling.process.materials.psd.material_test import *
#from auxi.modeling.process.materials.psd.materialpackage_test import *
#from auxi.modeling.process.materials.slurry.material_test import *
#from auxi.modeling.process.materials.slurry.materialpackage_test import *
#
#from auxi.modeling.financial.des.transactiontemplate_test import *
#from auxi.modeling.financial.des.transaction_test import *
#from auxi.modeling.financial.des.generalledgeraccount_test import *
#from auxi.modeling.financial.des.generalledgerstructure_test import *
#from auxi.modeling.financial.des.generalledger_test import *
#from auxi.modeling.financial.des.currency_test import *
#from auxi.modeling.financial.des.currencytable_test import *
#
#from auxi.modeling.financial.tax.rule_test import *
#from auxi.modeling.financial.tax.ruleset_test import *
#from auxi.modeling.financial.tax.salesrule_test import *
#from auxi.modeling.financial.tax.incomerule_test import *
#from auxi.modeling.financial.tax.capitalgainsrule_test import *
#
#from auxi.modeling.business.clock_test import *
#from auxi.modeling.business.activity_test import *
#from auxi.modeling.business.basicactivity_test import *
#from auxi.modeling.business.component_test import *
#from auxi.modeling.business.entity_test import *
#from auxi.modeling.business.timebasedmodel_test import *


__version__ = "0.2.0rc3"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman"
__credits__ = ["Christoff Kok", "Johan Zietsman"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


if __name__ == '__main__':
    unittest.main()
