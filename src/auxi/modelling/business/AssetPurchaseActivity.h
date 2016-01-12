#ifndef ASSETPURCHASEACTIVITY_H
#define ASSETPURCHASEACTIVITY_H



#include "TransactionTemplate.h"
#include "Clock.h"
#include "Activity.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//




namespace auxi { namespace modelling { namespace business { 
    class AssetPurchaseActivity;
}
}
}

namespace auxi { namespace modelling { namespace business { 
    using namespace auxi::core;

    // Declare classes
    //
    class AssetPurchaseActivity : public Activity
    {
        public:
            AssetPurchaseActivity();
            AssetPurchaseActivity(std::string name, std::string description) : Activity(name, description)
            {
                initialize();
            };
            ~AssetPurchaseActivity();
            AssetPurchaseActivity(const AssetPurchaseActivity& other);

            friend bool operator==(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs);
            friend bool operator!=(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs);
            friend std::ostream& operator<<(std::ostream&, const AssetPurchaseActivity&);

            bool IsValid() const { return true; }
            AssetPurchaseActivity* Clone() const { return new AssetPurchaseActivity(*this); }

	      
            void initialize();
	      
            virtual bool OnExecute_MeetExecutionCriteria(int executionIntervals);
	      
            void prepare_to_run(Clock* clock, int totalIntervalsToRun);
	      
            void run(Clock* clock, int ix_interval, auxi::modelling::accounting::financial::GeneralLedger* generalLedger, auxi::modelling::accounting::stock::StockLedger* stockLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);
            auxi::modelling::accounting::financial::GeneralLedgerAccount* GetGeneralLedgerExpenseAccount() const;
            void SetGeneralLedgerExpenseAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* generalLedgerExpenseAccount);
            auxi::modelling::accounting::financial::GeneralLedgerAccount* GetGeneralLedgerAssetAccount() const;
            void SetGeneralLedgerAssetAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* generalLedgerAssetAccount);
            auxi::modelling::accounting::financial::TransactionTemplate& GetAssetPurchaseTransactionTemplate();
            void SetAssetPurchaseTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& assetPurchaseTransactionTemplate);
            auxi::modelling::accounting::financial::TransactionTemplate& GetAddDepreciationTransactionTemplate();
            void SetAddDepreciationTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& addDepreciationTransactionTemplate);
            double GetPurchaseAmount() const;
            void SetPurchaseAmount(double purchaseAmount);
            double GetWriteOffAmount() const;
            void SetWriteOffAmount(double writeOffAmount);
            double GetMonthsTillWrittenOff() const;
            void SetMonthsTillWrittenOff(double monthsTillWrittenOff);
            double GetPeriodicDepreciationAmount() const;
            double GetAmountLeft() const;
            double GetMonthsLeft() const;
            double GetCurrentAssetValue() const;
            void SetCurrentAssetValue(double currentAssetValue);
        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        auxi::modelling::accounting::financial::GeneralLedgerAccount* m_generalLedgerExpenseAccount;
	        auxi::modelling::accounting::financial::GeneralLedgerAccount* m_generalLedgerAssetAccount;
	        auxi::modelling::accounting::financial::TransactionTemplate m_assetPurchaseTransactionTemplate;
	        auxi::modelling::accounting::financial::TransactionTemplate m_addDepreciationTransactionTemplate;
	        double m_purchaseAmount = 0.0;
	        double m_writeOffAmount = 0.0;
	        double m_monthsTillWrittenOff = 0.0;
	        double m_periodicDepreciationAmount = 0.0;
	        double m_amountLeft = 0.0;
	        double m_monthsLeft = 0.0;
	        double m_currentAssetValue = 0.0;
        private:
	      
            void updatePeriodicDepreciationAmount();
    };
}
}
}

#endif