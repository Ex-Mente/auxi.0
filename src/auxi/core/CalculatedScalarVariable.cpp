#include "CalculatedScalarVariable.h"

using namespace auxi::core;

template<typename T>
CalculatedScalarVariable<T>::CalculatedScalarVariable()
{
    //ctor
}

template<typename T>
CalculatedScalarVariable<T>::~CalculatedScalarVariable()
{
    //dtor
}

template<typename T>
CalculatedScalarVariable<T>::CalculatedScalarVariable(const CalculatedScalarVariable<T>& other) : ScalarVariable<T>(other.GetName(), other.GetDescription())
{
    //copy ctor
}

namespace auxi{ namespace core
{
/*template<typename T>
bool operator==(const CalculatedScalarVariable<T>& lhs, const CalculatedScalarVariable<T>& rhs)
{
    return false;
}*/

template class CalculatedScalarVariable<short>;
template class CalculatedScalarVariable<int>;
template class CalculatedScalarVariable<long>;
template class CalculatedScalarVariable<float>;
template class CalculatedScalarVariable<double>;
}}
