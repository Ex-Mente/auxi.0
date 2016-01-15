#ifndef CUSTOMPYTHONACTIVITY_H
#define CUSTOMPYTHONACTIVITY_H

#include <cmath>
#include "Activity.h"
#include "GeneralLedger.h"
#include "StockLedger.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/python.hpp>

namespace auxi { namespace py
{
    using namespace auxi::modelling::business;

    class CustomPythonActivity : public Activity
    {
    public:
        CustomPythonActivity();
        CustomPythonActivity(const CustomPythonActivity& other);

        friend bool operator==(const CustomPythonActivity& lhs, const CustomPythonActivity& rhs);

        bool IsValid() const { return true; }
        CustomPythonActivity* Clone() const { return new CustomPythonActivity(*this); }

        void prepare_to_run(Clock* clock, int totalIntervalsToRun);
        void run(Clock* clock, int ix_interval,
                 auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger,
                 auxi::modelling::stock::double_entry_system::StockLedger* stockLedger);
        void execute_serial();
        std::string GetScriptFile() const { return m_script_file; }
        void  SetScriptFile(std::string value) { m_script_file = value; }
        boost::posix_time::ptime GetStartDateTime() const { return m_start_dateTime; }
        int GetIXInterval() const { return m_ix_interval; }
        boost::python::object GetCustom_Python_Object() const { return m_custom_py_object; }
        void SetCustom_Python_Object(boost::python::object value) { m_custom_py_object = value; }
        auxi::modelling::financial::double_entry_system::GeneralLedger* GetGeneralLedger() const { return m_generalLedger; }
        auxi::modelling::stock::double_entry_system::StockLedger* GetStockLedger() const { return m_stockLedger; }
    protected:
    private:
    int m_id;
    std::string m_script_file;
    boost::posix_time::ptime m_start_dateTime;
    Clock* m_clock;
    int m_ix_interval;
    auxi::modelling::financial::double_entry_system::GeneralLedger* m_generalLedger;
    auxi::modelling::stock::double_entry_system::StockLedger* m_stockLedger;
    boost::python::object m_custom_py_object;
    };
}}
#endif // CUSTOMPYTHONACTIVITY_H
