#ifndef CALCULATIONENGINE_H
#define CALCULATIONENGINE_H

#include "NamedObject.h"


namespace auxi{ namespace core
{
    class CalculationEngine : public NamedObject
    {
        public:
            CalculationEngine();
            CalculationEngine(std::string name, std::string description) : NamedObject(name, description) {}
            virtual ~CalculationEngine();
            CalculationEngine(const CalculationEngine& other) : NamedObject(other.GetName(), other.GetDescription()) {}

            virtual CalculationEngine* Clone() const = 0;
        protected:
        private:
    };
}}

#endif // CALCULATIONENGINE_H
