#pragma once
#include "Object.h"

namespace auxi{ namespace core
{
class NamedObject :
    public Object
{
public:
    NamedObject();
    NamedObject(std::string name, std::string description) : m_name(name), m_description(description) {}
    NamedObject(NamedObject&) {}
    virtual ~NamedObject();

    virtual std::string GetName() const { return m_name; }
    virtual void SetName(std::string name) { m_name = name; }

    std::string GetDescription() const { return m_description; }
    void SetDescription(std::string description) { m_description = description; }
protected:
    std::string m_name = "";
    std::string m_description = "";
};
}}
