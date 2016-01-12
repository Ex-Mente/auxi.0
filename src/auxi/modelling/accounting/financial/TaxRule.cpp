#include "TaxRule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

TaxRule::TaxRule()
{
    //ctor
}

TaxRule::TaxRule(const TaxRule& other)
{
}

TaxRule::~TaxRule()
{

}



    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const TaxRule& lhs, const TaxRule& rhs)
    {
        return 1 == 1
	  ;
    }

    bool operator!=(const TaxRule& lhs, const TaxRule& rhs)
    {
        return 1 != 1
	;
    }

    std::ostream& operator<<(std::ostream& os, const TaxRule& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
