#ifndef FINANCIALCALCULATIONENGINE_H
#define FINANCIALCALCULATIONENGINE_H



#include "CalculationEngine.h"
#include "GeneralLedgerStructure.h"
#include "CalculationEngine.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace calculation_engines { 
    class FinancialCalculationEngine;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace calculation_engines { 
    using namespace auxi::core;

    // Declare classes
    //
    class FinancialCalculationEngine : public CalculationEngine
    {
        public:
            FinancialCalculationEngine();
            FinancialCalculationEngine(std::string name, std::string description) : CalculationEngine(name, description)
            {
            };
            ~FinancialCalculationEngine();
            FinancialCalculationEngine(const FinancialCalculationEngine& other);

            friend bool operator==(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs);
            friend bool operator!=(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs);
            friend std::ostream& operator<<(std::ostream&, const FinancialCalculationEngine&);

            bool IsValid() const { return true; }
            FinancialCalculationEngine* Clone() const { return new FinancialCalculationEngine(*this); }

	      
            auxi::modelling::financial::double_entry_system::GeneralLedgerStructure* create_generalLedgerStructure(std::string name);
	      
            void remove_generalLedgerStructure(std::string name);
	      
            void clean();
	      
            std::string to_string();
            std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerStructure*>& GetGeneralLedgerStructureList();


        protected:
	        std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerStructure*> m_generalLedgerStructureList;

        private:
    };
}}}}
#endif