
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerStructure.h"
#include "Transaction.h"
#include "GeneralLedger.h"

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





struct GeneralLedgerWrapper : GeneralLedger, wrapper<GeneralLedger>
{
};

void export_auxi_modelling_financial_double_entry_system_GeneralLedger()
{
  // Python C++ mappings



    class_<GeneralLedgerWrapper, GeneralLedger*, bases<NamedObject>>("GeneralLedger", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    .def("create_transaction", make_function(&GeneralLedger::create_transaction, return_internal_reference<1>()), "")
    
    
	.def("to_string", &GeneralLedger::to_string, "")

	.add_property("transactions", make_function(&GeneralLedger::GetTransactionList, return_internal_reference<1>()), """")

	.add_property("structure", make_function(&GeneralLedger::GetStructure, return_internal_reference<>()), &GeneralLedger::SetStructure, """")
    ;

    //implicitly_convertible<GeneralLedgerWrapper*,GeneralLedger*>();
    implicitly_convertible<GeneralLedger*,NamedObject*>();
    class_<std::vector<GeneralLedger*>>("GeneralLedgerList").def(vector_indexing_suite<std::vector<GeneralLedger*>>());
}