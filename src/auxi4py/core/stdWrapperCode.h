#include <cmath>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include "unordered_map_indexing_suite.hpp"
#include <vector>


/*
template<typename T>
inline std::vector<T> to_std_vector(const object& iterable)
{
    return std::vector<T>(stl_input_iterator<T>(iterable), stl_input_iterator<T>());
}*/