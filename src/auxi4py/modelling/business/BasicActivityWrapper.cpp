
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "BasicActivity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct BasicActivityWrapper : BasicActivity, wrapper<BasicActivity>
{
    
    bool OnExecute_MeetExecutionCriteria(int executionMonth)
    {
        if (override OnExecute_MeetExecutionCriteria = this->get_override("OnExecute_MeetExecutionCriteria"))
            return OnExecute_MeetExecutionCriteria(executionMonth);
        return BasicActivity::OnExecute_MeetExecutionCriteria(executionMonth);
    }
    bool default_OnExecute_MeetExecutionCriteria(int executionMonth) { return this->BasicActivity::OnExecute_MeetExecutionCriteria(executionMonth); }
};

void export_auxi_modelling_business_BasicActivity()
{
  // Python C++ mappings

    //class_<BasicActivity, BasicActivity*, bases<Activity>>("BasicActivity", init<>())
    class_<BasicActivity, BasicActivity*, bases<Activity>>("BasicActivity", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    //.def("onExecute_MeetExecutionCriteria", &BasicActivity::OnExecute_MeetExecutionCriteria, &BasicActivityWrapper::default_OnExecute_MeetExecutionCriteria)
    .def("onExecute_MeetExecutionCriteria", &BasicActivity::OnExecute_MeetExecutionCriteria)
	.def("prepare_to_run", &BasicActivity::prepare_to_run)
	.def("run", &BasicActivity::run)
	.add_property("date", &BasicActivity::GetDate, &BasicActivity::SetDate)
	.add_property("transactionTemplate", make_function(&BasicActivity::GetTransactionTemplate, return_internal_reference<>()), &BasicActivity::SetTransactionTemplate)
	.add_property("amount", &BasicActivity::GetAmount, &BasicActivity::SetAmount)
    ;

    //implicitly_convertible<BasicActivityWrapper*,BasicActivity*>();
    implicitly_convertible<BasicActivity*,Activity*>();
    class_<std::vector<BasicActivity*>>("BasicActivityList").def(vector_indexing_suite<std::vector<BasicActivity*>>());
}