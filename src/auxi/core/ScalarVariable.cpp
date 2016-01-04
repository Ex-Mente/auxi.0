#include "ScalarVariable.h"
#include <boost/lexical_cast.hpp>

using namespace auxi::core;

template<typename T>
ScalarVariable<T>::ScalarVariable() : Variable(), m_DefaultValue(T()), m_Value(T())
{
    //ctor
}

template<typename T>
ScalarVariable<T>::~ScalarVariable()
{
    //dtor
}

template<typename T>
ScalarVariable<T>::ScalarVariable(const ScalarVariable<T>& other) : Variable(other)
{
    m_DefaultValue = other.GetDefaultValue();
    m_Value = other.GetValue();
}



template<typename T>
void ScalarVariable<T>::SetDefaultValue(T val)
{
    m_DefaultValue = val;
    SetDefaultValueString(boost::lexical_cast<std::string>(val));
}

template<typename T>
void ScalarVariable<T>::SetValue(T val)
{
    m_Value = val;
    SetValueString(boost::lexical_cast<std::string>(val));
    SetValueSpecified(true);
}

template<typename T>
void ScalarVariable<T>::SetDefaultValueString(std::string val)
{
    Variable::SetDefaultValueString(val);
    m_DefaultValue = boost::lexical_cast<T>(val);
}

template<typename T>
void ScalarVariable<T>::SetValueString(std::string val)
{
    Variable::SetValueString(val);
    m_Value = boost::lexical_cast<T>(val);
}

namespace auxi{ namespace core
{
/*template<typename T>
bool operator==(const ScalarVariable<T>& lhs, const ScalarVariable<T>& rhs)
{
    return false;
}*/

template class ScalarVariable<short>;
template class ScalarVariable<int>;
template class ScalarVariable<long>;
template class ScalarVariable<float>;
template class ScalarVariable<double>;
}}
