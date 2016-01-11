#ifndef TIMEBASEDMODEL_H
#define TIMEBASEDMODEL_H



#include "Entity.h"
#include "Units.h"
#include "Clock.h"
#include "Model.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//




namespace auxi { namespace modelling { namespace business { 
    class TimeBasedModel;
}
}
}

namespace auxi { namespace modelling { namespace business { 
    using namespace auxi::core;

    // Declare classes
    //
    class TimeBasedModel : public Model
    {
        using NamedObject::GetName;
        public:
            TimeBasedModel();
            TimeBasedModel(std::string name, std::string description) : Model(name, description)
            {
                initialize();
            };
            ~TimeBasedModel();
            TimeBasedModel(const TimeBasedModel& other);

            friend bool operator==(const TimeBasedModel& lhs, const TimeBasedModel& rhs);
            friend bool operator!=(const TimeBasedModel& lhs, const TimeBasedModel& rhs);
            friend std::ostream& operator<<(std::ostream&, const TimeBasedModel&);

            bool IsValid() const { return true; }
            TimeBasedModel* Clone() const { return new TimeBasedModel(*this); }

	      
            void initialize();
	      
            Entity* create_entity(std::string name);
	      
            void remove_entity(std::string name);
	      
            virtual void prepare_to_run();
	      
            void run();
            std::vector<Entity*>& GetEntityList();
            Units& GetCurrency();
            void SetCurrency(Units& currency);
            int GetTotalIntervalsToRun() const;
            void SetTotalIntervalsToRun(int totalIntervalsToRun);
            Clock& GetClock();
        protected:
	        std::vector<Entity*> m_entityList;
	        Units m_currency;
	        int m_totalIntervalsToRun = 12;
	        Clock m_clock;
        private:
    };
}
}
}

#endif