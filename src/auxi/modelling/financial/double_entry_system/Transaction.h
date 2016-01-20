#ifndef TRANSACTION_H
#define TRANSACTION_H



#include "Units.h"
#include "GeneralLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    class Transaction;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
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

            std::string GetCrAccount() const;
            void SetCrAccount(std::string crAccount);

            std::string GetDtAccount() const;
            void SetDtAccount(std::string dtAccount);

            Units& GetCurrency();
            void SetCurrency(Units& currency);

            std::string GetSource() const;
            void SetSource(std::string source);

            bool GetIsClosingCrAccount() const;
            void SetIsClosingCrAccount(bool isClosingCrAccount);

            bool GetIsClosingDtAccount() const;
            void SetIsClosingDtAccount(bool isClosingDtAccount);

            double GetAmount() const;
            void SetAmount(double amount);


        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        std::string m_crAccount = "";
	        std::string m_dtAccount = "";
	        Units m_currency;
	        std::string m_source = "";
	        bool m_isClosingCrAccount = false;
	        bool m_isClosingDtAccount = false;
	        double m_amount = 0;

        private:
    };
}}}}
#endif