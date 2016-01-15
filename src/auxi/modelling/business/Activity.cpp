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
    m_executionStartAtInterval = other.m_executionStartAtInterval;
    m_executionEndAtInterval = other.m_executionEndAtInterval;
    m_executeInterval = other.m_executeInterval;
    m_totalIntervalsToRun = other.m_totalIntervalsToRun;
    m_path = other.m_path;
}

Activity::~Activity()
{

}

Units& Activity::GetCurrency() { return m_currency; }
void Activity::SetCurrency(Units& value) { m_currency = value; }
int Activity::GetExecutionStartAtInterval() const { return m_executionStartAtInterval; }
void Activity::SetExecutionStartAtInterval(int value) { m_executionStartAtInterval = value; }
int Activity::GetExecutionEndAtInterval() const { return m_executionEndAtInterval; }
void Activity::SetExecutionEndAtInterval(int value) { m_executionEndAtInterval = value; }
int Activity::GetExecuteInterval() const { return m_executeInterval; }
void Activity::SetExecuteInterval(int value) { m_executeInterval = value; }
int Activity::GetTotalIntervalsToRun() const { return m_totalIntervalsToRun; }
void Activity::SetTotalIntervalsToRun(int value) { m_totalIntervalsToRun = value; }
std::string Activity::Getpath() const { return m_path; }
void Activity::Setpath(std::string value) { m_path = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Activity& lhs, const Activity& rhs)
    {
        return 1 == 1
	  && lhs.m_currency == rhs.m_currency
	  && lhs.m_executionStartAtInterval == rhs.m_executionStartAtInterval
	  && lhs.m_executionEndAtInterval == rhs.m_executionEndAtInterval
	  && lhs.m_executeInterval == rhs.m_executeInterval
	  && lhs.m_totalIntervalsToRun == rhs.m_totalIntervalsToRun
	  && lhs.m_path == rhs.m_path
	  ;
    }

    bool operator!=(const Activity& lhs, const Activity& rhs)
    {
        return 1 != 1
	  || lhs.m_currency != rhs.m_currency
	  || lhs.m_executionStartAtInterval != rhs.m_executionStartAtInterval
	  || lhs.m_executionEndAtInterval != rhs.m_executionEndAtInterval
	  || lhs.m_executeInterval != rhs.m_executeInterval
	  || lhs.m_totalIntervalsToRun != rhs.m_totalIntervalsToRun
	  || lhs.m_path != rhs.m_path
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
