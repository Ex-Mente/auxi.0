#ifndef TAXRULE_H
#define TAXRULE_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class TaxRule;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class TaxRule : public NamedObject
    {
        public:
            TaxRule();
            TaxRule(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~TaxRule();
            TaxRule(const TaxRule& other);

            friend bool operator==(const TaxRule& lhs, const TaxRule& rhs);
            friend bool operator!=(const TaxRule& lhs, const TaxRule& rhs);
            friend std::ostream& operator<<(std::ostream&, const TaxRule&);

            bool IsValid() const { return true; }
            TaxRule* Clone() const { return new TaxRule(*this); }

        protected:
        private:
    };
}
}
}
}

#endif