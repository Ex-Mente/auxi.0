
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "IncomeRule.h"

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


struct IncomeRuleWrapper : IncomeRule, wrapper<IncomeRule>
{
};

void export_auxi_modelling_financial_tax_IncomeRule()
{
  // Python C++ mappings



    class_<IncomeRuleWrapper, IncomeRule*, bases<Rule>>("IncomeRule", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("percentage", &IncomeRule::GetPercentage, &IncomeRule::SetPercentage, """")
    ;

    //implicitly_convertible<IncomeRuleWrapper*,IncomeRule*>();
    implicitly_convertible<IncomeRule*,Rule*>();
    class_<std::vector<IncomeRule*>>("IncomeRuleList").def(vector_indexing_suite<std::vector<IncomeRule*>>());
}