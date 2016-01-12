
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Units.h"
#include "GeneralLedgerAccount.h"
#include "Transaction.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct TransactionWrapper : Transaction, wrapper<Transaction>
{
};

void export_auxi_modelling_accounting_financial_Transaction()
{
  // Python C++ mappings

    //class_<Transaction, Transaction*, bases<NamedObject>>("Transaction", init<>())
    class_<Transaction, Transaction*, bases<NamedObject>>("Transaction", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("date", &Transaction::GetDate, &Transaction::SetDate)
	.add_property("creditAccountName", &Transaction::GetCreditAccountName, &Transaction::SetCreditAccountName)
	.add_property("debitAccountName", &Transaction::GetDebitAccountName, &Transaction::SetDebitAccountName)
	.add_property("currency", make_function(&Transaction::GetCurrency, return_internal_reference<>()), &Transaction::SetCurrency)
	.add_property("source", &Transaction::GetSource, &Transaction::SetSource)
	.add_property("isClosingCreditAccount", &Transaction::GetIsClosingCreditAccount, &Transaction::SetIsClosingCreditAccount)
	.add_property("isClosingDebitAccount", &Transaction::GetIsClosingDebitAccount, &Transaction::SetIsClosingDebitAccount)
	.add_property("amount", &Transaction::GetAmount, &Transaction::SetAmount)
    ;

    //implicitly_convertible<TransactionWrapper*,Transaction*>();
    implicitly_convertible<Transaction*,NamedObject*>();
    class_<std::vector<Transaction*>>("TransactionList").def(vector_indexing_suite<std::vector<Transaction*>>());
}