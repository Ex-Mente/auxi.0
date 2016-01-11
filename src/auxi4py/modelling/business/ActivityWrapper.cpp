
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Units.h"
#include "StockLedger.h"
#include "GeneralLedger.h"
#include "Clock.h"
#include "Activity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

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
    
    void run(Clock* clock, int ix_interval, auxi::modelling::accounting::financial::GeneralLedger* generalLedger, auxi::modelling::accounting::stock::StockLedger* stockLedger)
    {
        if (override run = this->get_override("run"))
            run(clock, ix_interval, generalLedger, stockLedger);
        Activity::run(clock, ix_interval, generalLedger, stockLedger);
    }
    void default_run(Clock* clock, int ix_interval, auxi::modelling::accounting::financial::GeneralLedger* generalLedger, auxi::modelling::accounting::stock::StockLedger* stockLedger) { return this->Activity::run(clock, ix_interval, generalLedger, stockLedger); }
};

void export_auxi_modelling_business_Activity()
{
  // Python C++ mappings

    //class_<ActivityWrapper, bases<ExecutionObject>, boost::noncopyable>("Activity", init<>())
    class_<Activity, Activity*, bases<ExecutionObject>, boost::noncopyable>("Activity", no_init)
	.def(self == self)
    //.def("onExecute_MeetExecutionCriteria", &Activity::OnExecute_MeetExecutionCriteria, &ActivityWrapper::default_OnExecute_MeetExecutionCriteria)
    .def("onExecute_MeetExecutionCriteria", &Activity::OnExecute_MeetExecutionCriteria)
    //.def("prepare_to_run", &Activity::prepare_to_run, &ActivityWrapper::default_prepare_to_run)
    .def("prepare_to_run", &Activity::prepare_to_run)
	.def("setName", &Activity::SetName)
    //.def("set_path", &Activity::set_path, &ActivityWrapper::default_set_path)
    .def("set_path", &Activity::set_path)
    //.def("run", &Activity::run, &ActivityWrapper::default_run)
    .def("run", &Activity::run)
	.add_property("currency", make_function(&Activity::GetCurrency, return_internal_reference<>()), &Activity::SetCurrency)
	.add_property("executionStartAtInterval", &Activity::GetExecutionStartAtInterval, &Activity::SetExecutionStartAtInterval)
	.add_property("executionEndAtInterval", &Activity::GetExecutionEndAtInterval, &Activity::SetExecutionEndAtInterval)
	.add_property("executeInterval", &Activity::GetExecuteInterval, &Activity::SetExecuteInterval)
	.add_property("totalIntervalsToRun", &Activity::GetTotalIntervalsToRun, &Activity::SetTotalIntervalsToRun)
	.add_property("path", &Activity::Getpath, &Activity::Setpath)
    ;

    implicitly_convertible<Activity*,ExecutionObject*>();
    class_<std::vector<Activity*>>("ActivityList").def(vector_indexing_suite<std::vector<Activity*>>());
}