#include "StockCalculationEngine.h"

using namespace auxi::modelling::accounting::stock;

void StockCalculationEngine::clean()
{
    for(auto itr = m_stockLedgerStructureList.begin(); itr != m_stockLedgerStructureList.end(); ++itr)
        delete (*itr);
    m_stockLedgerStructureList.clear();
}

StockLedgerStructure* StockCalculationEngine::create_stockLedgerStructure(std::string name)
{
    auto stockLedger_structure = new StockLedgerStructure(name, "");
    m_stockLedgerStructureList.push_back(stockLedger_structure);
    return stockLedger_structure;
}

void StockCalculationEngine::remove_stockLedgerStructure(std::string name)
{
    for(auto itr = m_stockLedgerStructureList.begin(); itr != m_stockLedgerStructureList.end(); ++itr)
    {
        if((*itr)->GetName() == name)
        {
           delete (*itr);
           m_stockLedgerStructureList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The stock ledger structure: '" + name + "' does not exist in the stock calculation engine's stock ledger structure list'.");
}

std::string StockCalculationEngine::to_string()
{
    return GetName();
}


