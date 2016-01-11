#ifndef INCOMETAXRULE_H
#define INCOMETAXRULE_H



#include "TaxRule.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class IncomeTaxRule;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class IncomeTaxRule : public TaxRule
    {
        public:
            IncomeTaxRule();
            IncomeTaxRule(std::string name, std::string description) : TaxRule(name, description)
            {
            };
            ~IncomeTaxRule();
            IncomeTaxRule(const IncomeTaxRule& other);

            friend bool operator==(const IncomeTaxRule& lhs, const IncomeTaxRule& rhs);
            friend bool operator!=(const IncomeTaxRule& lhs, const IncomeTaxRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const IncomeTaxRule&);

            bool IsValid() const { return true; }
            IncomeTaxRule* Clone() const { return new IncomeTaxRule(*this); }

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