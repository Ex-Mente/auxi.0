
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Currency.h"
#include "CurrencyTable.h"

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



struct CurrencyTableWrapper : CurrencyTable, wrapper<CurrencyTable>
{
};

void export_auxi_modelling_financial_double_entry_system_CurrencyTable()
{
  // Python C++ mappings



    class_<CurrencyTableWrapper, CurrencyTable*, bases<NamedObject>>("CurrencyTable", """", init<>())
	.def(self == self)
    
        
    .def(init<std::string, optional<std::string, std::string, std::string> >())
    
    .def("create_currency", &CurrencyTable::create_currency, return_internal_reference<1>(), "")

	.add_property("currencys", make_function(&CurrencyTable::GetCurrencyList, return_internal_reference<1>()), """")

	.add_property("default_currency", make_function(&CurrencyTable::GetDefaultCurrency, return_internal_reference<>()), &CurrencyTable::SetDefaultCurrency, """")
    ;

    //implicitly_convertible<CurrencyTableWrapper*,CurrencyTable*>();
    implicitly_convertible<CurrencyTable*,NamedObject*>();
    class_<std::vector<CurrencyTable*>>("CurrencyTableList").def(vector_indexing_suite<std::vector<CurrencyTable*>>());
}