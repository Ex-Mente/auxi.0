#include "FinancialCalculationEngine.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::calculation_engines;

FinancialCalculationEngine::FinancialCalculationEngine()
{
    //ctor
}

FinancialCalculationEngine::FinancialCalculationEngine(const FinancialCalculationEngine& other)
{
    m_generalLedgerStructureList = other.m_generalLedgerStructureList;
}

FinancialCalculationEngine::~FinancialCalculationEngine()
{

    clean();
}

std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerStructure*>& FinancialCalculationEngine::GetGeneralLedgerStructureList() { return m_generalLedgerStructureList; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace calculation_engines { 
    bool operator==(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs)
    {
        return 1 == 1
	  && lhs.m_generalLedgerStructureList == rhs.m_generalLedgerStructureList
	  ;
    }

    bool operator!=(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs)
    {
        return 1 != 1
	  || lhs.m_generalLedgerStructureList != rhs.m_generalLedgerStructureList
	;
    }

    std::ostream& operator<<(std::ostream& os, const FinancialCalculationEngine& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
