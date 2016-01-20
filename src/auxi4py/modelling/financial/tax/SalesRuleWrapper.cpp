
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "SalesRule.h"

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


struct SalesRuleWrapper : SalesRule, wrapper<SalesRule>
{
};

void export_auxi_modelling_financial_tax_SalesRule()
{
  // Python C++ mappings



    class_<SalesRuleWrapper, SalesRule*, bases<Rule>>("SalesRule", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("percentage", &SalesRule::GetPercentage, &SalesRule::SetPercentage, """")
    ;

    //implicitly_convertible<SalesRuleWrapper*,SalesRule*>();
    implicitly_convertible<SalesRule*,Rule*>();
    class_<std::vector<SalesRule*>>("SalesRuleList").def(vector_indexing_suite<std::vector<SalesRule*>>());
}