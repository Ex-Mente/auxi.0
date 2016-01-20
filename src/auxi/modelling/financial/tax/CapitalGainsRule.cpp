#include "CapitalGainsRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::tax;

CapitalGainsRule::CapitalGainsRule()
{
    //ctor
}

CapitalGainsRule::CapitalGainsRule(const CapitalGainsRule& other)
{
    m_percentage = other.m_percentage;
}

CapitalGainsRule::~CapitalGainsRule()
{

}

double CapitalGainsRule::GetPercentage() const { return m_percentage; }
void CapitalGainsRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    bool operator==(const CapitalGainsRule& lhs, const CapitalGainsRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const CapitalGainsRule& lhs, const CapitalGainsRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const CapitalGainsRule& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
