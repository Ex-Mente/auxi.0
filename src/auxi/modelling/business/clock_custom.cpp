#include "Clock.h"
#include <cmath>

using namespace auxi::modelling::business;

void Clock::tick()
{
    m_timeStepIndex++;
}

void Clock::reset()
{
    m_timeStepIndex = 0;
}


boost::posix_time::ptime Clock::GetDateTimeAtInterval(int interval)
{
    switch (m_timeStepInterval)
    {
        case TimeInterval::Millisecond:
            return m_startDateTime + boost::posix_time::milliseconds(interval);
        case TimeInterval::Second:
            return m_startDateTime + boost::posix_time::seconds(interval);
        case TimeInterval::Minute:
            return m_startDateTime + boost::posix_time::minutes(interval);
        case TimeInterval::Hour:
            return m_startDateTime + boost::posix_time::hours(interval);
        case TimeInterval::Day:
            return m_startDateTime + boost::gregorian::days(interval);
        case TimeInterval::Week:
            return m_startDateTime + boost::gregorian::days(interval*7);
        case TimeInterval::Month:
            return m_startDateTime + boost::gregorian::months(interval);
        case TimeInterval::Year:
            return m_startDateTime + boost::gregorian::years(interval);
    }
    return m_startDateTime;
}

boost::posix_time::ptime Clock::GetDateTime()
{
    return GetDateTimeAtInterval(m_timeStepIndex);
}





