
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TaxRule.h"

using namespace boost::python;
using namespace auxi::modelling::accounting::financial;

struct TaxRuleWrapper : TaxRule, wrapper<TaxRule>
{
};

void export_auxi_modelling_accounting_financial_TaxRule()
{
  // Python C++ mappings

    //class_<TaxRule, TaxRule*, bases<NamedObject>>("TaxRule", init<>())
    class_<TaxRule, TaxRule*, bases<NamedObject>>("TaxRule", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    ;

    //implicitly_convertible<TaxRuleWrapper*,TaxRule*>();
    implicitly_convertible<TaxRule*,NamedObject*>();
    class_<std::vector<TaxRule*>>("TaxRuleList").def(vector_indexing_suite<std::vector<TaxRule*>>());
}