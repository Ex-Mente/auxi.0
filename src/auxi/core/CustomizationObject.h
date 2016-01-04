#ifndef CUSTOMIZATIONOBJECT_H
#define CUSTOMIZATIONOBJECT_H

#include "CustomExtention.h"

namespace auxi{ namespace core
{
    class CustomizationObject
    {
    public:
        CustomizationObject();
        virtual ~CustomizationObject();
        CustomExtention GetCustomExtention()
        {
            return m_CustomExtention;
        }
        void SetCustomExtention(CustomExtention val)
        {
            m_CustomExtention = val;
        }
    protected:
    private:
        CustomExtention m_CustomExtention;
    };
}}
#endif // CUSTOMIZATIONOBJECT_H
