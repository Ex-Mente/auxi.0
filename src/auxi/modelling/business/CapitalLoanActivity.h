#ifndef CAPITALLOANACTIVITY_H
#define CAPITALLOANACTIVITY_H



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
    class CapitalLoanActivity;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;

    // Declare classes
    //
    class CapitalLoanActivity : public Activity
    {
        public:
            CapitalLoanActivity();

            ~CapitalLoanActivity();
            CapitalLoanActivity(const CapitalLoanActivity& other);

            friend bool operator==(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs);
            friend bool operator!=(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs);
            friend std::ostream& operator<<(std::ostream&, const CapitalLoanActivity&);

            bool IsValid() const { return true; }
            CapitalLoanActivity* Clone() const { return new CapitalLoanActivity(*this); }


             //CapitalLoanActivity(std::string name, std::string description = "", int start = 0, int end = -1, int interval = 1);

             CapitalLoanActivity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, boost::posix_time::ptime end = boost::posix_time::max_date_time, int interval = 1);

             //CapitalLoanActivity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, int repeat = 1, int interval = 1);

            void initialize();

            bool OnExecute_MeetExecutionCriteria(int executionInterval);

            void prepare_to_run(Clock* clock, int totalIntervalsToRun);

            void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerLiabilityAccount() const;
            void SetGeneralLedgerLiabilityAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerLiabilityAccount);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerExpenseAccount() const;
            void SetGeneralLedgerExpenseAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerExpenseAccount);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetMakeLoanTxTemplate();
            void SetMakeLoanTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& makeLoanTxTemplate);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetConsiderInterestTxTemplate();
            void SetConsiderInterestTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& considerInterestTxTemplate);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetPayMonthlyLoanAmountTxTemplate();
            void SetPayMonthlyLoanAmountTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& payMonthlyLoanAmountTxTemplate);

            double GetLoanAmount() const;
            void SetLoanAmount(double loanAmount);

            double GetInterestRate() const;
            void SetInterestRate(double interestRate);

            double GetPeriodInMonths() const;
            void SetPeriodInMonths(double periodInMonths);

            double GetAmountLeft() const;

            double GetMonthsLeft() const;

            double GetMonthlyPayment();

            double GetCurrentInterestAmount();


        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* m_generalLedgerLiabilityAccount;
	        auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* m_generalLedgerExpenseAccount;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_makeLoanTxTemplate;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_considerInterestTxTemplate;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_payMonthlyLoanAmountTxTemplate;
	        double m_loanAmount = 0.0;
	        double m_interestRate = 0.0;
	        double m_monthlyInterestRate;
	        double m_periodInMonths = 0.0;
	        double m_amountLeft = 0.0;
	        double m_monthsLeft = 0.0;
	        double m_monthlyPayment;
	        double m_currentInterestAmount;

        private:
    };
}}}
#endif