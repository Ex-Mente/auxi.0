#include "Thermochemistry.h"
#include "Stoichiometry.h"
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <boost/filesystem.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <string>
#include <math.h>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <utility>

using namespace boost::filesystem;

namespace pt = boost::property_tree;

namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry {

std::string& static_default_path(){
    static std::string default_path = "";
    return default_path;
}

std::string get_default_data_path(){
    return static_default_path();
}

void set_default_data_path(std::string new_default){
    static_default_path() = new_default;
    //new_default;
}

bool replace(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

pt::ptree read_compound_from_fact_file(std::string file_path) {
    pt::ptree compound_tree, phases_tree, phase_tree, cp_records_tree, cp_record_tree, terms_tree;

    std::ifstream file(file_path);
    std::string str;
    bool first_line = true;
    bool started = false;
    std::string phaseold = "zz";
    std::string recordold = "0";
    std::string phase, record;
    while (std::getline(file, str))
    {
        if (started and str[0] != '_') {
            replace(str, " 298 ", " 298.15 ");
            replace(str, " - ", " ");
            while(str.find("  ") != std::string::npos)
                replace(str, "  ", " ");
            replace(str, " \n", "");
            replace(str, "\n", "");
            vector<string> strings;
            boost::split(strings,str,boost::is_any_of(" "));
            strings.pop_back(); // For some reason, the last splitted string is equal to something weird. When I 'cout' a # after the last item, it doesn't appear. It consists of nothing apparently.
            int strings_size = strings.size();
            if(strings_size < 2) // empty line
                continue;
            phase = strings[0];
            if(phase != phaseold) { // new phase detected
                // Finish of the old phase: Add the old phase to the cp_phases_tree
                if(phaseold != "zz") {// only if old phase exists
                    cp_record_tree.add_child("Terms", terms_tree);
                    cp_records_tree.push_back(std::make_pair("", cp_record_tree));
                    phase_tree.add_child("CpRecords", cp_records_tree);
                    phases_tree.push_back(std::make_pair("", phase_tree));
                    terms_tree = pt::ptree();
                    cp_record_tree = pt::ptree();
                    cp_records_tree = pt::ptree();
                    phase_tree = pt::ptree();
                }

                // Create the new phase_tree
                phaseold = phase;
                phase_tree.add("Name", phase);
                phase_tree.add("Code", phase);
                phase_tree.add("DH", boost::lexical_cast<double>(strings[2]));
                phase_tree.add("S", boost::lexical_cast<double>(strings[3]));
                pt::ptree cp_records_tree;
                record = strings[1];
                if(record != recordold) { // new record detected
                    // Finish of the old record: Add the old record to the cp_records_tree
                    pt::ptree cp_record_tree_curr;
                    if(recordold != "0") { // only if old cp_record exists
                        cp_record_tree.add_child("Terms", terms_tree);
                        cp_records_tree.push_back(std::make_pair("", cp_record_tree));
                        cp_record_tree = pt::ptree();
                        terms_tree = pt::ptree();
                    }

                    recordold = record;
                    cp_record_tree.add("Tmin", boost::lexical_cast<double>(strings[strings_size - 2]));
                    cp_record_tree.add("Tmax", boost::lexical_cast<double>(strings[strings_size - 1]));

                    pt::ptree term_tree;
                    term_tree.add("Coefficient", boost::lexical_cast<double>(strings[4]));
                    term_tree.add("Exponent", boost::lexical_cast<double>(strings[5]));
                    terms_tree.push_back(std::make_pair("", term_tree));
                    if(strings_size == 10) {
                        pt::ptree term_tree2;
                        term_tree2.add("Coefficient", boost::lexical_cast<double>(strings[6]));
                        term_tree2.add("Exponent", boost::lexical_cast<double>(strings[7]));
                        terms_tree.push_back(std::make_pair("", term_tree2));
                    }
                }
                else { //old record detected
                    pt::ptree term_tree;
                    term_tree.add("Coefficient", boost::lexical_cast<double>(strings[2]));    // ????
                    term_tree.add("Exponent", boost::lexical_cast<double>(strings[3]));       // ????  Why at pos 2 and 3? that is under DH and S headings?!
                    terms_tree.push_back(std::make_pair("", term_tree));
                    if(strings_size == 8) {
                        pt::ptree term_tree2;
                        term_tree2.add("Coefficient", boost::lexical_cast<double>(strings[4]));
                        term_tree2.add("Exponent", boost::lexical_cast<double>(strings[5]));
                        terms_tree.push_back(std::make_pair("", term_tree2));
                    }
                }
            }
            else { // old phase detected
                record = strings[1];
                if(record != recordold) { // new record detected
                    // Finish of the old record: Add the old record to the cp_records_tree
                    if(recordold != "0") { // only if old cp_record exists
                        cp_record_tree.add_child("Terms", terms_tree);
                        cp_records_tree.push_back(std::make_pair("", cp_record_tree));
                        cp_record_tree = pt::ptree();
                        terms_tree = pt::ptree();
                    }
                    recordold = record;
                    cp_record_tree.add("Tmin", boost::lexical_cast<double>(strings[strings_size - 2]));
                    cp_record_tree.add("Tmax", boost::lexical_cast<double>(strings[strings_size - 1]));

                    pt::ptree term_tree;
                    term_tree.add("Coefficient", boost::lexical_cast<double>(strings[2]));    // ????
                    term_tree.add("Exponent", boost::lexical_cast<double>(strings[3]));       // ????  Why at pos 2 and 3? that is under DH and S headings?!
                    terms_tree.push_back(std::make_pair("", term_tree));
                    if(strings_size == 8) {
                        pt::ptree term_tree2;
                        term_tree2.add("Coefficient", boost::lexical_cast<double>(strings[4]));
                        term_tree2.add("Exponent", boost::lexical_cast<double>(strings[5]));
                        terms_tree.push_back(std::make_pair("", term_tree2));
                    }
                }
                else { //old record detected
                    pt::ptree term_tree;
                    term_tree.add("Coefficient", boost::lexical_cast<double>(strings[2]));    // ????
                    term_tree.add("Exponent", boost::lexical_cast<double>(strings[3]));       // ????  Why at pos 2 and 3? that is under DH and S headings?!
                    terms_tree.push_back(std::make_pair("", term_tree));
                    if(strings_size == 8) {
                        pt::ptree term_tree2;
                        term_tree2.add("Coefficient", boost::lexical_cast<double>(strings[4]));
                        term_tree2.add("Exponent", boost::lexical_cast<double>(strings[5]));
                        terms_tree.push_back(std::make_pair("", term_tree2));
                    }
                }
            }
        }
        else
        {
            if(first_line) { // Set the Formula
                vector<string> strs;
                boost::split(strs,str,boost::is_any_of(" "));
                compound_tree.put("Compound.Formula", strs[1]);
                first_line = false;
            }
            else if(str[0] == '_') {
                started = true;
            }
        }
    }

    cp_record_tree.add_child("Terms", terms_tree);
    cp_records_tree.push_back(std::make_pair("", cp_record_tree));
    phase_tree.add_child("CpRecords", cp_records_tree);
    phases_tree.push_back(std::make_pair("", phase_tree));
    compound_tree.add_child("Compound.Phases", phases_tree);

    return compound_tree;
}

std::tuple<std::string, std::string> split_compound_string(std::string compound_string){
    std::string compound = compound_string;
    replace(compound, "]", "");
    vector<string> compound_splits;
    boost::split(compound_splits, compound, boost::is_any_of("["));
    return std::make_tuple( compound_splits[0], compound_splits[1]); // formula, phase
}

double finalise_result(Compound& compound, double value, double mass){
    auto result = value / 3.6E6; // J/x -> kWh/x
    result = result / compound.Getmolar_mass(); // x/mol -> x/kg
    return result * mass; // x/kg -> x
}

void read_compound(std::map<std::string, Compound>& compMap, std::string file_path_str) {

    //std::cout<<"Reading compound from file: " << file_path_str << std::endl;

    pt::ptree tree;
    pt::json_parser::read_json(file_path_str, tree);

    std::string formula = tree.get<std::string>("Compound.Formula");

    std::string phase_name, symbol;
    double DH, S, Tmin, Tmax;
    std::map<std::string,Phase> phaseMap;
    for(auto &phase_node: tree.get_child("Compound.Phases")) {
        phase_name = phase_node.second.get<std::string>("Name");
        symbol = phase_node.second.get<std::string>("Code");
        DH = phase_node.second.get<double>("DH");
        S = phase_node.second.get<double>("S");
        std::map<double, CpRecord> CpRecordMap;
        for(auto &cp_record_node: phase_node.second.get_child("CpRecords")) {
            Tmin = cp_record_node.second.get<double>("Tmin");
            Tmax = cp_record_node.second.get<double>("Tmax");
            std::vector<double> coefficientList, exponentList;
            std::map<double, CpRecord> m_cpRecordDict;
            for(auto &term_node: cp_record_node.second.get_child("Terms")) {
                coefficientList.push_back(term_node.second.get<double>("Coefficient"));
                exponentList.push_back(term_node.second.get<double>("Exponent"));
            }
            CpRecordMap[Tmax] = CpRecord(Tmin, Tmax, coefficientList, exponentList);
        }
        phaseMap[phase_name] =  Phase(phase_name, symbol, DH, S, CpRecordMap);
    }
    compMap[formula] = Compound(formula, phaseMap);

}

std::map<std::string, Compound> read_compounds(std::string file_path_str){
    std::map<std::string, Compound> result;

    std::string path_str = file_path_str;
    if(file_path_str == "")
        path_str = get_default_data_path();
    else path_str = file_path_str;
    path p(path_str);  // avoid repeated path construction below
    if (exists(p))    // does path p actually exist?
    {
        if (is_directory(p)) {
            /*
            for (auto&& x: directory_iterator(p)) {
                auto item_path = x.path();
                if (is_regular_file(item_path)) {
                    std::string file_name = item_path.filename().string();
                    if(file_name.substr(0, 9) == "Compound_" && extension(item_path) == ".json")
                        read_compound(result, item_path.string());
                }
            }
             */

            vector<path> v;
            copy(directory_iterator(p), directory_iterator(), back_inserter(v));
            for (auto&& x: v) {
                if (is_regular_file(x)) {
                    std::string file_name = x.filename().string();
                    if(file_name.substr(0, 9) == "Compound_" && extension(x) == ".json")
                        read_compound(result, x.string());
                }
            }
        }
        else throw std::invalid_argument("The path does not specify a directory.");
    }
    else throw std::invalid_argument("The path does not exist.");
    return result;
}

void convert_fact_file_to_auxi_thermo_file(std::string fact_file_path, std::string auxi_thermo_file_path)
{
    path source_path(fact_file_path);
    if (exists(source_path)) {
        if (is_regular_file(source_path)) {
            path dest_path(auxi_thermo_file_path);
            path dest_dir = dest_path.parent_path();
            if (exists(dest_dir)) {
                // All directories are OK: Convert.
                pt::json_parser::write_json(auxi_thermo_file_path, read_compound_from_fact_file(fact_file_path));
            }
            else throw std::invalid_argument("The auxi thermo file path does not not exist.");
        }
        else throw std::invalid_argument("The fact file path does not specify a fact file.");
    }
    else throw std::invalid_argument("The fact file path does not exist.");
}

void load_data(std::string path){
    m_compoundDict.clear();
    m_compoundDict = read_compounds(path);
}

void list_compounds(){
    std::cout << "Compounds currently loaded in the thermo module:" << std::endl;
    std::vector<std::string> m_sortedKeysCompoundList;
    for(auto &cmap: m_compoundDict)
        m_sortedKeysCompoundList.push_back(cmap.first);
    std::sort(m_sortedKeysCompoundList.begin(), m_sortedKeysCompoundList.end());
    std::vector<std::string> phaseList;
    for(auto compound: m_sortedKeysCompoundList) {
        phaseList = m_compoundDict[compound].get_phase_list();
        for(auto phase: phaseList)
            std::cout << compound << "[" << phase << "]" << std::endl;
    }
}

double molar_mass(std::string compound){
    return auxi::tools::chemistry::stoichiometry::molar_mass(compound) / 1000.0;
}

double Cp(std::string compound_string, double temperature, double mass) {
    auto formula_phase = split_compound_string(compound_string);
    auto formula = std::get<0>(formula_phase);
    auto phase = std::get<1>(formula_phase);
    auto temperature_K = temperature + 273.15;
    auto compound = m_compoundDict[formula];
    auto result = compound.Cp(phase, temperature_K);
    return finalise_result(compound, result, mass);
}

double H(std::string compound_string, double temperature, double mass) {
    auto formula_phase = split_compound_string(compound_string);
    auto formula = std::get<0>(formula_phase);
    auto phase = std::get<1>(formula_phase);
    auto temperature_K = temperature + 273.15;
    auto compound = m_compoundDict[formula];
    auto result = compound.H(phase, temperature_K);
    return finalise_result(compound, result, mass);
}

double S(std::string compound_string, double temperature, double mass) {
    auto formula_phase = split_compound_string(compound_string);
    auto formula = std::get<0>(formula_phase);
    auto phase = std::get<1>(formula_phase);
    auto temperature_K = temperature + 273.15;
    auto compound = m_compoundDict[formula];
    auto result = compound.S(phase, temperature_K);
    return finalise_result(compound, result, mass);
}

double G(std::string compound_string, double temperature, double mass) {
    auto formula_phase = split_compound_string(compound_string);
    auto formula = std::get<0>(formula_phase);
    auto phase = std::get<1>(formula_phase);
    auto temperature_K = temperature + 273.15;
    auto compound = m_compoundDict[formula];
    auto result = compound.G(phase, temperature_K);
    return finalise_result(compound, result, mass);
}

}}}}