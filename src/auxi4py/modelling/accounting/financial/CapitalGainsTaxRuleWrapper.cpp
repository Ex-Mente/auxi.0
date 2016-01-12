
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "CapitalGainsTaxRule.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct CapitalGainsTaxRuleWrapper : CapitalGainsTaxRule, wrapper<CapitalGainsTaxRule>
{
};

void export_auxi_modelling_accounting_financial_CapitalGainsTaxRule()
{
  // Python C++ mappings

    //class_<CapitalGainsTaxRule, CapitalGainsTaxRule*, bases<TaxRule>>("CapitalGainsTaxRule", init<>())
    class_<CapitalGainsTaxRule, CapitalGainsTaxRule*, bases<TaxRule>>("CapitalGainsTaxRule", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("percentage", &CapitalGainsTaxRule::GetPercentage, &CapitalGainsTaxRule::SetPercentage)
    ;

    //implicitly_convertible<CapitalGainsTaxRuleWrapper*,CapitalGainsTaxRule*>();
    implicitly_convertible<CapitalGainsTaxRule*,TaxRule*>();
    class_<std::vector<CapitalGainsTaxRule*>>("CapitalGainsTaxRuleList").def(vector_indexing_suite<std::vector<CapitalGainsTaxRule*>>());
}