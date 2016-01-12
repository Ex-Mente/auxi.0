
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedger.h"
#include "GeneralLedger.h"
#include "TaxRuleSet.h"
#include "Transaction.h"
#include "Units.h"
#include "VariableGroup.h"
#include "Component.h"
#include "Entity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct EntityWrapper : Entity, wrapper<Entity>
{
};

void export_auxi_modelling_business_Entity()
{
  // Python C++ mappings

    //class_<Entity, Entity*, bases<ExecutionObject>>("Entity", init<>())
    class_<Entity, Entity*, bases<ExecutionObject>>("Entity", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_component", make_function(&Entity::create_component, return_internal_reference<1>()), "Create a new component and add it to this class' componentList")
	.def("remove_component", &Entity::remove_component)
	.def("prepare_to_run", &Entity::prepare_to_run)
	.def("run", &Entity::run)
	.def("getSalesAccounts", &Entity::getSalesAccounts)
	.def("getCostOfSalesAccounts", &Entity::getCostOfSalesAccounts)
	.add_property("variableGroupList", make_function(&Entity::GetVariableGroupList, return_internal_reference<1>()))
	.add_property("componentList", make_function(&Entity::GetComponentList, return_internal_reference<1>()))
	.add_property("taxRuleSet", make_function(&Entity::GetTaxRuleSet, return_internal_reference<>()), &Entity::SetTaxRuleSet)
	.add_property("negativeIncomeTaxTotal", &Entity::GetNegativeIncomeTaxTotal, &Entity::SetNegativeIncomeTaxTotal)
	.add_property("totalIntervalsToRun", &Entity::GetTotalIntervalsToRun, &Entity::SetTotalIntervalsToRun)
	.add_property("stockLedger", make_function(&Entity::GetStockLedger, return_internal_reference<>()), &Entity::SetStockLedger)
	.add_property("generalLedger", make_function(&Entity::GetGeneralLedger, return_internal_reference<>()), &Entity::SetGeneralLedger)
    ;

    //implicitly_convertible<EntityWrapper*,Entity*>();
    implicitly_convertible<Entity*,ExecutionObject*>();
    class_<std::vector<Entity*>>("EntityList").def(vector_indexing_suite<std::vector<Entity*>>());
}
