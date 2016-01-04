#include "ModelingProject.h"

using namespace auxi::core;

ModelingProject::ModelingProject()
{
    //BOOST_LOG_TRIVIAL(trace) << "A modeling project created.";
}


ModelingProject::ModelingProject(const ModelingProject& other)  : ExecutionObject(other.GetName(), other.GetDescription())
{
    for(auto& group : other.m_VariableGroupList)
        m_VariableGroupList.emplace_back(group->Clone());
    for(auto& engine : other.m_CalculationEngineList)
        m_CalculationEngineList.emplace_back(engine->Clone());
    for(auto& model : other.m_ModelList)
        m_ModelList.emplace_back(model->Clone());
}

ModelingProject::~ModelingProject()
{

    // TODO: Make this work, currently getting an exception with Unit tests after destruction.
    // deleteVectorOfPointers(m_ModelList);
    // deleteVectorOfPointers(m_CalculationEngineList);
}


bool ModelingProject::IsValid() const
{
    /*for(auto& engine : m_CalculationEngineList)
        if(!engine->IsValid()) return false;
    for(auto& model : m_ModelList)
        if(!model->IsValid()) return false;
    return true;*/
    return true;
}

namespace auxi{ namespace core
{
    bool operator==(const ModelingProject& lhs, const ModelingProject& rhs)
    {

        return lhs.m_VariableGroupList == rhs.m_VariableGroupList &&
               lhs.m_CalculationEngineList == rhs.m_CalculationEngineList &&
               lhs.m_ModelList == rhs.m_ModelList;
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
