#ifndef ELEMENT_H
#define ELEMENT_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace tools { namespace chemistry { 
    class Element;
}}}

namespace auxi { namespace tools { namespace chemistry { 
    using namespace auxi::core;

    // Declare classes
    //
    class Element : public NamedObject
    {
        public:
            Element();
            Element(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Element();
            Element(const Element& other);

            friend bool operator==(const Element& lhs, const Element& rhs);
            friend bool operator!=(const Element& lhs, const Element& rhs);
            friend std::ostream& operator<<(std::ostream&, const Element&);

            bool IsValid() const { return true; }
            Element* Clone() const { return new Element(*this); }

	      
            std::string to_string();
            int GetPeriod() const;
            void SetPeriod(int period);

            int GetGroup() const;
            void SetGroup(int group);

            int GetAtomic_number() const;
            void SetAtomic_number(int atomic_number);

            std::string GetSymbol() const;
            void SetSymbol(std::string symbol);

            double GetMolar_mass() const;
            void SetMolar_mass(double molar_mass);


        protected:
	        int m_period;
	        int m_group;
	        int m_atomic_number;
	        std::string m_symbol = "";
	        double m_molar_mass;

        private:
    };
}}}
#endif