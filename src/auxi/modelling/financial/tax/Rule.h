#ifndef RULE_H
#define RULE_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace tax { 
    class Rule;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace tax { 
    using namespace auxi::core;

    // Declare classes
    //
    class Rule : public NamedObject
    {
        public:
            Rule();
            Rule(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Rule();
            Rule(const Rule& other);

            friend bool operator==(const Rule& lhs, const Rule& rhs);
            friend bool operator!=(const Rule& lhs, const Rule& rhs);
            friend std::ostream& operator<<(std::ostream&, const Rule&);

            bool IsValid() const { return true; }
            Rule* Clone() const { return new Rule(*this); }


        protected:

        private:
    };
}}}}
#endif