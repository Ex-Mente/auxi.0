#include "Stoichiometry.h"
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <string>
#include <math.h>
#include <iostream>
#include <algorithm>
#include <iterator>

namespace auxi { namespace tools { namespace chemistry { namespace stoichiometry {

std::string formula_code(std::string formula)
{
    std::string result = "";
    int formula_length = (int)formula.size();
    if(formula_length == 0)
        return result;

    int codeSum = 0;
    int b;
    for(int i=0; i<formula_length; i++)
    {
        b = formula[i];
        result = result + boost::lexical_cast<std::string>(b);
        codeSum += b;
    }
    result += "_" + boost::lexical_cast<std::string>(codeSum);

    return result;
}

std::tuple<char, int, int> get_character(std::string char_string, int index)
{
    if(index == (int)char_string.size()) {
        return std::tuple<char, int, int>{'\0', -1, index};
    }
    else {
        char character = char_string[index];
        return std::tuple<char, int, int>{character, (int)character, index + 1};
    }
}
std::string get_formula(std::string compound)
{
    std::vector<std::string> result;
    boost::split(result,compound,boost::is_any_of("["));
    return result[0];
}

std::tuple<double, int> parse_element_for_mass(std::string compound, int index)
{
    std::string element(1,compound[index]);
    index++;
    int compound_size = (int)compound.size();
    int code = 0;
    if(index < compound_size)
        code = compound[index];

    while(code >= 97 && code <= 123) {
        element += compound[index];
        index = index + 1;
        if(index == compound_size) {
            code = 0;
            break;
        }
        code = compound[index];
    }

    char multiplier = '\0';
    while((code >= 48 && code <= 57) || code == 46) {
        multiplier += compound[index];
        index++;
        if(index == compound_size) break;
        code = compound[index];
    }
    if(multiplier == '\0') multiplier = '1';

    double result = m_elementDict[element].GetMolar_mass() * boost::lexical_cast<double>(multiplier);
    return std::tuple<double, int>{result, index};
}

std::tuple<std::string, double, int> parse_element_for_stoichiometry(std::string compound, int index)
{
    std::string element_symbol(1, compound[index]);
    index++;
    int compound_size = (int)compound.size();
    int b = 0;
    if(index < compound_size)
        b = compound[index];

    while (b >= 97 && b <= 123) {
        element_symbol += compound[index];
        index++;
        if(index >= compound_size)
            return std::tuple<std::string, double, int>{element_symbol, 1.0, index};
        b = compound[index];
    }

    std::string stoichiometry_coefficient = "";

    while ((b >= 48 && b <= 57) || b == 46) {
        stoichiometry_coefficient += compound[index];
        index++;
        if(index >= compound_size) break;
        b = compound[index];
    }

    if(stoichiometry_coefficient == "") stoichiometry_coefficient = "1.0";

    return std::tuple<std::string, double, int>{element_symbol, boost::lexical_cast<double>(stoichiometry_coefficient), index};
}

std::set<std::string> parse_formula_for_elements(std::string compound)
{
    // Initialise the search variables.
    auto result = std::set<std::string>();
    int i = 0; // The index of the current character in the string.
    int compound_size = (int)compound.size();

    // Do the search.
    char c;
    int b, j;
    while(i < compound_size) {
        auto char_result = get_character(compound, i);
        c = std::get<0>(char_result);
        b = std::get<1>(char_result);
        i = std::get<2>(char_result);
        if(b >= 65 and b <= 90) { // Element found. Process it.
            j = i;
            std::string element(1, c);
            char_result = get_character(compound, j);
            c = std::get<0>(char_result);
            b = std::get<1>(char_result);
            j = std::get<2>(char_result);
            while(b >= 97 && b <= 122) {
                element += c;
                char_result = get_character(compound, j);
                c = std::get<0>(char_result);
                b = std::get<1>(char_result);
                j = std::get<2>(char_result);
            }
            result.insert(element);
        }
    }

    return result;
}

std::tuple<double, int> parse_formula_for_mass(std::string compound, int index)
{
    int compound_size = (int)compound.size();
    double result = 0.0;
    char c = '\0';
    int b;
    while(index < compound_size and c != ')') {
        c = compound[index];
        b = c;

        if(c == '(') {
            index++;
            auto for_mass = parse_formula_for_mass(compound, index);
            result += std::get<0>(for_mass);
            index = std::get<1>(for_mass);
        }
        else if(b >= 65 && b <= 90) {
            auto for_mass = parse_element_for_mass(compound, index);
            result += std::get<0>(for_mass);
            index = std::get<1>(for_mass);
        }
    }
    if(index >= compound_size) return std::tuple<double, int>{result, -1};

    if(c == ')') index++;
    b = compound[index];

    char multiplier = '\0';
    while ((b >= 48 && b <= 57) || b == 46)
    {
        multiplier += compound[index];
        index++;
        if(index == compound_size) break;
        b = compound[index];
    }

    if(multiplier == '\0')
        multiplier = '1';

    result = result * boost::lexical_cast<double>(multiplier);
    return std::tuple<double, int>{result, index};
}


void parse_formula_for_stoichiometry(std::string compound, int index, std::map<std::string, double>& stoichiometry_dict)
{
    int compound_size = (int)compound.size();
    char c = '\0';
    int b;
    while(index < compound_size and c != ')') {
        c = compound[index];
        b = c;

        if(c == '(') {
            index++;
            auto new_stoichiometry_records = std::map<std::string, double>();
            parse_formula_for_stoichiometry(compound, index, new_stoichiometry_records);
            for (auto it=stoichiometry_dict.begin(); it!=stoichiometry_dict.end(); ++it) {
                auto k = it->first;
                if(stoichiometry_dict.count(k))
                    stoichiometry_dict[k] += new_stoichiometry_records[k];
                else stoichiometry_dict[k] = it->second;
            }
        }
        else {
            if(b >= 65 && b <= 90) {
                auto element_details = parse_element_for_stoichiometry(compound, index);
                auto element = std::get<0>(element_details);
                auto coefficient = std::get<1>(element_details);
                index = std::get<2>(element_details);
                if(stoichiometry_dict.count(element) > 0)
                    stoichiometry_dict[element] += coefficient;
                else stoichiometry_dict[element] = coefficient;
            }
        }
    }

    if(index >= compound_size) return;

    if(c == '(') index++;
    c = compound[index];
    b = c;

    std::string multiplier_string = "";
    while ((b >= 48 and b <= 57) or b == 46) {
        multiplier_string += compound[index];
        index++;
        if(index == compound_size) return;
        c = compound[index];
        b = c;
    }

    if(multiplier_string != "") {
        double multiplier = boost::lexical_cast<double>(multiplier_string);
        for (auto it=stoichiometry_dict.begin(); it!=stoichiometry_dict.end(); ++it)
            stoichiometry_dict[it->first] *= multiplier;
    }
}


Element createElement(int m_period, int m_group, int m_atomic_number, std::string m_symbol, double m_molar_mass)
{
    auto result = Element();
    result.SetPeriod(m_period);
    result.SetGroup(m_group);
    result.SetAtomic_number(m_atomic_number);
    result.SetSymbol(m_symbol);
    result.SetMolar_mass(m_molar_mass);
    return result;
}

std::map<std::string, Element> populate_element_dictionary()
{
    return std::map<std::string, Element> {
        // period 1
        {"H",  createElement(1,  1,   1, "H",    1.00794)},
        {"He", createElement(1, 18,   2, "He",   4.002602)},
        // period 2
        {"Li", createElement(2,  1,   3, "Li",   6.941)},
        {"Be", createElement(2,  2,   4, "Be",   9.012182)},
        {"B",  createElement(2, 13,   5, "B",   10.811)},
        {"C",  createElement(2, 14,   6, "C",   12.0107)},
        {"N",  createElement(2, 15,   7, "N",   14.00674)},
        {"O",  createElement(2, 16,   8, "O",   15.9994)},
        {"F",  createElement(2, 17,   9, "F",   18.9984032)},
        {"Ne", createElement(2, 18,  10, "Ne",  20.1797)},
        // period 3
        {"Na", createElement(3,  1,  11, "Na",  22.98977)},
        {"Mg", createElement(3,  2,  12, "Mg",  24.305)},
        {"Al", createElement(3, 13,  13, "Al",  26.981538)},
        {"Si", createElement(3, 14,  14, "Si",  28.0855)},
        {"P",  createElement(3, 15,  15, "P",   30.973762)},
        {"S",  createElement(3, 16,  16, "S",   32.066)},
        {"Cl", createElement(3, 17,  17, "Cl",  35.4527)},
        {"Ar", createElement(3, 18,  18, "Ar",  39.948)},
        // period 4
        {"K",  createElement(4,  1,  19, "K",   39.0983)},
        {"Ca", createElement(4,  2,  20, "Ca",  40.078)},
        {"Sc", createElement(4,  3,  21, "Sc",  44.95591)},
        {"Ti", createElement(4,  4,  22, "Ti",  47.867)},
        {"V",  createElement(4,  5,  23, "V",   50.9415)},
        {"Cr", createElement(4,  6,  24, "Cr",  51.9961)},
        {"Mn", createElement(4,  7,  25, "Mn",  54.938049)},
        {"Fe", createElement(4,  8,  26, "Fe",  55.845)},
        {"Co", createElement(4,  9,  27, "Co",  58.9332)},
        {"Ni", createElement(4, 10,  28, "Ni",  58.6934)},
        {"Cu", createElement(4, 11,  29, "Cu",  63.546)},
        {"Zn", createElement(4, 12,  30, "Zn",  65.39)},
        {"Ga", createElement(4, 13,  31, "Ga",  69.723)},
        {"Ge", createElement(4, 14,  32, "Ge",  72.61)},
        {"As", createElement(4, 15,  33, "As",  74.9216)},
        {"Se", createElement(4, 16,  34, "Se",  78.96)},
        {"Br", createElement(4, 17,  35, "Br",  79.904)},
        {"Kr", createElement(4, 18,  36, "Kr",  83.8)},
        // period 5
        {"Rb", createElement(5,  1,  37, "Rb",  85.4678)},
        {"Sr", createElement(5,  2,  38, "Sr",  87.62)},
        {"Y",  createElement(5,  3,  39, "Y",   88.90585)},
        {"Zr", createElement(5,  4,  40, "Zr",  91.224)},
        {"Nb", createElement(5,  5,  41, "Nb",  92.90638)},
        {"Mo", createElement(5,  6,  42, "Mo",  95.94)},
        {"Tc", createElement(5,  7,  43, "Tc",  98.0)},
        {"Ru", createElement(5,  8,  44, "Ru",  101.07)},
        {"Rh", createElement(5,  9,  45, "Rh",  102.9055)},
        {"Pd", createElement(5, 10,  46, "Pd",  106.42)},
        {"Ag", createElement(5, 11,  47, "Ag",  107.8682)},
        {"Cd", createElement(5, 12,  48, "Cd",  112.411)},
        {"In", createElement(5, 13,  49, "In",  114.818)},
        {"Sn", createElement(5, 14,  50, "Sn",  118.71)},
        {"Sb", createElement(5, 15,  51, "Sb",  121.76)},
        {"Te", createElement(5, 16,  52, "Te",  127.6)},
        {"I",  createElement(5, 17,  53, "I",   126.90447)},
        {"Xe", createElement(5, 18,  54, "Xe",  131.29)},
        // period 6
        {"Cs", createElement(6,  1,  55, "Cs",  132.90545)},
        {"Ba", createElement(6,  2,  56, "Ba",  137.327)},
        {"La", createElement(6,  0,  57, "La",  138.9055)},
        {"Ce", createElement(6,  0,  58, "Ce",  140.116)},
        {"Pr", createElement(6,  0,  59, "Pr",  140.90765)},
        {"Nd", createElement(6,  0,  60, "Nd",  144.24)},
        {"Pm", createElement(6,  0,  61, "Pm",  145.0)},
        {"Sm", createElement(6,  0,  62, "Sm",  150.36)},
        {"Eu", createElement(6,  0,  63, "Eu",  151.964)},
        {"Gd", createElement(6,  0,  64, "Gd",  157.25)},
        {"Tb", createElement(6,  0,  65, "Tb",  158.92534)},
        {"Dy", createElement(6,  0,  66, "Dy",  162.5)},
        {"Ho", createElement(6,  0,  67, "Ho",  164.93032)},
        {"Er", createElement(6,  0,  68, "Er",  167.26)},
        {"Tm", createElement(6,  0,  69, "Tm",  168.93421)},
        {"Yb", createElement(6,  0,  70, "Yb",  173.04)},
        {"Lu", createElement(6,  0,  71, "Lu",  174.967)},
        {"Hf", createElement(6,  4,  72, "Hf",  178.49)},
        {"Ta", createElement(6,  5,  73, "Ta",  180.9479)},
        {"W",  createElement(6,  6,  74, "W",   183.84)},
        {"Re", createElement(6,  7,  75, "Re",  186.207)},
        {"Os", createElement(6,  8,  76, "Os",  190.23)},
        {"Ir", createElement(6,  9,  77, "Ir",  192.217)},
        {"Pt", createElement(6, 10,  78, "Pt",  195.078)},
        {"Au", createElement(6, 11,  79, "Au",  196.96655)},
        {"Hg", createElement(6, 12,  80, "Hg",  200.59)},
        {"Tl", createElement(6, 13,  81, "Tl",  204.3833)},
        {"Pb", createElement(6, 14,  82, "Pb",  207.2)},
        {"Bi", createElement(6, 15,  83, "Bi",  208.98038)},
        {"Po", createElement(6, 16,  84, "Po",  210.0)},
        {"At", createElement(6, 17,  85, "At",  210.0)},
        {"Rn", createElement(6, 18,  86, "Rn",  222.0)},
        // period 7
        {"Fr", createElement(7,  1, 87, "Fr",   223.0)},
        {"Ra", createElement(7,  2, 88, "Ra",   226.0)},
        {"Ac", createElement(7,  0, 89, "Ac",   227.0)},
        {"Th", createElement(7,  0, 90, "Th",   232.0381)},
        {"Pa", createElement(7,  0, 91, "Pa",   231.03588)},
        {"U",  createElement(7,  0, 92, "U",    238.0289)},
        {"Np", createElement(7,  0, 93, "Np",   237.0)},
        {"Pu", createElement(7,  0, 94, "Pu",   244.0)},
        {"Am", createElement(7,  0, 95, "Am",   243.0)},
        {"Cm", createElement(7,  0, 96, "Cm",   247.0)},
        {"Bk", createElement(7,  0, 97, "Bk",   247.0)},
        {"Cf", createElement(7,  0, 98, "Cf",   251.0)},
        {"Es", createElement(7,  0, 99, "Es",   252.0)},
        {"Fm", createElement(7,  0, 100, "Fm",  257.0)},
        {"Md", createElement(7,  0, 101, "Md",  258.0)},
        {"No", createElement(7,  0, 102, "No",  259.0)},
        {"Lr", createElement(7,  0, 103, "Lr",  262.0)},
        {"Rf", createElement(7,  4, 104, "Rf",  261.0)},
        {"Db", createElement(7,  5, 105, "Db",  262.0)},
        {"Sg", createElement(7,  6, 106, "Sg",  266.0)},
        {"Bh", createElement(7,  7, 107, "Bh",  264.0)},
        {"Hs", createElement(7,  8, 108, "Hs",  269.0)},
        {"Mt", createElement(7,  9, 109, "Mt",  268.0)},
        {"Ds", createElement(7, 10, 110, "Ds",  269.0)},
        {"Rg", createElement(7, 11, 111, "Rg",  272.0)}
        // Cn missing
        // Uut missing
        // Fl missing
        // Uup missing
        // Lv missing
        // Uus missing
        // Uuo missing
        // actinides
    };
}



double amount(std::string compound, double mass)
{
    return mass / molar_mass(get_formula(compound));
}

double mass(std::string compound, double amount)
{
    return amount * molar_mass(get_formula(compound));
}

double convert_compound(double mass, std::string source, std::string target, std::string element)
{
    // Convert compounds to formulas.
    std::string source_formula = get_formula(source);
    std::string target_formula = get_formula(target);

    // Perform the conversion.
    double source_mass_fraction = element_mass_fraction(source_formula, element);
    double target_mass_fraction = element_mass_fraction(target_formula, element);
    if(target_mass_fraction == 0.0) return 0.0;
    else return mass * source_mass_fraction / target_mass_fraction;
}

double element_mass_fraction(std::string compound, std::string element)
{
    double elementStoichiometryCoefficient = stoichiometry_coefficient(compound, element);
    if(elementStoichiometryCoefficient == 0.0)
        return 0.0;
    else {
        double formulaMass = molar_mass(compound);
        double elementMass = molar_mass(element);
        return elementStoichiometryCoefficient * elementMass / formulaMass;
    }
}

std::vector<double> element_mass_fractions(std::string compound, std::vector<std::string> elements)
{
    auto formula = get_formula(compound);
    auto result = std::vector<double>();
    for(auto e: elements)
        result.push_back(element_mass_fraction(formula, e));
    return result;
}

std::vector<std::string> elements(std::vector<std::string> compounds)
{
    auto result = std::set<std::string>();
    for(auto compound: compounds) {
        auto for_ele_list = parse_formula_for_elements(get_formula(compound));
        result.insert(for_ele_list.begin(), for_ele_list.end());
    }
    return std::vector<std::string>(result.begin(), result.end());
}

double molar_mass(std::string compound)
{
    double result = 0.0;
    boost::trim(compound);
    int compound_size = (int)compound.size();
    if(compound_size == 0) return result;

    auto code = formula_code(compound);
    if(m_molar_massDict.count(code) == 0) {
        int index = 0;
        m_molar_massDict[code] = std::get<0>(parse_formula_for_mass(compound, index));
    }
    return m_molar_massDict[code];
}

double stoichiometry_coefficient(std::string compound, std::string element)
{
    boost::trim(compound);

    std::map<std::string, double> stoichiometry;
    std::string compound_code = formula_code(compound);
    if(m_stoichiometryDict.count(compound) == 0) {
        parse_formula_for_stoichiometry(compound, 0, stoichiometry);
        m_stoichiometryDict[compound_code] = stoichiometry;
    }

    stoichiometry = m_stoichiometryDict[compound_code];

    if(stoichiometry.count(element) > 0) return stoichiometry[element];
    else return 0.0;
}

std::vector<double> stoichiometry_coefficients(std::string compound, std::vector<std::string> elements)
{
    std::vector<double> result;
    for(auto ele: elements)
        result.push_back(stoichiometry_coefficient(compound, ele));
    return result;
}

}}}}