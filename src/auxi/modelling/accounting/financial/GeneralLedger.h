#ifndef GENERALLEDGER_H
#define GENERALLEDGER_H



#include "GeneralLedgerStructure.h"
#include "Transaction.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class GeneralLedger;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class GeneralLedger : public NamedObject
    {
        public:
            GeneralLedger();
            GeneralLedger(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~GeneralLedger();
            GeneralLedger(const GeneralLedger& other);

            friend bool operator==(const GeneralLedger& lhs, const GeneralLedger& rhs);
            friend bool operator!=(const GeneralLedger& lhs, const GeneralLedger& rhs);
            friend std::ostream& operator<<(std::ostream&, const GeneralLedger&);

            bool IsValid() const { return true; }
            GeneralLedger* Clone() const { return new GeneralLedger(*this); }

	      
            Transaction* create_transaction(std::string name, std::string description, std::string creditAccount, std::string debitAccount, std::string source);
	      
            void clean();
	      
            std::string to_string();
            std::vector<Transaction*>& GetTransactionList();
            GeneralLedgerStructure* GetStructure() const;
            void SetStructure(GeneralLedgerStructure* structure);
        protected:
	        std::vector<Transaction*> m_transactionList;
	        GeneralLedgerStructure* m_structure = nullptr;
        private:
    };
}
}
}
}

#endif