#include "CustomPythonExecutionInjector.h"

using namespace auxi::py;

CustomPythonExecutionInjector::CustomPythonExecutionInjector()
{
    //ctor
}

CustomPythonExecutionInjector::~CustomPythonExecutionInjector()
{
    //dtor
}

CustomPythonExecutionInjector::CustomPythonExecutionInjector(const CustomPythonExecutionInjector& other)
{
    //copy ctor
}

void CustomPythonExecutionInjector::prepare_to_run()
{
    const char* attr_name = "prepare_to_run";
    try
    {
        if(!PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)();
    }
    catch(boost::python::error_already_set const &)
    {
        throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }

}

void CustomPythonExecutionInjector::before_run_step(int ix_step)
{
    const char* attr_name = "before_run_step";
    try
    {
        if(!PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)(ix_step);
    }
    catch(boost::python::error_already_set const &)
    {
        throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }
}

void CustomPythonExecutionInjector::after_run_step(int ix_step)
{
    const char* attr_name = "after_run_step";
    try
    {
        if(PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)(ix_step);
    }
    catch(boost::python::error_already_set const &)
    {
        throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }
}

void CustomPythonExecutionInjector::before_run()
{
    const char* attr_name = "before_run";
    try
    {
        if(!PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)();
    }
    catch(boost::python::error_already_set const &)
    {
        throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }
}

void CustomPythonExecutionInjector::after_run()
{
    const char* attr_name = "after_run";
    try
    {
        if(!PyObject_HasAttrString(m_custom_py_object.ptr(), attr_name))
            m_custom_py_object.attr(attr_name)();
    }
    catch(boost::python::error_already_set const &)
    {
        throw std::invalid_argument(std::string("The method: '") + attr_name + std::string("' threw an exception'."));
    }
}
