
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"

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






struct GeneralLedgerAccountWrapper : GeneralLedgerAccount, wrapper<GeneralLedgerAccount>
{
};

void export_auxi_modelling_financial_double_entry_system_GeneralLedgerAccount()
{
  // Python C++ mappings
  enum_<auxi::modelling::financial::double_entry_system::AccountType::AccountType>("AccountType", "None")
      .value("Asset", AccountType::Asset)
      .value("Equity", AccountType::Equity)
      .value("Expense", AccountType::Expense)
      .value("Liability", AccountType::Liability)
      .value("Revenue", AccountType::Revenue)
      ;



    class_<GeneralLedgerAccountWrapper, GeneralLedgerAccount*, bases<NamedObject>>("GeneralLedgerAccount", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    .def("create_account", make_function(&GeneralLedgerAccount::create_account, return_internal_reference<1>()), "")
    
	.def("remove_account", &GeneralLedgerAccount::remove_account, "")
    
    
	.def("to_string", &GeneralLedgerAccount::to_string, "")

	.add_property("accounts", make_function(&GeneralLedgerAccount::GetAccountList, return_internal_reference<1>()), """")

	.add_property("number", &GeneralLedgerAccount::GetNumber, &GeneralLedgerAccount::SetNumber, """")

	.add_property("type", &GeneralLedgerAccount::GetType, &GeneralLedgerAccount::SetType, """")
    ;

    //implicitly_convertible<GeneralLedgerAccountWrapper*,GeneralLedgerAccount*>();
    implicitly_convertible<GeneralLedgerAccount*,NamedObject*>();
    class_<std::vector<GeneralLedgerAccount*>>("GeneralLedgerAccountList").def(vector_indexing_suite<std::vector<GeneralLedgerAccount*>>());
}