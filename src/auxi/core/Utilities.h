#ifndef UTILITIES_H
#define UTILITIES_H

#include <vector>
#include <boost/lexical_cast.hpp>
#include <iostream>
using namespace std;

namespace auxi{ namespace core
{

template<class T>
typename std::enable_if<!std::numeric_limits<T>::is_integer, bool>::type
    almost_equal(T x, T y, int ulp)
{
    // the machine epsilon has to be scaled to the magnitude of the values used
    // and multiplied by the desired precision in ULPs (units in the last place)
    return std::abs(x-y) < std::numeric_limits<T>::epsilon() * std::abs(x+y) * ulp
    // unless the result is subnormal
           || std::abs(x-y) < std::numeric_limits<T>::min();
}


/**** VECTOR MANAGEMENT ****/
/*
 * Pointer deleter for a vector of pointers
 */
template <class T>
void delete_ptr_vector(T ptr_vector)
{
    for(auto &it:ptr_vector) delete it;
    ptr_vector.clear();

}


template <class T>
void remove_ptr_from_vector(T ptr_vector, unsigned int index)
{
    unsigned int list_size = ptr_vector.size();
    if (index >= list_size) throw std::out_of_range("The index: '" + boost::lexical_cast<std::string>(index) + "' is larger than the size of the list: '" + boost::lexical_cast<std::string>(list_size) + "'.");

    delete ptr_vector[index];
    ptr_vector.erase(ptr_vector.begin()+index);
}

template <class T, class U>
void remove_ptr_from_vector(T ptr_vector, std::string name)
{
    auto it = std::find_if(ptr_vector.begin(), ptr_vector.end(), [name](const U* obj) -> bool {return obj->GetName() == name;});

    if (it == ptr_vector.end()) throw std::invalid_argument("'" + name + "' could not be found.");

    remove_ptr_from_vector(ptr_vector, std::distance(ptr_vector.begin(), it));
}




template <class T>
void log_VectorVector(std::vector<std::vector<T>> vec)
{
    for(int i=0; i<vec.size(); i++)
        for(int j=0; j<vec[i].size(); j++)
            std::cout << "i: " << i << " j: " << j << " val: " << vec[i][j] << std::endl;
}






}}

#endif // UTILITIES_H
