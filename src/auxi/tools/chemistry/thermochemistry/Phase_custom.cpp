#include "Phase.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <algorithm>
#include <math.h>

using namespace auxi::tools::chemistry::thermochemistry;

Phase::Phase(std::string name, std::string symbol, double DHref, double Sref, std::map<double, CpRecord> cpRecordMap) {
    SetName(name);
    m_symbol = symbol;
    m_tref = 298.15;
    m_dHref = DHref;
    m_sref = Sref;

    m_cpRecordDict = cpRecordMap;

    for(auto &cpmap: cpRecordMap)
        m_sortedKeysCpRecordList.push_back(cpmap.first);
    std::sort(m_sortedKeysCpRecordList.begin(), m_sortedKeysCpRecordList.end());
}

double Phase::Cp(double temperature)
{
    for(auto Tmax: m_sortedKeysCpRecordList) {
        if(temperature < Tmax)
            return m_cpRecordDict[Tmax].Cp(temperature);
    }
    auto Tmax = m_sortedKeysCpRecordList.back();
    return m_cpRecordDict[Tmax].Cp(Tmax);
}

double Phase::H(double temperature)
{
    auto result = m_dHref;
    for(auto Tmax: m_sortedKeysCpRecordList) {
        result = result + m_cpRecordDict[Tmax].H(temperature);
        if(temperature <= Tmax)
            return result;
    }
    // Extrapolate beyond the upper limit by using a constant heat capacity.
    auto Tmax = m_sortedKeysCpRecordList.back();
    result += Cp(Tmax)*(temperature - Tmax);
    return result;
}

double Phase::S(double temperature)
{
    auto result = m_sref;
    for(auto Tmax: m_sortedKeysCpRecordList) {
        result = result + m_cpRecordDict[Tmax].S(temperature);
        if(temperature <= Tmax)
            return result;
    }
    // Extrapolate beyond the upper limit by using a constant heat capacity.
    auto Tmax = m_sortedKeysCpRecordList.back();
    result += Cp(Tmax)*log(temperature / Tmax);
    return result;
}

double Phase::G(double temperature)
{
    auto h = m_dHref;
    auto s = m_sref;
    for(auto Tmax: m_sortedKeysCpRecordList) {
        h = h + m_cpRecordDict[Tmax].H(temperature);
        s = s + m_cpRecordDict[Tmax].S(temperature);
        if(temperature <= Tmax)
            return h - temperature * s;
    }
    // Extrapolate beyond the upper limit by using a constant heat capacity.
    auto Tmax = m_sortedKeysCpRecordList.back();
    h = h + Cp(Tmax)*(temperature - Tmax);
    s = s + Cp(Tmax)*log(temperature / Tmax);
    return h - temperature * s;
}

std::string Phase::to_string()
{
    std::string result = "\tPHASE: " + GetName() + "\n";
    result += "\t\tName: " + GetName() + "\n";
    result += "\t\tSymbol: " + m_symbol + "\n";
    result += "\t\tTref: " + boost::lexical_cast<std::string>(m_tref) + "\n";
    result += "\t\tDHref: " + boost::lexical_cast<std::string>(m_dHref) + "\n";
    result += "\t\tSref: " + boost::lexical_cast<std::string>(m_sref) + "\n";
    result += "\t\tCp record count:" + boost::lexical_cast<std::string>(m_sortedKeysCpRecordList.size()) + "\n";

    for(auto &cpmap: m_cpRecordDict)
        result += cpmap.second.to_string();

    return result;
}
