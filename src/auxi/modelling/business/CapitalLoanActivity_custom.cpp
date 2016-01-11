#include "CapitalLoanActivity.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

void CapitalLoanActivity::initialize()
{
    m_makeLoanTransactionTemplate.SetName("MakeLoan");
    m_considerInterestTransactionTemplate.SetName("ConsiderInterest");
    m_payMonthlyLoanAmountTransactionTemplate.SetName("PayInterest");
}

void CapitalLoanActivity::SetInterestRate(double value)
{
    m_interestRate = value;
    m_monthlyInterestRate = m_interestRate / 12;
}

double CapitalLoanActivity::GetMonthlyPayment()
{
    m_monthlyPayment = (m_loanAmount * m_monthlyInterestRate) / (1 - (1 / std::pow((1 + m_monthlyInterestRate), m_periodInMonths)));
    return m_monthlyPayment;
}

double CapitalLoanActivity::GetCurrentInterestAmount()
{
    m_currentInterestAmount = (m_amountLeft * m_interestRate) / 12.0;
    return m_currentInterestAmount;
}

bool CapitalLoanActivity::OnExecute_MeetExecutionCriteria(int ix_interval)
{
    return Activity::OnExecute_MeetExecutionCriteria(ix_interval) && ix_interval <= m_executionStartAtInterval + m_periodInMonths;
}

void CapitalLoanActivity::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    Activity::prepare_to_run(clock, totalIntervalsToRun);
    m_monthsLeft = m_periodInMonths;
    m_amountLeft = m_loanAmount;
}

void CapitalLoanActivity::run(Clock* clock, int ix_interval,
                              auxi::modelling::accounting::financial::GeneralLedger* generalLedger,
                              auxi::modelling::accounting::stock::StockLedger* stockLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_interval)) return;
    boost::posix_time::ptime currentExecutionDateTime = clock->GetDateTimeAtInterval(ix_interval);

    if (ix_interval == m_executionStartAtInterval)
    {
        auto make_loan_t = generalLedger->create_transaction(
            m_makeLoanTransactionTemplate.GetName(),
            m_makeLoanTransactionTemplate.GetName(),
            m_makeLoanTransactionTemplate.GetCreditAccountName(),
            m_makeLoanTransactionTemplate.GetDebitAccountName(),
            path);
        make_loan_t->SetDate(currentExecutionDateTime);
        make_loan_t->SetCurrency(m_currency);
        make_loan_t->SetAmount(std::abs(m_loanAmount));
    }
    else
    {
        GetCurrentInterestAmount();
        auto consider_interest_t = generalLedger->create_transaction(
            m_considerInterestTransactionTemplate.GetName(),
            m_considerInterestTransactionTemplate.GetName(),
            m_considerInterestTransactionTemplate.GetCreditAccountName(),
            m_considerInterestTransactionTemplate.GetDebitAccountName(),
            path);
        consider_interest_t->SetDate(currentExecutionDateTime);
        consider_interest_t->SetCurrency(m_currency);
        consider_interest_t->SetAmount(std::abs(m_currentInterestAmount));

        auto monthly_loan_t = generalLedger->create_transaction(
            m_payMonthlyLoanAmountTransactionTemplate.GetName(),
            m_payMonthlyLoanAmountTransactionTemplate.GetName(),
            m_payMonthlyLoanAmountTransactionTemplate.GetCreditAccountName(),
            m_payMonthlyLoanAmountTransactionTemplate.GetDebitAccountName(),
            path);
        monthly_loan_t->SetDate(currentExecutionDateTime);
        monthly_loan_t->SetCurrency(m_currency);
        monthly_loan_t->SetAmount(std::abs(m_monthlyPayment));

        m_amountLeft += m_currentInterestAmount - m_monthlyPayment;
    }
    m_monthsLeft--;
}




