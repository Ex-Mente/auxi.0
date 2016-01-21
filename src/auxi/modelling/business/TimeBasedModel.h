#ifndef TIMEBASEDMODEL_H
#define TIMEBASEDMODEL_H



#include "Entity.h"
#include "Units.h"
#include "Clock.h"
#include "Model.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business { 
    class TimeBasedModel;
}}}

namespace auxi { namespace modelling { namespace business { 
    using namespace auxi::core;

    // Declare classes
    //
    class TimeBasedModel : public Model
    {
        using NamedObject::GetName;
        public:
            TimeBasedModel();
            
            ~TimeBasedModel();
            TimeBasedModel(const TimeBasedModel& other);

            friend bool operator==(const TimeBasedModel& lhs, const TimeBasedModel& rhs);
            friend bool operator!=(const TimeBasedModel& lhs, const TimeBasedModel& rhs);
            friend std::ostream& operator<<(std::ostream&, const TimeBasedModel&);

            bool IsValid() const { return true; }
            TimeBasedModel* Clone() const { return new TimeBasedModel(*this); }

	      
             TimeBasedModel(std::string name, std::string description = "", boost::posix_time::ptime start_date = boost::posix_time::ptime(boost::posix_time::second_clock::local_time()), TimePeriod::TimePeriod period_duration = TimePeriod::month, int period_count = 60);
	      
            void initialize();
	      
            Entity* create_entity(std::string name);
	      
            void remove_entity(std::string name);
	      
            void prepare_to_run();
	      
            void run();
            std::vector<Entity*>& GetEntityList();

            Units& GetCurrency();
            void SetCurrency(Units& currency);

            int GetPeriodCount() const;
            void SetPeriodCount(int periodCount);

            Clock& GetClock();


        protected:
	        std::vector<Entity*> m_entityList;
	        Units m_currency;
	        int m_periodCount = 60;
	        Clock m_clock;

        private:
    };
}}}
#endif