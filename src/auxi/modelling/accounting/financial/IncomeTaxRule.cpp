#include "IncomeTaxRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

IncomeTaxRule::IncomeTaxRule()
{
    //ctor
}

IncomeTaxRule::IncomeTaxRule(const IncomeTaxRule& other)
{
    m_percentage = other.m_percentage;
}

IncomeTaxRule::~IncomeTaxRule()
{

}

double IncomeTaxRule::GetPercentage() const { return m_percentage; }
void IncomeTaxRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const IncomeTaxRule& lhs, const IncomeTaxRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const IncomeTaxRule& lhs, const IncomeTaxRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const IncomeTaxRule& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
