#ifndef ENTITY_H
#define ENTITY_H



#include "StockLedger.h"
#include "GeneralLedger.h"
#include "TaxRuleSet.h"
#include "Transaction.h"
#include "Units.h"
#include "VariableGroup.h"
#include "Component.h"
#include "ExecutionObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//




namespace auxi { namespace modelling { namespace business { 
    class Entity;
}
}
}

namespace auxi { namespace modelling { namespace business { 
    using namespace auxi::core;

    // Declare classes
    //
    class Entity : public ExecutionObject
    {
        public:
            Entity();
            Entity(std::string name, std::string description) : ExecutionObject(name, description)
            {
            };
            ~Entity();
            Entity(const Entity& other);

            friend bool operator==(const Entity& lhs, const Entity& rhs);
            friend bool operator!=(const Entity& lhs, const Entity& rhs);
            friend std::ostream& operator<<(std::ostream&, const Entity&);

            bool IsValid() const { return true; }
            Entity* Clone() const { return new Entity(*this); }

	      
            Component* create_component(std::string name);
	      
            void remove_component(std::string name);
	      
            void prepare_to_run(Clock* clock, int totalIntervalsToRun);
	      
            void run(Clock* clock, int ix_interval, Units currency);
	      
            std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*> getSalesAccounts(auxi::modelling::accounting::financial::GeneralLedgerAccount* currentAccount, std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*> salesAccounts = std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*>());
	      
            std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*> getCostOfSalesAccounts(auxi::modelling::accounting::financial::GeneralLedgerAccount* currentAccount, std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*> costOfSalesAccounts = std::vector<auxi::modelling::accounting::financial::GeneralLedgerAccount*>());
            std::vector<VariableGroup*>& GetVariableGroupList();
            std::vector<Component*>& GetComponentList();
            auxi::modelling::accounting::financial::TaxRuleSet& GetTaxRuleSet();
            void SetTaxRuleSet(auxi::modelling::accounting::financial::TaxRuleSet& taxRuleSet);
            double GetNegativeIncomeTaxTotal() const;
            void SetNegativeIncomeTaxTotal(double negativeIncomeTaxTotal);
            int GetTotalIntervalsToRun() const;
            void SetTotalIntervalsToRun(int totalIntervalsToRun);
            auxi::modelling::accounting::stock::StockLedger& GetStockLedger();
            void SetStockLedger(auxi::modelling::accounting::stock::StockLedger& stockLedger);
            auxi::modelling::accounting::financial::GeneralLedger& GetGeneralLedger();
            void SetGeneralLedger(auxi::modelling::accounting::financial::GeneralLedger& generalLedger);
        protected:
	        std::vector<VariableGroup*> m_variableGroupList;
	        std::vector<Component*> m_componentList;
	        auxi::modelling::accounting::financial::TaxRuleSet m_taxRuleSet;
	        double m_negativeIncomeTaxTotal;
	        boost::posix_time::ptime m_prev_year_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        boost::posix_time::ptime m_curr_year_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        boost::posix_time::ptime m_execution_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        int m_totalIntervalsToRun;
	        auxi::modelling::accounting::stock::StockLedger m_stockLedger;
	        auxi::modelling::accounting::financial::GeneralLedger m_generalLedger;
        private:
	      
            double perform_year_end_procedure_gross_profit_and_income_summary(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff, std::map<std::string, double> incomeSummaryAccountsToWriteOff);
	      
            double perform_year_end_procedure_gross_profit(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff);
	      
            double perform_year_end_procedure_income_summary(boost::posix_time::ptime yearEndDate, Units currency, double grossProfit, std::map<std::string, double> incomeSummaryAccountsToWriteOff);
	      
            double perform_year_end_procedure_income_tax(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount);
	      
            void perform_year_end_procedure_retained_earnings(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount);
	      
            void perform_year_end_procedure(Clock* clock, int ix_interval, Units currency);
    };
}
}
}

#endif