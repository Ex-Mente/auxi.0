#ifndef STOICHIOMETRYWRAPPER_CPP
#define STOICHIOMETRYWRAPPER_CPP

#include "../../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace boost::python;


void export_auxi_tools_chemistry_Element();
void export_auxi_tools_chemistry_Stoichiometry();
//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

BOOST_PYTHON_MODULE(stoichiometry)
{
    boost::python::docstring_options local_docstring_options(true, true, false);
    scope().attr("__doc__") = "This module provides a number of functions for doing stoichiometry calculations.";
    // The modules classes
    export_auxi_tools_chemistry_Element();
    export_auxi_tools_chemistry_Stoichiometry();
}

#endif // STOICHIOMETRYWRAPPER_CPP
