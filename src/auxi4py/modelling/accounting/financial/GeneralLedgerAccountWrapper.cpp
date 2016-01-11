
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct GeneralLedgerAccountWrapper : GeneralLedgerAccount, wrapper<GeneralLedgerAccount>
{
};

void export_auxi_modelling_accounting_financial_GeneralLedgerAccount()
{
  // Python C++ mappings
  enum_<auxi::modelling::accounting::financial::GeneralLedgerAccountType::GeneralLedgerAccountType>("GeneralLedgerAccountType")
      .value("Asset", GeneralLedgerAccountType::Asset)
      .value("Equity", GeneralLedgerAccountType::Equity)
      .value("Expense", GeneralLedgerAccountType::Expense)
      .value("Liability", GeneralLedgerAccountType::Liability)
      .value("Revenue", GeneralLedgerAccountType::Revenue)
      ;

    //class_<GeneralLedgerAccount, GeneralLedgerAccount*, bases<NamedObject>>("GeneralLedgerAccount", init<>())
    class_<GeneralLedgerAccount, GeneralLedgerAccount*, bases<NamedObject>>("GeneralLedgerAccount", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_account", make_function(&GeneralLedgerAccount::create_account, return_internal_reference<1>()))
	.def("remove_account", &GeneralLedgerAccount::remove_account)
	.def("to_string", &GeneralLedgerAccount::to_string)
	.add_property("accountList", make_function(&GeneralLedgerAccount::GetAccountList, return_internal_reference<1>()))
	.add_property("number", &GeneralLedgerAccount::GetNumber, &GeneralLedgerAccount::SetNumber)
	.add_property("type", &GeneralLedgerAccount::GetType, &GeneralLedgerAccount::SetType)
    ;

    //implicitly_convertible<GeneralLedgerAccountWrapper*,GeneralLedgerAccount*>();
    implicitly_convertible<GeneralLedgerAccount*,NamedObject*>();
    class_<std::vector<GeneralLedgerAccount*>>("GeneralLedgerAccountList").def(vector_indexing_suite<std::vector<GeneralLedgerAccount*>>());
}