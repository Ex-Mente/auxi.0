#include "IncomeRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::tax;

IncomeRule::IncomeRule()
{
    //ctor
}

IncomeRule::IncomeRule(const IncomeRule& other)
{
    m_percentage = other.m_percentage;
}

IncomeRule::~IncomeRule()
{

}

double IncomeRule::GetPercentage() const { return m_percentage; }
void IncomeRule::SetPercentage(double value) { m_percentage = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    bool operator==(const IncomeRule& lhs, const IncomeRule& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	  ;
    }

    bool operator!=(const IncomeRule& lhs, const IncomeRule& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_percentage, rhs.m_percentage, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const IncomeRule& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
