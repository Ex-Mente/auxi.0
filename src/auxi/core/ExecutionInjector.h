#ifndef EXECUTIONINJECTOR_H
#define EXECUTIONINJECTOR_H

#include "NamedObject.h"

namespace auxi{ namespace core
{
class ExecutionInjector : public NamedObject
{
    public:
        ExecutionInjector();
        ExecutionInjector(std::string name, std::string description);
        virtual ~ExecutionInjector();
        ExecutionInjector(const ExecutionInjector& other);

        virtual void prepare_to_run();

        virtual void before_run_step(int step_ix);
        virtual void after_run_step(int step_ix);

        virtual void before_run();
        virtual void after_run();
    protected:
    private:
};
}}
#endif // EXECUTIONINJECTOR_H
