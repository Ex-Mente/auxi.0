#ifndef FINANCIAL_MODULE_CPP
#define FINANCIAL_MODULE_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;


void export_auxi_modelling_accounting_financial_GeneralLedgerAccount();
void export_auxi_modelling_accounting_financial_GeneralLedgerStructure();
void export_auxi_modelling_accounting_financial_TaxRule();
void export_auxi_modelling_accounting_financial_TaxRuleSet();
void export_auxi_modelling_accounting_financial_IncomeTaxRule();
void export_auxi_modelling_accounting_financial_SalesTaxRule();
void export_auxi_modelling_accounting_financial_CapitalGainsTaxRule();
void export_auxi_modelling_accounting_financial_Transaction();
void export_auxi_modelling_accounting_financial_TransactionTemplate();
void export_auxi_modelling_accounting_financial_FinancialCalculationEngine();
void export_auxi_modelling_accounting_financial_GeneralLedger();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(_financial)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a classes to create a financial structure as well as to aid in financial operations.";
    // The modules classes
    export_auxi_modelling_accounting_financial_GeneralLedgerAccount();
    export_auxi_modelling_accounting_financial_GeneralLedgerStructure();
    export_auxi_modelling_accounting_financial_TaxRule();
    export_auxi_modelling_accounting_financial_TaxRuleSet();
    export_auxi_modelling_accounting_financial_IncomeTaxRule();
    export_auxi_modelling_accounting_financial_SalesTaxRule();
    export_auxi_modelling_accounting_financial_CapitalGainsTaxRule();
    export_auxi_modelling_accounting_financial_Transaction();
    export_auxi_modelling_accounting_financial_TransactionTemplate();
    export_auxi_modelling_accounting_financial_FinancialCalculationEngine();
    export_auxi_modelling_accounting_financial_GeneralLedger();
}

#endif // FINANCIAL_MODULE_CPP
