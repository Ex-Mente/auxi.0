#include "GeneralLedger.h"

using namespace auxi::modelling::financial::double_entry_system;

void GeneralLedger::clean()
{
    for(auto itr = m_transactionList.begin(); itr != m_transactionList.end(); ++itr)
        delete (*itr);
    m_transactionList.clear();
}

Transaction* GeneralLedger::create_transaction(std::string name, std::string description, std::string crAccount, std::string dtAccount, std::string source)
{
    auto t = new Transaction();
    t->SetName(name);
    t->SetDescription(description);
    t->SetSource(source);
    t->SetCrAccount(crAccount);
    t->SetDtAccount(dtAccount);
    m_transactionList.push_back(t);
    return t;
}

std::string GeneralLedger::to_string()
{
    return GetName();
}
