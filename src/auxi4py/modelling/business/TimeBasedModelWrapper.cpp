
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Entity.h"
#include "Units.h"
#include "Clock.h"
#include "TimeBasedModel.h"

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







struct TimeBasedModelWrapper : TimeBasedModel, wrapper<TimeBasedModel>
{
};

void export_auxi_modelling_business_TimeBasedModel()
{
  // Python C++ mappings



    class_<TimeBasedModelWrapper, TimeBasedModel*, bases<Model>>("TimeBasedModel", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    
    .def("create_entity", make_function(&TimeBasedModel::create_entity, return_internal_reference<1>()), "")
    
	.def("remove_entity", &TimeBasedModel::remove_entity, "")
    
	.def("prepare_to_run", &TimeBasedModel::prepare_to_run, "")
    
	.def("run", &TimeBasedModel::run, "")

	.add_property("entities", make_function(&TimeBasedModel::GetEntityList, return_internal_reference<1>()), """")

	.add_property("currency", make_function(&TimeBasedModel::GetCurrency, return_internal_reference<>()), &TimeBasedModel::SetCurrency, """")

	.add_property("total_intervals_to_run", &TimeBasedModel::GetTotalIntervalsToRun, &TimeBasedModel::SetTotalIntervalsToRun, """")

	.add_property("clock", make_function(&TimeBasedModel::GetClock, return_internal_reference<>()), """")
    ;

    //implicitly_convertible<TimeBasedModelWrapper*,TimeBasedModel*>();
    implicitly_convertible<TimeBasedModel*,Model*>();
    class_<std::vector<TimeBasedModel*>>("TimeBasedModelList").def(vector_indexing_suite<std::vector<TimeBasedModel*>>());
}