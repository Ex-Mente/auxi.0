#ifndef EXECUTIONOBJECT_H
#define EXECUTIONOBJECT_H

/********************
Architectural Decisions:
3 virtual methods: Serial, parallel and custom.
Having a seperate executor object (has a relationship) will mean that the execution won't have access to the private variables it is executing on.

For parallel execution to assign this execution to the best possible execution resource:
An estimate of the execution time needs to be known.
estimate_execution variable.
calcuated_execution variable. This one is calculated from the execution history. This one is used by default. User must specify if he wants to use a fixed estimate.
   Remember, different execution resources perform differently, this estimated calculation needs to take that into consideration.

********************/
#include <string>
#include <vector>
#include "NamedObject.h"
#include "ExecutionInjector.h"

namespace auxi{ namespace core
{
class ExecutionObject : public NamedObject
{
public:
    ExecutionObject();
    ExecutionObject(std::string name, std::string description) : NamedObject(name, description) {}
    virtual ~ExecutionObject();

    virtual void execute() {}
    virtual void execute_serial() {}
    virtual void execute_parallel() {}
    virtual void prepare_to_execute() {}

    //std::vector<ExecutionInjector*>& GetExecutionInjectorList() { return m_executionInjectorList; }
private:
    //std::vector<ExecutionInjector*> m_executionInjectorList;
};
}}
#endif // EXECUTIONOBJECT_H
