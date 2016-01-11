#include "StockTransaction.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::stock;

StockTransaction::StockTransaction()
{
    //ctor
}

StockTransaction::StockTransaction(const StockTransaction& other)
{
    m_date = other.m_date;
    m_fromAccountName = other.m_fromAccountName;
    m_toAccountName = other.m_toAccountName;
    m_currency = other.m_currency;
    m_source = other.m_source;
    m_amount = other.m_amount;
}

StockTransaction::~StockTransaction()
{

}

boost::posix_time::ptime StockTransaction::GetDate() const { return m_date; }
void StockTransaction::SetDate(boost::posix_time::ptime value) { m_date = value; }
std::string StockTransaction::GetFromAccountName() const { return m_fromAccountName; }
void StockTransaction::SetFromAccountName(std::string value) { m_fromAccountName = value; }
std::string StockTransaction::GetToAccountName() const { return m_toAccountName; }
void StockTransaction::SetToAccountName(std::string value) { m_toAccountName = value; }
Units& StockTransaction::GetCurrency() { return m_currency; }
void StockTransaction::SetCurrency(Units& value) { m_currency = value; }
std::string StockTransaction::GetSource() const { return m_source; }
void StockTransaction::SetSource(std::string value) { m_source = value; }
double StockTransaction::GetAmount() const { return m_amount; }
void StockTransaction::SetAmount(double value) { m_amount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    bool operator==(const StockTransaction& lhs, const StockTransaction& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_fromAccountName == rhs.m_fromAccountName
	  && lhs.m_toAccountName == rhs.m_toAccountName
	  && lhs.m_currency == rhs.m_currency
	  && lhs.m_source == rhs.m_source
	  && almost_equal(lhs.m_amount, rhs.m_amount, 5)
	  ;
    }

    bool operator!=(const StockTransaction& lhs, const StockTransaction& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_fromAccountName != rhs.m_fromAccountName
	  || lhs.m_toAccountName != rhs.m_toAccountName
	  || lhs.m_currency != rhs.m_currency
	  || lhs.m_source != rhs.m_source
	  || !almost_equal(lhs.m_amount, rhs.m_amount, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const StockTransaction& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
