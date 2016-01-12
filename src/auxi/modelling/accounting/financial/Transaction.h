#ifndef TRANSACTION_H
#define TRANSACTION_H



#include "Units.h"
#include "GeneralLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class Transaction;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class Transaction : public NamedObject
    {
        public:
            Transaction();
            Transaction(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Transaction();
            Transaction(const Transaction& other);

            friend bool operator==(const Transaction& lhs, const Transaction& rhs);
            friend bool operator!=(const Transaction& lhs, const Transaction& rhs);
            friend std::ostream& operator<<(std::ostream&, const Transaction&);

            bool IsValid() const { return true; }
            Transaction* Clone() const { return new Transaction(*this); }

            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);
            std::string GetCreditAccountName() const;
            void SetCreditAccountName(std::string creditAccountName);
            std::string GetDebitAccountName() const;
            void SetDebitAccountName(std::string debitAccountName);
            Units& GetCurrency();
            void SetCurrency(Units& currency);
            std::string GetSource() const;
            void SetSource(std::string source);
            bool GetIsClosingCreditAccount() const;
            void SetIsClosingCreditAccount(bool isClosingCreditAccount);
            bool GetIsClosingDebitAccount() const;
            void SetIsClosingDebitAccount(bool isClosingDebitAccount);
            double GetAmount() const;
            void SetAmount(double amount);
        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        std::string m_creditAccountName = "";
	        std::string m_debitAccountName = "";
	        Units m_currency;
	        std::string m_source = "";
	        bool m_isClosingCreditAccount = false;
	        bool m_isClosingDebitAccount = false;
	        double m_amount = 0;
        private:
    };
}
}
}
}

#endif