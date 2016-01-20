
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedger.h"
#include "RuleSet.h"
#include "Transaction.h"
#include "Units.h"
#include "VariableGroup.h"
#include "Component.h"
#include "Entity.h"

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






struct EntityWrapper : Entity, wrapper<Entity>
{
};

void export_auxi_modelling_business_Entity()
{
  // Python C++ mappings



    class_<EntityWrapper, Entity*, bases<ExecutionObject>>("Entity", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    .def("create_component", make_function(&Entity::create_component, return_internal_reference<1>()), "")
    
	.def("remove_component", &Entity::remove_component, "")
    
	.def("prepare_to_run", &Entity::prepare_to_run, "")
    
    
    
    
    
    
    
	.def("run", &Entity::run, "")
    
    

	.add_property("variable_groups", make_function(&Entity::GetVariableGroupList, return_internal_reference<1>()), """")

	.add_property("components", make_function(&Entity::GetComponentList, return_internal_reference<1>()), """")

	.add_property("tax_rule_set", make_function(&Entity::GetTaxRuleSet, return_internal_reference<>()), &Entity::SetTaxRuleSet, """")

	.add_property("negative_income_tax_total", &Entity::GetNegativeIncomeTaxTotal, &Entity::SetNegativeIncomeTaxTotal, """")

	.add_property("total_intervals_to_run", &Entity::GetTotalIntervalsToRun, &Entity::SetTotalIntervalsToRun, """")

	.add_property("gl", make_function(&Entity::GetGl, return_internal_reference<>()), &Entity::SetGl, "The entity's General Ledger.")
    ;

    //implicitly_convertible<EntityWrapper*,Entity*>();
    implicitly_convertible<Entity*,ExecutionObject*>();
    class_<std::vector<Entity*>>("EntityList").def(vector_indexing_suite<std::vector<Entity*>>());
}