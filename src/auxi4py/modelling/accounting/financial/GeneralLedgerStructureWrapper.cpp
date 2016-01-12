
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"
#include "GeneralLedgerStructure.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct GeneralLedgerStructureWrapper : GeneralLedgerStructure, wrapper<GeneralLedgerStructure>
{
};

void export_auxi_modelling_accounting_financial_GeneralLedgerStructure()
{
  // Python C++ mappings

    //class_<GeneralLedgerStructure, GeneralLedgerStructure*, bases<NamedObject>>("GeneralLedgerStructure", init<>())
    class_<GeneralLedgerStructure, GeneralLedgerStructure*, bases<NamedObject>>("GeneralLedgerStructure", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_account", make_function(&GeneralLedgerStructure::create_account, return_internal_reference<1>()))
	.def("remove_account", &GeneralLedgerStructure::remove_account)
    .def("get_account", make_function(&GeneralLedgerStructure::get_account, return_internal_reference<1>()))
	.def("to_string", &GeneralLedgerStructure::to_string)
	.add_property("accountList", make_function(&GeneralLedgerStructure::GetAccountList, return_internal_reference<1>()))
	.add_property("bankAccount", make_function(&GeneralLedgerStructure::GetBankAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetBankAccount)
	.add_property("incomeTaxPayableAccount", make_function(&GeneralLedgerStructure::GetIncomeTaxPayableAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeTaxPayableAccount)
	.add_property("incomeTaxExpenseAccount", make_function(&GeneralLedgerStructure::GetIncomeTaxExpenseAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeTaxExpenseAccount)
	.add_property("salesAccount", make_function(&GeneralLedgerStructure::GetSalesAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetSalesAccount)
	.add_property("costOfSalesAccount", make_function(&GeneralLedgerStructure::GetCostOfSalesAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetCostOfSalesAccount)
	.add_property("grossProfitAccount", make_function(&GeneralLedgerStructure::GetGrossProfitAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetGrossProfitAccount)
	.add_property("incomeSummaryAccount", make_function(&GeneralLedgerStructure::GetIncomeSummaryAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeSummaryAccount)
	.add_property("retainedEarningsAccount", make_function(&GeneralLedgerStructure::GetRetainedEarningsAccount, return_internal_reference<>()), &GeneralLedgerStructure::SetRetainedEarningsAccount)
    ;

    //implicitly_convertible<GeneralLedgerStructureWrapper*,GeneralLedgerStructure*>();
    implicitly_convertible<GeneralLedgerStructure*,NamedObject*>();
    class_<std::vector<GeneralLedgerStructure*>>("GeneralLedgerStructureList").def(vector_indexing_suite<std::vector<GeneralLedgerStructure*>>());
}