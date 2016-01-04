#ifndef COMPOUND_H
#define COMPOUND_H



#include "Phase.h"
#include "Object.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    class Compound;
}}}}

namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    using namespace auxi::core;

    // Declare classes
    //
    class Compound : public Object
    {
        public:
            Compound() : Object()
            {
            };
            ~Compound();
            Compound(const Compound& other);

            friend bool operator==(const Compound& lhs, const Compound& rhs);
            friend bool operator!=(const Compound& lhs, const Compound& rhs);
            friend std::ostream& operator<<(std::ostream&, const Compound&);

            bool IsValid() const { return true; }
            Compound* Clone() const { return new Compound(*this); }

	      
             Compound(std::string formula, std::map<std::string,Phase> phaseMap);
	      
            std::string to_string();
	      
            std::vector<std::string> get_phase_list();
	      
            double Cp(std::string phase, double temperature);
	      
            double H(std::string phase, double temperature);
	      
            double S(std::string phase, double temperature);
	      
            double G(std::string phase, double temperature);
            std::string GetFormula() const;
            void SetFormula(std::string formula);

            double Getmolar_mass() const;
            void Setmolar_mass(double molar_mass);


        protected:
	        std::map<std::string,Phase> m_phaseDict;
	        std::vector<std::string> m_sortedKeysPhaseList;
	        std::string m_formula = "";
	        double m_molar_mass;

        private:
    };
}}}}
#endif