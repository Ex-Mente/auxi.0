#include "PathReferenceValue.h"

using namespace auxi::core;

template<typename T>
PathReferenceValue<T>::PathReferenceValue()
{
    //ctor
}

template<typename T>
PathReferenceValue<T>::~PathReferenceValue()
{
    //dtor
}

template<typename T>
PathReferenceValue<T>::PathReferenceValue(const PathReferenceValue<T>& other)
{
    //copy ctor
    m_Path = other.m_Path;
}


namespace auxi{ namespace core
{
/**template<typename T>
bool operator==(const PathReferenceValue<T>& lhs, const PathReferenceValue<T>& rhs)
{
    return false;
}**/

template class PathReferenceValue<short>;
template class PathReferenceValue<int>;
template class PathReferenceValue<long>;
template class PathReferenceValue<float>;
template class PathReferenceValue<double>;
}}

