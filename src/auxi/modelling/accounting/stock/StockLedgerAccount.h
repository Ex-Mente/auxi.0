#ifndef STOCKLEDGERACCOUNT_H
#define STOCKLEDGERACCOUNT_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockLedgerAccount;
    class StockLedger;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare enums
    //
    namespace StockLedgerAccountType
    {
        enum StockLedgerAccountType
        {
	        RawMaterial,
	        MROSupplies,
        };
    }

    // Declare classes
    //
    class StockLedgerAccount : public NamedObject
    {
        public:
            StockLedgerAccount();
            StockLedgerAccount(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~StockLedgerAccount();
            StockLedgerAccount(const StockLedgerAccount& other);

            friend bool operator==(const StockLedgerAccount& lhs, const StockLedgerAccount& rhs);
            friend bool operator!=(const StockLedgerAccount& lhs, const StockLedgerAccount& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockLedgerAccount&);

            bool IsValid() const { return true; }
            StockLedgerAccount* Clone() const { return new StockLedgerAccount(*this); }

	      
            StockLedgerAccount* create_account(std::string name, std::string number, StockLedgerAccountType::StockLedgerAccountType type);
	      
            void remove_account(std::string number);
	      
            void clean();
	      
            std::string to_string();
            std::vector<StockLedgerAccount*>& GetAccountList();
            std::string GetNumber() const;
            void SetNumber(std::string number);
            StockLedgerAccountType::StockLedgerAccountType GetType() const;
            void SetType(StockLedgerAccountType::StockLedgerAccountType type);
        protected:
	        std::vector<StockLedgerAccount*> m_accountList;
	        std::string m_number = "";
	        StockLedgerAccountType::StockLedgerAccountType m_type;
        private:
    };
}
}
}
}

#endif