#include "BasicActivity.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

void BasicActivity::initialize()
{
    m_transactionTemplate.SetName("Unkown");
}

bool BasicActivity::OnExecute_MeetExecutionCriteria(int ix_interval)
{
    return Activity::OnExecute_MeetExecutionCriteria(ix_interval) && m_amount > 0;
}

void BasicActivity::prepare_to_run(Clock* clock, int totalMonthsToRun)
{
    Activity::prepare_to_run(clock, totalMonthsToRun);
}

void BasicActivity::run(Clock* clock, int ix_interval,
                        auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_interval)) return;

    auto t = generalLedger->create_transaction(
        m_transactionTemplate.GetName(),
        m_transactionTemplate.GetName(),
        m_transactionTemplate.GetCreditAccountName(),
        m_transactionTemplate.GetDebitAccountName(),
        path);
    t->SetDate(clock->GetDateTimeAtInterval(ix_interval));
    t->SetCurrency(m_currency);
    t->SetAmount(std::abs(m_amount));
}




