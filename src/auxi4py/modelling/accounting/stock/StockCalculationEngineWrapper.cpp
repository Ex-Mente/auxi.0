
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "StockLedgerStructure.h"
#include "StockCalculationEngine.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::stock;

struct StockCalculationEngineWrapper : StockCalculationEngine, wrapper<StockCalculationEngine>
{
};

void export_auxi_modelling_accounting_stock_StockCalculationEngine()
{
  // Python C++ mappings

    //class_<StockCalculationEngine, StockCalculationEngine*, bases<NamedObject>>("StockCalculationEngine", init<>())
    class_<StockCalculationEngine, StockCalculationEngine*, bases<NamedObject>>("StockCalculationEngine", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    .def("create_stockLedgerStructure", make_function(&StockCalculationEngine::create_stockLedgerStructure, return_internal_reference<1>()))
	.def("remove_stockLedgerStructure", &StockCalculationEngine::remove_stockLedgerStructure)
	.def("to_string", &StockCalculationEngine::to_string)
	.add_property("stockLedgerStructureList", make_function(&StockCalculationEngine::GetStockLedgerStructureList, return_internal_reference<1>()))
    ;

    //implicitly_convertible<StockCalculationEngineWrapper*,StockCalculationEngine*>();
    implicitly_convertible<StockCalculationEngine*,NamedObject*>();
    class_<std::vector<StockCalculationEngine*>>("StockCalculationEngineList").def(vector_indexing_suite<std::vector<StockCalculationEngine*>>());
}