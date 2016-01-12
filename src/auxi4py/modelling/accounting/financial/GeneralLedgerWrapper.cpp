
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerStructure.h"
#include "Transaction.h"
#include "GeneralLedger.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct GeneralLedgerWrapper : GeneralLedger, wrapper<GeneralLedger>
{
};

void export_auxi_modelling_accounting_financial_GeneralLedger()
{
  // Python C++ mappings

    //class_<GeneralLedger, GeneralLedger*, bases<NamedObject>>("GeneralLedger", init<>())
    class_<GeneralLedger, GeneralLedger*, bases<NamedObject>>("GeneralLedger", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_transaction", make_function(&GeneralLedger::create_transaction, return_internal_reference<1>()))
	.def("to_string", &GeneralLedger::to_string)
	.add_property("transactionList", make_function(&GeneralLedger::GetTransactionList, return_internal_reference<1>()))
	.add_property("structure", make_function(&GeneralLedger::GetStructure, return_internal_reference<>()), &GeneralLedger::SetStructure)
    ;

    //implicitly_convertible<GeneralLedgerWrapper*,GeneralLedger*>();
    implicitly_convertible<GeneralLedger*,NamedObject*>();
    class_<std::vector<GeneralLedger*>>("GeneralLedgerList").def(vector_indexing_suite<std::vector<GeneralLedger*>>());
}