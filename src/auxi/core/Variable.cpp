#include "Variable.h"

using namespace auxi::core;

Variable::Variable() : m_ValueSpecified(false)
{
    //ctor
}

Variable::Variable(const Variable& other) : NamedObject(other.GetName(), other.GetDescription()), m_ValueSpecified(false)
{
    std::string defaultValueString = other.GetDefaultValueString();
    std::string valueString = other.GetValueString();
    if(!defaultValueString.empty()) m_DefaultValueString = defaultValueString;
    if(!valueString.empty()) m_ValueString = valueString;
    m_Units = other.GetUnitsValue();
}

Variable::~Variable()
{
    //dtor
}
