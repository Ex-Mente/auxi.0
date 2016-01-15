#include "CustomPythonActivity.h"
#include <boost/python.hpp>

using namespace auxi::py;

CustomPythonActivity::CustomPythonActivity() : Activity()
{
    //ctor
}

CustomPythonActivity::CustomPythonActivity(const CustomPythonActivity& other) : Activity(other)
{
    //copy ctor
    m_script_file = other.m_script_file;
}

void CustomPythonActivity::prepare_to_run(Clock* clock, int totalMonthsToRun)
{
    Activity::prepare_to_run(clock, totalMonthsToRun);

    const char* attr_name = "prepare_to_run";
    try
    {

        if(PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)(this, clock, totalMonthsToRun);
    }
    catch(boost::python::error_already_set const &)
    {
        PyErr_Print();
        //throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }
}

void CustomPythonActivity::run(Clock* clock, int ix_interval,
                               auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger,
                               auxi::modelling::stock::double_entry_system::StockLedger* stockLedger)
{
    m_clock = clock;
    m_ix_interval = ix_interval;
    m_generalLedger = generalLedger;
    m_stockLedger = stockLedger;

    const char* attr_name = "run";
    try
    {

        if(PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)(this, clock, ix_interval, generalLedger, stockLedger);
    }
    catch(boost::python::error_already_set const &)
    {
        PyErr_Print();
    }
}

void CustomPythonActivity::execute_serial()
{
    try
    {
        Py_Initialize();
        boost::python::object main_module = boost::python::import("__main__");
        boost::python::object main_namespace = main_module.attr("__dict__");

        main_namespace["activity"] = boost::python::ptr(&*this);

        boost::python::object ignored = boost::python::exec_file(m_script_file.c_str(), main_namespace, main_namespace);
    }
    catch(boost::python::error_already_set)
    {
        PyErr_Print();
    }
}

namespace auxi { namespace py
{
    bool operator==(const CustomPythonActivity&, const CustomPythonActivity&)
    {
        return true;
    }
}}
