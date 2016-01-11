#include "Component.h"
#include "Activity.h"

using namespace auxi::modelling::business;

void Component::SetName(std::string value)
{
    m_name = value;
    unsigned int ix = m_path.rfind("/");
    if(ix != string::npos) m_path = value;
    else m_path = m_path.substr(0,ix) + value;
}

void Component::set_path(std::string parent_path)
{
    m_path = parent_path + "/" + m_name;
    for(auto item: m_activityList) item->set_path(m_path);
    for(auto item: m_componentList) item->set_path(m_path);
}

Component* Component::create_component(std::string name)
{
    auto component = new Component(name, "");
    component->set_path(m_path);
    m_componentList.push_back(component);
    return component;
}

void Component::remove_component(std::string name)
{
    for(auto itr = m_componentList.begin(); itr != m_componentList.end(); ++itr)
    {
        if((*itr)->GetName() == name)
        {
           delete (*itr);
           m_componentList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The component: '" + name + "' does not exist in the component's component list'.");
}

void Component::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    for(auto item: m_activityList) item->prepare_to_run(clock, totalIntervalsToRun);
    for(auto item: m_componentList) item->prepare_to_run(clock, totalIntervalsToRun);
}

void Component::run(Clock* clock, int ix_interval,
                    auxi::modelling::accounting::financial::GeneralLedger* generalLedger,
                    auxi::modelling::accounting::stock::StockLedger* stockLedger)
{
    for(auto item: m_activityList)
        item->run(clock, ix_interval, generalLedger, stockLedger);
    for(auto item: m_componentList)
        item->run(clock, ix_interval, generalLedger, stockLedger);
}


