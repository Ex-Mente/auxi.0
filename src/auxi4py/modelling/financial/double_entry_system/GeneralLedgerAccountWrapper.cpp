
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



BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(GeneralLedgerAccountcreate_account, create_account, 1, 2)


struct GeneralLedgerAccountWrapper : GeneralLedgerAccount, wrapper<GeneralLedgerAccount>
{
};

void export_auxi_modelling_financial_double_entry_system_GeneralLedgerAccount()
{
  // Python C++ mappings
  enum_<auxi::modelling::financial::double_entry_system::AccountType::AccountType>("AccountType", "The type of the general ledger account account.")
      .value("asset", AccountType::asset)
      .value("equity", AccountType::equity)
      .value("expense", AccountType::expense)
      .value("liability", AccountType::liability)
      .value("revenue", AccountType::revenue)
      ;



    class_<GeneralLedgerAccountWrapper, GeneralLedgerAccount*, bases<NamedObject>>("GeneralLedgerAccount", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    .def("create_account", &GeneralLedgerAccount::create_account, return_internal_reference<1>(), GeneralLedgerAccountcreate_account(args("name", "number"), "Create sub account.\n"
"\n"
":param name: The account name.\n"
":param number: The account number. The default is an empty string.\n"
"\n"
":return: A reference to the account"))
    
	.def("remove_account", &GeneralLedgerAccount::remove_account, args("number"), "Removes a specific account.\n"
"\n"
":param number: The number of the account to remove.\n"
)
    
    
	.def("to_string", &GeneralLedgerAccount::to_string, "")

	.add_property("accounts", make_function(&GeneralLedgerAccount::GetAccountList, return_internal_reference<1>()), """")

	.add_property("number", &GeneralLedgerAccount::GetNumber, &GeneralLedgerAccount::SetNumber, """")

	.add_property("type", &GeneralLedgerAccount::GetType, &GeneralLedgerAccount::SetType, """")
    ;

    //implicitly_convertible<GeneralLedgerAccountWrapper*,GeneralLedgerAccount*>();
    implicitly_convertible<GeneralLedgerAccount*,NamedObject*>();
    class_<std::vector<GeneralLedgerAccount*>>("GeneralLedgerAccountList").def(vector_indexing_suite<std::vector<GeneralLedgerAccount*>>());
}