
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "SalesTaxRule.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct SalesTaxRuleWrapper : SalesTaxRule, wrapper<SalesTaxRule>
{
};

void export_auxi_modelling_accounting_financial_SalesTaxRule()
{
  // Python C++ mappings

    //class_<SalesTaxRule, SalesTaxRule*, bases<TaxRule>>("SalesTaxRule", init<>())
    class_<SalesTaxRule, SalesTaxRule*, bases<TaxRule>>("SalesTaxRule", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("percentage", &SalesTaxRule::GetPercentage, &SalesTaxRule::SetPercentage)
    ;

    //implicitly_convertible<SalesTaxRuleWrapper*,SalesTaxRule*>();
    implicitly_convertible<SalesTaxRule*,TaxRule*>();
    class_<std::vector<SalesTaxRule*>>("SalesTaxRuleList").def(vector_indexing_suite<std::vector<SalesTaxRule*>>());
}