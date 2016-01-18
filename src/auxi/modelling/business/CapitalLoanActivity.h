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
            CapitalLoanActivity(std::string name, std::string description) : Activity(name, description)
            {
                initialize();
            };
            ~CapitalLoanActivity();
            CapitalLoanActivity(const CapitalLoanActivity& other);

            friend bool operator==(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs);
            friend bool operator!=(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs);
            friend std::ostream& operator<<(std::ostream&, const CapitalLoanActivity&);

            bool IsValid() const { return true; }
            CapitalLoanActivity* Clone() const { return new CapitalLoanActivity(*this); }


            void initialize();

            virtual bool OnExecute_MeetExecutionCriteria(int executionInterval);

            void prepare_to_run(Clock* clock, int totalIntervalsToRun);

            void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerLiabilityAccount() const;
            void SetGeneralLedgerLiabilityAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerLiabilityAccount);

            auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* GetGeneralLedgerExpenseAccount() const;
            void SetGeneralLedgerExpenseAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* generalLedgerExpenseAccount);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetMakeLoanTransactionTemplate();
            void SetMakeLoanTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& makeLoanTransactionTemplate);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetConsiderInterestTransactionTemplate();
            void SetConsiderInterestTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& considerInterestTransactionTemplate);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetPayMonthlyLoanAmountTransactionTemplate();
            void SetPayMonthlyLoanAmountTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& payMonthlyLoanAmountTransactionTemplate);

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
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_makeLoanTransactionTemplate;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_considerInterestTransactionTemplate;
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_payMonthlyLoanAmountTransactionTemplate;
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