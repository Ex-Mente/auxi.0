#include "CustomPythonModel.h"
#include <boost/python.hpp>

using namespace auxi::py;


//Object::addObjectConstructorToTable<CustomPythonModel> addCustomPythonModelConstructorToObjectTable_;

CustomPythonModel::CustomPythonModel()
{
    //ctor
}

CustomPythonModel::~CustomPythonModel()
{
    //dtor
}

CustomPythonModel::CustomPythonModel(const CustomPythonModel& other)
{
    //copy ctor
    m_pythonExecutionCode = other.m_pythonExecutionCode;
}


void CustomPythonModel::execute_serial()
{/*
    try
    {
        Py_Initialize();
        boost::python::object main_module = boost::python::import("__main__");
        boost::python::object main_namespace = main_module.attr("__dict__");

        main_namespace["model"] = boost::python::ptr(&*this);

        boost::python::object ignored = boost::python::exec(m_pythonExecutionCode.c_str(), main_namespace);
    }
    catch(boost::python::error_already_set)
    {
        PyErr_Print();
    }*/
}

namespace auxi { namespace py
{
    bool operator==(const CustomPythonModel&, const CustomPythonModel&)
    {
        return true;
    }
}}
