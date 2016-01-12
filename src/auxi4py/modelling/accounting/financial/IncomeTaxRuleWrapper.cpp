
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "IncomeTaxRule.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct IncomeTaxRuleWrapper : IncomeTaxRule, wrapper<IncomeTaxRule>
{
};

void export_auxi_modelling_accounting_financial_IncomeTaxRule()
{
  // Python C++ mappings

    //class_<IncomeTaxRule, IncomeTaxRule*, bases<TaxRule>>("IncomeTaxRule", init<>())
    class_<IncomeTaxRule, IncomeTaxRule*, bases<TaxRule>>("IncomeTaxRule", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("percentage", &IncomeTaxRule::GetPercentage, &IncomeTaxRule::SetPercentage)
    ;

    //implicitly_convertible<IncomeTaxRuleWrapper*,IncomeTaxRule*>();
    implicitly_convertible<IncomeTaxRule*,TaxRule*>();
    class_<std::vector<IncomeTaxRule*>>("IncomeTaxRuleList").def(vector_indexing_suite<std::vector<IncomeTaxRule*>>());
}