#include "StockTransactionTemplate.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockTransactionTemplate::StockTransactionTemplate()
{
    //ctor
}

StockTransactionTemplate::StockTransactionTemplate(const StockTransactionTemplate& other)
{
    m_fromAccountName = other.m_fromAccountName;
    m_toAccountName = other.m_toAccountName;
}

StockTransactionTemplate::~StockTransactionTemplate()
{

}

std::string StockTransactionTemplate::GetFromAccountName() const { return m_fromAccountName; }
void StockTransactionTemplate::SetFromAccountName(std::string value) { m_fromAccountName = value; }
std::string StockTransactionTemplate::GetToAccountName() const { return m_toAccountName; }
void StockTransactionTemplate::SetToAccountName(std::string value) { m_toAccountName = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockTransactionTemplate& lhs, const StockTransactionTemplate& rhs)
    {
        return 1 == 1
	  && lhs.m_fromAccountName == rhs.m_fromAccountName
	  && lhs.m_toAccountName == rhs.m_toAccountName
	  ;
    }

    bool operator!=(const StockTransactionTemplate& lhs, const StockTransactionTemplate& rhs)
    {
        return 1 != 1
	  || lhs.m_fromAccountName != rhs.m_fromAccountName
	  || lhs.m_toAccountName != rhs.m_toAccountName
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockTransactionTemplate& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
