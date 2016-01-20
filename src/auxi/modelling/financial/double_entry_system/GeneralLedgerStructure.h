#ifndef GENERALLEDGERSTRUCTURE_H
#define GENERALLEDGERSTRUCTURE_H



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
    class GeneralLedgerStructure;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    using namespace auxi::core;

    // Declare classes
    //
    class GeneralLedgerStructure : public NamedObject
    {
        public:
            GeneralLedgerStructure();
            
            ~GeneralLedgerStructure();
            GeneralLedgerStructure(const GeneralLedgerStructure& other);

            friend bool operator==(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs);
            friend bool operator!=(const GeneralLedgerStructure& lhs, const GeneralLedgerStructure& rhs);
            friend std::ostream& operator<<(std::ostream&, const GeneralLedgerStructure&);

            bool IsValid() const { return true; }
            GeneralLedgerStructure* Clone() const { return new GeneralLedgerStructure(*this); }

	      
             GeneralLedgerStructure(std::string name, std::string description = "", std::string json_path = "");
	      
            GeneralLedgerAccount* create_account(std::string name, std::string number = "", AccountType::AccountType type = AccountType::asset);
	      
            void remove_account(std::string account_number);
	      
            GeneralLedgerAccount* get_account(std::string name);
	      
            void initialize();
	      
            void clean();
	      
            std::string to_string();
            std::vector<GeneralLedgerAccount*>& GetAccountList();

            GeneralLedgerAccount* GetBank() const;
            void SetBank(GeneralLedgerAccount* bank);

            GeneralLedgerAccount* GetIncomeTaxPayable() const;
            void SetIncomeTaxPayable(GeneralLedgerAccount* incomeTaxPayable);

            GeneralLedgerAccount* GetIncomeTaxExpense() const;
            void SetIncomeTaxExpense(GeneralLedgerAccount* incomeTaxExpense);

            GeneralLedgerAccount* GetSales() const;
            void SetSales(GeneralLedgerAccount* sales);

            GeneralLedgerAccount* GetCostOfSales() const;
            void SetCostOfSales(GeneralLedgerAccount* costOfSales);

            GeneralLedgerAccount* GetGrossProfit() const;
            void SetGrossProfit(GeneralLedgerAccount* grossProfit);

            GeneralLedgerAccount* GetIncomeSummary() const;
            void SetIncomeSummary(GeneralLedgerAccount* incomeSummary);

            GeneralLedgerAccount* GetRetainedEarnings() const;
            void SetRetainedEarnings(GeneralLedgerAccount* retainedEarnings);

            std::string GetTaxPaymentAccount() const;
            void SetTaxPaymentAccount(std::string taxPaymentAccount);


        protected:
	        std::vector<GeneralLedgerAccount*> m_accountList;
	        GeneralLedgerAccount* m_bank;
	        GeneralLedgerAccount* m_incomeTaxPayable;
	        GeneralLedgerAccount* m_incomeTaxExpense;
	        GeneralLedgerAccount* m_sales;
	        GeneralLedgerAccount* m_costOfSales;
	        GeneralLedgerAccount* m_grossProfit;
	        GeneralLedgerAccount* m_incomeSummary;
	        GeneralLedgerAccount* m_retainedEarnings;
            std::string m_taxPaymentAccount = "";

        private:
    };
}}}}
#endif