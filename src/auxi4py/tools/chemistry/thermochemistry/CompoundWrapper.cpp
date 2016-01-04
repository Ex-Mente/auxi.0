
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Phase.h"
#include "Compound.h"

using namespace boost::python;
using namespace auxi::tools::chemistry::thermochemistry;

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









struct CompoundWrapper : Compound, wrapper<Compound>
{
    
    static Compound* initWrapper(std::string formula, dict phaseMap)
    {
        
		list keys = phaseMap.keys();
		std::map<std::string,Phase> phaseMap_prepped;
		for(int i=0; i<len(keys); ++i) {
			auto curObj = phaseMap[keys[i]];
			if(curObj) phaseMap_prepped[extract<std::string>(keys[i])] = extract<Phase>(phaseMap[keys[i]]);
		}
        auto result = new Compound(formula, phaseMap_prepped);
        return result;
    }
    
    static list get_phase_listWrapper(Compound self)
    {
        
        auto result = self.get_phase_list();
        return to_python_list(result);
    }
};

void export_auxi_tools_chemistry_thermochemistry_Compound()
{
  // Python C++ mappings



    class_<CompoundWrapper, Compound*, bases<Object>>("Compound", "Represents chemical compound.", no_init)
	.def("__init__", make_constructor(&CompoundWrapper::initWrapper))
	.def(self == self)
    
    
	.def("to_string", &Compound::to_string, "")
    
	.def("get_phase_list", &CompoundWrapper::get_phase_listWrapper, "Get a list of the compound's phases.\n"
"\n"
"\n"
":return: List of phases.")
    
	.def("Cp", &Compound::Cp, args("phase", "temperature"), "Calculate the heat capacity of a phase of the compound at a specified temperature.\n"
"\n"
":param phase: A phase of the compound, e.g. \"S\", \"L\", \"G\".\n"
":param temperature: [K]\n"
"\n"
":return: Heat capacity. [J/mol/K]")
    
	.def("H", &Compound::H, args("phase", "temperature"), "Calculate the enthalpy of a phase of the compound at a specified temperature.\n"
"\n"
":param phase: A phase of the compound, e.g. \"S\", \"L\", \"G\".\n"
":param temperature: [K]\n"
"\n"
":return: Enthalpy. [J/mol]")
    
	.def("S", &Compound::S, args("phase", "temperature"), "Calculate the entropy of a phase of the compound at a specified temperature.\n"
"\n"
":param phase: A phase of the compound, e.g. \"S\", \"L\", \"G\".\n"
":param temperature: [K]\n"
"\n"
":return: Entropy. [J/mol/K]")
    
	.def("G", &Compound::G, args("phase", "temperature"), "Calculate the Gibbs free energy of a phase of the compound at a specified temperature.\n"
"\n"
":param phase: A phase of the compound, e.g. \"S\", \"L\", \"G\".\n"
":param temperature: [K]\n"
"\n"
":return: Gibbs free energy. [J/mol]")

	.add_property("formula", &Compound::GetFormula, &Compound::SetFormula, "Chemical formula, e.g. \"Fe\", \"CO2\".")

	.add_property("molar_mass", &Compound::Getmolar_mass, &Compound::Setmolar_mass, "Molar mass. [kg/mol]")
    ;

    //implicitly_convertible<CompoundWrapper*,Compound*>();
    implicitly_convertible<Compound*,Object*>();
    class_<std::vector<Compound*>>("CompoundList").def(vector_indexing_suite<std::vector<Compound*>>());
}