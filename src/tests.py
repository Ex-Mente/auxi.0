#!/usr/bin/env python3
"""
This module runs all the tests of the auxi package at once.
"""

import unittest

import auxi.core.object_test
import auxi.core.namedobject_test

import auxi.tools.chemistry.stoichiometry_test
import auxi.tools.chemistry.thermochemistry_test

import auxi.modeling.financial.des.transactiontemplate_test
import auxi.modeling.financial.des.transaction_test
import auxi.modeling.financial.des.generalledgeraccount_test
import auxi.modeling.financial.des.generalledgerstructure_test
import auxi.modeling.financial.des.generalledger_test
import auxi.modeling.financial.des.currency_test
import auxi.modeling.financial.des.currencytable_test

import auxi.modeling.financial.tax.rule_test
import auxi.modeling.financial.tax.ruleset_test
import auxi.modeling.financial.tax.salesrule_test
import auxi.modeling.financial.tax.incomerule_test
import auxi.modeling.financial.tax.capitalgainsrule_test

import auxi.modeling.business.clock_test
import auxi.modeling.business.activity_test
import auxi.modeling.business.basicactivity_test
import auxi.modeling.business.component_test
import auxi.modeling.business.entity_test
import auxi.modeling.business.timebasedmodel_test

import auxi.modeling.process.materials.chem.material_test
import auxi.modeling.process.materials.chem.materialpackage_test
import auxi.modeling.process.materials.thermo.material_test
import auxi.modeling.process.materials.thermo.materialpackage_test
import auxi.modeling.process.materials.psd.material_test
import auxi.modeling.process.materials.psd.materialpackage_test
import auxi.modeling.process.materials.slurry.material_test
import auxi.modeling.process.materials.slurry.materialpackage_test

from auxi.modeling.process.materials.chemistry.material_test import TestMaterial as chem_test_material
from auxi.modeling.process.materials.chemistry.material_test import TestMaterialPackage as chem_test_material_package
#from auxi.modeling.process.materials.thermochemistry.material_test import TestMaterial as thermo_test_material
#from auxi.modeling.process.materials.thermochemistry.material_test import TestMaterialPackage as thermo_test_material_package
from auxi.modeling.process.materials.psd.material_test import TestMaterial as psd_test_material
from auxi.modeling.process.materials.psd.material_test import TestMaterialPackage as psd_test_material_package


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
