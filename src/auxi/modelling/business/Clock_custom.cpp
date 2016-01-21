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


boost::posix_time::ptime Clock::GetDateTimeAtPeriodIndex(int periodCount)
{
    switch (m_timeStepPeriodDuration)
    {
        case TimePeriod::millisecond:
            return m_startDateTime + boost::posix_time::milliseconds(periodCount);
        case TimePeriod::second:
            return m_startDateTime + boost::posix_time::seconds(periodCount);
        case TimePeriod::minute:
            return m_startDateTime + boost::posix_time::minutes(periodCount);
        case TimePeriod::hour:
            return m_startDateTime + boost::posix_time::hours(periodCount);
        case TimePeriod::day:
            return m_startDateTime + boost::gregorian::days(periodCount);
        case TimePeriod::week:
            return m_startDateTime + boost::gregorian::days(periodCount*7);
        case TimePeriod::month:
            return m_startDateTime + boost::gregorian::months(periodCount);
        case TimePeriod::year:
            return m_startDateTime + boost::gregorian::years(periodCount);
    }
    return m_startDateTime;
}

boost::posix_time::ptime Clock::GetDateTime()
{
    return GetDateTimeAtPeriodIndex(m_timeStepIndex);
}





