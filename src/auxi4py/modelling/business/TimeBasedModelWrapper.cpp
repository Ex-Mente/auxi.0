
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Entity.h"
#include "Units.h"
#include "Clock.h"
#include "TimeBasedModel.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct TimeBasedModelWrapper : TimeBasedModel, wrapper<TimeBasedModel>
{
    
    void prepare_to_run()
    {
        if (override prepare_to_run = this->get_override("prepare_to_run"))
            prepare_to_run();
        TimeBasedModel::prepare_to_run();
    }
    void default_prepare_to_run() { return this->TimeBasedModel::prepare_to_run(); }
};

void export_auxi_modelling_business_TimeBasedModel()
{
  // Python C++ mappings

    //class_<TimeBasedModel, TimeBasedModel*, bases<Model>>("TimeBasedModel", init<>())
    class_<TimeBasedModel, TimeBasedModel*, bases<Model>>("TimeBasedModel", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_entity", make_function(&TimeBasedModel::create_entity, return_internal_reference<1>()))
	.def("remove_entity", &TimeBasedModel::remove_entity)
    //.def("prepare_to_run", &TimeBasedModel::prepare_to_run, &TimeBasedModelWrapper::default_prepare_to_run)
    .def("prepare_to_run", &TimeBasedModel::prepare_to_run)
	.def("run", &TimeBasedModel::run)
	.add_property("entityList", make_function(&TimeBasedModel::GetEntityList, return_internal_reference<1>()))
	.add_property("currency", make_function(&TimeBasedModel::GetCurrency, return_internal_reference<>()), &TimeBasedModel::SetCurrency)
	.add_property("totalIntervalsToRun", &TimeBasedModel::GetTotalIntervalsToRun, &TimeBasedModel::SetTotalIntervalsToRun)
	.add_property("clock", make_function(&TimeBasedModel::GetClock, return_internal_reference<>()))
    ;

    //implicitly_convertible<TimeBasedModelWrapper*,TimeBasedModel*>();
    implicitly_convertible<TimeBasedModel*,Model*>();
    class_<std::vector<TimeBasedModel*>>("TimeBasedModelList").def(vector_indexing_suite<std::vector<TimeBasedModel*>>());
}