#include "CapitalGainsTaxRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

CapitalGainsTaxRule::CapitalGainsTaxRule()
{
    //ctor
}

CapitalGainsTaxRule::CapitalGainsTaxRule(const CapitalGainsTaxRule& other)
{
    m_percentage = other.m_percentage;
}

CapitalGainsTaxRule::~CapitalGainsTaxRule()
{

}

double CapitalGainsTaxRule::GetPercentage() const { return m_percentage; }
void CapitalGainsTaxRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const CapitalGainsTaxRule& lhs, const CapitalGainsTaxRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const CapitalGainsTaxRule& lhs, const CapitalGainsTaxRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const CapitalGainsTaxRule& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
