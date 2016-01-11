#include "StockLedger.h"

using namespace auxi::modelling::accounting::stock;

void StockLedger::clean()
{
    for(auto itr = m_stockTransactionList.begin(); itr != m_stockTransactionList.end(); ++itr)
        delete (*itr);
    m_stockTransactionList.clear();
}

StockTransaction* StockLedger::create_transaction(std::string name, std::string description, std::string fromAccountName, std::string toAccountName, std::string source)
{
    auto t = new StockTransaction();
    t->SetName(name);
    t->SetDescription(description);
    t->SetSource(source);
    t->SetFromAccountName(fromAccountName);
    t->SetToAccountName(toAccountName);
    m_stockTransactionList.push_back(t);
    return t;
}

std::string StockLedger::to_string()
{
    return GetName();
}
