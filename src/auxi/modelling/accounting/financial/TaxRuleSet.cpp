#include "TaxRuleSet.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

TaxRuleSet::TaxRuleSet()
{
    //ctor
}

TaxRuleSet::TaxRuleSet(const TaxRuleSet& other)
{
    m_taxRuleList = other.m_taxRuleList;
    m_code = other.m_code;
}

TaxRuleSet::~TaxRuleSet()
{

}

std::vector<TaxRule*>& TaxRuleSet::GetTaxRuleList() { return m_taxRuleList; }
std::string TaxRuleSet::GetCode() const { return m_code; }
void TaxRuleSet::SetCode(std::string value) { m_code = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const TaxRuleSet& lhs, const TaxRuleSet& rhs)
    {
        return 1 == 1
	  && lhs.m_taxRuleList == rhs.m_taxRuleList
	  && lhs.m_code == rhs.m_code
	  ;
    }

    bool operator!=(const TaxRuleSet& lhs, const TaxRuleSet& rhs)
    {
        return 1 != 1
	  || lhs.m_taxRuleList != rhs.m_taxRuleList
	  || lhs.m_code != rhs.m_code
	;
    }

    std::ostream& operator<<(std::ostream& os, const TaxRuleSet& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
