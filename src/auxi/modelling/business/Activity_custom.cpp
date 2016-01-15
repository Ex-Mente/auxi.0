#include "Activity.h"
#include <iostream>

using namespace auxi::modelling::business;

void Activity::SetName(std::string value)
{
    m_name = value;
    unsigned int ix = m_path.rfind("/");
    if(ix != string::npos) m_path = value;
    else m_path = m_path.substr(0,ix) + value;
}

void Activity::set_path(std::string parent_path)
{
    m_path = parent_path + "/" + m_name;
}

bool Activity::OnExecute_MeetExecutionCriteria(int executionMonth)
{
    if (m_executeInterval != 0 && (executionMonth+1) % m_executeInterval != 0) return false; //executionMonth + 1 as execution month is zero based
    return executionMonth >= m_executionStartAtInterval && executionMonth + m_executeInterval <= m_executionEndAtInterval;
}

void Activity::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    if (m_totalIntervalsToRun != -1)
        m_executionEndAtInterval = m_executionStartAtInterval + m_totalIntervalsToRun;
    else
        m_executionEndAtInterval = m_executionStartAtInterval + totalIntervalsToRun;

}

void Activity::run(Clock* clock, int ix_month,
                   auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger,
                   auxi::modelling::stock::double_entry_system::StockLedger* stockLedger)
{

}
