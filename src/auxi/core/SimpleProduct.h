#ifndef SIMPLEPRODUCT_H
#define SIMPLEPRODUCT_H

#include "CalculatedScalarVariable.h"
#include "ParameterizedObject.h"


namespace auxi{ namespace core
{
    template<typename T>
    class SimpleProduct : public CalculatedScalarVariable<T>
    {
    public:
        SimpleProduct();
        ~SimpleProduct();
        SimpleProduct(const SimpleProduct<T>&);

        bool IsValid() const
        {
            return false;
        }
        SimpleProduct* Clone() const
        {
            return new SimpleProduct(*this);
        };

        template<typename TT>
        friend bool operator==(const SimpleProduct<T>&, const SimpleProduct<T>&)
        {
            return false;
        }

        ParameterizedObject<T>& GetInput1()
        {
            return m_Input1;
        }
        void SetInput1(ParameterizedObject<T> val)
        {
            m_Input1 = val;
        }
        ParameterizedObject<T>& GetInput2()
        {
            return m_Input2;
        }
        void SetInput2(ParameterizedObject<T> val)
        {
            m_Input2 = val;
        }
    protected:
    private:
        ParameterizedObject<T> m_Input1;
        ParameterizedObject<T> m_Input2;
    };
}}
#endif // SIMPLEPRODUCT_H
