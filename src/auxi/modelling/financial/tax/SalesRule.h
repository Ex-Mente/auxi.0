#ifndef SALESRULE_H
#define SALESRULE_H



#include "Rule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    class SalesRule;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace tax { 
    using namespace auxi::core;

    // Declare classes
    //
    class SalesRule : public Rule
    {
        public:
            SalesRule();
            SalesRule(std::string name, std::string description) : Rule(name, description)
            {
            };
            ~SalesRule();
            SalesRule(const SalesRule& other);

            friend bool operator==(const SalesRule& lhs, const SalesRule& rhs);
            friend bool operator!=(const SalesRule& lhs, const SalesRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const SalesRule&);

            bool IsValid() const { return true; }
            SalesRule* Clone() const { return new SalesRule(*this); }

            double GetPercentage() const;
            void SetPercentage(double percentage);


        protected:
	        double m_percentage;

        private:
    };
}}}}
#endif