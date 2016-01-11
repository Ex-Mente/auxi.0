#include "StockLedgerAccount.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockLedgerAccount::StockLedgerAccount()
{
    //ctor
}

StockLedgerAccount::StockLedgerAccount(const StockLedgerAccount& other)
{
    m_accountList = other.m_accountList;
    m_number = other.m_number;
    m_type = other.m_type;
}

StockLedgerAccount::~StockLedgerAccount()
{

    clean();
}

std::vector<StockLedgerAccount*>& StockLedgerAccount::GetAccountList() { return m_accountList; }
std::string StockLedgerAccount::GetNumber() const { return m_number; }
void StockLedgerAccount::SetNumber(std::string value) { m_number = value; }
StockLedgerAccountType::StockLedgerAccountType StockLedgerAccount::GetType() const { return m_type; }
void StockLedgerAccount::SetType(StockLedgerAccountType::StockLedgerAccountType value) { m_type = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockLedgerAccount& lhs, const StockLedgerAccount& rhs)
    {
        return 1 == 1
	  && lhs.m_accountList == rhs.m_accountList
	  && lhs.m_number == rhs.m_number
	  && lhs.m_type == rhs.m_type
	  ;
    }

    bool operator!=(const StockLedgerAccount& lhs, const StockLedgerAccount& rhs)
    {
        return 1 != 1
	  || lhs.m_accountList != rhs.m_accountList
	  || lhs.m_number != rhs.m_number
	  || lhs.m_type != rhs.m_type
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockLedgerAccount& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
