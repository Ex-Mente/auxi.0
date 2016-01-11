#include "SalesTaxRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

SalesTaxRule::SalesTaxRule()
{
    //ctor
}

SalesTaxRule::SalesTaxRule(const SalesTaxRule& other)
{
    m_percentage = other.m_percentage;
}

SalesTaxRule::~SalesTaxRule()
{

}

double SalesTaxRule::GetPercentage() const { return m_percentage; }
void SalesTaxRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const SalesTaxRule& lhs, const SalesTaxRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const SalesTaxRule& lhs, const SalesTaxRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const SalesTaxRule& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
