#ifndef STOCKTRANSACTION_H
#define STOCKTRANSACTION_H



#include "Units.h"
#include "StockLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    class StockTransaction;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace stock { 
    using namespace auxi::core;

    // Declare classes
    //
    class StockTransaction : public NamedObject
    {
        public:
            StockTransaction();
            StockTransaction(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~StockTransaction();
            StockTransaction(const StockTransaction& other);

            friend bool operator==(const StockTransaction& lhs, const StockTransaction& rhs);
            friend bool operator!=(const StockTransaction& lhs, const StockTransaction& rhs);
            friend std::ostream& operator<<(std::ostream&, const StockTransaction&);

            bool IsValid() const { return true; }
            StockTransaction* Clone() const { return new StockTransaction(*this); }

            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);
            std::string GetFromAccountName() const;
            void SetFromAccountName(std::string fromAccountName);
            std::string GetToAccountName() const;
            void SetToAccountName(std::string toAccountName);
            Units& GetCurrency();
            void SetCurrency(Units& currency);
            std::string GetSource() const;
            void SetSource(std::string source);
            double GetAmount() const;
            void SetAmount(double amount);
        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        std::string m_fromAccountName = "";
	        std::string m_toAccountName = "";
	        Units m_currency;
	        std::string m_source = "";
	        double m_amount = 0;
        private:
    };
}
}
}
}

#endif