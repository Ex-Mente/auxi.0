#ifndef STOICHIOMETRY_H
#define STOICHIOMETRY_H



#include "Element.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


        
namespace auxi { namespace tools { namespace chemistry { namespace stoichiometry {

std::string formula_code(std::string formula = "");

std::tuple<char, int, int> get_character(std::string char_string, int index = 0);

std::string get_formula(std::string compound);

std::tuple<double, int> parse_element_for_mass(std::string compound, int index);

std::tuple<std::string, double, int> parse_element_for_stoichiometry(std::string compound, int index);

std::set<std::string> parse_formula_for_elements(std::string compound);

std::tuple<double, int> parse_formula_for_mass(std::string compound, int index);

void parse_formula_for_stoichiometry(std::string compound, int index, std::map<std::string, double>& stoichiometry_dict);

std::map<std::string, Element> populate_element_dictionary();

double amount(std::string compound, double mass);

double mass(std::string compound, double amount);

double convert_compound(double mass, std::string source, std::string target, std::string element);

double element_mass_fraction(std::string compound, std::string element);

std::vector<double> element_mass_fractions(std::string compound, std::vector<std::string> elements);

std::vector<std::string> elements(std::vector<std::string> compounds);

double molar_mass(std::string compound = "");

double stoichiometry_coefficient(std::string compound, std::string element);

std::vector<double> stoichiometry_coefficients(std::string compound, std::vector<std::string> elements);
//// Property accessor methods ////

//// Properties ////
extern std::map<std::string, Element> m_elementDict;
extern std::map<std::string, double> m_molar_massDict;
extern std::map<std::string, std::map<std::string, double>> m_stoichiometryDict;
}}}}
#endif