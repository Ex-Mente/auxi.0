#ifndef CPRECORD_H
#define CPRECORD_H



#include "Object.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    class CpRecord;
}}}}

namespace auxi { namespace tools { namespace chemistry { namespace thermochemistry { 
    using namespace auxi::core;

    // Declare classes
    //
    class CpRecord : public Object
    {
        public:
            CpRecord() : Object()
            {
            };
            ~CpRecord();
            CpRecord(const CpRecord& other);

            friend bool operator==(const CpRecord& lhs, const CpRecord& rhs);
            friend bool operator!=(const CpRecord& lhs, const CpRecord& rhs);
            friend std::ostream& operator<<(std::ostream&, const CpRecord&);

            bool IsValid() const { return true; }
            CpRecord* Clone() const { return new CpRecord(*this); }

	      
             CpRecord(double Tmin, double Tmax, std::vector<double> coefficientList, std::vector<double> exponentList);
	      
            std::string to_string();
	      
            double Cp(double temperature);
	      
            double H(double temperature);
	      
            double S(double temperature);
            double GetTmin() const;
            void SetTmin(double tmin);

            double GetTmax() const;
            void SetTmax(double tmax);


        protected:
	        std::vector<double> m_coefficientList;
	        std::vector<double> m_exponentList;
	        double m_tmin;
	        double m_tmax;

        private:
    };
}}}}
#endif