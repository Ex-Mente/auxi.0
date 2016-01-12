#include "GeneralLedgerStructure.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::accounting::financial;

GeneralLedgerStructure::GeneralLedgerStructure()
{
    //ctor
    initialize();
}

GeneralLedgerStructure::GeneralLedgerStructure(const GeneralLedgerStructure& other)
{
    m_accountList = other.m_accountList;
    m_bankAccount = other.m_bankAccount;
    m_incomeTaxPayableAccount = other.m_incomeTaxPayableAccount;
    m_incomeTaxExpenseAccount = other.m_incomeTaxExpenseAccount;
    m_salesAccount = other.m_salesAccount;
    m_costOfSalesAccount = other.m_costOfSalesAccount;
    m_grossProfitAccount = other.m_grossProfitAccount;
    m_incomeSummaryAccount = other.m_incomeSummaryAccount;
    m_retainedEarningsAccount = other.m_retainedEarningsAccount;
}

GeneralLedgerStructure::~GeneralLedgerStructure()
{

    clean();
}

std::vector<GeneralLedgerAccount*>& GeneralLedgerStructure::GetAccountList() { return m_accountList; }
GeneralLedgerAccount* GeneralLedgerStructure::GetBankAccount() const { return m_bankAccount; }
void GeneralLedgerStructure::SetBankAccount(GeneralLedgerAccount* value) { m_bankAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeTaxPayableAccount() const { return m_incomeTaxPayableAccount; }
void GeneralLedgerStructure::SetIncomeTaxPayableAccount(GeneralLedgerAccount* value) { m_incomeTaxPayableAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeTaxExpenseAccount() const { return m_incomeTaxExpenseAccount; }
void GeneralLedgerStructure::SetIncomeTaxExpenseAccount(GeneralLedgerAccount* value) { m_incomeTaxExpenseAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetSalesAccount() const { return m_salesAccount; }
void GeneralLedgerStructure::SetSalesAccount(GeneralLedgerAccount* value) { m_salesAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetCostOfSalesAccount() const { return m_costOfSalesAccount; }
void GeneralLedgerStructure::SetCostOfSalesAccount(GeneralLedgerAccount* value) { m_costOfSalesAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetGrossProfitAccount() const { return m_grossProfitAccount; }
void GeneralLedgerStructure::SetGrossProfitAccount(GeneralLedgerAccount* value) { m_grossProfitAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeSummaryAccount() const { return m_incomeSummaryAccount; }
void GeneralLedgerStructure::SetIncomeSummaryAccount(GeneralLedgerAccount* value) { m_incomeSummaryAccount = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetRetainedEarningsAccount() const { return m_retainedEarningsAccount; }
void GeneralLedgerStructure::SetRetainedEarningsAccount(GeneralLedgerAccount* value) { m_retainedEarningsAccount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    bool operator==(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs)
    {
        return 1 == 1
	  && lhs.m_accountList == rhs.m_accountList
	  && lhs.m_bankAccount == rhs.m_bankAccount
	  && lhs.m_incomeTaxPayableAccount == rhs.m_incomeTaxPayableAccount
	  && lhs.m_incomeTaxExpenseAccount == rhs.m_incomeTaxExpenseAccount
	  && lhs.m_salesAccount == rhs.m_salesAccount
	  && lhs.m_costOfSalesAccount == rhs.m_costOfSalesAccount
	  && lhs.m_grossProfitAccount == rhs.m_grossProfitAccount
	  && lhs.m_incomeSummaryAccount == rhs.m_incomeSummaryAccount
	  && lhs.m_retainedEarningsAccount == rhs.m_retainedEarningsAccount
	  ;
    }

    bool operator!=(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs)
    {
        return 1 != 1
	  || lhs.m_accountList != rhs.m_accountList
	  || lhs.m_bankAccount != rhs.m_bankAccount
	  || lhs.m_incomeTaxPayableAccount != rhs.m_incomeTaxPayableAccount
	  || lhs.m_incomeTaxExpenseAccount != rhs.m_incomeTaxExpenseAccount
	  || lhs.m_salesAccount != rhs.m_salesAccount
	  || lhs.m_costOfSalesAccount != rhs.m_costOfSalesAccount
	  || lhs.m_grossProfitAccount != rhs.m_grossProfitAccount
	  || lhs.m_incomeSummaryAccount != rhs.m_incomeSummaryAccount
	  || lhs.m_retainedEarningsAccount != rhs.m_retainedEarningsAccount
	;
    }

    std::ostream& operator<<(std::ostream& os, const GeneralLedgerStructure& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
}
