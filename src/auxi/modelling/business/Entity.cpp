#include "Entity.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::business;

Entity::Entity()
{
    //ctor
}

Entity::Entity(const Entity& other)
{
    m_variableGroupList = other.m_variableGroupList;
    m_componentList = other.m_componentList;
    m_taxRuleSet = other.m_taxRuleSet;
    m_negativeIncomeTaxTotal = other.m_negativeIncomeTaxTotal;
    m_prev_year_end_date = other.m_prev_year_end_date;
    m_curr_year_end_date = other.m_curr_year_end_date;
    m_execution_end_date = other.m_execution_end_date;
    m_totalIntervalsToRun = other.m_totalIntervalsToRun;
    m_stockLedger = other.m_stockLedger;
    m_generalLedger = other.m_generalLedger;
}

Entity::~Entity()
{

}

std::vector<VariableGroup*>& Entity::GetVariableGroupList() { return m_variableGroupList; }
std::vector<Component*>& Entity::GetComponentList() { return m_componentList; }
auxi::modelling::accounting::financial::TaxRuleSet& Entity::GetTaxRuleSet() { return m_taxRuleSet; }
void Entity::SetTaxRuleSet(auxi::modelling::accounting::financial::TaxRuleSet& value) { m_taxRuleSet = value; }
double Entity::GetNegativeIncomeTaxTotal() const { return m_negativeIncomeTaxTotal; }
void Entity::SetNegativeIncomeTaxTotal(double value) { m_negativeIncomeTaxTotal = value; }
int Entity::GetTotalIntervalsToRun() const { return m_totalIntervalsToRun; }
void Entity::SetTotalIntervalsToRun(int value) { m_totalIntervalsToRun = value; }
auxi::modelling::accounting::stock::StockLedger& Entity::GetStockLedger() { return m_stockLedger; }
void Entity::SetStockLedger(auxi::modelling::accounting::stock::StockLedger& value) { m_stockLedger = value; }
auxi::modelling::accounting::financial::GeneralLedger& Entity::GetGeneralLedger() { return m_generalLedger; }
void Entity::SetGeneralLedger(auxi::modelling::accounting::financial::GeneralLedger& value) { m_generalLedger = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Entity& lhs, const Entity& rhs)
    {
        return 1 == 1
	  && lhs.m_variableGroupList == rhs.m_variableGroupList
	  && lhs.m_componentList == rhs.m_componentList
	  && lhs.m_taxRuleSet == rhs.m_taxRuleSet
	  && almost_equal(lhs.m_negativeIncomeTaxTotal, rhs.m_negativeIncomeTaxTotal, 5)
	  && lhs.m_prev_year_end_date == rhs.m_prev_year_end_date
	  && lhs.m_curr_year_end_date == rhs.m_curr_year_end_date
	  && lhs.m_execution_end_date == rhs.m_execution_end_date
	  && lhs.m_totalIntervalsToRun == rhs.m_totalIntervalsToRun
	  && lhs.m_stockLedger == rhs.m_stockLedger
	  && lhs.m_generalLedger == rhs.m_generalLedger
	  ;
    }

    bool operator!=(const Entity& lhs, const Entity& rhs)
    {
        return 1 != 1
	  || lhs.m_variableGroupList != rhs.m_variableGroupList
	  || lhs.m_componentList != rhs.m_componentList
	  || lhs.m_taxRuleSet != rhs.m_taxRuleSet
	  || !almost_equal(lhs.m_negativeIncomeTaxTotal, rhs.m_negativeIncomeTaxTotal, 5)
	  || lhs.m_prev_year_end_date != rhs.m_prev_year_end_date
	  || lhs.m_curr_year_end_date != rhs.m_curr_year_end_date
	  || lhs.m_execution_end_date != rhs.m_execution_end_date
	  || lhs.m_totalIntervalsToRun != rhs.m_totalIntervalsToRun
	  || lhs.m_stockLedger != rhs.m_stockLedger
	  || lhs.m_generalLedger != rhs.m_generalLedger
	;
    }

    std::ostream& operator<<(std::ostream& os, const Entity& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
