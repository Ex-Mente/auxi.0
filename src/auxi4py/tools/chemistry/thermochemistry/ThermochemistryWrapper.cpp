
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Compound.h"
#include <boost/property_tree/ptree.hpp>
#include "Thermochemistry.h"

using namespace boost::python;
using namespace auxi::tools::chemistry;

// Converts a C++ vector to a python list
template <class T>
boost::python::list to_python_list(std::vector<T> vector) {
    typename std::vector<T>::iterator iter;
    boost::python::list list;
    for (iter = vector.begin(); iter != vector.end(); ++iter) {
        list.append(*iter);
    }
    return list;
}


using namespace auxi::tools::chemistry::thermochemistry;




BOOST_PYTHON_FUNCTION_OVERLOADS(Thermochemistryload_data, load_data, 0, 1)



BOOST_PYTHON_FUNCTION_OVERLOADS(ThermochemistryCp, Cp, 2, 3)

BOOST_PYTHON_FUNCTION_OVERLOADS(ThermochemistryH, H, 2, 3)

BOOST_PYTHON_FUNCTION_OVERLOADS(ThermochemistryS, S, 2, 3)

BOOST_PYTHON_FUNCTION_OVERLOADS(ThermochemistryG, G, 2, 3)

void export_auxi_tools_chemistry_Thermochemistry()
{
  // Python C++ mappings


    using namespace auxi::tools::chemistry::thermochemistry;
/////////////////// NAMESPACE Thermochemistry ///////////////////
    
    
    def("get_default_data_path", get_default_data_path, "Calculate the default path in which thermochemical data is stored.\n"
"\n"
"\n"
":return: Default path.");
    
    def("set_default_data_path", set_default_data_path, args("new_default_path"), "Sets the default path in which thermochemical data is stored.\n"
"\n"
":param new_default_path: The new default path.\n"
);
    
    
    def("convert_fact_file_to_auxi_thermo_file", convert_fact_file_to_auxi_thermo_file, args("fact_file_path", "auxi_thermo_file_path"), "Convert a Factsage file to a new auxi thermochemical file.\n"
"\n"
":param fact_file_path: The path of the Factsage file.\n"
":param auxi_thermo_file_path: The path the auxi thermochemical file.\n"
);
    
    def("load_data", load_data, Thermochemistryload_data(args("path"), "Load all the thermochemical data files located at a path.\n"
"\n"
":param path: Path at which the data files are located.\n"
));
    
    def("list_compounds", list_compounds, "List all compounds that are currently loaded in the thermo module, and     their phases.\n"
"\n"
);
    
    def("molar_mass", molar_mass, args("compound"), "Determine the molar mass of a chemical compound.\n"
"\n"
":param compound: Formula of a chemical compound, e.g. \"Fe2O3\".\n"
);
    
    def("Cp", Cp, ThermochemistryCp(args("compound_String", "temperature", "mass"), "Calculate the heat capacity of the compound for the specified     temperature and mass.\n"
"\n"
":param compound_String: Formula and phase of chemical compound, e.g. \"Fe2O3[S1]\".\n"
":param temperature: [°C]\n"
":param mass: [kg]\n"
"\n"
":return: Heat capacity. [kWh/K]"));
    
    def("H", H, ThermochemistryH(args("compound_String", "temperature", "mass"), "Calculate the enthalpy of the compound for the specified     temperature and mass.\n"
"\n"
":param compound_String: Formula and phase of chemical compound, e.g. \"Fe2O3[S1]\".\n"
":param temperature: [°C]\n"
":param mass: [kg]\n"
"\n"
":return: Enthalpy. [kWh/K]"));
    
    def("S", S, ThermochemistryS(args("compound_String", "temperature", "mass"), "Calculate the entropy of the compound for the specified     temperature and mass.\n"
"\n"
":param compound_String: Formula and phase of chemical compound, e.g. \"Fe2O3[S1]\".\n"
":param temperature: [°C]\n"
":param mass: [kg]\n"
"\n"
":return: Entropy. [kWh/K]"));
    
    def("G", G, ThermochemistryG(args("compound_String", "temperature", "mass"), "Calculate the Gibbs free energy of the compound for the specified     temperature and mass.\n"
"\n"
":param compound_String: Formula and phase of chemical compound, e.g. \"Fe2O3[S1]\".\n"
":param temperature: [°C]\n"
":param mass: [kg]\n"
"\n"
":return: Gibbs free energy. [kWh/K]"));

    class_<std::map<std::string, Compound>>("CompoundDictDictionary").def(map_indexing_suite<std::map<std::string, Compound>>());
    scope().attr("compoundDict") = object(m_compoundDict);
////////////////////////////////////////////////////

}