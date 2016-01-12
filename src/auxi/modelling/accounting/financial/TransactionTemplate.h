#ifndef TRANSACTIONTEMPLATE_H
#define TRANSACTIONTEMPLATE_H



#include "GeneralLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class TransactionTemplate;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class TransactionTemplate : public NamedObject
    {
        public:
            TransactionTemplate();
            TransactionTemplate(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~TransactionTemplate();
            TransactionTemplate(const TransactionTemplate& other);

            friend bool operator==(const TransactionTemplate& lhs, const TransactionTemplate& rhs);
            friend bool operator!=(const TransactionTemplate& lhs, const TransactionTemplate& rhs);
            friend std::ostream& operator<<(std::ostream&, const TransactionTemplate&);

            bool IsValid() const { return true; }
            TransactionTemplate* Clone() const { return new TransactionTemplate(*this); }

            std::string GetDebitAccountName() const;
            void SetDebitAccountName(std::string debitAccountName);
            std::string GetCreditAccountName() const;
            void SetCreditAccountName(std::string creditAccountName);
        protected:
	        std::string m_debitAccountName = "";
	        std::string m_creditAccountName = "";
        private:
    };
}
}
}
}

#endif