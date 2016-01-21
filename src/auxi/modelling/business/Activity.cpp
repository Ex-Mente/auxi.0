#include "Activity.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::business;

Activity::Activity()
{
    //ctor
}

Activity::Activity(const Activity& other)
{
    m_currency = other.m_currency;
    m_startPeriod = other.m_startPeriod;
    m_endPeriod = other.m_endPeriod;
    m_interval = other.m_interval;
    m_periodCount = other.m_periodCount;
    m_path = other.m_path;
    m_startDate = other.m_startDate;
    m_endDate = other.m_endDate;
}

Activity::~Activity()
{

}

Units& Activity::GetCurrency() { return m_currency; }
void Activity::SetCurrency(Units& value) { m_currency = value; }
int Activity::GetStartPeriod() const { return m_startPeriod; }
void Activity::SetStartPeriod(int value) { m_startPeriod = value; }
int Activity::GetEndPeriod() const { return m_endPeriod; }
void Activity::SetEndPeriod(int value) { m_endPeriod = value; }
int Activity::GetInterval() const { return m_interval; }
void Activity::SetInterval(int value) { m_interval = value; }
int Activity::GetPeriodCount() const { return m_periodCount; }
void Activity::SetPeriodCount(int value) { m_periodCount = value; }
std::string Activity::Getpath() const { return m_path; }
void Activity::Setpath(std::string value) { m_path = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Activity& lhs, const Activity& rhs)
    {
        return 1 == 1
	  && lhs.m_currency == rhs.m_currency
	  && lhs.m_startPeriod == rhs.m_startPeriod
	  && lhs.m_endPeriod == rhs.m_endPeriod
	  && lhs.m_interval == rhs.m_interval
	  && lhs.m_periodCount == rhs.m_periodCount
	  && lhs.m_path == rhs.m_path
	  && lhs.m_startDate == rhs.m_startDate
	  && lhs.m_endDate == rhs.m_endDate
	  ;
    }

    bool operator!=(const Activity& lhs, const Activity& rhs)
    {
        return 1 != 1
	  || lhs.m_currency != rhs.m_currency
	  || lhs.m_startPeriod != rhs.m_startPeriod
	  || lhs.m_endPeriod != rhs.m_endPeriod
	  || lhs.m_interval != rhs.m_interval
	  || lhs.m_periodCount != rhs.m_periodCount
	  || lhs.m_path != rhs.m_path
	  || lhs.m_startDate != rhs.m_startDate
	  || lhs.m_endDate != rhs.m_endDate
	;
    }

    std::ostream& operator<<(std::ostream& os, const Activity& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
