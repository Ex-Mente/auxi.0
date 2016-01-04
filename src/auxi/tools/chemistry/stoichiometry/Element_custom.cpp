#include "Element.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>

using namespace auxi::tools::chemistry;

std::string Element::to_string()
{
    std::string result = "\t\tElement:\n";
    result = result + "\t\t\tPeroid: " + boost::lexical_cast<std::string>(m_period) + "\n";
    result = result + "\t\t\tGroup: " + boost::lexical_cast<std::string>(m_group) + "\n";
    result = result + "\t\t\tAtomic_number: " + boost::lexical_cast<std::string>(m_atomic_number) + "\n";
    result = result + "\t\t\tSymbol: " + m_symbol + "\n";
    result = result + "\t\t\tMolar Mass: " + boost::lexical_cast<std::string>(m_molar_mass) + "\n";

    return result;
}