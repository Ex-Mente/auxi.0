#include "SalesRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::tax;

SalesRule::SalesRule()
{
    //ctor
}

SalesRule::SalesRule(const SalesRule& other)
{
    m_percentage = other.m_percentage;
}

SalesRule::~SalesRule()
{

}

double SalesRule::GetPercentage() const { return m_percentage; }
void SalesRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    bool operator==(const SalesRule& lhs, const SalesRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const SalesRule& lhs, const SalesRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const SalesRule& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
