#include "Thermochemistry.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



        
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry {
//// Properties ////
std::map<std::string, Compound> m_compoundDict;
std::string m_a = "";


std::map<std::string, Compound>& GetCompoundDict() { return m_compoundDict; }
}}}}
