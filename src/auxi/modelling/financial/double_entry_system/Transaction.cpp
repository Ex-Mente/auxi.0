#include "Transaction.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

Transaction::Transaction()
{
    //ctor
}

Transaction::Transaction(const Transaction& other)
{
    m_date = other.m_date;
    m_crAccount = other.m_crAccount;
    m_dtAccount = other.m_dtAccount;
    m_currency = other.m_currency;
    m_source = other.m_source;
    m_isClosingCrAccount = other.m_isClosingCrAccount;
    m_isClosingDtAccount = other.m_isClosingDtAccount;
    m_amount = other.m_amount;
}

Transaction::~Transaction()
{

}

boost::posix_time::ptime Transaction::GetDate() const { return m_date; }
void Transaction::SetDate(boost::posix_time::ptime value) { m_date = value; }
std::string Transaction::GetCrAccount() const { return m_crAccount; }
void Transaction::SetCrAccount(std::string value) { m_crAccount = value; }
std::string Transaction::GetDtAccount() const { return m_dtAccount; }
void Transaction::SetDtAccount(std::string value) { m_dtAccount = value; }
Units& Transaction::GetCurrency() { return m_currency; }
void Transaction::SetCurrency(Units& value) { m_currency = value; }
std::string Transaction::GetSource() const { return m_source; }
void Transaction::SetSource(std::string value) { m_source = value; }
bool Transaction::GetIsClosingCrAccount() const { return m_isClosingCrAccount; }
void Transaction::SetIsClosingCrAccount(bool value) { m_isClosingCrAccount = value; }
bool Transaction::GetIsClosingDtAccount() const { return m_isClosingDtAccount; }
void Transaction::SetIsClosingDtAccount(bool value) { m_isClosingDtAccount = value; }
double Transaction::GetAmount() const { return m_amount; }
void Transaction::SetAmount(double value) { m_amount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const Transaction& lhs, const Transaction& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_crAccount == rhs.m_crAccount
	  && lhs.m_dtAccount == rhs.m_dtAccount
	  && lhs.m_currency == rhs.m_currency
	  && lhs.m_source == rhs.m_source
	  && lhs.m_isClosingCrAccount == rhs.m_isClosingCrAccount
	  && lhs.m_isClosingDtAccount == rhs.m_isClosingDtAccount
	  && almost_equal(lhs.m_amount, rhs.m_amount, 5)
	  ;
    }

    bool operator!=(const Transaction& lhs, const Transaction& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_crAccount != rhs.m_crAccount
	  || lhs.m_dtAccount != rhs.m_dtAccount
	  || lhs.m_currency != rhs.m_currency
	  || lhs.m_source != rhs.m_source
	  || lhs.m_isClosingCrAccount != rhs.m_isClosingCrAccount
	  || lhs.m_isClosingDtAccount != rhs.m_isClosingDtAccount
	  || !almost_equal(lhs.m_amount, rhs.m_amount, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const Transaction& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
