#include "Currency.h"

using namespace auxi::modelling::financial::double_entry_system;

std::string Currency::to_string()
{
    return GetName();
}
