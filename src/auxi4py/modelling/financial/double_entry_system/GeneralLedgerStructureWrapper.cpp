
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"
#include "GeneralLedgerStructure.h"

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



BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(GeneralLedgerStructurecreate_account, create_account, 1, 3)





struct GeneralLedgerStructureWrapper : GeneralLedgerStructure, wrapper<GeneralLedgerStructure>
{
};

void export_auxi_modelling_financial_double_entry_system_GeneralLedgerStructure()
{
  // Python C++ mappings



    class_<GeneralLedgerStructureWrapper, GeneralLedgerStructure*, bases<NamedObject>>("GeneralLedgerStructure", "This class contains and stuctures the accounts for a general ledger.", init<std::string, optional<std::string, std::string> >(args("name","description","json_path"), "TEETETETSST"))
	.def(self == self)


    //.def(init<std::string, optional<std::string, std::string> >(args("name","description","json_path"), "TEETETETSST"))

    .def("create_account", &GeneralLedgerStructure::create_account, return_internal_reference<1>(), GeneralLedgerStructurecreate_account(args("name", "number", "type"), "Create an account in the general ledger\n"
"\n"
":param name: The account name.\n"
":param number: The account number. The default is an empty string.\n"
":param type: The account type. The default is AccountType.asset.\n"
"\n"
":return: A reference to the account"))

	.def("remove_account", &GeneralLedgerStructure::remove_account, "")

    .def("get_account", &GeneralLedgerStructure::get_account, return_internal_reference<1>(), "")



	.def("to_string", &GeneralLedgerStructure::to_string, "")

	.add_property("accounts", make_function(&GeneralLedgerStructure::GetAccountList, return_internal_reference<1>()), """")

	.add_property("bank", make_function(&GeneralLedgerStructure::GetBank, return_internal_reference<>()), &GeneralLedgerStructure::SetBank, "The main bank account of the business. It can be divided into sub-accounts, or used as is.")

	.add_property("income_tax_payable", make_function(&GeneralLedgerStructure::GetIncomeTaxPayable, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeTaxPayable, """")

	.add_property("income_tax_expense", make_function(&GeneralLedgerStructure::GetIncomeTaxExpense, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeTaxExpense, """")

	.add_property("sales", make_function(&GeneralLedgerStructure::GetSales, return_internal_reference<>()), &GeneralLedgerStructure::SetSales, """")

	.add_property("cost_of_sales", make_function(&GeneralLedgerStructure::GetCostOfSales, return_internal_reference<>()), &GeneralLedgerStructure::SetCostOfSales, """")

	.add_property("gross_profit", make_function(&GeneralLedgerStructure::GetGrossProfit, return_internal_reference<>()), &GeneralLedgerStructure::SetGrossProfit, """")

	.add_property("income_summary", make_function(&GeneralLedgerStructure::GetIncomeSummary, return_internal_reference<>()), &GeneralLedgerStructure::SetIncomeSummary, """")

	.add_property("retained_earnings", make_function(&GeneralLedgerStructure::GetRetainedEarnings, return_internal_reference<>()), &GeneralLedgerStructure::SetRetainedEarnings, """")

	.add_property("tax_payment_account", &GeneralLedgerStructure::GetTaxPaymentAccount, &GeneralLedgerStructure::SetTaxPaymentAccount, "The bank account from which taxes will be deducted. If this property is empty, the main bank account will be used.")
    ;

    //implicitly_convertible<GeneralLedgerStructureWrapper*,GeneralLedgerStructure*>();
    implicitly_convertible<GeneralLedgerStructure*,NamedObject*>();
    class_<std::vector<GeneralLedgerStructure*>>("GeneralLedgerStructureList").def(vector_indexing_suite<std::vector<GeneralLedgerStructure*>>());
}