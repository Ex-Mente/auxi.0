#include "GeneralLedger.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

GeneralLedger::GeneralLedger()
{
    //ctor
}

GeneralLedger::GeneralLedger(const GeneralLedger& other)
{
    m_transactionList = other.m_transactionList;
    m_structure = other.m_structure;
}

GeneralLedger::~GeneralLedger()
{

    clean();
}

std::vector<Transaction*>& GeneralLedger::GetTransactionList() { return m_transactionList; }
GeneralLedgerStructure* GeneralLedger::GetStructure() const { return m_structure; }
void GeneralLedger::SetStructure(GeneralLedgerStructure* value) { m_structure = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const GeneralLedger& lhs, const GeneralLedger& rhs)
    {
        return 1 == 1
	  && lhs.m_transactionList == rhs.m_transactionList
	  && lhs.m_structure == rhs.m_structure
	  ;
    }

    bool operator!=(const GeneralLedger& lhs, const GeneralLedger& rhs)
    {
        return 1 != 1
	  || lhs.m_transactionList != rhs.m_transactionList
	  || lhs.m_structure != rhs.m_structure
	;
    }

    std::ostream& operator<<(std::ostream& os, const GeneralLedger& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
