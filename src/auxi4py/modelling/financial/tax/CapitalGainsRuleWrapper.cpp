
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "CapitalGainsRule.h"

using namespace boost::python;
using namespace auxi::modelling::financial::tax;

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


struct CapitalGainsRuleWrapper : CapitalGainsRule, wrapper<CapitalGainsRule>
{
};

void export_auxi_modelling_financial_tax_CapitalGainsRule()
{
  // Python C++ mappings



    class_<CapitalGainsRuleWrapper, CapitalGainsRule*, bases<Rule>>("CapitalGainsRule", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("percentage", &CapitalGainsRule::GetPercentage, &CapitalGainsRule::SetPercentage, """")
    ;

    //implicitly_convertible<CapitalGainsRuleWrapper*,CapitalGainsRule*>();
    implicitly_convertible<CapitalGainsRule*,Rule*>();
    class_<std::vector<CapitalGainsRule*>>("CapitalGainsRuleList").def(vector_indexing_suite<std::vector<CapitalGainsRule*>>());
}