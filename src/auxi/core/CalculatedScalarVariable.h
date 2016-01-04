#ifndef CALCULATEDSCALARVARIABLE_H
#define CALCULATEDSCALARVARIABLE_H

#include "ScalarVariable.h"

namespace auxi{ namespace core
{
    template<typename T>
    class CalculatedScalarVariable : public ScalarVariable<T>
    {
    public:
        CalculatedScalarVariable();
        ~CalculatedScalarVariable();
        CalculatedScalarVariable(std::string name, std::string description) : ScalarVariable<T>(name, description) {}
        CalculatedScalarVariable(const CalculatedScalarVariable<T>&);

        template<typename TT>
        friend bool operator==(const CalculatedScalarVariable<T>&, const CalculatedScalarVariable<T>&)
        {
            return false;
        }
    protected:
    private:
    };
}}
#endif // CALCULATEDSCALARVARIABLE_H
