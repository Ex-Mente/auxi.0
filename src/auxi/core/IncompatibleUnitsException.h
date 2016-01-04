#ifndef INCOMPATIBLEUNITSEXCEPTION_H
#define INCOMPATIBLEUNITSEXCEPTION_H

#include <exception>
#include "Units.h"

namespace auxi{ namespace core
{
class Units;
class IncompatibleUnitsException : public std::exception
{
public:
    IncompatibleUnitsException(const Units* from, const Units* to) : m_from(from), m_to(to) {}
    ~IncompatibleUnitsException() {}
protected:
private:
    const Units *m_from, *m_to;

    virtual const char* what() const throw()
    {
        return ("Incompatible units. Cannot convert from '" + m_from->GetSymbol() + "' to '" + m_to->GetSymbol() + "'.").c_str();
    }
};
}}
#endif // INCOMPATIBLEUNITSEXCEPTION_H
