#include "StockCalculationEngine.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockCalculationEngine::StockCalculationEngine()
{
    //ctor
}

StockCalculationEngine::StockCalculationEngine(const StockCalculationEngine& other)
{
    m_stockLedgerStructureList = other.m_stockLedgerStructureList;
}

StockCalculationEngine::~StockCalculationEngine()
{

    clean();
}

std::vector<StockLedgerStructure*>& StockCalculationEngine::GetStockLedgerStructureList() { return m_stockLedgerStructureList; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockCalculationEngine& lhs, const StockCalculationEngine& rhs)
    {
        return 1 == 1
	  && lhs.m_stockLedgerStructureList == rhs.m_stockLedgerStructureList
	  ;
    }

    bool operator!=(const StockCalculationEngine& lhs, const StockCalculationEngine& rhs)
    {
        return 1 != 1
	  || lhs.m_stockLedgerStructureList != rhs.m_stockLedgerStructureList
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockCalculationEngine& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
