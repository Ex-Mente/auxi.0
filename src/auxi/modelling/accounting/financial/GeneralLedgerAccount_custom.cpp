#include "GeneralLedgerAccount.h"

using namespace auxi::modelling::accounting::financial;

void GeneralLedgerAccount::clean()
{
    for(auto itr = m_accountList.begin(); itr != m_accountList.end(); ++itr)
        delete (*itr);
    m_accountList.clear();
}

GeneralLedgerAccount* GeneralLedgerAccount::create_account(std::string name, std::string number, GeneralLedgerAccountType::GeneralLedgerAccountType type)
{
    auto acc = new GeneralLedgerAccount(name, "");
    acc->SetNumber(number);
    acc->SetType(type);

    m_accountList.push_back(acc);
    return acc;
}

void GeneralLedgerAccount::remove_account(std::string number)
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

std::string GeneralLedgerAccount::to_string()
{
    return GetName();
}
