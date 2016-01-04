#include "ExecutionInjector.h"

using namespace auxi::core;

ExecutionInjector::ExecutionInjector()
{
    //ctor
}

ExecutionInjector::ExecutionInjector(std::string name, std::string description) : NamedObject(name, description)
{

}

ExecutionInjector::~ExecutionInjector()
{
    //dtor
}

ExecutionInjector::ExecutionInjector(const ExecutionInjector& other) : NamedObject(other.GetName(), other.GetDescription())
{
    //copy ctor
}

void ExecutionInjector::prepare_to_run() {}

void ExecutionInjector::before_run_step(int) {}
void ExecutionInjector::after_run_step(int) {}

void ExecutionInjector::before_run() {}
void ExecutionInjector::after_run() {}
