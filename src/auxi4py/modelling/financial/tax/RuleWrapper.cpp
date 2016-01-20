
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Rule.h"

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


struct RuleWrapper : Rule, wrapper<Rule>
{
};

void export_auxi_modelling_financial_tax_Rule()
{
  // Python C++ mappings



    class_<RuleWrapper, Rule*, bases<NamedObject>>("Rule", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    ;

    //implicitly_convertible<RuleWrapper*,Rule*>();
    implicitly_convertible<Rule*,NamedObject*>();
    class_<std::vector<Rule*>>("RuleList").def(vector_indexing_suite<std::vector<Rule*>>());
}