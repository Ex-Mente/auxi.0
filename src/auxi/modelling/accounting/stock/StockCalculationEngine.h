#ifndef STOCKCALCULATIONENGINE_H
#define STOCKCALCULATIONENGINE_H



#include "StockLedgerStructure.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockCalculationEngine;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare classes
    //
    class StockCalculationEngine : public NamedObject
    {
        public:
            StockCalculationEngine();
            StockCalculationEngine(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~StockCalculationEngine();
            StockCalculationEngine(const StockCalculationEngine& other);

            friend bool operator==(const StockCalculationEngine& lhs, const StockCalculationEngine& rhs);
            friend bool operator!=(const StockCalculationEngine& lhs, const StockCalculationEngine& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockCalculationEngine&);

            bool IsValid() const { return true; }
            StockCalculationEngine* Clone() const { return new StockCalculationEngine(*this); }

	      
            StockLedgerStructure* create_stockLedgerStructure(std::string name);
	      
            void remove_stockLedgerStructure(std::string name);
	      
            void clean();
	      
            std::string to_string();
            std::vector<StockLedgerStructure*>& GetStockLedgerStructureList();
        protected:
	        std::vector<StockLedgerStructure*> m_stockLedgerStructureList;
        private:
    };
}
}
}
}

#endif