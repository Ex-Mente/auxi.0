#include "GeneralLedgerStructure.h"

using namespace auxi::modelling::accounting::financial;

void GeneralLedgerStructure::initialize()
{
    m_bankAccount = create_account("Bank", "Bank", GeneralLedgerAccountType::Asset);
    m_incomeTaxPayableAccount = create_account("IncomeTaxPayable", "IncomeTaxPayable", GeneralLedgerAccountType::Liability);
    m_incomeTaxExpenseAccount = create_account("IncomeTaxExpense", "IncomeTaxExpense", GeneralLedgerAccountType::Expense);
    m_salesAccount = create_account("Sales", "Sales", GeneralLedgerAccountType::Revenue);
    m_costOfSalesAccount = create_account("CostOfSales", "CostOfSales", GeneralLedgerAccountType::Expense);
    m_grossProfitAccount = create_account("GrossProfit", "GrossProfit", GeneralLedgerAccountType::Revenue);
    m_incomeSummaryAccount = create_account("IncomeSummary", "IncomeSummary", GeneralLedgerAccountType::Revenue);
    m_retainedEarningsAccount = create_account("RetainedEarnings", "RetainedEarnings", GeneralLedgerAccountType::Equity);
}

void GeneralLedgerStructure::clean()
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
        delete (*itr);
    m_accountList.clear();
}

GeneralLedgerAccount* GeneralLedgerStructure::create_account(std::string name, std::string number, GeneralLedgerAccountType::GeneralLedgerAccountType type)
{
    auto acc = new GeneralLedgerAccount(name, "");
    acc->SetNumber(number);
    acc->SetType(type);

    m_accountList.push_back(acc);
    return acc;
}

void GeneralLedgerStructure::remove_account(std::string number)
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
    {
        if((*itr)->GetNumber() == number)
        {
           delete (*itr);
           m_accountList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The account number: '" + number + "' does not exist in the account's account list'.");
}

GeneralLedgerAccount* get_account_from_child(std::vector<GeneralLedgerAccount*>& account_list, std::string account_name)
{
    for(auto itr = account_list.begin(); itr != account_list.end(); ++itr)
    {
        if((*itr)->GetName() == account_name) return (*itr);
    }
    return nullptr;
}

GeneralLedgerAccount* GeneralLedgerStructure::get_account(std::string account_name)
{
    for(unsigned int i=0; i<m_accountList.size(); i++)
    {
        if(m_accountList[i]->GetName() == account_name)
        {
           return m_accountList[i];
        }
        else
        {
            auto result = get_account_from_child(m_accountList[i]->GetAccountList(), account_name);
            if(result != nullptr) return result;
        }
    }
    throw std::out_of_range("The account name: '" + account_name + "' does not exist in the ledger's account list'.");
}

std::string GeneralLedgerStructure::to_string()
{
    return GetName();
}
