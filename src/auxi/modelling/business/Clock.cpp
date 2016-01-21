#include "Clock.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::business;

Clock::Clock()
{
    //ctor
}

Clock::Clock(const Clock& other)
{
    m_startDateTime = other.m_startDateTime;
    m_timeStepPeriodDuration = other.m_timeStepPeriodDuration;
    m_timeStepPeriodCount = other.m_timeStepPeriodCount;
    m_timeStepIndex = other.m_timeStepIndex;
}

Clock::~Clock()
{

}

boost::posix_time::ptime Clock::GetStartDateTime() const { return m_startDateTime; }
void Clock::SetStartDateTime(boost::posix_time::ptime value) { m_startDateTime = value; }
TimePeriod::TimePeriod Clock::GetTimeStepPeriodDuration() const { return m_timeStepPeriodDuration; }
void Clock::SetTimeStepPeriodDuration(TimePeriod::TimePeriod value) { m_timeStepPeriodDuration = value; }
int Clock::GetTimeStepPeriodCount() const { return m_timeStepPeriodCount; }
void Clock::SetTimeStepPeriodCount(int value) { m_timeStepPeriodCount = value; }
int Clock::GetTimeStepIndex() const { return m_timeStepIndex; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Clock& lhs, const Clock& rhs)
    {
        return 1 == 1
	  && lhs.m_startDateTime == rhs.m_startDateTime
	  && lhs.m_timeStepPeriodDuration == rhs.m_timeStepPeriodDuration
	  && lhs.m_timeStepPeriodCount == rhs.m_timeStepPeriodCount
	  && lhs.m_timeStepIndex == rhs.m_timeStepIndex
	  ;
    }

    bool operator!=(const Clock& lhs, const Clock& rhs)
    {
        return 1 != 1
	  || lhs.m_startDateTime != rhs.m_startDateTime
	  || lhs.m_timeStepPeriodDuration != rhs.m_timeStepPeriodDuration
	  || lhs.m_timeStepPeriodCount != rhs.m_timeStepPeriodCount
	  || lhs.m_timeStepIndex != rhs.m_timeStepIndex
	;
    }

    std::ostream& operator<<(std::ostream& os, const Clock& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
