#ifndef GENERALLEDGERACCOUNT_H
#define GENERALLEDGERACCOUNT_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class GeneralLedgerAccount;
    class GeneralLedger;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare enums
    //
    namespace GeneralLedgerAccountType
    {
        enum GeneralLedgerAccountType
        {
	        Asset,
	        Equity,
	        Expense,
	        Liability,
	        Revenue,
        };
    }

    // Declare classes
    //
    class GeneralLedgerAccount : public NamedObject
    {
        public:
            GeneralLedgerAccount();
            GeneralLedgerAccount(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~GeneralLedgerAccount();
            GeneralLedgerAccount(const GeneralLedgerAccount& other);

            friend bool operator==(const GeneralLedgerAccount& lhs, const GeneralLedgerAccount& rhs);
            friend bool operator!=(const GeneralLedgerAccount& lhs, const GeneralLedgerAccount& rhs);
            friend std::ostream& operator<<(std::ostream&, const GeneralLedgerAccount&);

            bool IsValid() const { return true; }
            GeneralLedgerAccount* Clone() const { return new GeneralLedgerAccount(*this); }

	      
            GeneralLedgerAccount* create_account(std::string name, std::string number, GeneralLedgerAccountType::GeneralLedgerAccountType type);
	      
            void remove_account(std::string number);
	      
            void clean();
	      
            std::string to_string();
            std::vector<GeneralLedgerAccount*>& GetAccountList();
            std::string GetNumber() const;
            void SetNumber(std::string number);
            GeneralLedgerAccountType::GeneralLedgerAccountType GetType() const;
            void SetType(GeneralLedgerAccountType::GeneralLedgerAccountType type);
        protected:
	        std::vector<GeneralLedgerAccount*> m_accountList;
	        std::string m_number = "";
	        GeneralLedgerAccountType::GeneralLedgerAccountType m_type;
        private:
    };
}
}
}
}

#endif