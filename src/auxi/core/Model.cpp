#include "Model.h"

using namespace auxi::core;

Model::Model(void)
{
}


Model::~Model(void)
{
}

namespace auxi{ namespace core
{
    bool operator==(const Model&, const Model&)
    {
        return true;
    }
}}
