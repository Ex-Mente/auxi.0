#ifndef GENERALLEDGERSTRUCTURE_H
#define GENERALLEDGERSTRUCTURE_H



#include "GeneralLedgerAccount.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class GeneralLedgerStructure;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class GeneralLedgerStructure : public NamedObject
    {
        public:
            GeneralLedgerStructure();
            GeneralLedgerStructure(std::string name, std::string description) : NamedObject(name, description)
            {
                initialize();
            };
            ~GeneralLedgerStructure();
            GeneralLedgerStructure(const GeneralLedgerStructure& other);

            friend bool operator==(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs);
            friend bool operator!=(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs);
            friend std::ostream& operator<<(std::ostream&, const GeneralLedgerStructure&);

            bool IsValid() const { return true; }
            GeneralLedgerStructure* Clone() const { return new GeneralLedgerStructure(*this); }

	      
            GeneralLedgerAccount* create_account(std::string name, std::string account_number, GeneralLedgerAccountType::GeneralLedgerAccountType account_type);
	      
            void remove_account(std::string account_number);
	      
            GeneralLedgerAccount* get_account(std::string name);
	      
            void initialize();
	      
            void clean();
	      
            std::string to_string();
            std::vector<GeneralLedgerAccount*>& GetAccountList();
            GeneralLedgerAccount* GetBankAccount() const;
            void SetBankAccount(GeneralLedgerAccount* bankAccount);
            GeneralLedgerAccount* GetIncomeTaxPayableAccount() const;
            void SetIncomeTaxPayableAccount(GeneralLedgerAccount* incomeTaxPayableAccount);
            GeneralLedgerAccount* GetIncomeTaxExpenseAccount() const;
            void SetIncomeTaxExpenseAccount(GeneralLedgerAccount* incomeTaxExpenseAccount);
            GeneralLedgerAccount* GetSalesAccount() const;
            void SetSalesAccount(GeneralLedgerAccount* salesAccount);
            GeneralLedgerAccount* GetCostOfSalesAccount() const;
            void SetCostOfSalesAccount(GeneralLedgerAccount* costOfSalesAccount);
            GeneralLedgerAccount* GetGrossProfitAccount() const;
            void SetGrossProfitAccount(GeneralLedgerAccount* grossProfitAccount);
            GeneralLedgerAccount* GetIncomeSummaryAccount() const;
            void SetIncomeSummaryAccount(GeneralLedgerAccount* incomeSummaryAccount);
            GeneralLedgerAccount* GetRetainedEarningsAccount() const;
            void SetRetainedEarningsAccount(GeneralLedgerAccount* retainedEarningsAccount);
        protected:
	        std::vector<GeneralLedgerAccount*> m_accountList;
	        GeneralLedgerAccount* m_bankAccount;
	        GeneralLedgerAccount* m_incomeTaxPayableAccount;
	        GeneralLedgerAccount* m_incomeTaxExpenseAccount;
	        GeneralLedgerAccount* m_salesAccount;
	        GeneralLedgerAccount* m_costOfSalesAccount;
	        GeneralLedgerAccount* m_grossProfitAccount;
	        GeneralLedgerAccount* m_incomeSummaryAccount;
	        GeneralLedgerAccount* m_retainedEarningsAccount;
        private:
    };
}
}
}
}

#endif