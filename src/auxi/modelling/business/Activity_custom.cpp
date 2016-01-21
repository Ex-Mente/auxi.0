#include "Activity.h"
#include <iostream>

using namespace auxi::modelling::business;
/*
Activity::Activity(std::string name, std::string description, int start, int end, int interval) : ExecutionObject(name, description)
{
    m_startPeriod = start;
    m_endPeriod = end;
    m_interval = interval;
    if(end == -1) m_periodCount = -1;
    else m_periodCount = end - start;
}*/

Activity::Activity(std::string name, std::string description, boost::posix_time::ptime start, boost::posix_time::ptime end, int interval) : ExecutionObject(name, description)
{
    m_startDate = start;
    m_endDate = end;
    m_interval = interval;
}
/*
Activity::Activity(std::string name, std::string description, boost::posix_time::ptime start, int repeat, int interval) : ExecutionObject(name, description)
{
    m_startDate = start;
    m_interval = interval;
    m_periodCount = repeat;
}*/

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

bool Activity::OnExecute_MeetExecutionCriteria(int ix_period)
{
    if (m_interval != 0 && (ix_period+1) % m_interval != 0) return false; //executionMonth + 1 as execution month is zero based
    return ix_period >= m_startPeriod && ix_period + m_interval <= m_endPeriod;
}

void Activity::prepare_to_run(Clock* clock, int period_count)
{
    if(m_startPeriod == -1 && m_startDate != boost::posix_time::min_date_time) {
        // Set the Start date
        for(int i=0; i<period_count; i++)
            if(clock->GetDateTimeAtPeriodIndex(i) > m_startDate) {
                m_startPeriod = i;
                break;
            }
    }
    if(m_startPeriod == -1) m_startPeriod = 0;
    if(m_periodCount == -1 && m_endDate != boost::posix_time::max_date_time) {
        // Set the Start date
        for(int i=0; i<period_count; i++)
            if(clock->GetDateTimeAtPeriodIndex(i) > m_endDate) {
                m_periodCount = i - m_startPeriod;
                break;
            }
    }
    if (m_periodCount != -1)
        m_endPeriod = m_startPeriod + m_periodCount;
    else
        m_endPeriod = m_startPeriod + period_count;

}

void Activity::run(Clock* clock, int ix_month,
                   auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{

}
