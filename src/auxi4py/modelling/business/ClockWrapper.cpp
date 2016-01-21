
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Clock.h"

using namespace boost::python;
using namespace auxi::modelling::business;

// Converts a C++ vector to a python list
template <class T>
boost::python::list to_python_list(std::vector<T> vector) {
    typename std::vector<T>::iterator iter;
    boost::python::list list;
    for (iter = vector.begin(); iter != vector.end(); ++iter) {
        list.append(*iter);
    }
    return list;
}






struct ClockWrapper : Clock, wrapper<Clock>
{
};

void export_auxi_modelling_business_Clock()
{
  // Python C++ mappings
  enum_<auxi::modelling::business::TimePeriod::TimePeriod>("TimePeriod", "None")
      .value("millisecond", TimePeriod::millisecond)
      .value("second", TimePeriod::second)
      .value("minute", TimePeriod::minute)
      .value("hour", TimePeriod::hour)
      .value("day", TimePeriod::day)
      .value("week", TimePeriod::week)
      .value("month", TimePeriod::month)
      .value("year", TimePeriod::year)
      ;



    class_<ClockWrapper, Clock*, bases<NamedObject>>("Clock", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
	.def("tick", &Clock::tick, "")
    
	.def("reset", &Clock::reset, "")
    
	.def("getDateTime", &Clock::GetDateTime, "")
    
	.def("getDateTimeAtPeriodIndex", &Clock::GetDateTimeAtPeriodIndex, "")

	.add_property("start_date_time", &Clock::GetStartDateTime, &Clock::SetStartDateTime, """")

	.add_property("time_step_period_duration", &Clock::GetTimeStepPeriodDuration, &Clock::SetTimeStepPeriodDuration, """")

	.add_property("time_step_period_count", &Clock::GetTimeStepPeriodCount, &Clock::SetTimeStepPeriodCount, """")

	.add_property("time_step_index", &Clock::GetTimeStepIndex, """")
    ;

    //implicitly_convertible<ClockWrapper*,Clock*>();
    implicitly_convertible<Clock*,NamedObject*>();
    class_<std::vector<Clock*>>("ClockList").def(vector_indexing_suite<std::vector<Clock*>>());
}