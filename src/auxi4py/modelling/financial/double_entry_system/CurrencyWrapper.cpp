
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Currency.h"

using namespace boost::python;
using namespace auxi::modelling::financial::double_entry_system;

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



struct CurrencyWrapper : Currency, wrapper<Currency>
{
};

void export_auxi_modelling_financial_double_entry_system_Currency()
{
  // Python C++ mappings



    class_<CurrencyWrapper, Currency*, bases<NamedObject>>("Currency", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
	.def("to_string", &Currency::to_string, "")

	.add_property("default_exchange_rate", &Currency::GetDefaultExchangeRate, &Currency::SetDefaultExchangeRate, """")
    ;

    //implicitly_convertible<CurrencyWrapper*,Currency*>();
    implicitly_convertible<Currency*,NamedObject*>();
    class_<std::vector<Currency*>>("CurrencyList").def(vector_indexing_suite<std::vector<Currency*>>());
}