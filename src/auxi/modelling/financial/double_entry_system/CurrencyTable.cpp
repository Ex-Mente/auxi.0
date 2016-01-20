#include "CurrencyTable.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

CurrencyTable::CurrencyTable()
{
    //ctor
}

CurrencyTable::CurrencyTable(const CurrencyTable& other)
{
    m_currencyList = other.m_currencyList;
    m_defaultCurrency = other.m_defaultCurrency;
}

CurrencyTable::~CurrencyTable()
{

}

std::vector<Currency*>& CurrencyTable::GetCurrencyList() { return m_currencyList; }
Currency* CurrencyTable::GetDefaultCurrency() const { return m_defaultCurrency; }
void CurrencyTable::SetDefaultCurrency(Currency* value) { m_defaultCurrency = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const CurrencyTable& lhs, const CurrencyTable& rhs)
    {
        return 1 == 1
	  && lhs.m_currencyList == rhs.m_currencyList
	  && lhs.m_defaultCurrency == rhs.m_defaultCurrency
	  ;
    }

    bool operator!=(const CurrencyTable& lhs, const CurrencyTable& rhs)
    {
        return 1 != 1
	  || lhs.m_currencyList != rhs.m_currencyList
	  || lhs.m_defaultCurrency != rhs.m_defaultCurrency
	;
    }

    std::ostream& operator<<(std::ostream& os, const CurrencyTable& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
