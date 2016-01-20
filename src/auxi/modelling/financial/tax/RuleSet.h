#ifndef RULESET_H
#define RULESET_H



#include "Rule.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    class RuleSet;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace tax { 
    using namespace auxi::core;

    // Declare classes
    //
    class RuleSet : public NamedObject
    {
        public:
            RuleSet();
            RuleSet(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~RuleSet();
            RuleSet(const RuleSet& other);

            friend bool operator==(const RuleSet& lhs, const RuleSet& rhs);
            friend bool operator!=(const RuleSet& lhs, const RuleSet& rhs);
            friend std::ostream& operator<<(std::ostream&, const RuleSet&);

            bool IsValid() const { return true; }
            RuleSet* Clone() const { return new RuleSet(*this); }

            std::vector<Rule*>& GetRuleList();

            std::string GetCode() const;
            void SetCode(std::string code);


        protected:
	        std::vector<Rule*> m_ruleList;
	        std::string m_code = "";

        private:
    };
}}}}
#endif