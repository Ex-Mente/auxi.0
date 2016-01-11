#include "StockLedgerAccount.h"

using namespace auxi::modelling::accounting::stock;

void StockLedgerAccount::clean()
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
        delete (*itr);
    m_accountList.clear();
}

StockLedgerAccount* StockLedgerAccount::create_account(std::string name, std::string number, StockLedgerAccountType::StockLedgerAccountType type)
{
    auto acc = new StockLedgerAccount(name, "");
    acc->SetNumber(number);
    acc->SetType(type);

    m_accountList.push_back(acc);
    return acc;
}

void StockLedgerAccount::remove_account(std::string number)
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

std::string StockLedgerAccount::to_string()
{
    return GetName();
}
