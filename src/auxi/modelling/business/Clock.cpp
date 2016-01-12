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
    m_timeStepInterval = other.m_timeStepInterval;
    m_timeStepIntervalCount = other.m_timeStepIntervalCount;
    m_timeStepIndex = other.m_timeStepIndex;
}

Clock::~Clock()
{

}

boost::posix_time::ptime Clock::GetStartDateTime() const { return m_startDateTime; }
void Clock::SetStartDateTime(boost::posix_time::ptime value) { m_startDateTime = value; }
TimeInterval::TimeInterval Clock::GetTimeStepInterval() const { return m_timeStepInterval; }
void Clock::SetTimeStepInterval(TimeInterval::TimeInterval value) { m_timeStepInterval = value; }
int Clock::GetTimeStepIntervalCount() const { return m_timeStepIntervalCount; }
void Clock::SetTimeStepIntervalCount(int value) { m_timeStepIntervalCount = value; }
int Clock::GetTimeStepIndex() const { return m_timeStepIndex; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Clock& lhs, const Clock& rhs)
    {
        return 1 == 1
	  && lhs.m_startDateTime == rhs.m_startDateTime
	  && lhs.m_timeStepInterval == rhs.m_timeStepInterval
	  && lhs.m_timeStepIntervalCount == rhs.m_timeStepIntervalCount
	  && lhs.m_timeStepIndex == rhs.m_timeStepIndex
	  ;
    }

    bool operator!=(const Clock& lhs, const Clock& rhs)
    {
        return 1 != 1
	  || lhs.m_startDateTime != rhs.m_startDateTime
	  || lhs.m_timeStepInterval != rhs.m_timeStepInterval
	  || lhs.m_timeStepIntervalCount != rhs.m_timeStepIntervalCount
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
