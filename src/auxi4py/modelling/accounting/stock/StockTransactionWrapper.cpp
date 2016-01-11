
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Units.h"
#include "StockLedgerAccount.h"
#include "StockTransaction.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockTransactionWrapper : StockTransaction, wrapper<StockTransaction>
{
};

void export_auxi_modelling_accounting_stock_StockTransaction()
{
  // Python C++ mappings

    //class_<StockTransaction, StockTransaction*, bases<NamedObject>>("StockTransaction", init<>())
    class_<StockTransaction, StockTransaction*, bases<NamedObject>>("StockTransaction", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("date", &StockTransaction::GetDate, &StockTransaction::SetDate)
	.add_property("fromAccountName", &StockTransaction::GetFromAccountName, &StockTransaction::SetFromAccountName)
	.add_property("toAccountName", &StockTransaction::GetToAccountName, &StockTransaction::SetToAccountName)
	.add_property("currency", make_function(&StockTransaction::GetCurrency, return_internal_reference<>()), &StockTransaction::SetCurrency)
	.add_property("source", &StockTransaction::GetSource, &StockTransaction::SetSource)
	.add_property("amount", &StockTransaction::GetAmount, &StockTransaction::SetAmount)
    ;

    //implicitly_convertible<StockTransactionWrapper*,StockTransaction*>();
    implicitly_convertible<StockTransaction*,NamedObject*>();
    class_<std::vector<StockTransaction*>>("StockTransactionList").def(vector_indexing_suite<std::vector<StockTransaction*>>());
}