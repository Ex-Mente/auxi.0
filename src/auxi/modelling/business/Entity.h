#ifndef ENTITY_H
#define ENTITY_H



#include "StockLedger.h"
#include "GeneralLedger.h"
#include "RuleSet.h"
#include "Transaction.h"
#include "Units.h"
#include "VariableGroup.h"
#include "Component.h"
#include "ExecutionObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business {
    class Entity;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;
    using namespace auxi::modelling::financial::double_entry_system;

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

            std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> getSalesAccounts(GeneralLedgerAccount* currentAccount, std::vector<GeneralLedgerAccount*> salesAccounts = std::vector<GeneralLedgerAccount*>());

            std::vector<GeneralLedgerAccount*> getCostOfSalesAccounts(GeneralLedgerAccount* currentAccount, std::vector<GeneralLedgerAccount*> costOfSalesAccounts = std::vector<GeneralLedgerAccount*>());
            std::vector<VariableGroup*>& GetVariableGroupList();

            std::vector<Component*>& GetComponentList();

            auxi::modelling::financial::tax::RuleSet& GetTaxRuleSet();
            void SetTaxRuleSet(auxi::modelling::financial::tax::RuleSet& taxRuleSet);

            double GetNegativeIncomeTaxTotal() const;
            void SetNegativeIncomeTaxTotal(double negativeIncomeTaxTotal);

            int GetTotalIntervalsToRun() const;
            void SetTotalIntervalsToRun(int totalIntervalsToRun);

            auxi::modelling::stock::double_entry_system::StockLedger& GetStockLedger();
            void SetStockLedger(auxi::modelling::stock::double_entry_system::StockLedger& stockLedger);

            auxi::modelling::financial::double_entry_system::GeneralLedger& GetGeneralLedger();
            void SetGeneralLedger(auxi::modelling::financial::double_entry_system::GeneralLedger& generalLedger);


        protected:
	        std::vector<VariableGroup*> m_variableGroupList;
	        std::vector<Component*> m_componentList;
	        auxi::modelling::financial::tax::RuleSet m_taxRuleSet;
	        double m_negativeIncomeTaxTotal;
	        boost::posix_time::ptime m_prev_year_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        boost::posix_time::ptime m_curr_year_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        boost::posix_time::ptime m_execution_end_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        int m_totalIntervalsToRun;
	        auxi::modelling::stock::double_entry_system::StockLedger m_stockLedger;
	        auxi::modelling::financial::double_entry_system::GeneralLedger m_generalLedger;

        private:

            double perform_year_end_procedure_gross_profit_and_income_summary(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff, std::map<std::string, double> incomeSummaryAccountsToWriteOff);

            double perform_year_end_procedure_gross_profit(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff);

            double perform_year_end_procedure_income_summary(boost::posix_time::ptime yearEndDate, Units currency, double grossProfit, std::map<std::string, double> incomeSummaryAccountsToWriteOff);

            double perform_year_end_procedure_income_tax(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount);

            void perform_year_end_procedure_retained_earnings(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount);

            void perform_year_end_procedure(Clock* clock, int ix_interval, Units currency);
    };
}}}
#endif