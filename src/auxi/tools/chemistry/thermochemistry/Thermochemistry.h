#ifndef THERMOCHEMISTRY_H
#define THERMOCHEMISTRY_H



#include "Compound.h"
#include <boost/property_tree/ptree.hpp>
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


        
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry {

boost::property_tree::ptree read_compound_from_auxi_file(std::string file_name);

std::string get_default_data_path();

void set_default_data_path(std::string new_default_path);

std::map<std::string, Compound> read_compounds(std::string path = "");

void convert_fact_file_to_auxi_thermo_file(std::string fact_file_path, std::string auxi_thermo_file_path);

void load_data(std::string path = "");

void list_compounds();

double molar_mass(std::string compound);

double Cp(std::string compound_String, double temperature, double mass = 1.0);

double H(std::string compound_String, double temperature, double mass = 1.0);

double S(std::string compound_String, double temperature, double mass = 1.0);

double G(std::string compound_String, double temperature, double mass = 1.0);
//// Property accessor methods ////
    std::map<std::string, Compound>& GetCompoundDict();

//// Properties ////
extern std::map<std::string, Compound> m_compoundDict;
extern std::string m_a;
}}}}
#endif