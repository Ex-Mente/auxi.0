#include "CpRecord.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <math.h>

using namespace auxi::tools::chemistry::thermochemistry;

CpRecord::CpRecord(double Tmin, double Tmax, std::vector<double> coefficientList, std::vector<double> expoonentList) {
    SetTmin(Tmin);
    SetTmax(Tmax);

    m_coefficientList = coefficientList;
    m_exponentList = expoonentList;
}

double CpRecord::Cp(double temperature)
{
    double result = 0.0;
    for(unsigned int i = 0; i < m_coefficientList.size(); i++)
        result = result + m_coefficientList[i] * pow(temperature, m_exponentList[i]);
    return result;
}

double CpRecord::H(double temperature)
{
    double result = 0.0;
    double T;
    if(temperature < m_tmax)
        T = temperature;
    else T = m_tmax;
    double Tref = m_tmin;
    for(unsigned int i = 0; i < m_coefficientList.size(); i++)
    {
        double c = m_coefficientList[i];
        double e = m_exponentList[i];
        // Analytically integrate Cp(T).
        if(e == -1.0)
            result = result + c * (log(T) - log(Tref));
        else
            result = result + c * (pow(T, (e + 1.0)) - pow(Tref, (e + 1.0))) / (e + 1.0);
    }
    return result;
}

double CpRecord::S(double temperature)
{
    double result = 0.0;
    double T;
    if(temperature < m_tmax)
        T = temperature;
    else T = m_tmax;
    double Tref = m_tmin;
    for(unsigned int i = 0; i < m_coefficientList.size(); i++)
    {
        double c = m_coefficientList[i];
        double e = m_exponentList[i];
        // Create a modified exponent to analytically integrate Cp(T)/T instead of Cp(T).
        double e_modified = e - 1.0;
        if(e_modified == -1.0)
            result = result + c * (log(T) - log(Tref));
        else
            result = result + c * (pow(T, (e_modified + 1.0)) - pow(Tref, (e_modified + 1.0))) / (e_modified + 1.0);
    }
    return result;
}

std::string CpRecord::to_string()
{
    std::string result = "\t\tCp RECORD:\n";
    result = result + "\t\t\tTmin: " + boost::lexical_cast<std::string>(m_tmin) + "\n";
    result = result + "\t\t\tTmax: " + boost::lexical_cast<std::string>(m_tmax) + "\n";
    for(unsigned int i = 0; i < m_coefficientList.size(); i++)
    {
        int int_i = int(i);
        result += "\t\t\t" + (boost::format("%.8e") % m_coefficientList[int_i]).str() + " ";
        result += boost::lexical_cast<std::string>(m_exponentList[int_i]) + "\n";
    }
    return result;
}
