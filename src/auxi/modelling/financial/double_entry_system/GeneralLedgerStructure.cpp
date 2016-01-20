#include "GeneralLedgerStructure.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::financial::double_entry_system;

GeneralLedgerStructure::GeneralLedgerStructure()
{
    //ctor
    initialize();
}

GeneralLedgerStructure::GeneralLedgerStructure(const GeneralLedgerStructure& other)
{
    m_accountList = other.m_accountList;
    m_bank = other.m_bank;
    m_incomeTaxPayable = other.m_incomeTaxPayable;
    m_incomeTaxExpense = other.m_incomeTaxExpense;
    m_sales = other.m_sales;
    m_costOfSales = other.m_costOfSales;
    m_grossProfit = other.m_grossProfit;
    m_incomeSummary = other.m_incomeSummary;
    m_retainedEarnings = other.m_retainedEarnings;
    m_taxPaymentAccount = other.m_taxPaymentAccount;
}

GeneralLedgerStructure::~GeneralLedgerStructure()
{

    clean();
}

std::vector<GeneralLedgerAccount*>& GeneralLedgerStructure::GetAccountList() { return m_accountList; }
GeneralLedgerAccount* GeneralLedgerStructure::GetBank() const { return m_bank; }
void GeneralLedgerStructure::SetBank(GeneralLedgerAccount* value) { m_bank = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeTaxPayable() const { return m_incomeTaxPayable; }
void GeneralLedgerStructure::SetIncomeTaxPayable(GeneralLedgerAccount* value) { m_incomeTaxPayable = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeTaxExpense() const { return m_incomeTaxExpense; }
void GeneralLedgerStructure::SetIncomeTaxExpense(GeneralLedgerAccount* value) { m_incomeTaxExpense = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetSales() const { return m_sales; }
void GeneralLedgerStructure::SetSales(GeneralLedgerAccount* value) { m_sales = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetCostOfSales() const { return m_costOfSales; }
void GeneralLedgerStructure::SetCostOfSales(GeneralLedgerAccount* value) { m_costOfSales = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetGrossProfit() const { return m_grossProfit; }
void GeneralLedgerStructure::SetGrossProfit(GeneralLedgerAccount* value) { m_grossProfit = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetIncomeSummary() const { return m_incomeSummary; }
void GeneralLedgerStructure::SetIncomeSummary(GeneralLedgerAccount* value) { m_incomeSummary = value; }
GeneralLedgerAccount* GeneralLedgerStructure::GetRetainedEarnings() const { return m_retainedEarnings; }
void GeneralLedgerStructure::SetRetainedEarnings(GeneralLedgerAccount* value) { m_retainedEarnings = value; }
std::string GeneralLedgerStructure::GetTaxPaymentAccount() const { return m_taxPaymentAccount; }
void GeneralLedgerStructure::SetTaxPaymentAccount(std::string value) { m_taxPaymentAccount = value; }


    
    
    
    
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    bool operator==(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs)
    {
        return 1 == 1
	  && lhs.m_accountList == rhs.m_accountList
	  && lhs.m_bank == rhs.m_bank
	  && lhs.m_incomeTaxPayable == rhs.m_incomeTaxPayable
	  && lhs.m_incomeTaxExpense == rhs.m_incomeTaxExpense
	  && lhs.m_sales == rhs.m_sales
	  && lhs.m_costOfSales == rhs.m_costOfSales
	  && lhs.m_grossProfit == rhs.m_grossProfit
	  && lhs.m_incomeSummary == rhs.m_incomeSummary
	  && lhs.m_retainedEarnings == rhs.m_retainedEarnings
	  && lhs.m_taxPaymentAccount == rhs.m_taxPaymentAccount
	  ;
    }

    bool operator!=(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs)
    {
        return 1 != 1
	  || lhs.m_accountList != rhs.m_accountList
	  || lhs.m_bank != rhs.m_bank
	  || lhs.m_incomeTaxPayable != rhs.m_incomeTaxPayable
	  || lhs.m_incomeTaxExpense != rhs.m_incomeTaxExpense
	  || lhs.m_sales != rhs.m_sales
	  || lhs.m_costOfSales != rhs.m_costOfSales
	  || lhs.m_grossProfit != rhs.m_grossProfit
	  || lhs.m_incomeSummary != rhs.m_incomeSummary
	  || lhs.m_retainedEarnings != rhs.m_retainedEarnings
	  || lhs.m_taxPaymentAccount != rhs.m_taxPaymentAccount
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
