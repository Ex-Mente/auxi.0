#include "CapitalLoanActivity.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>


using namespace auxi::modelling::business;

CapitalLoanActivity::CapitalLoanActivity()
{
    //ctor
    initialize();
}

CapitalLoanActivity::CapitalLoanActivity(const CapitalLoanActivity& other)
{
    m_date = other.m_date;
    m_generalLedgerLiabilityAccount = other.m_generalLedgerLiabilityAccount;
    m_generalLedgerExpenseAccount = other.m_generalLedgerExpenseAccount;
    m_makeLoanTransactionTemplate = other.m_makeLoanTransactionTemplate;
    m_considerInterestTransactionTemplate = other.m_considerInterestTransactionTemplate;
    m_payMonthlyLoanAmountTransactionTemplate = other.m_payMonthlyLoanAmountTransactionTemplate;
    m_loanAmount = other.m_loanAmount;
    m_interestRate = other.m_interestRate;
    m_monthlyInterestRate = other.m_monthlyInterestRate;
    m_periodInMonths = other.m_periodInMonths;
    m_amountLeft = other.m_amountLeft;
    m_monthsLeft = other.m_monthsLeft;
    m_monthlyPayment = other.m_monthlyPayment;
    m_currentInterestAmount = other.m_currentInterestAmount;
}

CapitalLoanActivity::~CapitalLoanActivity()
{

}

boost::posix_time::ptime CapitalLoanActivity::GetDate() const { return m_date; }
void CapitalLoanActivity::SetDate(boost::posix_time::ptime value) { m_date = value; }
auxi::modelling::accounting::financial::GeneralLedgerAccount* CapitalLoanActivity::GetGeneralLedgerLiabilityAccount() const { return m_generalLedgerLiabilityAccount; }
void CapitalLoanActivity::SetGeneralLedgerLiabilityAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* value) { m_generalLedgerLiabilityAccount = value; }
auxi::modelling::accounting::financial::GeneralLedgerAccount* CapitalLoanActivity::GetGeneralLedgerExpenseAccount() const { return m_generalLedgerExpenseAccount; }
void CapitalLoanActivity::SetGeneralLedgerExpenseAccount(auxi::modelling::accounting::financial::GeneralLedgerAccount* value) { m_generalLedgerExpenseAccount = value; }
auxi::modelling::accounting::financial::TransactionTemplate& CapitalLoanActivity::GetMakeLoanTransactionTemplate() { return m_makeLoanTransactionTemplate; }
void CapitalLoanActivity::SetMakeLoanTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& value) { m_makeLoanTransactionTemplate = value; }
auxi::modelling::accounting::financial::TransactionTemplate& CapitalLoanActivity::GetConsiderInterestTransactionTemplate() { return m_considerInterestTransactionTemplate; }
void CapitalLoanActivity::SetConsiderInterestTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& value) { m_considerInterestTransactionTemplate = value; }
auxi::modelling::accounting::financial::TransactionTemplate& CapitalLoanActivity::GetPayMonthlyLoanAmountTransactionTemplate() { return m_payMonthlyLoanAmountTransactionTemplate; }
void CapitalLoanActivity::SetPayMonthlyLoanAmountTransactionTemplate(auxi::modelling::accounting::financial::TransactionTemplate& value) { m_payMonthlyLoanAmountTransactionTemplate = value; }
double CapitalLoanActivity::GetLoanAmount() const { return m_loanAmount; }
void CapitalLoanActivity::SetLoanAmount(double value) { m_loanAmount = value; }
double CapitalLoanActivity::GetInterestRate() const { return m_interestRate; }
double CapitalLoanActivity::GetPeriodInMonths() const { return m_periodInMonths; }
void CapitalLoanActivity::SetPeriodInMonths(double value) { m_periodInMonths = value; }
double CapitalLoanActivity::GetAmountLeft() const { return m_amountLeft; }
double CapitalLoanActivity::GetMonthsLeft() const { return m_monthsLeft; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_generalLedgerLiabilityAccount == rhs.m_generalLedgerLiabilityAccount
	  && lhs.m_generalLedgerExpenseAccount == rhs.m_generalLedgerExpenseAccount
	  && lhs.m_makeLoanTransactionTemplate == rhs.m_makeLoanTransactionTemplate
	  && lhs.m_considerInterestTransactionTemplate == rhs.m_considerInterestTransactionTemplate
	  && lhs.m_payMonthlyLoanAmountTransactionTemplate == rhs.m_payMonthlyLoanAmountTransactionTemplate
	  && almost_equal(lhs.m_loanAmount, rhs.m_loanAmount, 5)
	  && almost_equal(lhs.m_interestRate, rhs.m_interestRate, 5)
	  && almost_equal(lhs.m_monthlyInterestRate, rhs.m_monthlyInterestRate, 5)
	  && almost_equal(lhs.m_periodInMonths, rhs.m_periodInMonths, 5)
	  && almost_equal(lhs.m_amountLeft, rhs.m_amountLeft, 5)
	  && almost_equal(lhs.m_monthsLeft, rhs.m_monthsLeft, 5)
	  && almost_equal(lhs.m_monthlyPayment, rhs.m_monthlyPayment, 5)
	  && almost_equal(lhs.m_currentInterestAmount, rhs.m_currentInterestAmount, 5)
	  ;
    }

    bool operator!=(const CapitalLoanActivity& lhs, const CapitalLoanActivity& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_generalLedgerLiabilityAccount != rhs.m_generalLedgerLiabilityAccount
	  || lhs.m_generalLedgerExpenseAccount != rhs.m_generalLedgerExpenseAccount
	  || lhs.m_makeLoanTransactionTemplate != rhs.m_makeLoanTransactionTemplate
	  || lhs.m_considerInterestTransactionTemplate != rhs.m_considerInterestTransactionTemplate
	  || lhs.m_payMonthlyLoanAmountTransactionTemplate != rhs.m_payMonthlyLoanAmountTransactionTemplate
	  || !almost_equal(lhs.m_loanAmount, rhs.m_loanAmount, 5)
	  || !almost_equal(lhs.m_interestRate, rhs.m_interestRate, 5)
	  || !almost_equal(lhs.m_monthlyInterestRate, rhs.m_monthlyInterestRate, 5)
	  || !almost_equal(lhs.m_periodInMonths, rhs.m_periodInMonths, 5)
	  || !almost_equal(lhs.m_amountLeft, rhs.m_amountLeft, 5)
	  || !almost_equal(lhs.m_monthsLeft, rhs.m_monthsLeft, 5)
	  || !almost_equal(lhs.m_monthlyPayment, rhs.m_monthlyPayment, 5)
	  || !almost_equal(lhs.m_currentInterestAmount, rhs.m_currentInterestAmount, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const CapitalLoanActivity& obj)
    {
        os << obj.GetName();
        return os;
    }
}
}
}
