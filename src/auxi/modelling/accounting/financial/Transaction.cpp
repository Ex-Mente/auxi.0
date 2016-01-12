#include "Transaction.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

Transaction::Transaction()
{
    //ctor
}

Transaction::Transaction(const Transaction& other)
{
    m_date = other.m_date;
    m_creditAccountName = other.m_creditAccountName;
    m_debitAccountName = other.m_debitAccountName;
    m_currency = other.m_currency;
    m_source = other.m_source;
    m_isClosingCreditAccount = other.m_isClosingCreditAccount;
    m_isClosingDebitAccount = other.m_isClosingDebitAccount;
    m_amount = other.m_amount;
}

Transaction::~Transaction()
{

}

boost::posix_time::ptime Transaction::GetDate() const { return m_date; }
void Transaction::SetDate(boost::posix_time::ptime value) { m_date = value; }
std::string Transaction::GetCreditAccountName() const { return m_creditAccountName; }
void Transaction::SetCreditAccountName(std::string value) { m_creditAccountName = value; }
std::string Transaction::GetDebitAccountName() const { return m_debitAccountName; }
void Transaction::SetDebitAccountName(std::string value) { m_debitAccountName = value; }
Units& Transaction::GetCurrency() { return m_currency; }
void Transaction::SetCurrency(Units& value) { m_currency = value; }
std::string Transaction::GetSource() const { return m_source; }
void Transaction::SetSource(std::string value) { m_source = value; }
bool Transaction::GetIsClosingCreditAccount() const { return m_isClosingCreditAccount; }
void Transaction::SetIsClosingCreditAccount(bool value) { m_isClosingCreditAccount = value; }
bool Transaction::GetIsClosingDebitAccount() const { return m_isClosingDebitAccount; }
void Transaction::SetIsClosingDebitAccount(bool value) { m_isClosingDebitAccount = value; }
double Transaction::GetAmount() const { return m_amount; }
void Transaction::SetAmount(double value) { m_amount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const Transaction& lhs, const Transaction& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_creditAccountName == rhs.m_creditAccountName
	  && lhs.m_debitAccountName == rhs.m_debitAccountName
	  && lhs.m_currency == rhs.m_currency
	  && lhs.m_source == rhs.m_source
	  && lhs.m_isClosingCreditAccount == rhs.m_isClosingCreditAccount
	  && lhs.m_isClosingDebitAccount == rhs.m_isClosingDebitAccount
	  && almost_equal(lhs.m_amount, rhs.m_amount, 5)
	  ;
    }

    bool operator!=(const Transaction& lhs, const Transaction& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_creditAccountName != rhs.m_creditAccountName
	  || lhs.m_debitAccountName != rhs.m_debitAccountName
	  || lhs.m_currency != rhs.m_currency
	  || lhs.m_source != rhs.m_source
	  || lhs.m_isClosingCreditAccount != rhs.m_isClosingCreditAccount
	  || lhs.m_isClosingDebitAccount != rhs.m_isClosingDebitAccount
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
