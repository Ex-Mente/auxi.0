#ifndef STOCKLEDGER_H
#define STOCKLEDGER_H



#include "StockLedgerStructure.h"
#include "StockTransaction.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockLedger;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare classes
    //
    class StockLedger : public NamedObject
    {
        public:
            StockLedger();
            StockLedger(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~StockLedger();
            StockLedger(const StockLedger& other);

            friend bool operator==(const StockLedger& lhs, const StockLedger& rhs);
            friend bool operator!=(const StockLedger& lhs, const StockLedger& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockLedger&);

            bool IsValid() const { return true; }
            StockLedger* Clone() const { return new StockLedger(*this); }

	      
            StockTransaction* create_transaction(std::string name, std::string description, std::string toAccount, std::string fromAccount, std::string source);
	      
            void clean();
	      
            std::string to_string();
            std::vector<StockTransaction*>& GetStockTransactionList();
            StockLedgerStructure* GetStructure() const;
            void SetStructure(StockLedgerStructure* structure);
        protected:
	        std::vector<StockTransaction*> m_stockTransactionList;
	        StockLedgerStructure* m_structure = nullptr;
        private:
    };
}
}
}
}

#endif