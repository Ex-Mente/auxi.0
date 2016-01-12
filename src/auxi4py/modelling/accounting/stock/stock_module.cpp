#ifndef FINANCIAL_MODULE_CPP
#define FINANCIAL_MODULE_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;

void export_auxi_modelling_accounting_stock_StockLedgerAccount();
void export_auxi_modelling_accounting_stock_StockLedgerStructure();
void export_auxi_modelling_accounting_stock_StockTransaction();
void export_auxi_modelling_accounting_stock_StockTransactionTemplate();
void export_auxi_modelling_accounting_stock_StockCalculationEngine();
void export_auxi_modelling_accounting_stock_StockLedger();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(_stock)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a classes to create a financial structure as well as to aid in financial operations.";
    // The modules classes
    export_auxi_modelling_accounting_stock_StockLedgerAccount();
    export_auxi_modelling_accounting_stock_StockLedgerStructure();
    export_auxi_modelling_accounting_stock_StockTransaction();
    export_auxi_modelling_accounting_stock_StockTransactionTemplate();
    export_auxi_modelling_accounting_stock_StockCalculationEngine();
    export_auxi_modelling_accounting_stock_StockLedger();
}

#endif // FINANCIAL_MODULE_CPP
