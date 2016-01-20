#ifndef CAPITALGAINSRULE_H
#define CAPITALGAINSRULE_H



#include "Rule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    class CapitalGainsRule;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace tax { 
    using namespace auxi::core;

    // Declare classes
    //
    class CapitalGainsRule : public Rule
    {
        public:
            CapitalGainsRule();
            CapitalGainsRule(std::string name, std::string description) : Rule(name, description)
            {
            };
            ~CapitalGainsRule();
            CapitalGainsRule(const CapitalGainsRule& other);

            friend bool operator==(const CapitalGainsRule& lhs, const CapitalGainsRule& rhs);
            friend bool operator!=(const CapitalGainsRule& lhs, const CapitalGainsRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const CapitalGainsRule&);

            bool IsValid() const { return true; }
            CapitalGainsRule* Clone() const { return new CapitalGainsRule(*this); }

            double GetPercentage() const;
            void SetPercentage(double percentage);


        protected:
	        double m_percentage;

        private:
    };
}}}}
#endif