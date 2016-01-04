#include "ParameterizedObject.h"

#include <boost/lexical_cast.hpp>


using namespace auxi::core;

template <typename T>
ParameterizedObject<T>::ParameterizedObject() : m_value(T()), m_valueConstant(T()), m_valueLocalVariable(ScalarVariable<T>())
{
}

template <typename T>
ParameterizedObject<T>::~ParameterizedObject()
{
    //dtor
}

template <typename T>
ParameterizedObject<T>::ParameterizedObject(const ParameterizedObject<T>& other) : NamedObject(other.GetName(), other.GetDescription())
{
    //copy ctor
}

template <typename T>
ParameterizedObjectValueSourceType::ValueSourceType ParameterizedObject<T>::ValueSourceType() const
{
    if (m_valueSourceType == ParameterizedObjectValueSourceType::LocalVariable)
        return ParameterizedObjectValueSourceType::LocalVariable;
    else if (m_valueSourceType == ParameterizedObjectValueSourceType::ReferencedVariable && m_valueVariableReference != nullptr)
        return ParameterizedObjectValueSourceType::ReferencedVariable;
    else if (m_valueSourceType == ParameterizedObjectValueSourceType::ReferencedPath)
        return ParameterizedObjectValueSourceType::ReferencedPath;
    else
        return ParameterizedObjectValueSourceType::Constant;
}

template <typename T>
bool ParameterizedObject<T>::IsValid() const
{
    return true;
}


template <typename T>
void ParameterizedObject<T>::SetValueConstant(T val)
{
    m_valueConstant = val;
    m_valueSourceType = ParameterizedObjectValueSourceType::Constant;
}

template <typename T>
void ParameterizedObject<T>::SetValueLocalVariable(ScalarVariable<T> val)
{
    m_valueLocalVariable = val;
    m_valueSourceType = ParameterizedObjectValueSourceType::LocalVariable;
}

template <typename T>
void ParameterizedObject<T>::SetValueVariableReference(ScalarVariable<T>* val)
{
    m_valueVariableReference = val;
    m_valueSourceType = ParameterizedObjectValueSourceType::ReferencedVariable;
}

template <typename T>
void ParameterizedObject<T>::SetValueReferencePath(PathReferenceValue<T> val)
{
    m_valueReferencedPath = val;
    m_valueSourceType = ParameterizedObjectValueSourceType::ReferencedPath;
}

template <typename T>
std::string ParameterizedObject<T>::ToString() const
{
    if (m_valueSourceType == ParameterizedObjectValueSourceType::LocalVariable)
        return m_valueLocalVariable.ToString();
    else if (m_valueSourceType == ParameterizedObjectValueSourceType::ReferencedVariable && m_valueVariableReference != nullptr)
        return m_valueVariableReference->ToString();
    else if (m_valueSourceType == ParameterizedObjectValueSourceType::ReferencedPath)
    {
        if(m_LocalUnits != nullptr) return m_LocalUnits->ToString(boost::lexical_cast<std::string>(m_valueReferencedPath.GetValue()));
        return boost::lexical_cast<std::string>(m_valueReferencedPath.GetValue());
    }
    else
    {
        if(m_LocalUnits != nullptr) return m_LocalUnits->ToString(boost::lexical_cast<std::string>(m_valueConstant));
        return boost::lexical_cast<std::string>(m_valueConstant);
    }
}

namespace auxi{ namespace core
{
/*template<typename T>
bool operator==(const ParameterizedObject<T>& lhs, const ParameterizedObject<T>& rhs)
{
    return false;
}*/

template class ParameterizedObject<short>;
template class ParameterizedObject<int>;
template class ParameterizedObject<long>;
template class ParameterizedObject<float>;
template class ParameterizedObject<double>;
}}

