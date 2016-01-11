
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedgerAccount.h"
#include "StockTransactionTemplate.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockTransactionTemplateWrapper : StockTransactionTemplate, wrapper<StockTransactionTemplate>
{
};

void export_auxi_modelling_accounting_stock_StockTransactionTemplate()
{
  // Python C++ mappings

    //class_<StockTransactionTemplate, StockTransactionTemplate*, bases<NamedObject>>("StockTransactionTemplate", init<>())
    class_<StockTransactionTemplate, StockTransactionTemplate*, bases<NamedObject>>("StockTransactionTemplate", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("fromAccountName", &StockTransactionTemplate::GetFromAccountName, &StockTransactionTemplate::SetFromAccountName)
	.add_property("toAccountName", &StockTransactionTemplate::GetToAccountName, &StockTransactionTemplate::SetToAccountName)
    ;

    //implicitly_convertible<StockTransactionTemplateWrapper*,StockTransactionTemplate*>();
    implicitly_convertible<StockTransactionTemplate*,NamedObject*>();
    class_<std::vector<StockTransactionTemplate*>>("StockTransactionTemplateList").def(vector_indexing_suite<std::vector<StockTransactionTemplate*>>());
}