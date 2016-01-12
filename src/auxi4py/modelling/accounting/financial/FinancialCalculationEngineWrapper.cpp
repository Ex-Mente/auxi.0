
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "GeneralLedgerStructure.h"
#include "FinancialCalculationEngine.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct FinancialCalculationEngineWrapper : FinancialCalculationEngine, wrapper<FinancialCalculationEngine>
{
};

void export_auxi_modelling_accounting_financial_FinancialCalculationEngine()
{
  // Python C++ mappings

    //class_<FinancialCalculationEngine, FinancialCalculationEngine*, bases<NamedObject>>("FinancialCalculationEngine", init<>())
    class_<FinancialCalculationEngine, FinancialCalculationEngine*, bases<NamedObject>>("FinancialCalculationEngine", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_generalLedgerStructure", make_function(&FinancialCalculationEngine::create_generalLedgerStructure, return_internal_reference<1>()))
	.def("remove_generalLedgerStructure", &FinancialCalculationEngine::remove_generalLedgerStructure)
	.def("to_string", &FinancialCalculationEngine::to_string)
	.add_property("generalLedgerStructureList", make_function(&FinancialCalculationEngine::GetGeneralLedgerStructureList, return_internal_reference<1>()))
    ;

    //implicitly_convertible<FinancialCalculationEngineWrapper*,FinancialCalculationEngine*>();
    implicitly_convertible<FinancialCalculationEngine*,NamedObject*>();
    class_<std::vector<FinancialCalculationEngine*>>("FinancialCalculationEngineList").def(vector_indexing_suite<std::vector<FinancialCalculationEngine*>>());
}