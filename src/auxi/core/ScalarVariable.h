#ifndef SCALARVARIABLE_H
#define SCALARVARIABLE_H

#include "Variable.h"

/**
Note:
I made set the operators definition in the .h file as I could fix an undefined error that seems to be caused by the templated stuff when it is declared in the .cpp files.
**/

namespace auxi{ namespace core
{
    template <typename T> class ScalarVariable;

    template <typename T>
    bool operator==(const ScalarVariable<T>& lhs, const ScalarVariable<T>& rhs)
    {
        return lhs.baseEqualTo(rhs)
               && lhs.GetDefaultValue() == rhs.GetDefaultValue()
               && lhs.GetValue() == rhs.GetValue();
    }

    template<typename T>
    class ScalarVariable : public Variable
    {
    public:
        ScalarVariable();
        ScalarVariable(std::string name, std::string description) : Variable(name, description) {}
        ScalarVariable(const ScalarVariable<T>& other);
        virtual ~ScalarVariable();

        bool IsValid() const
        {
            return true;
        }
        ScalarVariable<T>* Clone() const
        {
            return new ScalarVariable<T>(*this);
        };

        friend bool operator== <>(const ScalarVariable<T>& lhs, const ScalarVariable<T>& rhs);

        T GetDefaultValue() const
        {
            return m_DefaultValue;
        }
        void SetDefaultValue(T val);

        T GetValue() const
        {
            return GetValueSpecified() ? m_Value : m_DefaultValue;
        }
        void SetValue(T val);

        using Variable::GetDefaultValueString;
        void SetDefaultValueString(std::string val);

        using Variable::GetValueString;
        void SetValueString(std::string val);
    protected:
    private:
        T m_DefaultValue;
        T m_Value;
    };
}}
#endif // SCALARVARIABLE_H
