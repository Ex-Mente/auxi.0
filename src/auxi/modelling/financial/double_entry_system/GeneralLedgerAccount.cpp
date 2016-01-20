#include "GeneralLedgerAccount.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

GeneralLedgerAccount::GeneralLedgerAccount()
{
    //ctor
}

GeneralLedgerAccount::GeneralLedgerAccount(const GeneralLedgerAccount& other)
{
    m_accountList = other.m_accountList;
    m_number = other.m_number;
    m_type = other.m_type;
}

GeneralLedgerAccount::~GeneralLedgerAccount()
{

    clean();
}

std::vector<GeneralLedgerAccount*>& GeneralLedgerAccount::GetAccountList() { return m_accountList; }
std::string GeneralLedgerAccount::GetNumber() const { return m_number; }
void GeneralLedgerAccount::SetNumber(std::string value) { m_number = value; }
AccountType::AccountType GeneralLedgerAccount::GetType() const { return m_type; }
void GeneralLedgerAccount::SetType(AccountType::AccountType value) { m_type = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const GeneralLedgerAccount& lhs, const GeneralLedgerAccount& rhs)
    {
        return 1 == 1
	  && lhs.m_accountList == rhs.m_accountList
	  && lhs.m_number == rhs.m_number
	  && lhs.m_type == rhs.m_type
	  ;
    }

    bool operator!=(const GeneralLedgerAccount& lhs, const GeneralLedgerAccount& rhs)
    {
        return 1 != 1
	  || lhs.m_accountList != rhs.m_accountList
	  || lhs.m_number != rhs.m_number
	  || lhs.m_type != rhs.m_type
	;
    }

    std::ostream& operator<<(std::ostream& os, const GeneralLedgerAccount& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
