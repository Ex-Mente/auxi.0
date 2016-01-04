#ifndef STOICHIOMETRYWRAPPER_CPP
#define STOICHIOMETRYWRAPPER_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;


void export_auxi_tools_chemistry_thermochemistry_CpRecord();
void export_auxi_tools_chemistry_thermochemistry_Phase();
void export_auxi_tools_chemistry_thermochemistry_Compound();
void export_auxi_tools_chemistry_Thermochemistry();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(thermochemistry)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a number of functions for doing thermochemical calculations.";
    // The modules classes
    export_auxi_tools_chemistry_thermochemistry_CpRecord();
    export_auxi_tools_chemistry_thermochemistry_Phase();
    export_auxi_tools_chemistry_thermochemistry_Compound();
    export_auxi_tools_chemistry_Thermochemistry();
}

#endif // STOICHIOMETRYWRAPPER_CPP
