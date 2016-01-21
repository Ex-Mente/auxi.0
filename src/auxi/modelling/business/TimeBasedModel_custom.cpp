#include "TimeBasedModel.h"
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

TimeBasedModel::TimeBasedModel(std::string name, std::string description, boost::posix_time::ptime start_date, TimePeriod::TimePeriod period_duration, int period_count) : Model(name, description) {
    m_periodCount = period_count;
    m_clock.SetName("Clock");
    m_clock.SetStartDateTime(start_date);
    m_clock.SetTimeStepPeriodDuration(period_duration);
}

void TimeBasedModel::initialize()
{
    m_clock.SetName("Clock");
    m_clock.SetStartDateTime(boost::posix_time::second_clock::local_time());
    m_clock.SetTimeStepPeriodDuration(TimePeriod::month);
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
        item->prepare_to_run(&m_clock, m_periodCount);
}
void TimeBasedModel::run()
{
    prepare_to_run();
    for (int interval=0; interval<m_periodCount; interval++)
    {
        m_clock.tick();
        for(auto item: m_entityList)
            item->run(&m_clock, interval, m_currency);
    }
}






