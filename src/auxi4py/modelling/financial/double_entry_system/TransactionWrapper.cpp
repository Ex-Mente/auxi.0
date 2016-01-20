
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Units.h"
#include "GeneralLedgerAccount.h"
#include "Transaction.h"

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


struct TransactionWrapper : Transaction, wrapper<Transaction>
{
};

void export_auxi_modelling_financial_double_entry_system_Transaction()
{
  // Python C++ mappings



    class_<TransactionWrapper, Transaction*, bases<NamedObject>>("Transaction", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("date", &Transaction::GetDate, &Transaction::SetDate, """")

	.add_property("cr_account", &Transaction::GetCrAccount, &Transaction::SetCrAccount, """")

	.add_property("dt_account", &Transaction::GetDtAccount, &Transaction::SetDtAccount, """")

	.add_property("currency", make_function(&Transaction::GetCurrency, return_internal_reference<>()), &Transaction::SetCurrency, """")

	.add_property("source", &Transaction::GetSource, &Transaction::SetSource, """")

	.add_property("is_closing_cr_account", &Transaction::GetIsClosingCrAccount, &Transaction::SetIsClosingCrAccount, """")

	.add_property("is_closing_dt_account", &Transaction::GetIsClosingDtAccount, &Transaction::SetIsClosingDtAccount, """")

	.add_property("amount", &Transaction::GetAmount, &Transaction::SetAmount, """")
    ;

    //implicitly_convertible<TransactionWrapper*,Transaction*>();
    implicitly_convertible<Transaction*,NamedObject*>();
    class_<std::vector<Transaction*>>("TransactionList").def(vector_indexing_suite<std::vector<Transaction*>>());
}