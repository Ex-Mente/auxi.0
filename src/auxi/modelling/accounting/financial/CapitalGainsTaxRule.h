#ifndef CAPITALGAINSTAXRULE_H
#define CAPITALGAINSTAXRULE_H



#include "TaxRule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class CapitalGainsTaxRule;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class CapitalGainsTaxRule : public TaxRule
    {
        public:
            CapitalGainsTaxRule();
            CapitalGainsTaxRule(std::string name, std::string description) : TaxRule(name, description)
            {
            };
            ~CapitalGainsTaxRule();
            CapitalGainsTaxRule(const CapitalGainsTaxRule& other);

            friend bool operator==(const CapitalGainsTaxRule& lhs, const CapitalGainsTaxRule& rhs);
            friend bool operator!=(const CapitalGainsTaxRule& lhs, const CapitalGainsTaxRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const CapitalGainsTaxRule&);

            bool IsValid() const { return true; }
            CapitalGainsTaxRule* Clone() const { return new CapitalGainsTaxRule(*this); }

            double GetPercentage() const;
            void SetPercentage(double percentage);
        protected:
	        double m_percentage;
        private:
    };
}
}
}
}

#endif