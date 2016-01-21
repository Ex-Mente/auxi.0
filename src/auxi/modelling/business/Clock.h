#ifndef CLOCK_H
#define CLOCK_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business { 
    class Clock;
}}}

namespace auxi { namespace modelling { namespace business { 
    using namespace auxi::core;

    // Declare enums
    //
    namespace TimePeriod
    {
        enum TimePeriod
        {
	        millisecond,
	        second,
	        minute,
	        hour,
	        day,
	        week,
	        month,
	        year,
        };
    }

    // Declare classes
    //
    class Clock : public NamedObject
    {
        public:
            Clock();
            
            Clock(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Clock();
            Clock(const Clock& other);

            friend bool operator==(const Clock& lhs, const Clock& rhs);
            friend bool operator!=(const Clock& lhs, const Clock& rhs);
            friend std::ostream& operator<<(std::ostream&, const Clock&);

            bool IsValid() const { return true; }
            Clock* Clone() const { return new Clock(*this); }

	      
            void tick();
	      
            void reset();
	      
            boost::posix_time::ptime GetDateTime();
	      
            boost::posix_time::ptime GetDateTimeAtPeriodIndex(int period_count);
            boost::posix_time::ptime GetStartDateTime() const;
            void SetStartDateTime(boost::posix_time::ptime startDateTime);

            TimePeriod::TimePeriod GetTimeStepPeriodDuration() const;
            void SetTimeStepPeriodDuration(TimePeriod::TimePeriod timeStepPeriodDuration);

            int GetTimeStepPeriodCount() const;
            void SetTimeStepPeriodCount(int timeStepPeriodCount);

            int GetTimeStepIndex() const;


        protected:
	        boost::posix_time::ptime m_startDateTime = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        TimePeriod::TimePeriod m_timeStepPeriodDuration = TimePeriod::TimePeriod::month;
	        int m_timeStepPeriodCount = 1;
	        int m_timeStepIndex = 0;

        private:
    };
}}}
#endif