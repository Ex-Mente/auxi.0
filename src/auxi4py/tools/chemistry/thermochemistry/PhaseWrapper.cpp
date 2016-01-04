
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "CpRecord.h"
#include "Phase.h"

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








struct PhaseWrapper : Phase, wrapper<Phase>
{
    
    static Phase* initWrapper(std::string name, std::string symbol, double DHref, double Sref, dict cpRecordMap)
    {
        
		list keys = cpRecordMap.keys();
		std::map<double, CpRecord> cpRecordMap_prepped;
		for(int i=0; i<len(keys); ++i) {
			auto curObj = cpRecordMap[keys[i]];
			if(curObj) cpRecordMap_prepped[extract<double>(keys[i])] = extract< CpRecord>(cpRecordMap[keys[i]]);
		}
        auto result = new Phase(name, symbol, DHref, Sref, cpRecordMap_prepped);
        return result;
    }
};

void export_auxi_tools_chemistry_thermochemistry_Phase()
{
  // Python C++ mappings



    class_<PhaseWrapper, Phase*, bases<NamedObject>>("Phase", "Represents a phase of a chemical compound.", no_init)
	.def("__init__", make_constructor(&PhaseWrapper::initWrapper))
	.def(self == self)
    
    
	.def("to_string", &Phase::to_string, "")
    
	.def("Cp", &Phase::Cp, args("temperature"), "Calculate the heat capacity of the compound phase at the specified         temperature.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: The heat capacity of the compound phase. [J/mol/K]")
    
	.def("H", &Phase::H, args("temperature"), "Calculate the enthalpy of the compound phase at the specified         temperature.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: The heat capacity of the compound phase. [J/mol/K]")
    
	.def("S", &Phase::S, args("temperature"), "Calculate the entropy of the compound phase at the specified         temperature.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: The heat capacity of the compound phase. [J/mol/K]")
    
	.def("G", &Phase::G, args("temperature"), "Calculate the Gibbs free energy of the compound phase at the specified         temperature.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: The heat capacity of the compound phase. [J/mol/K]")

	.add_property("symbol", &Phase::GetSymbol, &Phase::SetSymbol, "The phase's symbol, e.g. S1 = solid 1, L = liquid, etc.")

	.add_property("Tref", &Phase::GetTref, &Phase::SetTref, "The reference temperature of the phase. [K]")

	.add_property("DHref", &Phase::GetDHref, &Phase::SetDHref, "The formation enthalpy of the phase at Tref. [J/mol]")

	.add_property("Sref", &Phase::GetSref, &Phase::SetSref, "The standard entropy of the phase at Tref. [J/mol/K]")
    ;

    //implicitly_convertible<PhaseWrapper*,Phase*>();
    implicitly_convertible<Phase*,NamedObject*>();
    class_<std::vector<Phase*>>("PhaseList").def(vector_indexing_suite<std::vector<Phase*>>());
}