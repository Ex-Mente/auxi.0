#include "CpRecord.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::tools::chemistry::thermochemistry;


CpRecord::CpRecord(const CpRecord& other)
{
    m_coefficientList = other.m_coefficientList;
    m_exponentList = other.m_exponentList;
    m_tmin = other.m_tmin;
    m_tmax = other.m_tmax;
}

CpRecord::~CpRecord()
{

}

double CpRecord::GetTmin() const { return m_tmin; }
void CpRecord::SetTmin(double value) { m_tmin = value; }
double CpRecord::GetTmax() const { return m_tmax; }
void CpRecord::SetTmax(double value) { m_tmax = value; }


    
    
    
    
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    bool operator==(const CpRecord& lhs, const CpRecord& rhs)
    {
        return 1 == 1
	  && lhs.m_coefficientList == rhs.m_coefficientList
	  && lhs.m_exponentList == rhs.m_exponentList
	  && almost_equal(lhs.m_tmin, rhs.m_tmin, 5)
	  && almost_equal(lhs.m_tmax, rhs.m_tmax, 5)
	  ;
    }

    bool operator!=(const CpRecord& lhs, const CpRecord& rhs)
    {
        return 1 != 1
	  || lhs.m_coefficientList != rhs.m_coefficientList
	  || lhs.m_exponentList != rhs.m_exponentList
	  || !almost_equal(lhs.m_tmin, rhs.m_tmin, 5)
	  || !almost_equal(lhs.m_tmax, rhs.m_tmax, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const CpRecord& obj)
    {

        os << "A CpRecord instance.";
        return os;
    }
}
}
}
}
