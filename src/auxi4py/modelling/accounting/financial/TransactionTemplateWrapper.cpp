
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"
#include "TransactionTemplate.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct TransactionTemplateWrapper : TransactionTemplate, wrapper<TransactionTemplate>
{
};

void export_auxi_modelling_accounting_financial_TransactionTemplate()
{
  // Python C++ mappings

    //class_<TransactionTemplate, TransactionTemplate*, bases<NamedObject>>("TransactionTemplate", init<>())
    class_<TransactionTemplate, TransactionTemplate*, bases<NamedObject>>("TransactionTemplate", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("debitAccountName", &TransactionTemplate::GetDebitAccountName, &TransactionTemplate::SetDebitAccountName)
	.add_property("creditAccountName", &TransactionTemplate::GetCreditAccountName, &TransactionTemplate::SetCreditAccountName)
    ;

    //implicitly_convertible<TransactionTemplateWrapper*,TransactionTemplate*>();
    implicitly_convertible<TransactionTemplate*,NamedObject*>();
    class_<std::vector<TransactionTemplate*>>("TransactionTemplateList").def(vector_indexing_suite<std::vector<TransactionTemplate*>>());
}