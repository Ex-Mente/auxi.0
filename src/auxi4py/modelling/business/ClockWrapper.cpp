
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Clock.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct ClockWrapper : Clock, wrapper<Clock>
{
};

void export_auxi_modelling_business_Clock()
{
  // Python C++ mappings
  enum_<auxi::modelling::business::TimeInterval::TimeInterval>("TimeInterval")
      .value("Millisecond", TimeInterval::Millisecond)
      .value("Second", TimeInterval::Second)
      .value("Minute", TimeInterval::Minute)
      .value("Hour", TimeInterval::Hour)
      .value("Day", TimeInterval::Day)
      .value("Week", TimeInterval::Week)
      .value("Month", TimeInterval::Month)
      .value("Year", TimeInterval::Year)
      ;

    //class_<Clock, Clock*, bases<NamedObject>>("Clock", init<>())
    class_<Clock, Clock*, bases<NamedObject>>("Clock", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
	.def("tick", &Clock::tick)
	.def("reset", &Clock::reset)
	.def("getDateTime", &Clock::GetDateTime)
	.def("getDateTimeAtInterval", &Clock::GetDateTimeAtInterval)
	.add_property("startDateTime", &Clock::GetStartDateTime, &Clock::SetStartDateTime)
	.add_property("timeStepInterval", &Clock::GetTimeStepInterval, &Clock::SetTimeStepInterval)
	.add_property("timeStepIntervalCount", &Clock::GetTimeStepIntervalCount, &Clock::SetTimeStepIntervalCount)
	.add_property("timeStepIndex", &Clock::GetTimeStepIndex)
    ;

    //implicitly_convertible<ClockWrapper*,Clock*>();
    implicitly_convertible<Clock*,NamedObject*>();
    class_<std::vector<Clock*>>("ClockList").def(vector_indexing_suite<std::vector<Clock*>>());
}