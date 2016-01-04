#ifndef UNITS_H
#define UNITS_H

#include <vector>

#include <boost/format.hpp>

#include "NamedObject.h"
#include "BaseUnit.h"

namespace auxi{ namespace core
{
    class Units : public NamedObject
    {
    public:
        Units();
        Units(const Units& units);
        Units(std::string quantity,
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
              double usdExponent);

        virtual ~Units();

        bool IsValid() const
        {
            return true;
        }
        Units* Clone() const
        {
            return new Units(*this);
        };

        double GetCoefficient() const
        {
            return m_Coefficient;
        }
        void SetCoefficient(double val)
        {
            if(val <= 0.0) throw std::domain_error("The Coefficient must be greater than 0");
            m_Coefficient = val;
        }

        double GetOffset() const
        {
            return m_Offset;
        }
        void SetOffset(double val)
        {
            m_Offset = val;
        }

        const std::string GetQuantity() const
        {
            return m_Quantity;
        }
        void SetQuantity(std::string val)
        {
            m_Quantity = val;
        }

        std::string GetSymbol() const;
        void SetSymbol(std::string val)
        {
            m_Symbol = val;
        }
        bool GetSymbolEmpty() const
        {
            return m_Symbol == ""; //m_Symbol.empty();
        }

        bool GetSymbolAfter() const { return m_SymbolAfter; }
        void SetSymbolAfter(bool val) { m_SymbolAfter = val; }

        double GetAmpereExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::A);
            return m_Exponents[index];
        }
        void SetAmpereExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::A);
            m_Exponents[index] = val;
        }

        double GetCandelaExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::cd);
            return m_Exponents[index];
        }
        void SetCandelaExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::cd);
            m_Exponents[index] = val;
        }

        double GetKelvinExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::K);
            return m_Exponents[index];
        }
        void SetKelvinExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::K);
            m_Exponents[index] = val;
        }

        double GetKilogramExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::kg);
            return m_Exponents[index];
        }
        void SetKilogramExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::kg);
            m_Exponents[index] = val;
        }

        double GetMeterExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::m);
            return m_Exponents[index];
        }
        void SetMeterExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::m);
            m_Exponents[index] = val;
        }

        double GetMoleExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::mol);
            return m_Exponents[index];
        }
        void SetMoleExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::mol);
            m_Exponents[index] = val;
        }

        double GetSecondExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::s);
            return m_Exponents[index];
        }
        void SetSecondExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::s);
            m_Exponents[index] = val;
        }

        double GetUsdExponent() const
        {
            constexpr int index = static_cast<int>(BaseUnit::USD);
            return m_Exponents[index];
        }
        void SetUsdExponent(double val)
        {
            constexpr int index = static_cast<int>(BaseUnit::USD);
            m_Exponents[index] = val;
        }

        friend Units operator+(const Units& lhs, double scalar);
        friend Units operator-(const Units& lhs, double scalar);
        friend Units operator*(const Units& lhs, const Units& rhs);
        friend Units operator*(const Units& lhs, double scalar);
        friend Units operator/(const Units& lhs, const Units& rhs);
        friend Units operator/(const Units& lhs, double scalar);
        friend bool operator==(const Units& lhs, const Units& rhs);
        friend bool operator!=(const Units& lhs, const Units& rhs);
        friend std::ostream& operator<<(std::ostream& os, const Units& units);

        static Units Add(Units unit, double scalar) { return unit + scalar; }
        static Units Subtract(Units unit, double scalar) { return unit - scalar; }
        static Units Multiply(Units unit1, Units unit2) { return unit1 * unit2; }
        static Units Multiply(Units unit, double scalar) { return unit * scalar; }
        static Units Divide(Units unit1, Units unit2) { return unit1 / unit2; }
        static Units Divide(Units unit, double scalar) { return unit / scalar; }

        static double Convert(double quantity, const Units& from, const Units& to);

        std::string ToString() const { return GetSymbol(); }
        std::string ToString(double quantity) const;
        std::string ToString(std::string quantity) const;
        std::string ToString(double quantity, std::string format) const;

        static constexpr int baseUnitsMinIndex = static_cast<int>(BaseUnit::baseUnitFirst);
        static constexpr int baseUnitsMaxIndex = static_cast<int>(BaseUnit::baseUnitLast);
    protected:
    private:
        double m_Coefficient;
        std::vector<double> m_Exponents;
        double m_Offset;
        std::string m_Quantity;
        std::string m_Symbol = "";
        bool m_SymbolAfter;
    };
}}
#endif // UNITS_H
