#ifndef STOCKTRANSACTIONTEMPLATE_H
#define STOCKTRANSACTIONTEMPLATE_H



#include "StockLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockTransactionTemplate;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare classes
    //
    class StockTransactionTemplate : public NamedObject
    {
        public:
            StockTransactionTemplate();
            StockTransactionTemplate(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~StockTransactionTemplate();
            StockTransactionTemplate(const StockTransactionTemplate& other);

            friend bool operator==(const StockTransactionTemplate& lhs, const StockTransactionTemplate& rhs);
            friend bool operator!=(const StockTransactionTemplate& lhs, const StockTransactionTemplate& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockTransactionTemplate&);

            bool IsValid() const { return true; }
            StockTransactionTemplate* Clone() const { return new StockTransactionTemplate(*this); }

            std::string GetFromAccountName() const;
            void SetFromAccountName(std::string fromAccountName);
            std::string GetToAccountName() const;
            void SetToAccountName(std::string toAccountName);
        protected:
	        std::string m_fromAccountName = "";
	        std::string m_toAccountName = "";
        private:
    };
}
}
}
}

#endif