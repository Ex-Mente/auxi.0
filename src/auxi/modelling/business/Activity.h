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
            Activity(std::string name, std::string description) : ExecutionObject(name, description)
            {
            };
            ~Activity();
            Activity(const Activity& other);

            friend bool operator==(const Activity& lhs, const Activity& rhs);
            friend bool operator!=(const Activity& lhs, const Activity& rhs);
            friend std::ostream& operator<<(std::ostream&, const Activity&);

            bool IsValid() const { return true; }


            virtual bool OnExecute_MeetExecutionCriteria(int executionMonth);

            virtual void prepare_to_run(Clock* clock, int totalMonthsToRun);

            void SetName(std::string value);

            virtual void set_path(std::string parent_path);

            virtual void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            Units& GetCurrency();
            void SetCurrency(Units& currency);

            int GetExecutionStartAtInterval() const;
            void SetExecutionStartAtInterval(int executionStartAtInterval);

            int GetExecutionEndAtInterval() const;
            void SetExecutionEndAtInterval(int executionEndAtInterval);

            int GetExecuteInterval() const;
            void SetExecuteInterval(int executeInterval);

            int GetTotalIntervalsToRun() const;
            void SetTotalIntervalsToRun(int totalIntervalsToRun);

            std::string Getpath() const;
            void Setpath(std::string path);


        protected:
	        Units m_currency;
	        int m_executionStartAtInterval = 0;
	        int m_executionEndAtInterval = 0;
	        int m_executeInterval = 12;
	        int m_totalIntervalsToRun = -1;
	        std::string m_path = "";




        private:
    };
}}}
#endif