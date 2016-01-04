#include "Compound.h"
#include "Stoichiometry.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <algorithm>
#include <math.h>

using namespace auxi::tools::chemistry::thermochemistry;

Compound::Compound(std::string formula, std::map<std::string,Phase> phaseMap) {
    m_formula = formula;
    m_molar_mass = auxi::tools::chemistry::stoichiometry::molar_mass(m_formula) / 1000.0;

    m_phaseDict = phaseMap;

    for(auto &pmap: phaseMap)
        m_sortedKeysPhaseList.push_back(pmap.first);
    std::sort(m_sortedKeysPhaseList.begin(), m_sortedKeysPhaseList.end());
}

std::vector<std::string> Compound::get_phase_list()
{
    return m_sortedKeysPhaseList;
}

double Compound::Cp(std::string phase, double temperature)
{
    if(m_phaseDict.count(phase) == 0)
        throw std::out_of_range("The phase '" + phase + "' was not found in compound '" + m_formula + "'.");
    return m_phaseDict[phase].Cp(temperature);
}

double Compound::H(std::string phase, double temperature)
{
    if(m_phaseDict.count(phase) == 0)
        throw std::out_of_range("The phase '" + phase + "' was not found in compound '" + m_formula + "'.");
    return m_phaseDict[phase].H(temperature);
}

double Compound::S(std::string phase, double temperature)
{
    if(m_phaseDict.count(phase) == 0)
        throw std::out_of_range("The phase '" + phase + "' was not found in compound '" + m_formula + "'.");
    return m_phaseDict[phase].S(temperature);
}

double Compound::G(std::string phase, double temperature)
{
    if(m_phaseDict.count(phase) == 0)
        throw std::out_of_range("The phase '" + phase + "' was not found in compound '" + m_formula + "'.");
    return m_phaseDict[phase].G(temperature);
}

std::string Compound::to_string()
{
    std::string result = "COMPOUND:\n";
    result += "\tFormula: " + m_formula + "\n";

    for(auto &p_iter: m_phaseDict)
        result += p_iter.second.to_string();

    return result;
}
