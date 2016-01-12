#ifndef TAXRULESET_H
#define TAXRULESET_H



#include "TaxRule.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>


// Forward declarations.
//





namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    class TaxRuleSet;
}
}
}
}

namespace auxi { namespace modelling { namespace accounting { namespace financial { 
    using namespace auxi::core;

    // Declare classes
    //
    class TaxRuleSet : public NamedObject
    {
        public:
            TaxRuleSet();
            TaxRuleSet(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~TaxRuleSet();
            TaxRuleSet(const TaxRuleSet& other);

            friend bool operator==(const TaxRuleSet& lhs, const TaxRuleSet& rhs);
            friend bool operator!=(const TaxRuleSet& lhs, const TaxRuleSet& rhs);
            friend std::ostream& operator<<(std::ostream&, const TaxRuleSet&);

            bool IsValid() const { return true; }
            TaxRuleSet* Clone() const { return new TaxRuleSet(*this); }

            std::vector<TaxRule*>& GetTaxRuleList();
            std::string GetCode() const;
            void SetCode(std::string code);
        protected:
	        std::vector<TaxRule*> m_taxRuleList;
	        std::string m_code = "";
        private:
    };
}
}
}
}

#endif