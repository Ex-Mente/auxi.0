#include "TimeBasedModel.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

void TimeBasedModel::initialize()
{
    m_clock.SetName("Clock");
    m_clock.SetStartDateTime(boost::posix_time::second_clock::local_time());
    m_clock.SetTimeStepInterval(TimeInterval::Month);
}

Entity* TimeBasedModel::create_entity(std::string name)
{
    auto entity = new Entity(name, "");
    m_entityList.push_back(entity);
    return entity;
}

void TimeBasedModel::remove_entity(std::string name)
{
    for(auto itr = m_entityList.begin(); itr != m_entityList.end(); ++itr)
    {
        if((*itr)->GetName() == name)
        {
           delete (*itr);
           m_entityList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The entity: '" + name + "' does not exist in the time based model's entity list'.");
}

void TimeBasedModel::prepare_to_run()
{
    m_clock.reset();
    for(auto item: m_entityList)
        item->prepare_to_run(&m_clock, m_totalIntervalsToRun);
}
void TimeBasedModel::run()
{
    prepare_to_run();
    for (int interval=0; interval<m_totalIntervalsToRun; interval++)
    {
        m_clock.tick();
        for(auto item: m_entityList)
            item->run(&m_clock, interval, m_currency);
    }
}






