#ifndef ACTIVITY_H
#define ACTIVITY_H



#include "Units.h"
#include "GeneralLedger.h"
#include "Clock.h"
#include "ExecutionObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business {
    class Activity;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;

    // Declare classes
    //
    class Activity : public ExecutionObject
    {
        public:
            Activity();

            ~Activity();
            Activity(const Activity& other);

            friend bool operator==(const Activity& lhs, const Activity& rhs);
            friend bool operator!=(const Activity& lhs, const Activity& rhs);
            friend std::ostream& operator<<(std::ostream&, const Activity&);

            bool IsValid() const { return true; }


             //Activity(std::string name, std::string description = "", int start = 0, int end = -1, int interval = 1);

             Activity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, boost::posix_time::ptime end = boost::posix_time::max_date_time, int interval = 1);

             //Activity(std::string name, std::string description = "", boost::posix_time::ptime start = boost::posix_time::min_date_time, int repeat = 1, int interval = 1);

            virtual bool OnExecute_MeetExecutionCriteria(int executionMonth);

            virtual void prepare_to_run(Clock* clock, int ix_period);

            void SetName(std::string value);

            virtual void set_path(std::string parent_path);

            virtual void run(Clock* clock, int ix_period, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            Units& GetCurrency();
            void SetCurrency(Units& currency);

            int GetStartPeriod() const;
            void SetStartPeriod(int startPeriod);

            int GetEndPeriod() const;
            void SetEndPeriod(int endPeriod);

            int GetInterval() const;
            void SetInterval(int interval);

            int GetPeriodCount() const;
            void SetPeriodCount(int periodCount);

            std::string Getpath() const;
            void Setpath(std::string path);


        protected:
	        Units m_currency;
	        int m_startPeriod = -1;
	        int m_endPeriod = -1;
	        int m_interval = 1;
	        int m_periodCount = -1;
	        std::string m_path = "";
	        boost::posix_time::ptime m_startDate = boost::posix_time::min_date_time;
	        boost::posix_time::ptime m_endDate = boost::posix_time::max_date_time;

        private:
    };
}}}
#endif