#include "TransactionTemplate.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

TransactionTemplate::TransactionTemplate()
{
    //ctor
}

TransactionTemplate::TransactionTemplate(const TransactionTemplate& other)
{
    m_debitAccountName = other.m_debitAccountName;
    m_creditAccountName = other.m_creditAccountName;
}

TransactionTemplate::~TransactionTemplate()
{

}

std::string TransactionTemplate::GetDebitAccountName() const { return m_debitAccountName; }
void TransactionTemplate::SetDebitAccountName(std::string value) { m_debitAccountName = value; }
std::string TransactionTemplate::GetCreditAccountName() const { return m_creditAccountName; }
void TransactionTemplate::SetCreditAccountName(std::string value) { m_creditAccountName = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const TransactionTemplate& lhs, const TransactionTemplate& rhs)
    {
        return 1 == 1
	  && lhs.m_debitAccountName == rhs.m_debitAccountName
	  && lhs.m_creditAccountName == rhs.m_creditAccountName
	  ;
    }

    bool operator!=(const TransactionTemplate& lhs, const TransactionTemplate& rhs)
    {
        return 1 != 1
	  || lhs.m_debitAccountName != rhs.m_debitAccountName
	  || lhs.m_creditAccountName != rhs.m_creditAccountName
	;
    }

    std::ostream& operator<<(std::ostream& os, const TransactionTemplate& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
