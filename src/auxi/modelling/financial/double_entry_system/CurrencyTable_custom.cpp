#include "CurrencyTable.h"

using namespace auxi::modelling::financial::double_entry_system;

CurrencyTable::CurrencyTable(std::string name, std::string description, std::string default_currency_name, std::string default_currency_description) : NamedObject(name, description)
{
    m_defaultCurrency = create_currency(default_currency_name, default_currency_description, 1.0);
}

Currency* CurrencyTable::create_currency(std::string name, std::string description, double defaultExchangeRate)
{
    auto c = new Currency();
    c->SetName(name);
    c->SetDescription(description);
    c->SetDefaultExchangeRate(defaultExchangeRate);
    m_currencyList.push_back(c);
    return c;
}
