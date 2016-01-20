#ifndef INCOMERULE_H
#define INCOMERULE_H



#include "Rule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    class IncomeRule;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace tax { 
    using namespace auxi::core;

    // Declare classes
    //
    class IncomeRule : public Rule
    {
        public:
            IncomeRule();
            IncomeRule(std::string name, std::string description) : Rule(name, description)
            {
            };
            ~IncomeRule();
            IncomeRule(const IncomeRule& other);

            friend bool operator==(const IncomeRule& lhs, const IncomeRule& rhs);
            friend bool operator!=(const IncomeRule& lhs, const IncomeRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const IncomeRule&);

            bool IsValid() const { return true; }
            IncomeRule* Clone() const { return new IncomeRule(*this); }

            double GetPercentage() const;
            void SetPercentage(double percentage);


        protected:
	        double m_percentage;

        private:
    };
}}}}
#endif