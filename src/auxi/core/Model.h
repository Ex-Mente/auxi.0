#pragma once
#include "NamedObject.h"
#include "ExecutionObject.h"

namespace auxi{ namespace core
{
class Model : public ExecutionObject
{
public:
    Model();
    Model(std::string name, std::string description) : ExecutionObject(name, description) {}
    virtual ~Model();

    friend bool operator==(const Model& lhs, const Model& rhs);

    virtual Model* Clone() const = 0;
};
}}
