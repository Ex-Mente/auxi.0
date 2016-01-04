#include "Units.h"
#include "IncompatibleUnitsException.h"

using namespace auxi::core;

Units::Units() : m_Coefficient(1.0), m_Offset(0.0)
{
    m_Exponents = std::vector<double>(static_cast<int>(BaseUnit::baseUnitLast)  + 1);
}

Units::Units(std::string quantity,
             std::string name,
             std::string symbol,
             double offset,
             double coefficient,
             bool symbolAfter,
             double ampereExponent,
             double candelaExponent,
             double kelvinExponent,
             double kilogramExponent,
             double meterExponent,
             double moleExponent,
             double secondExponent,
             double usdExponent) : NamedObject(name, "")
{
    m_Quantity = quantity;
    m_Symbol = symbol;
    m_Offset = offset;
    m_Coefficient = coefficient;
    m_SymbolAfter = symbolAfter;

    m_Exponents = std::vector<double>(static_cast<int>(BaseUnit::baseUnitLast)  + 1);
    SetAmpereExponent(ampereExponent);
    SetCandelaExponent(candelaExponent);
    SetKelvinExponent(kelvinExponent);
    SetKilogramExponent(kilogramExponent);
    SetMeterExponent(meterExponent);
    SetMoleExponent(moleExponent);
    SetSecondExponent(secondExponent);
    SetUsdExponent(usdExponent);
}

Units::Units(const Units& units) : NamedObject(units.GetName(), units.GetDescription())
{
    if(!units.GetSymbolEmpty()) m_Symbol = units.GetSymbol();
    m_Quantity = units.GetQuantity();

    m_Offset = units.GetOffset();
    m_Coefficient = units.GetCoefficient();
    m_SymbolAfter = units.GetSymbolAfter();

    m_Exponents = std::vector<double>(static_cast<int>(BaseUnit::baseUnitLast)  + 1);
    SetAmpereExponent(units.GetAmpereExponent());
    SetCandelaExponent(units.GetCandelaExponent());
    SetKelvinExponent(units.GetKelvinExponent());
    SetKilogramExponent(units.GetKilogramExponent());
    SetMeterExponent(units.GetMeterExponent());
    SetMoleExponent(units.GetMoleExponent());
    SetSecondExponent(units.GetSecondExponent());
    SetUsdExponent(units.GetUsdExponent());
}

Units::~Units()
{
    //dtor
}

std::string Units::GetSymbol() const
{
    if(GetSymbolEmpty())
    {
        std::string result = "";
        double ampere = GetAmpereExponent();
        double candela = GetCandelaExponent();
        double kelvin = GetKelvinExponent();
        double kilogram = GetKilogramExponent();
        double meter = GetMeterExponent();
        double mole = GetMoleExponent();
        double second = GetSecondExponent();
        double usd = GetUsdExponent();

        if(m_Coefficient != 1.0) result += to_string(m_Coefficient);
        if(ampere == 1.0)        result += ".A";
        else if(ampere != 0.0)   result += ".A^(" + to_string(ampere) + ")";
        if(candela == 1.0)       result += ".cd";
        else if(candela != 0.0)  result += ".cd^(" + to_string(candela) + ")";
        if(kelvin == 1.0)        result += ".K";
        else if(kelvin != 0.0)   result += ".K^(" + to_string(kelvin) + ")";
        if(kilogram == 1.0)      result += ".kg";
        else if(kilogram != 0.0) result += ".kg^(" + to_string(kilogram) + ")";
        if(meter == 1.0)         result += ".m";
        else if(meter != 0.0)    result += ".m^(" + to_string(meter) + ")";
        if(mole == 1.0)          result += ".mol";
        else if(mole != 0.0)     result += ".mol^(" + to_string(mole) + ")";
        if(second == 1.0)        result += ".s";
        else if(second != 0.0)   result += ".s^(" + to_string(second) + ")";
        if(usd == 1.0)           result += ".USD";
        else if(usd != 0.0)      result += ".USD^(" + to_string(usd) + ")";

        return result;
    }
    else return m_Symbol;
}

namespace auxi{ namespace core
{
Units operator+(const Units& lhs, double scalar)
{
    std::string symbol = lhs.GetSymbolEmpty() ? "" : lhs.GetSymbol();
    Units result {lhs.GetQuantity(), lhs.GetName(), symbol, lhs.GetOffset() + scalar, lhs.GetCoefficient(), lhs.GetSymbolAfter(),
                  lhs.GetAmpereExponent(), lhs.GetCandelaExponent(), lhs.GetKelvinExponent(), lhs.GetKilogramExponent(), lhs.GetMeterExponent(), lhs.GetMoleExponent(), lhs.GetSecondExponent(), lhs.GetUsdExponent()
                 };
    return result;
}

Units operator-(const Units& lhs, double scalar)
{
    std::string symbol = lhs.GetSymbolEmpty() ? "" : lhs.GetSymbol();
    Units result {lhs.GetQuantity(), lhs.GetName(), symbol, lhs.GetOffset() - scalar, lhs.GetCoefficient(), lhs.GetSymbolAfter(),
                  lhs.GetAmpereExponent(), lhs.GetCandelaExponent(), lhs.GetKelvinExponent(), lhs.GetKilogramExponent(), lhs.GetMeterExponent(), lhs.GetMoleExponent(), lhs.GetSecondExponent(), lhs.GetUsdExponent()
                 };
    return result;
}

Units operator*(const Units& lhs, const Units& rhs)
{
    Units result {""/*Quantity*/, ""/*Name*/, ""/*Symbol*/, 0.0/*Offset*/, lhs.GetCoefficient() * rhs.GetCoefficient(), true/*SymbolAfter*/,
                  lhs.GetAmpereExponent() + rhs.GetAmpereExponent(),
                  lhs.GetCandelaExponent() + rhs.GetCandelaExponent(),
                  lhs.GetKelvinExponent() + rhs.GetKelvinExponent(),
                  lhs.GetKilogramExponent() + rhs.GetKilogramExponent(),
                  lhs.GetMeterExponent() + rhs.GetMeterExponent(),
                  lhs.GetMoleExponent() + rhs.GetMoleExponent(),
                  lhs.GetSecondExponent() + rhs.GetSecondExponent(),
                  lhs.GetUsdExponent() + rhs.GetUsdExponent()
                 };
    return result;
}

Units operator*(const Units& lhs, double scalar)
{
    std::string symbol = lhs.GetSymbolEmpty() ? "" : lhs.GetSymbol();
    Units result {lhs.GetQuantity(), lhs.GetName(), symbol, lhs.GetOffset(), lhs.GetCoefficient() * scalar, lhs.GetSymbolAfter(),
                  lhs.GetAmpereExponent(), lhs.GetCandelaExponent(), lhs.GetKelvinExponent(), lhs.GetKilogramExponent(), lhs.GetMeterExponent(), lhs.GetMoleExponent(), lhs.GetSecondExponent(), lhs.GetUsdExponent()
                 };
    return result;
}

Units operator/(const Units& lhs, const Units& rhs)
{
    Units result {""/*Quantity*/, ""/*Name*/, ""/*Symbol*/, 0.0/*Offset*/,
                  lhs.GetCoefficient() / rhs.GetCoefficient(), true/*SymbolAfter*/,
                  lhs.GetAmpereExponent() - rhs.GetAmpereExponent(),
                  lhs.GetCandelaExponent() - rhs.GetCandelaExponent(),
                  lhs.GetKelvinExponent() - rhs.GetKelvinExponent(),
                  lhs.GetKilogramExponent() - rhs.GetKilogramExponent(),
                  lhs.GetMeterExponent() - rhs.GetMeterExponent(),
                  lhs.GetMoleExponent() - rhs.GetMoleExponent(),
                  lhs.GetSecondExponent() - rhs.GetSecondExponent(),
                  lhs.GetUsdExponent() - rhs.GetUsdExponent()
                 };
    return result;
}

Units operator/(const Units& lhs, double scalar)
{
    std::string symbol = lhs.GetSymbolEmpty() ? "" : lhs.GetSymbol();
    Units result {lhs.GetQuantity(), lhs.GetName(), symbol, lhs.GetOffset(), lhs.GetCoefficient() / scalar, lhs.GetSymbolAfter(),
                  lhs.GetAmpereExponent(), lhs.GetCandelaExponent(), lhs.GetKelvinExponent(), lhs.GetKilogramExponent(), lhs.GetMeterExponent(), lhs.GetMoleExponent(), lhs.GetSecondExponent(), lhs.GetUsdExponent()
                 };
    return result;
}

// TODO: Discuss with Johan the Accuracies to do the floating point comparisons with. == is not enough.
bool operator==(const Units& lhs, const Units& rhs)
{
    return lhs.GetQuantity() == rhs.GetQuantity() &&
           lhs.GetSymbol() == rhs.GetSymbol() &&
           lhs.GetOffset() == rhs.GetOffset() &&
           lhs.GetCoefficient() == rhs.GetCoefficient() &&
           lhs.GetSymbolAfter() == rhs.GetSymbolAfter() &&
           lhs.GetAmpereExponent() == rhs.GetAmpereExponent() &&
           lhs.GetCandelaExponent() == rhs.GetCandelaExponent() &&
           lhs.GetKelvinExponent() == rhs.GetKelvinExponent() &&
           lhs.GetKilogramExponent() == rhs.GetKilogramExponent() &&
           lhs.GetMeterExponent() == rhs.GetMeterExponent() &&
           lhs.GetMoleExponent() == rhs.GetMoleExponent() &&
           lhs.GetSecondExponent() == rhs.GetSecondExponent() &&
           lhs.GetUsdExponent() == rhs.GetUsdExponent();
}

bool operator!=(const Units& lhs, const Units& rhs)
{
    return !(lhs == rhs);
}


std::ostream& operator<<(std::ostream& os, const Units& units)
{
    os << units.ToString();
    return os;
}
}}

// TODO: Discuss with Johan the Accuracies to do the floating point comparisons with. != is not enough.
double Units::Convert(double quantity, const Units& from, const Units& to)
{
    if(from.GetAmpereExponent() != to.GetAmpereExponent() ||
            from.GetCandelaExponent() != to.GetCandelaExponent() ||
            from.GetKelvinExponent() != to.GetKelvinExponent() ||
            from.GetKilogramExponent() != to.GetKilogramExponent() ||
            from.GetMeterExponent() != to.GetMeterExponent() ||
            from.GetMoleExponent() != to.GetMoleExponent() ||
            from.GetSecondExponent() != to.GetSecondExponent() ||
            from.GetUsdExponent() != to.GetUsdExponent())
        throw IncompatibleUnitsException(&from, &to);

    double result = quantity;
    result -= from.GetOffset();
    result /=from.GetCoefficient();

    result *= to.GetCoefficient();
    result += to.GetOffset();

    return result;
}

std::string Units::ToString(double quantity) const
{
    if(m_SymbolAfter)
        return to_string(quantity) + " " + m_Symbol;
    else return m_Symbol + " " + to_string(quantity);
}

std::string Units::ToString(std::string quantity) const
{
    if(m_SymbolAfter)
        return quantity + " " + m_Symbol;
    else return m_Symbol + " " + quantity;
}

std::string Units::ToString(double quantity, std::string format) const
{
    std::string quantityString = (boost::format(format) % quantity).str();
    if(m_SymbolAfter)
        return quantityString + " " + m_Symbol;
    else return m_Symbol + " " + quantityString;
}
