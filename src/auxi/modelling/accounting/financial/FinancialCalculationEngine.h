#ifndef FINANCIALCALCULATIONENGINE_H
#define FINANCIALCALCULATIONENGINE_H



#include "GeneralLedgerStructure.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class FinancialCalculationEngine;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class FinancialCalculationEngine : public NamedObject
    {
        public:
            FinancialCalculationEngine();
            FinancialCalculationEngine(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~FinancialCalculationEngine();
            FinancialCalculationEngine(const FinancialCalculationEngine& other);

            friend bool operator==(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs);
            friend bool operator!=(const FinancialCalculationEngine& lhs, const FinancialCalculationEngine& rhs);
            friend std::ostream& operator<<(std::ostream&, const FinancialCalculationEngine&);

            bool IsValid() const { return true; }
            FinancialCalculationEngine* Clone() const { return new FinancialCalculationEngine(*this); }

	      
            GeneralLedgerStructure* create_generalLedgerStructure(std::string name);
	      
            void remove_generalLedgerStructure(std::string name);
	      
            void clean();
	      
            std::string to_string();
            std::vector<GeneralLedgerStructure*>& GetGeneralLedgerStructureList();
        protected:
	        std::vector<GeneralLedgerStructure*> m_generalLedgerStructureList;
        private:
    };
}
}
}
}

#endif