#include "Element.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::tools::chemistry;

Element::Element()
{
    //ctor
}

Element::Element(const Element& other)
{
    m_period = other.m_period;
    m_group = other.m_group;
    m_atomic_number = other.m_atomic_number;
    m_symbol = other.m_symbol;
    m_molar_mass = other.m_molar_mass;
}

Element::~Element()
{

}

int Element::GetPeriod() const { return m_period; }
void Element::SetPeriod(int value) { m_period = value; }
int Element::GetGroup() const { return m_group; }
void Element::SetGroup(int value) { m_group = value; }
int Element::GetAtomic_number() const { return m_atomic_number; }
void Element::SetAtomic_number(int value) { m_atomic_number = value; }
std::string Element::GetSymbol() const { return m_symbol; }
void Element::SetSymbol(std::string value) { m_symbol = value; }
double Element::GetMolar_mass() const { return m_molar_mass; }
void Element::SetMolar_mass(double value) { m_molar_mass = value; }


    
    
    
namespace auxi { namespace tools { namespace chemistry { 
    bool operator==(const Element& lhs, const Element& rhs)
    {
        return 1 == 1
	  && lhs.m_period == rhs.m_period
	  && lhs.m_group == rhs.m_group
	  && lhs.m_atomic_number == rhs.m_atomic_number
	  && lhs.m_symbol == rhs.m_symbol
	  && almost_equal(lhs.m_molar_mass, rhs.m_molar_mass, 5)
	  ;
    }

    bool operator!=(const Element& lhs, const Element& rhs)
    {
        return 1 != 1
	  || lhs.m_period != rhs.m_period
	  || lhs.m_group != rhs.m_group
	  || lhs.m_atomic_number != rhs.m_atomic_number
	  || lhs.m_symbol != rhs.m_symbol
	  || !almost_equal(lhs.m_molar_mass, rhs.m_molar_mass, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const Element& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
