#ifndef CURRENCYTABLE_H
#define CURRENCYTABLE_H



#include "Currency.h"
#include "NamedObject.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    class CurrencyTable;
}}}}

namespace auxi { namespace modelling { namespace financial { namespace double_entry_system { 
    using namespace auxi::core;

    // Declare classes
    //
    class CurrencyTable : public NamedObject
    {
        public:
            CurrencyTable();
            
            ~CurrencyTable();
            CurrencyTable(const CurrencyTable& other);

            friend bool operator==(const CurrencyTable& lhs, const CurrencyTable& rhs);
            friend bool operator!=(const CurrencyTable& lhs, const CurrencyTable& rhs);
            friend std::ostream& operator<<(std::ostream&, const CurrencyTable&);

            bool IsValid() const { return true; }
            CurrencyTable* Clone() const { return new CurrencyTable(*this); }

	      
             CurrencyTable(std::string name, std::string description = "", std::string default_currency_name = "", std::string default_currency_description = "");
	      
            Currency* create_currency(std::string name, std::string description, double defaultExchangeRate);
            std::vector<Currency*>& GetCurrencyList();

            Currency* GetDefaultCurrency() const;
            void SetDefaultCurrency(Currency* defaultCurrency);


        protected:
	        std::vector<Currency*> m_currencyList;
	        Currency* m_defaultCurrency = nullptr;

        private:
    };
}}}}
#endif