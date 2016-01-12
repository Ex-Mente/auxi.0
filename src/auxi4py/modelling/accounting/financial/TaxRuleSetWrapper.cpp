
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TaxRule.h"
#include "TaxRuleSet.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct TaxRuleSetWrapper : TaxRuleSet, wrapper<TaxRuleSet>
{
};

void export_auxi_modelling_accounting_financial_TaxRuleSet()
{
  // Python C++ mappings

    //class_<TaxRuleSet, TaxRuleSet*, bases<NamedObject>>("TaxRuleSet", init<>())
    class_<TaxRuleSet, TaxRuleSet*, bases<NamedObject>>("TaxRuleSet", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.add_property("taxRuleList", make_function(&TaxRuleSet::GetTaxRuleList, return_internal_reference<1>()))
	.add_property("code", &TaxRuleSet::GetCode, &TaxRuleSet::SetCode)
    ;

    //implicitly_convertible<TaxRuleSetWrapper*,TaxRuleSet*>();
    implicitly_convertible<TaxRuleSet*,NamedObject*>();
    class_<std::vector<TaxRuleSet*>>("TaxRuleSetList").def(vector_indexing_suite<std::vector<TaxRuleSet*>>());
}