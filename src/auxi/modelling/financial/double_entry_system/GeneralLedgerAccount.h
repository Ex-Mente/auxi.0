#ifndef GENERALLEDGERACCOUNT_H
#define GENERALLEDGERACCOUNT_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    class GeneralLedgerAccount;
    class GeneralLedger;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    using namespace auxi::core;

    // Declare enums
    //
    namespace AccountType
    {
        enum AccountType
        {
	        asset,
	        equity,
	        expense,
	        liability,
	        revenue,
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

	      
            GeneralLedgerAccount* create_account(std::string name, std::string number = "");
	      
            void remove_account(std::string number);
	      
            std::string to_string();
            std::vector<GeneralLedgerAccount*>& GetAccountList();

            std::string GetNumber() const;
            void SetNumber(std::string number);

            AccountType::AccountType GetType() const;
            void SetType(AccountType::AccountType type);


        protected:
	        std::vector<GeneralLedgerAccount*> m_accountList;
	        std::string m_number = "";
	        AccountType::AccountType m_type;

        private:
	      
            void clean();
    };
}}}}
#endif