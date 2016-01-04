#include "SimpleProduct.h"

using namespace auxi::core;

template<typename T>
SimpleProduct<T>::SimpleProduct()
{
    //ctor
}

template<typename T>
SimpleProduct<T>::~SimpleProduct()
{
    //dtor
}

template<typename T>
SimpleProduct<T>::SimpleProduct(const SimpleProduct<T>& other) : CalculatedScalarVariable<T>(other.GetName(), other.GetDescription())
{

}

namespace auxi{ namespace core
{
    /*template<typename T>
    bool operator==(const SimpleProduct<T>& lhs, const SimpleProduct<T>& rhs)
    {
        return false;
    }*/

    template class SimpleProduct<short>;
    template class SimpleProduct<int>;
    template class SimpleProduct<long>;
    template class SimpleProduct<float>;
    template class SimpleProduct<double>;
}}
