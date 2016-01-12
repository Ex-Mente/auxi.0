#ifndef CAPITALLOANACTIVITY_H
#define CAPITALLOANACTIVITY_H



#include "TransactionTemplate.h"
#include "Clock.h"
#include "Activity.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//




namespace auxi { namespace modelling { namespace business { 
    class CapitalLoanActivity;
}
}
}

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
	      
            void run(Clock* clock, int ix_interval, auxi::modelling::accounting::financial::GeneralLedger* generalLedger, auxi::modelling::accounting::stock::StockLedger* stockLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);
            auxi::modelling::accounting::financial::GeneralLedgerAccount* GetGeneralLedgerLiabilityAccount() const;
            void SetGeneralLedgerLiabilityAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* generalLedgerLiabilityAccount);
            auxi::modelling::accounting::financial::GeneralLedgerAccount* GetGeneralLedgerExpenseAccount() const;
            void SetGeneralLedgerExpenseAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* generalLedgerExpenseAccount);
            auxi::modelling::accounting::financial::TransactionTemplate& GetMakeLoanTransactionTemplate();
            void SetMakeLoanTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& makeLoanTransactionTemplate);
            auxi::modelling::accounting::financial::TransactionTemplate& GetConsiderInterestTransactionTemplate();
            void SetConsiderInterestTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& considerInterestTransactionTemplate);
            auxi::modelling::accounting::financial::TransactionTemplate& GetPayMonthlyLoanAmountTransactionTemplate();
            void SetPayMonthlyLoanAmountTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& payMonthlyLoanAmountTransactionTemplate);
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
	        auxi::modelling::accounting::financial::GeneralLedgerAccount* m_generalLedgerLiabilityAccount;
	        auxi::modelling::accounting::financial::GeneralLedgerAccount* m_generalLedgerExpenseAccount;
	        auxi::modelling::accounting::financial::TransactionTemplate m_makeLoanTransactionTemplate;
	        auxi::modelling::accounting::financial::TransactionTemplate m_considerInterestTransactionTemplate;
	        auxi::modelling::accounting::financial::TransactionTemplate m_payMonthlyLoanAmountTransactionTemplate;
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
}
}
}

#endif