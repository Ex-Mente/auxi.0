#include "BasicActivity.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;
/*
BasicActivity::BasicActivity(std::string name, std::string description, int start, int end, int interval, double amount, auxi::modelling::financial::double_entry_system::TransactionTemplate tx_template) : Activity(name, description, start, end, interval)
{
    m_amount = amount;
    m_txTemplate = tx_template;
}*/

BasicActivity::BasicActivity(std::string name, std::string description, boost::posix_time::ptime start, boost::posix_time::ptime end, int interval, double amount, auxi::modelling::financial::double_entry_system::TransactionTemplate tx_template) : Activity(name, description, start, end, interval)
{
    m_amount = amount;
    m_txTemplate = tx_template;
}
/*
BasicActivity::BasicActivity(std::string name, std::string description, boost::posix_time::ptime start, int repeat, int interval, double amount, auxi::modelling::financial::double_entry_system::TransactionTemplate tx_template) : Activity(name, description, start, repeat, interval)
{
    m_amount = amount;
    m_txTemplate = tx_template;
}*/

void BasicActivity::initialize()
{
    m_txTemplate.SetName("Unkown");
}

bool BasicActivity::OnExecute_MeetExecutionCriteria(int ix_period)
{
    return Activity::OnExecute_MeetExecutionCriteria(ix_period) && m_amount > 0;
}

void BasicActivity::prepare_to_run(Clock* clock, int period_count)
{
    Activity::prepare_to_run(clock, period_count);
}

void BasicActivity::run(Clock* clock, int ix_period,
                        auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_period)) return;

    auto t = generalLedger->create_transaction(
        m_txTemplate.GetName(),
        m_txTemplate.GetName(),
        m_txTemplate.GetCrAccount(),
        m_txTemplate.GetDtAccount(),
        path);
    t->SetDate(clock->GetDateTimeAtPeriodIndex(ix_period));
    t->SetCurrency(m_currency);
    t->SetAmount(std::abs(m_amount));
}




