#include "FinancialCalculationEngine.h"

using namespace auxi::modelling::accounting::financial;

void FinancialCalculationEngine::clean()
{
    for(auto itr = m_generalLedgerStructureList.begin(); itr != m_generalLedgerStructureList.end(); ++itr)
        delete (*itr);
    m_generalLedgerStructureList.clear();
}

GeneralLedgerStructure* FinancialCalculationEngine::create_generalLedgerStructure(std::string name)
{
    auto generalLedger_structure = new GeneralLedgerStructure(name, "");
    m_generalLedgerStructureList.push_back(generalLedger_structure);
    return generalLedger_structure;
}

void FinancialCalculationEngine::remove_generalLedgerStructure(std::string name)
{
    for(auto itr = m_generalLedgerStructureList.begin(); itr != m_generalLedgerStructureList.end(); ++itr)
    {
        if((*itr)->GetName() == name)
        {
           delete (*itr);
           m_generalLedgerStructureList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The general ledger structure: '" + name + "' does not exist in the financial calculation engine's general ledger structure list'.");
}

std::string FinancialCalculationEngine::to_string()
{
    return GetName();
}


