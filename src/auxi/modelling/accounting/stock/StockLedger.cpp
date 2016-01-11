#include "StockLedger.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockLedger::StockLedger()
{
    //ctor
}

StockLedger::StockLedger(const StockLedger& other)
{
    m_stockTransactionList = other.m_stockTransactionList;
    m_structure = other.m_structure;
}

StockLedger::~StockLedger()
{

    clean();
}

std::vector<StockTransaction*>& StockLedger::GetStockTransactionList() { return m_stockTransactionList; }
StockLedgerStructure* StockLedger::GetStructure() const { return m_structure; }
void StockLedger::SetStructure(StockLedgerStructure* value) { m_structure = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockLedger& lhs, const StockLedger& rhs)
    {
        return 1 == 1
	  && lhs.m_stockTransactionList == rhs.m_stockTransactionList
	  && lhs.m_structure == rhs.m_structure
	  ;
    }

    bool operator!=(const StockLedger& lhs, const StockLedger& rhs)
    {
        return 1 != 1
	  || lhs.m_stockTransactionList != rhs.m_stockTransactionList
	  || lhs.m_structure != rhs.m_structure
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockLedger& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
