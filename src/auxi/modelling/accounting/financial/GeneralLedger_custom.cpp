#include "GeneralLedger.h"

using namespace auxi::modelling::accounting::financial;

void GeneralLedger::clean()
{
    for(auto itr = m_transactionList.begin(); itr != m_transactionList.end(); ++itr)
        delete (*itr);
    m_transactionList.clear();
}

Transaction* GeneralLedger::create_transaction(std::string name, std::string description, std::string creditAccountName, std::string debitAccountName, std::string source)
{
    auto t = new Transaction();
    t->SetName(name);
    t->SetDescription(description);
    t->SetSource(source);
    t->SetCreditAccountName(creditAccountName);
    t->SetDebitAccountName(debitAccountName);
    m_transactionList.push_back(t);
    return t;
}

std::string GeneralLedger::to_string()
{
    return GetName();
}
