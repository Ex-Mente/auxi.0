#include "GeneralLedgerStructure.h"

using namespace auxi::modelling::financial::double_entry_system;


GeneralLedgerStructure::GeneralLedgerStructure(std::string name, std::string description, std::string json_path) : NamedObject(name, description)
{
    initialize();
}

void GeneralLedgerStructure::initialize()
{
    m_bank = create_account("Bank", "Bank", AccountType::Asset);
    m_incomeTaxPayable = create_account("IncomeTaxPayable", "IncomeTaxPayable", AccountType::Liability);
    m_incomeTaxExpense = create_account("IncomeTaxExpense", "IncomeTaxExpense", AccountType::Expense);
    m_sales = create_account("Sales", "Sales", AccountType::Revenue);
    m_costOfSales = create_account("CostOfSales", "CostOfSales", AccountType::Expense);
    m_grossProfit = create_account("GrossProfit", "GrossProfit", AccountType::Revenue);
    m_incomeSummary = create_account("IncomeSummary", "IncomeSummary", AccountType::Revenue);
    m_retainedEarnings = create_account("RetainedEarnings", "RetainedEarnings", AccountType::Equity);
}

void GeneralLedgerStructure::clean()
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
        delete (*itr);
    m_accountList.clear();
}

GeneralLedgerAccount* GeneralLedgerStructure::create_account(std::string name, std::string number, AccountType::AccountType type)
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
