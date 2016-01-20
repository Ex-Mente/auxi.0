#include "BasicActivity.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::business;

BasicActivity::BasicActivity()
{
    //ctor
    initialize();
}

BasicActivity::BasicActivity(const BasicActivity& other)
{
    m_date = other.m_date;
    m_txTemplate = other.m_txTemplate;
    m_amount = other.m_amount;
}

BasicActivity::~BasicActivity()
{

}

boost::posix_time::ptime BasicActivity::GetDate() const { return m_date; }
void BasicActivity::SetDate(boost::posix_time::ptime value) { m_date = value; }
auxi::modelling::financial::double_entry_system::TransactionTemplate& BasicActivity::GetTxTemplate() { return m_txTemplate; }
void BasicActivity::SetTxTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& value) { m_txTemplate = value; }
double BasicActivity::GetAmount() const { return m_amount; }
void BasicActivity::SetAmount(double value) { m_amount = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const BasicActivity& lhs, const BasicActivity& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_txTemplate == rhs.m_txTemplate
	  && almost_equal(lhs.m_amount, rhs.m_amount, 5)
	  ;
    }

    bool operator!=(const BasicActivity& lhs, const BasicActivity& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_txTemplate != rhs.m_txTemplate
	  || !almost_equal(lhs.m_amount, rhs.m_amount, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const BasicActivity& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
