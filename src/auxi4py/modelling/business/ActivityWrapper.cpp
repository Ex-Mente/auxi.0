
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Units.h"
#include "GeneralLedger.h"
#include "Clock.h"
#include "Activity.h"

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







struct ActivityWrapper : Activity, wrapper<Activity>
{
    
    bool OnExecute_MeetExecutionCriteria(int executionMonth)
    {
        if (override OnExecute_MeetExecutionCriteria = this->get_override("OnExecute_MeetExecutionCriteria"))
            return OnExecute_MeetExecutionCriteria(executionMonth);
        return Activity::OnExecute_MeetExecutionCriteria(executionMonth);
    }
    bool default_OnExecute_MeetExecutionCriteria(int executionMonth) { return this->Activity::OnExecute_MeetExecutionCriteria(executionMonth); }
    
    void prepare_to_run(Clock* clock, int totalMonthsToRun)
    {
        if (override prepare_to_run = this->get_override("prepare_to_run"))
            prepare_to_run(clock, totalMonthsToRun);
        Activity::prepare_to_run(clock, totalMonthsToRun);
    }
    void default_prepare_to_run(Clock* clock, int totalMonthsToRun) { return this->Activity::prepare_to_run(clock, totalMonthsToRun); }
    
    void set_path(std::string parent_path)
    {
        if (override set_path = this->get_override("set_path"))
            set_path(parent_path);
        Activity::set_path(parent_path);
    }
    void default_set_path(std::string parent_path) { return this->Activity::set_path(parent_path); }
    
    void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
    {
        if (override run = this->get_override("run"))
            run(clock, ix_interval, generalLedger);
        Activity::run(clock, ix_interval, generalLedger);
    }
    void default_run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger) { return this->Activity::run(clock, ix_interval, generalLedger); }
};

void export_auxi_modelling_business_Activity()
{
  // Python C++ mappings



    class_<ActivityWrapper, Activity*, bases<ExecutionObject>, boost::noncopyable>("Activity", """", no_init)
	.def(self == self)
    
    //.def("onExecute_MeetExecutionCriteria", &Activity::OnExecute_MeetExecutionCriteria, &ActivityWrapper::default_OnExecute_MeetExecutionCriteria, "")
    .def("onExecute_MeetExecutionCriteria", &Activity::OnExecute_MeetExecutionCriteria, "")
    
    //.def("prepare_to_run", &Activity::prepare_to_run, &ActivityWrapper::default_prepare_to_run, "")
    .def("prepare_to_run", &Activity::prepare_to_run, "")
    
	.def("setName", &Activity::SetName, "")
    
    //.def("set_path", &Activity::set_path, &ActivityWrapper::default_set_path, "")
    .def("set_path", &Activity::set_path, "")
    
    //.def("run", &Activity::run, &ActivityWrapper::default_run, "")
    .def("run", &Activity::run, "")

	.add_property("currency", make_function(&Activity::GetCurrency, return_internal_reference<>()), &Activity::SetCurrency, """")

	.add_property("execution_start_at_interval", &Activity::GetExecutionStartAtInterval, &Activity::SetExecutionStartAtInterval, """")

	.add_property("execution_end_at_interval", &Activity::GetExecutionEndAtInterval, &Activity::SetExecutionEndAtInterval, """")

	.add_property("execute_interval", &Activity::GetExecuteInterval, &Activity::SetExecuteInterval, """")

	.add_property("total_intervals_to_run", &Activity::GetTotalIntervalsToRun, &Activity::SetTotalIntervalsToRun, """")

	.add_property("path", &Activity::Getpath, &Activity::Setpath, """")
    ;

    implicitly_convertible<Activity*,ExecutionObject*>();
    class_<std::vector<Activity*>>("ActivityList").def(vector_indexing_suite<std::vector<Activity*>>());
}