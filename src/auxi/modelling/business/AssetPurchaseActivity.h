#ifndef ASSETPURCHASEACTIVITY_H
#define ASSETPURCHASEACTIVITY_H



#include "TransactionTemplate.h"
#include "Clock.h"
#include "Activity.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business {
    class AssetPurchaseActivity;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;

    // Declare classes
    //
    class AssetPurchaseActivity : public Activity
    {
        public:
            AssetPurchaseActivity();

            ~AssetPurchaseActivity();
            AssetPurchaseActivity(const AssetPurchaseActivity& other);

            friend bool operator==(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs);
            friend bool operator!=(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs);
            friend std::ostream& operator<<(std::ostream&, const AssetPurchaseActivity&);

            bool IsValid() const { return true; }
            AssetPurchaseActivity* Clone() const { return new AssetPurchaseActivity(*this); }


             //AssetPurchaseActivity(std::string name, std::string description = "", int start = 0, int end = -1, int interval = 1);

             AssetPurchaseActivity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, boost::posix_time::ptime end = boost::posix_time::max_date_time, int interval = 1);

             //AssetPurchaseActivity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, int repeat = 1, int interval = 1);

            void initialize();

            bool OnExecute_MeetExecutionCriteria(int ix_period);

            void prepare_to_run(Clock* clock, int ix_period);

            void run(Clock* clock, int ix_period, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerExpenseAccount() const;
            void SetGeneralLedgerExpenseAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerExpenseAccount);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerAssetAccount() const;
            void SetGeneralLedgerAssetAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerAssetAccount);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetAssetPurchaseTxTemplate();
            void SetAssetPurchaseTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& assetPurchaseTxTemplate);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetAddDepreciationTxTemplate();
            void SetAddDepreciationTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& addDepreciationTxTemplate);

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
	        auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* m_generalLedgerExpenseAccount;
	        auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* m_generalLedgerAssetAccount;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_assetPurchaseTxTemplate;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_addDepreciationTxTemplate;
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
}}}
#endif