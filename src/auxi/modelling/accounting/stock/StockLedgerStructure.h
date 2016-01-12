#ifndef STOCKLEDGERSTRUCTURE_H
#define STOCKLEDGERSTRUCTURE_H



#include "StockLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockLedgerStructure;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare classes
    //
    class StockLedgerStructure : public NamedObject
    {
        public:
            StockLedgerStructure();
            StockLedgerStructure(std::string name, std::string description) : NamedObject(name, description)
            {
                initialize();
            };
            ~StockLedgerStructure();
            StockLedgerStructure(const StockLedgerStructure& other);

            friend bool operator==(const StockLedgerStructure& lhs, const StockLedgerStructure& rhs);
            friend bool operator!=(const StockLedgerStructure& lhs, const StockLedgerStructure& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockLedgerStructure&);

            bool IsValid() const { return true; }
            StockLedgerStructure* Clone() const { return new StockLedgerStructure(*this); }

	      
            StockLedgerAccount* create_account(std::string name, std::string account_number, StockLedgerAccountType::StockLedgerAccountType account_type);
	      
            void remove_account(std::string account_number);
	      
            StockLedgerAccount* get_account(std::string name);
	      
            void initialize();
	      
            void clean();
	      
            std::string to_string();
            std::vector<StockLedgerAccount*>& GetAccountList();
            StockLedgerAccount* GetMiscAccount() const;
            void SetMiscAccount(StockLedgerAccount* miscAccount);
        protected:
	        std::vector<StockLedgerAccount*> m_accountList;
	        StockLedgerAccount* m_miscAccount;
        private:
    };
}
}
}
}

#endif