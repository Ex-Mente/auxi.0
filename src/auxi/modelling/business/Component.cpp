#include "Component.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::business;

Component::Component()
{
    //ctor
}

Component::Component(const Component& other)
{
    m_variableGroupList = other.m_variableGroupList;
    m_componentList = other.m_componentList;
    m_activityList = other.m_activityList;
    m_path = other.m_path;
}

Component::~Component()
{

}

std::vector<VariableGroup*>& Component::GetVariableGroupList() { return m_variableGroupList; }
std::vector<Component*>& Component::GetComponentList() { return m_componentList; }
std::vector<Activity*>& Component::GetActivityList() { return m_activityList; }
std::string Component::Getpath() const { return m_path; }
void Component::Setpath(std::string value) { m_path = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const Component& lhs, const Component& rhs)
    {
        return 1 == 1
	  && lhs.m_variableGroupList == rhs.m_variableGroupList
	  && lhs.m_componentList == rhs.m_componentList
	  && lhs.m_activityList == rhs.m_activityList
	  && lhs.m_path == rhs.m_path
	  ;
    }

    bool operator!=(const Component& lhs, const Component& rhs)
    {
        return 1 != 1
	  || lhs.m_variableGroupList != rhs.m_variableGroupList
	  || lhs.m_componentList != rhs.m_componentList
	  || lhs.m_activityList != rhs.m_activityList
	  || lhs.m_path != rhs.m_path
	;
    }

    std::ostream& operator<<(std::ostream& os, const Component& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
