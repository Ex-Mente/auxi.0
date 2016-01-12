
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedgerAccount.h"
#include "StockLedgerStructure.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockLedgerStructureWrapper : StockLedgerStructure, wrapper<StockLedgerStructure>
{
};

void export_auxi_modelling_accounting_stock_StockLedgerStructure()
{
  // Python C++ mappings

    //class_<StockLedgerStructure, StockLedgerStructure*, bases<NamedObject>>("StockLedgerStructure", init<>())
    class_<StockLedgerStructure, StockLedgerStructure*, bases<NamedObject>>("StockLedgerStructure", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_account", make_function(&StockLedgerStructure::create_account, return_internal_reference<1>()))
	.def("remove_account", &StockLedgerStructure::remove_account)
    .def("get_account", make_function(&StockLedgerStructure::get_account, return_internal_reference<1>()))
	.def("to_string", &StockLedgerStructure::to_string)
	.add_property("accountList", make_function(&StockLedgerStructure::GetAccountList, return_internal_reference<1>()))
	.add_property("miscAccount", make_function(&StockLedgerStructure::GetMiscAccount, return_internal_reference<>()), &StockLedgerStructure::SetMiscAccount)
    ;

    //implicitly_convertible<StockLedgerStructureWrapper*,StockLedgerStructure*>();
    implicitly_convertible<StockLedgerStructure*,NamedObject*>();
    class_<std::vector<StockLedgerStructure*>>("StockLedgerStructureList").def(vector_indexing_suite<std::vector<StockLedgerStructure*>>());
}