
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerAccount.h"
#include "TransactionTemplate.h"

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


struct TransactionTemplateWrapper : TransactionTemplate, wrapper<TransactionTemplate>
{
};

void export_auxi_modelling_financial_double_entry_system_TransactionTemplate()
{
  // Python C++ mappings



    class_<TransactionTemplateWrapper, TransactionTemplate*, bases<NamedObject>>("TransactionTemplate", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)

	.add_property("dt_account", &TransactionTemplate::GetDtAccount, &TransactionTemplate::SetDtAccount, """")

	.add_property("cr_account", &TransactionTemplate::GetCrAccount, &TransactionTemplate::SetCrAccount, """")
    ;

    //implicitly_convertible<TransactionTemplateWrapper*,TransactionTemplate*>();
    implicitly_convertible<TransactionTemplate*,NamedObject*>();
    class_<std::vector<TransactionTemplate*>>("TransactionTemplateList").def(vector_indexing_suite<std::vector<TransactionTemplate*>>());
}