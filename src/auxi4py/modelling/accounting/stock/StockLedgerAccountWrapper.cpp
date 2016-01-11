
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedgerAccount.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockLedgerAccountWrapper : StockLedgerAccount, wrapper<StockLedgerAccount>
{
};

void export_auxi_modelling_accounting_stock_StockLedgerAccount()
{
  // Python C++ mappings
  enum_<auxi::modelling::accounting::stock::StockLedgerAccountType::StockLedgerAccountType>("StockLedgerAccountType")
      .value("RawMaterial", StockLedgerAccountType::RawMaterial)
      .value("MROSupplies", StockLedgerAccountType::MROSupplies)
      ;

    //class_<StockLedgerAccount, StockLedgerAccount*, bases<NamedObject>>("StockLedgerAccount", init<>())
    class_<StockLedgerAccount, StockLedgerAccount*, bases<NamedObject>>("StockLedgerAccount", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_account", make_function(&StockLedgerAccount::create_account, return_internal_reference<1>()))
	.def("remove_account", &StockLedgerAccount::remove_account)
	.def("to_string", &StockLedgerAccount::to_string)
	.add_property("accountList", make_function(&StockLedgerAccount::GetAccountList, return_internal_reference<1>()))
	.add_property("number", &StockLedgerAccount::GetNumber, &StockLedgerAccount::SetNumber)
	.add_property("type", &StockLedgerAccount::GetType, &StockLedgerAccount::SetType)
    ;

    //implicitly_convertible<StockLedgerAccountWrapper*,StockLedgerAccount*>();
    implicitly_convertible<StockLedgerAccount*,NamedObject*>();
    class_<std::vector<StockLedgerAccount*>>("StockLedgerAccountList").def(vector_indexing_suite<std::vector<StockLedgerAccount*>>());
}