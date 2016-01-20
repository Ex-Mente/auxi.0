#ifndef DES_MODULE_CPP
#define DES_MODULE_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;


void export_auxi_modelling_financial_double_entry_system_GeneralLedgerAccount();
void export_auxi_modelling_financial_double_entry_system_GeneralLedgerStructure();
void export_auxi_modelling_financial_double_entry_system_Transaction();
void export_auxi_modelling_financial_double_entry_system_TransactionTemplate();
void export_auxi_modelling_financial_double_entry_system_GeneralLedger();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(des)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a classes to create a double entry system (des) as well as to aid in double entry system operations.";
    // The modules classes
    export_auxi_modelling_financial_double_entry_system_GeneralLedgerAccount();
    export_auxi_modelling_financial_double_entry_system_GeneralLedgerStructure();
    export_auxi_modelling_financial_double_entry_system_Transaction();
    export_auxi_modelling_financial_double_entry_system_TransactionTemplate();
    export_auxi_modelling_financial_double_entry_system_GeneralLedger();
}

#endif // DES_MODULE_CPP
