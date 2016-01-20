#include "Currency.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

Currency::Currency()
{
    //ctor
}

Currency::Currency(const Currency& other)
{
    m_defaultExchangeRate = other.m_defaultExchangeRate;
}

Currency::~Currency()
{

}

double Currency::GetDefaultExchangeRate() const { return m_defaultExchangeRate; }
void Currency::SetDefaultExchangeRate(double value) { m_defaultExchangeRate = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const Currency& lhs, const Currency& rhs)
    {
        return 1 == 1
	  && almost_equal(lhs.m_defaultExchangeRate, rhs.m_defaultExchangeRate, 5)
	  ;
    }

    bool operator!=(const Currency& lhs, const Currency& rhs)
    {
        return 1 != 1
	  || !almost_equal(lhs.m_defaultExchangeRate, rhs.m_defaultExchangeRate, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const Currency& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
