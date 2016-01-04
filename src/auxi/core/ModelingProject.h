#pragma once
#include "NamedObject.h"
#include "ExecutionObject.h"
#include "VariableGroup.h"
#include "CalculationEngine.h"
#include "Model.h"
#include "Model.h"
#include <vector>
#include <memory>

namespace auxi{ namespace core
{
    class ModelingProject : public ExecutionObject
    {
    public:
        ModelingProject();
        ModelingProject(std::string name, std::string description) : ExecutionObject(name, description) {};
        ModelingProject(const ModelingProject& other);
        ~ModelingProject();

        friend bool operator==(const ModelingProject& lhs, const ModelingProject& rhs);

        ModelingProject* Clone() const
        {
            return new ModelingProject(*this);
        };
        bool IsValid() const;

        std::vector<VariableGroup*>& GetVariableGroupList()
        {
            return m_VariableGroupList;
        }
        std::vector<CalculationEngine*>& GetCalculationEngineList()
        {
            return m_CalculationEngineList;
        }
        std::vector<Model*>& GetModelList()
        {
            return m_ModelList;
        }
    private:
        std::vector<VariableGroup*> m_VariableGroupList;
        std::vector<CalculationEngine*> m_CalculationEngineList;
        std::vector<Model*> m_ModelList;
    };
}}
