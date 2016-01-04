
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "CpRecord.h"

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







struct CpRecordWrapper : CpRecord, wrapper<CpRecord>
{
    
    static CpRecord* initWrapper(double Tmin, double Tmax, list coefficientList, list exponentList)
    {
        
		std::vector<double> coefficientList_prepped;
		for(int i=0; i<len(coefficientList); ++i) coefficientList_prepped.push_back(extract<double>(coefficientList[i]));
			
		std::vector<double> exponentList_prepped;
		for(int i=0; i<len(exponentList); ++i) exponentList_prepped.push_back(extract<double>(exponentList[i]));
			
        auto result = new CpRecord(Tmin, Tmax, coefficientList_prepped, exponentList_prepped);
        return result;
    }
};

void export_auxi_tools_chemistry_thermochemistry_CpRecord()
{
  // Python C++ mappings



    class_<CpRecordWrapper, CpRecord*, bases<Object>>("CpRecord", "A Cp equation record for a compound phase over a specific temperature range.", no_init)
	.def("__init__", make_constructor(&CpRecordWrapper::initWrapper))
	.def(self == self)
    
    
	.def("to_string", &CpRecord::to_string, "")
    
	.def("Cp", &CpRecord::Cp, args("temperature"), "Calculate the heat capacity of the compound phase covered by this Cp record.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: Heat capacity. [J/mol/K]")
    
	.def("H", &CpRecord::H, args("temperature"), "Calculate the enthalpy of the compound phase covered by this Cp record.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: Enthalpy. [J/mol]")
    
	.def("S", &CpRecord::S, args("temperature"), "Calculate the entropy of the compound phase covered by this Cp record.\n"
"\n"
":param temperature: [K]\n"
"\n"
":return: Entropy. [J/mol/K]")

	.add_property("Tmin", &CpRecord::GetTmin, &CpRecord::SetTmin, "The minimum temperature of the range covered by this record. [K]")

	.add_property("Tmax", &CpRecord::GetTmax, &CpRecord::SetTmax, "The maximum temperature of the range covered by this record. [K]")
    ;

    //implicitly_convertible<CpRecordWrapper*,CpRecord*>();
    implicitly_convertible<CpRecord*,Object*>();
    class_<std::vector<CpRecord*>>("CpRecordList").def(vector_indexing_suite<std::vector<CpRecord*>>());
}