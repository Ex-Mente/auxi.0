#include "StockLedgerStructure.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockLedgerStructure::StockLedgerStructure()
{
    //ctor
    initialize();
}

StockLedgerStructure::StockLedgerStructure(const StockLedgerStructure& other)
{
    m_accountList = other.m_accountList;
    m_miscAccount = other.m_miscAccount;
}

StockLedgerStructure::~StockLedgerStructure()
{

    clean();
}

std::vector<StockLedgerAccount*>& StockLedgerStructure::GetAccountList() { return m_accountList; }
StockLedgerAccount* StockLedgerStructure::GetMiscAccount() const { return m_miscAccount; }
void StockLedgerStructure::SetMiscAccount(StockLedgerAccount* value) { m_miscAccount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockLedgerStructure& lhs, const StockLedgerStructure& rhs)
    {
        return 1 == 1
	  && lhs.m_accountList == rhs.m_accountList
	  && lhs.m_miscAccount == rhs.m_miscAccount
	  ;
    }

    bool operator!=(const StockLedgerStructure& lhs, const StockLedgerStructure& rhs)
    {
        return 1 != 1
	  || lhs.m_accountList != rhs.m_accountList
	  || lhs.m_miscAccount != rhs.m_miscAccount
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockLedgerStructure& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
