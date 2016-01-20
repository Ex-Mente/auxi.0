
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Rule.h"
#include "RuleSet.h"

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


struct RuleSetWrapper : RuleSet, wrapper<RuleSet>
{
};

void export_auxi_modelling_financial_tax_RuleSet()
{
  // Python C++ mappings



    class_<RuleSetWrapper, RuleSet*, bases<NamedObject>>("RuleSet", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("ruleList", make_function(&RuleSet::GetRuleList, return_internal_reference<1>()), """")

	.add_property("code", &RuleSet::GetCode, &RuleSet::SetCode, """")
    ;

    //implicitly_convertible<RuleSetWrapper*,RuleSet*>();
    implicitly_convertible<RuleSet*,NamedObject*>();
    class_<std::vector<RuleSet*>>("RuleSetList").def(vector_indexing_suite<std::vector<RuleSet*>>());
}