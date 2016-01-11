#ifndef SALESTAXRULE_H
#define SALESTAXRULE_H



#include "TaxRule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class SalesTaxRule;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class SalesTaxRule : public TaxRule
    {
        public:
            SalesTaxRule();
            SalesTaxRule(std::string name, std::string description) : TaxRule(name, description)
            {
            };
            ~SalesTaxRule();
            SalesTaxRule(const SalesTaxRule& other);

            friend bool operator==(const SalesTaxRule& lhs, const SalesTaxRule& rhs);
            friend bool operator!=(const SalesTaxRule& lhs, const SalesTaxRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const SalesTaxRule&);

            bool IsValid() const { return true; }
            SalesTaxRule* Clone() const { return new SalesTaxRule(*this); }

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