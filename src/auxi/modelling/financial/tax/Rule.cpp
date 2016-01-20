#include "Rule.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::tax;

Rule::Rule()
{
    //ctor
}

Rule::Rule(const Rule& other)
{
}

Rule::~Rule()
{

}



    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    bool operator==(const Rule& lhs, const Rule& rhs)
    {
        return 1 == 1
	  ;
    }

    bool operator!=(const Rule& lhs, const Rule& rhs)
    {
        return 1 != 1
	;
    }

    std::ostream& operator<<(std::ostream& os, const Rule& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
