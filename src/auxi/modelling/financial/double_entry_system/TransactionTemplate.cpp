#include "TransactionTemplate.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

TransactionTemplate::TransactionTemplate()
{
    //ctor
}

TransactionTemplate::TransactionTemplate(const TransactionTemplate& other)
{
    m_dtAccount = other.m_dtAccount;
    m_crAccount = other.m_crAccount;
}

TransactionTemplate::~TransactionTemplate()
{

}

std::string TransactionTemplate::GetDtAccount() const { return m_dtAccount; }
void TransactionTemplate::SetDtAccount(std::string value) { m_dtAccount = value; }
std::string TransactionTemplate::GetCrAccount() const { return m_crAccount; }
void TransactionTemplate::SetCrAccount(std::string value) { m_crAccount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const TransactionTemplate& lhs, const TransactionTemplate& rhs)
    {
        return 1 == 1
	  && lhs.m_dtAccount == rhs.m_dtAccount
	  && lhs.m_crAccount == rhs.m_crAccount
	  ;
    }

    bool operator!=(const TransactionTemplate& lhs, const TransactionTemplate& rhs)
    {
        return 1 != 1
	  || lhs.m_dtAccount != rhs.m_dtAccount
	  || lhs.m_crAccount != rhs.m_crAccount
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
