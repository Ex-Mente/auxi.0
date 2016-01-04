#include "Phase.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::tools::chemistry::thermochemistry;

Phase::Phase()
{
    //ctor
}

Phase::Phase(const Phase& other)
{
    m_cpRecordDict = other.m_cpRecordDict;
    m_sortedKeysCpRecordList = other.m_sortedKeysCpRecordList;
    m_symbol = other.m_symbol;
    m_tref = other.m_tref;
    m_dHref = other.m_dHref;
    m_sref = other.m_sref;
}

Phase::~Phase()
{

}

std::string Phase::GetSymbol() const { return m_symbol; }
void Phase::SetSymbol(std::string value) { m_symbol = value; }
double Phase::GetTref() const { return m_tref; }
void Phase::SetTref(double value) { m_tref = value; }
double Phase::GetDHref() const { return m_dHref; }
void Phase::SetDHref(double value) { m_dHref = value; }
double Phase::GetSref() const { return m_sref; }
void Phase::SetSref(double value) { m_sref = value; }


    
    
    
    
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    bool operator==(const Phase& lhs, const Phase& rhs)
    {
        return 1 == 1
	  && lhs.m_cpRecordDict == rhs.m_cpRecordDict
	  && lhs.m_sortedKeysCpRecordList == rhs.m_sortedKeysCpRecordList
	  && lhs.m_symbol == rhs.m_symbol
	  && almost_equal(lhs.m_tref, rhs.m_tref, 5)
	  && almost_equal(lhs.m_dHref, rhs.m_dHref, 5)
	  && almost_equal(lhs.m_sref, rhs.m_sref, 5)
	  ;
    }

    bool operator!=(const Phase& lhs, const Phase& rhs)
    {
        return 1 != 1
	  || lhs.m_cpRecordDict != rhs.m_cpRecordDict
	  || lhs.m_sortedKeysCpRecordList != rhs.m_sortedKeysCpRecordList
	  || lhs.m_symbol != rhs.m_symbol
	  || !almost_equal(lhs.m_tref, rhs.m_tref, 5)
	  || !almost_equal(lhs.m_dHref, rhs.m_dHref, 5)
	  || !almost_equal(lhs.m_sref, rhs.m_sref, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const Phase& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
}
