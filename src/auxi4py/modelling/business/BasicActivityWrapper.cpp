
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "BasicActivity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

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






struct BasicActivityWrapper : BasicActivity, wrapper<BasicActivity>
{
};

void export_auxi_modelling_business_BasicActivity()
{
  // Python C++ mappings



    class_<BasicActivityWrapper, BasicActivity*, bases<Activity>>("BasicActivity", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    
	.def("onExecute_MeetExecutionCriteria", &BasicActivity::OnExecute_MeetExecutionCriteria, "")
    
	.def("prepare_to_run", &BasicActivity::prepare_to_run, "")
    
	.def("run", &BasicActivity::run, "")

	.add_property("date", &BasicActivity::GetDate, &BasicActivity::SetDate, """")

	.add_property("tx_template", make_function(&BasicActivity::GetTxTemplate, return_internal_reference<>()), &BasicActivity::SetTxTemplate, """")

	.add_property("amount", &BasicActivity::GetAmount, &BasicActivity::SetAmount, """")
    ;

    //implicitly_convertible<BasicActivityWrapper*,BasicActivity*>();
    implicitly_convertible<BasicActivity*,Activity*>();
    class_<std::vector<BasicActivity*>>("BasicActivityList").def(vector_indexing_suite<std::vector<BasicActivity*>>());
}