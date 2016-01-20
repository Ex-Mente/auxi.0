#include "CapitalLoanActivity.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

void CapitalLoanActivity::initialize()
{
    m_makeLoanTxTemplate.SetName("MakeLoan");
    m_considerInterestTxTemplate.SetName("ConsiderInterest");
    m_payMonthlyLoanAmountTxTemplate.SetName("PayInterest");
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
                              auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_interval)) return;
    boost::posix_time::ptime currentExecutionDateTime = clock->GetDateTimeAtInterval(ix_interval);

    if (ix_interval == m_executionStartAtInterval)
    {
        auto make_loan_t = generalLedger->create_transaction(
            m_makeLoanTxTemplate.GetName(),
            m_makeLoanTxTemplate.GetName(),
            m_makeLoanTxTemplate.GetCrAccount(),
            m_makeLoanTxTemplate.GetDtAccount(),
            path);
        make_loan_t->SetDate(currentExecutionDateTime);
        make_loan_t->SetCurrency(m_currency);
        make_loan_t->SetAmount(std::abs(m_loanAmount));
    }
    else
    {
        GetCurrentInterestAmount();
        auto consider_interest_t = generalLedger->create_transaction(
            m_considerInterestTxTemplate.GetName(),
            m_considerInterestTxTemplate.GetName(),
            m_considerInterestTxTemplate.GetCrAccount(),
            m_considerInterestTxTemplate.GetDtAccount(),
            path);
        consider_interest_t->SetDate(currentExecutionDateTime);
        consider_interest_t->SetCurrency(m_currency);
        consider_interest_t->SetAmount(std::abs(m_currentInterestAmount));

        auto monthly_loan_t = generalLedger->create_transaction(
            m_payMonthlyLoanAmountTxTemplate.GetName(),
            m_payMonthlyLoanAmountTxTemplate.GetName(),
            m_payMonthlyLoanAmountTxTemplate.GetCrAccount(),
            m_payMonthlyLoanAmountTxTemplate.GetDtAccount(),
            path);
        monthly_loan_t->SetDate(currentExecutionDateTime);
        monthly_loan_t->SetCurrency(m_currency);
        monthly_loan_t->SetAmount(std::abs(m_monthlyPayment));

        m_amountLeft += m_currentInterestAmount - m_monthlyPayment;
    }
    m_monthsLeft--;
}




