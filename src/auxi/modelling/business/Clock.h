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
    namespace TimeInterval
    {
        enum TimeInterval
        {
	        Millisecond,
	        Second,
	        Minute,
	        Hour,
	        Day,
	        Week,
	        Month,
	        Year,
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
	      
            boost::posix_time::ptime GetDateTimeAtInterval(int interval);
            boost::posix_time::ptime GetStartDateTime() const;
            void SetStartDateTime(boost::posix_time::ptime startDateTime);

            TimeInterval::TimeInterval GetTimeStepInterval() const;
            void SetTimeStepInterval(TimeInterval::TimeInterval timeStepInterval);

            int GetTimeStepIntervalCount() const;
            void SetTimeStepIntervalCount(int timeStepIntervalCount);

            int GetTimeStepIndex() const;


        protected:
	        boost::posix_time::ptime m_startDateTime = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        TimeInterval::TimeInterval m_timeStepInterval;
	        int m_timeStepIntervalCount = 1;
	        int m_timeStepIndex = 0;

        private:
    };
}}}
#endif