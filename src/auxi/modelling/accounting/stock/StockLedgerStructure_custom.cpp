#include "StockLedgerStructure.h"

using namespace auxi::modelling::accounting::stock;

void StockLedgerStructure::initialize()
{
    m_miscAccount = create_account("Misc", "010", StockLedgerAccountType::RawMaterial);
}

void StockLedgerStructure::clean()
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
        delete (*itr);
    m_accountList.clear();
}

StockLedgerAccount* StockLedgerStructure::create_account(std::string name, std::string number, StockLedgerAccountType::StockLedgerAccountType type)
{
    auto acc = new StockLedgerAccount(name, "");
    acc->SetNumber(number);
    acc->SetType(type);

    m_accountList.push_back(acc);
    return acc;
}

void StockLedgerStructure::remove_account(std::string number)
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

StockLedgerAccount* get_account_from_child(std::vector<StockLedgerAccount*>& account_list, std::string account_name)
{
    for(auto itr = account_list.begin(); itr != account_list.end(); ++itr)
    {
        if((*itr)->GetName() == account_name) return (*itr);
    }
    return nullptr;
}

StockLedgerAccount* StockLedgerStructure::get_account(std::string account_name)
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

std::string StockLedgerStructure::to_string()
{
    return GetName();
}
