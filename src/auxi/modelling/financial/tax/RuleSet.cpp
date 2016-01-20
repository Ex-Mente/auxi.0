#include "RuleSet.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::tax;

RuleSet::RuleSet()
{
    //ctor
}

RuleSet::RuleSet(const RuleSet& other)
{
    m_ruleList = other.m_ruleList;
    m_code = other.m_code;
}

RuleSet::~RuleSet()
{

}

std::vector<Rule*>& RuleSet::GetRuleList() { return m_ruleList; }
std::string RuleSet::GetCode() const { return m_code; }
void RuleSet::SetCode(std::string value) { m_code = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    bool operator==(const RuleSet& lhs, const RuleSet& rhs)
    {
        return 1 == 1
	  && lhs.m_ruleList == rhs.m_ruleList
	  && lhs.m_code == rhs.m_code
	  ;
    }

    bool operator!=(const RuleSet& lhs, const RuleSet& rhs)
    {
        return 1 != 1
	  || lhs.m_ruleList != rhs.m_ruleList
	  || lhs.m_code != rhs.m_code
	;
    }

    std::ostream& operator<<(std::ostream& os, const RuleSet& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
