#ifndef INDEXEDNAMEDObject_H
#define INDEXEDNAMEDObject_H

#include "NamedObject.h"

namespace auxi{ namespace core
{
    class IndexedNamedObject : public NamedObject
    {
        public:
            IndexedNamedObject() : NamedObject() {}
            IndexedNamedObject(std::string name, std::string description, int index) : NamedObject(name, description), m_index(index) {}
            virtual ~IndexedNamedObject();

            int GetIndex() const { return m_index; }
            void SetIndex(int index) { m_index = index; }
        protected:
        private:
            int m_index = -1;
    };
}}
#endif // INDEXEDNAMEDObject_H
