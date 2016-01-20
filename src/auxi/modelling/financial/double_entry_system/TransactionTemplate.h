#ifndef TRANSACTIONTEMPLATE_H
#define TRANSACTIONTEMPLATE_H



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
    class TransactionTemplate;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
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

            std::string GetDtAccount() const;
            void SetDtAccount(std::string dtAccount);

            std::string GetCrAccount() const;
            void SetCrAccount(std::string crAccount);


        protected:
	        std::string m_dtAccount = "";
	        std::string m_crAccount = "";

        private:
    };
}}}}
#endif