#ifndef COMPONENT_H
#define COMPONENT_H



#include "VariableGroup.h"
#include "Activity.h"
#include "Clock.h"
#include "Transaction.h"
#include "ExecutionObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business {
    class Component;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;

    // Declare classes
    //
    class Component : public ExecutionObject
    {
        public:
            Component();
            Component(std::string name, std::string description) : ExecutionObject(name, description)
            {
            };
            ~Component();
            Component(const Component& other);

            friend bool operator==(const Component& lhs, const Component& rhs);
            friend bool operator!=(const Component& lhs, const Component& rhs);
            friend std::ostream& operator<<(std::ostream&, const Component&);

            bool IsValid() const { return true; }
            Component* Clone() const { return new Component(*this); }


            Component* create_component(std::string name);

            void remove_component(std::string name);

            void SetName(std::string value);

            void set_path(std::string parent_path);

            void prepare_to_run(Clock* clock, int totalIntervalsToRun);

            void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            std::vector<VariableGroup*>& GetVariableGroupList();

            std::vector<Component*>& GetComponentList();

            std::vector<Activity*>& GetActivityList();

            std::string Getpath() const;
            void Setpath(std::string path);


        protected:
	        std::vector<VariableGroup*> m_variableGroupList;
	        std::vector<Component*> m_componentList;
	        std::vector<Activity*> m_activityList;
	        std::string m_path = "";

        private:
    };
}}}
#endif