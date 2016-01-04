#ifndef PARAMETERIZEDObject_H
#define PARAMETERIZEDObject_H

#include "NamedObject.h"
#include "ScalarVariable.h"
#include "PathReferenceValue.h"
#include "ParameterizedObjectValueSourceType.h"

/**
Note:
ParameterizedObject is restricted to only allow specified types for <T>:
    - Issue: Received an "undefined reference to `em::sim::core::ParameterizedObject<double>::ParameterizedObject()'" error.
    - Solution: http://stackoverflow.com/questions/8752837/undefined-reference-to-template-class-constructor
Of the 2 possible solutions to the issue, I can either add all the implementation to the header file, or declare all the possible types for <T>
The benefit of the chosen solution is that we can test for all possible (allowed) types of <T>.
**/

namespace auxi{ namespace core
{
    template<typename T>
    class ParameterizedObject : public NamedObject
    {
    public:
        ParameterizedObject();
        ParameterizedObject(std::string name, std::string description) : NamedObject(name, description) {}
        ParameterizedObject(const ParameterizedObject<T>& other);

        bool IsValid() const;
        ParameterizedObject<T>* Clone() const { return new ParameterizedObject<T>(*this); }

        ~ParameterizedObject();
/*
        template<typename Tt>
        friend bool operator==(const ParameterizedObject<Tt>&, const ParameterizedObject<Tt>&)
        {
            return false;
        }
*/
        ParameterizedObjectValueSourceType::ValueSourceType ValueSourceType() const;

        T GetValue() const { return m_value; }
        void SetValue(T val) { m_value = val; }

        T GetValueConstant() const { return m_valueConstant; }
        void SetValueConstant(T val);

        ScalarVariable<T> GetValueLocalVariable() const { return m_valueLocalVariable; }
        void SetValueLocalVariable(ScalarVariable<T> val);

        ScalarVariable<T>* GetValueVariableReference() { return m_valueVariableReference; }
        void SetValueVariableReference(ScalarVariable<T>* val);

        PathReferenceValue<T> GetValueReferencedPath() const { return m_valueReferencedPath; }
        void SetValueReferencePath(PathReferenceValue<T> val);

        Units* GetLocalUnits() const { return m_LocalUnits; }
        void SetLocalUnits(Units* val) { m_LocalUnits = val; }

        Units* GetUnitsValue();

        std::string ToString() const;
    protected:
    private:
        T m_value = T();
        T m_valueConstant = T();
        ScalarVariable<T> m_valueLocalVariable;
        ScalarVariable<T>* m_valueVariableReference = nullptr;
        PathReferenceValue<T> m_valueReferencedPath;
        Units* m_LocalUnits = nullptr;
        ParameterizedObjectValueSourceType::ValueSourceType m_valueSourceType;
    };
}}

#endif // PARAMETERIZEDObject_H
