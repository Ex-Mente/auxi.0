#ifndef PHASE_H
#define PHASE_H



#include "CpRecord.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    class Phase;
}}}}

namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    using namespace auxi::core;

    // Declare classes
    //
    class Phase : public NamedObject
    {
        public:
            Phase();
            Phase(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Phase();
            Phase(const Phase& other);

            friend bool operator==(const Phase& lhs, const Phase& rhs);
            friend bool operator!=(const Phase& lhs, const Phase& rhs);
            friend std::ostream& operator<<(std::ostream&, const Phase&);

            bool IsValid() const { return true; }
            Phase* Clone() const { return new Phase(*this); }

	      
             Phase(std::string name, std::string symbol, double DHref, double Sref, std::map<double, CpRecord> cpRecordMap);
	      
            std::string to_string();
	      
            double Cp(double temperature);
	      
            double H(double temperature);
	      
            double S(double temperature);
	      
            double G(double temperature);
            std::string GetSymbol() const;
            void SetSymbol(std::string symbol);

            double GetTref() const;
            void SetTref(double tref);

            double GetDHref() const;
            void SetDHref(double dHref);

            double GetSref() const;
            void SetSref(double sref);


        protected:
	        std::map<double, CpRecord> m_cpRecordDict;
	        std::vector<double> m_sortedKeysCpRecordList;
	        std::string m_symbol = "";
	        double m_tref;
	        double m_dHref;
	        double m_sref;

        private:
    };
}}}}
#endif