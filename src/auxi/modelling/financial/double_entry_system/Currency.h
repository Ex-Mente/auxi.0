#ifndef CURRENCY_H
#define CURRENCY_H



#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    class Currency;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    using namespace auxi::core;

    // Declare classes
    //
    class Currency : public NamedObject
    {
        public:
            Currency();
            
            Currency(std::string name, std::string description) : NamedObject(name, description)
            {
            };
            ~Currency();
            Currency(const Currency& other);

            friend bool operator==(const Currency& lhs, const Currency& rhs);
            friend bool operator!=(const Currency& lhs, const Currency& rhs);
            friend std::ostream& operator<<(std::ostream&, const Currency&);

            bool IsValid() const { return true; }
            Currency* Clone() const { return new Currency(*this); }

	      
            std::string to_string();
            double GetDefaultExchangeRate() const;
            void SetDefaultExchangeRate(double defaultExchangeRate);


        protected:
	        double m_defaultExchangeRate;

        private:
    };
}}}}
#endif