
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedgerStructure.h"
#include "StockTransaction.h"
#include "StockLedger.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockLedgerWrapper : StockLedger, wrapper<StockLedger>
{
};

void export_auxi_modelling_accounting_stock_StockLedger()
{
  // Python C++ mappings

    //class_<StockLedger, StockLedger*, bases<NamedObject>>("StockLedger", init<>())
    class_<StockLedger, StockLedger*, bases<NamedObject>>("StockLedger", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_transaction", make_function(&StockLedger::create_transaction, return_internal_reference<1>()))
	.def("to_string", &StockLedger::to_string)
	.add_property("stockTransactionList", make_function(&StockLedger::GetStockTransactionList, return_internal_reference<1>()))
	.add_property("structure", make_function(&StockLedger::GetStructure, return_internal_reference<>()), &StockLedger::SetStructure)
    ;

    //implicitly_convertible<StockLedgerWrapper*,StockLedger*>();
    implicitly_convertible<StockLedger*,NamedObject*>();
    class_<std::vector<StockLedger*>>("StockLedgerList").def(vector_indexing_suite<std::vector<StockLedger*>>());
}