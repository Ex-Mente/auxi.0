#include "Compound.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::tools::chemistry::thermochemistry;


Compound::Compound(const Compound& other)
{
    m_phaseDict = other.m_phaseDict;
    m_sortedKeysPhaseList = other.m_sortedKeysPhaseList;
    m_formula = other.m_formula;
    m_molar_mass = other.m_molar_mass;
}

Compound::~Compound()
{

}

std::string Compound::GetFormula() const { return m_formula; }
void Compound::SetFormula(std::string value) { m_formula = value; }
double Compound::Getmolar_mass() const { return m_molar_mass; }
void Compound::Setmolar_mass(double value) { m_molar_mass = value; }


    
    
    
    
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    bool operator==(const Compound& lhs, const Compound& rhs)
    {
        return 1 == 1
	  && lhs.m_phaseDict == rhs.m_phaseDict
	  && lhs.m_sortedKeysPhaseList == rhs.m_sortedKeysPhaseList
	  && lhs.m_formula == rhs.m_formula
	  && almost_equal(lhs.m_molar_mass, rhs.m_molar_mass, 5)
	  ;
    }

    bool operator!=(const Compound& lhs, const Compound& rhs)
    {
        return 1 != 1
	  || lhs.m_phaseDict != rhs.m_phaseDict
	  || lhs.m_sortedKeysPhaseList != rhs.m_sortedKeysPhaseList
	  || lhs.m_formula != rhs.m_formula
	  || !almost_equal(lhs.m_molar_mass, rhs.m_molar_mass, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const Compound& obj)
    {

        os << "A Compound instance.";
        return os;
    }
}
}
}
}
