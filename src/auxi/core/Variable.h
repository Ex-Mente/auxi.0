#ifndef VARIABLE_H
#define VARIABLE_H

#include "NamedObject.h"
#include "Units.h"

namespace auxi{ namespace core
{
    class Variable : public NamedObject
    {
    public:
        Variable();
        Variable(const Variable& variable);
        Variable(std::string name, std::string description) : NamedObject(name, description), m_ValueSpecified(false) {};
        virtual ~Variable();

        bool IsValid() const
        {
            return true;
        }
        virtual Variable* Clone() { return new Variable(*this); }

        std::string GetDefaultValueString() const
        {
            return m_DefaultValueString;
        }
        virtual void SetDefaultValueString(std::string val)
        {
            m_DefaultValueString = val;
        }

        std::string GetValueString() const
        {
            return m_ValueString;
        }
        virtual void SetValueString(std::string val)
        {
            m_ValueString = val;
            m_ValueSpecified = true;
        }

        Units* GetUnitsValue() const
        {
            return m_Units;
        }
        void SetUnitsValue(Units* val)
        {
            m_Units = val;
        }

        bool GetValueSpecified() const
        {
            return m_ValueSpecified;
        }

        virtual std::string ToString() const
        {
            return m_Units == nullptr ? m_ValueString : m_Units->ToString(m_ValueString);
        }
    protected:
        void SetValueSpecified(bool val)
        {
            m_ValueSpecified = val;
        }

        // Helper for the Derived classes == operator.
        bool baseEqualTo(const Variable& rhs) const
        {
            return GetDefaultValueString() == rhs.GetDefaultValueString()
                   && GetValueString() == rhs.GetValueString()
                   && GetUnitsValue() == rhs.GetUnitsValue()
                   && GetValueSpecified() == rhs.GetValueSpecified();
        }
    private:
        std::string m_DefaultValueString; //!< Member variable "m_DefaultValueString"
        std::string m_ValueString; //!< Member variable "m_ValueString"
        Units *m_Units = nullptr; //!< Member variable "m_Units"
        bool m_ValueSpecified; //!< Member variable "m_ValueSpecified"
    };
}}
#endif // VARIABLE_H
