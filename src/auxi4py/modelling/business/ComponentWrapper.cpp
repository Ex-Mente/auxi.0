
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "VariableGroup.h"
#include "Activity.h"
#include "Clock.h"
#include "Transaction.h"
#include "Component.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct ComponentWrapper : Component, wrapper<Component>
{
};

void export_auxi_modelling_business_Component()
{
  // Python C++ mappings

    //class_<Component, Component*, bases<ExecutionObject>>("Component", init<>())
    class_<Component, Component*, bases<ExecutionObject>>("Component", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_component", make_function(&Component::create_component, return_internal_reference<1>()), "Create a new component and add it to this class' componentList")
	.def("remove_component", &Component::remove_component, "Remove the specified component from this class' componentList")
	.def("setName", &Component::SetName)
	.def("set_path", &Component::set_path)
	.def("prepare_to_run", &Component::prepare_to_run)
	.def("run", &Component::run)
	.add_property("variableGroupList", make_function(&Component::GetVariableGroupList, return_internal_reference<1>()))
	.add_property("componentList", make_function(&Component::GetComponentList, return_internal_reference<1>()))
	.add_property("activityList", make_function(&Component::GetActivityList, return_internal_reference<1>()))
	.add_property("path", &Component::Getpath, &Component::Setpath)
    ;

    //implicitly_convertible<ComponentWrapper*,Component*>();
    implicitly_convertible<Component*,ExecutionObject*>();
    class_<std::vector<Component*>>("ComponentList").def(vector_indexing_suite<std::vector<Component*>>());
}
