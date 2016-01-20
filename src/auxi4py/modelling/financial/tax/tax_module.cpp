#ifndef FINANCIAL_MODULE_CPP
#define FINANCIAL_MODULE_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;


void export_auxi_modelling_financial_tax_Rule();
void export_auxi_modelling_financial_tax_RuleSet();
void export_auxi_modelling_financial_tax_IncomeRule();
void export_auxi_modelling_financial_tax_SalesRule();
void export_auxi_modelling_financial_tax_CapitalGainsRule();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(tax)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a classes to create a tax structure for the as well as to aid in tax operations.";
    // The modules classes
    export_auxi_modelling_financial_tax_Rule();
    export_auxi_modelling_financial_tax_RuleSet();
    export_auxi_modelling_financial_tax_IncomeRule();
    export_auxi_modelling_financial_tax_SalesRule();
    export_auxi_modelling_financial_tax_CapitalGainsRule();
}

#endif // FINANCIAL_MODULE_CPP
