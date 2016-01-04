#include "VariableGroup.h"

using namespace auxi::core;

VariableGroup::VariableGroup()
{

}

VariableGroup::~VariableGroup()
{
    // TODO: Make this work, currently getting an exception with Unit tests after destruction.
    //deleteVectorOfPointers(m_VariableList);
}

VariableGroup::VariableGroup(const VariableGroup& other) : NamedObject(other.GetName(), other.GetDescription())
{
    for(auto& group : other.m_VariableGroupList)
        m_VariableGroupList.emplace_back(group->Clone());
    for(auto& variable : other.m_VariableList)
        m_VariableList.emplace_back(variable->Clone());
}

namespace auxi{ namespace core
{
    bool operator==(const VariableGroup& lhs, const VariableGroup& rhs)
    {

        return lhs.m_VariableGroupList == rhs.m_VariableGroupList && lhs.m_VariableList == rhs.m_VariableList;
    /*
        const auto& rhsVariableGroupList = rhs.m_VariableGroupList;
        const auto& lhsVariableGroupList = lhs.m_VariableGroupList;
        unsigned long rhsVariableGroupListSize = rhsVariableGroupList.size();
        if(lhsVariableGroupList.size() != rhsVariableGroupListSize) return false;
        for(unsigned long i = 0; i < rhsVariableGroupListSize; i++)
            if(!(rhsVariableGroupList[i] == lhsVariableGroupList[i])) return false;

        const auto& rhsVariableList = rhs.m_VariableList;
        const auto& lhsVariableList = lhs.m_VariableList;
        unsigned long rhsVariableListSize = rhsVariableList.size();
        if(lhsVariableList.size() != rhsVariableListSize) return false;
        for(unsigned long i = 0; i < rhsVariableListSize; i++)
            if(&rhsVariableList[i] != &lhsVariableList[i]) return false;

        return true;
        */
    }
}}
