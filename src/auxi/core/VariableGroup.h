#ifndef VARIABLEGROUP_H
#define VARIABLEGROUP_H

#include "NamedObject.h"
#include "Variable.h"
#include <memory.h>


namespace auxi{ namespace core
{
    class VariableGroup : public NamedObject
    {
        public:
            VariableGroup();
            VariableGroup(std::string name, std::string description) : NamedObject(name, description) {};
            ~VariableGroup();
            VariableGroup(const VariableGroup& other);

            friend bool operator==(const VariableGroup& lhs, const VariableGroup& rhs);

            bool IsValid() const { return true; }
            VariableGroup* Clone() const { return new VariableGroup(*this); };

            std::vector<VariableGroup*>& GetVariableGroupList() { return m_VariableGroupList; }
            std::vector<Variable*>& GetVariableList() { return m_VariableList; }
        protected:
        private:
            std::vector<VariableGroup*> m_VariableGroupList;
            std::vector<Variable*> m_VariableList;
    };
}}
#endif // VARIABLEGROUP_H
