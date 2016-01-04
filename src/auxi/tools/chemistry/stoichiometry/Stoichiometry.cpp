#include "Stoichiometry.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



        
namespace auxi { namespace tools { namespace chemistry { namespace stoichiometry {
//// Properties ////
std::map<std::string, Element> m_elementDict = populate_element_dictionary();
std::map<std::string, double> m_molar_massDict;
std::map<std::string, std::map<std::string, double>> m_stoichiometryDict;


}}}}
