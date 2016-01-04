#ifndef CUSTOMPYTHONEXECUTIONINJECTOR_H
#define CUSTOMPYTHONEXECUTIONINJECTOR_H

#include <boost/python.hpp>
#include "ExecutionInjector.h"

namespace auxi { namespace py
{
    using namespace auxi::core;

    class CustomPythonExecutionInjector : public ExecutionInjector
    {
        public:
            CustomPythonExecutionInjector();
            ~CustomPythonExecutionInjector();
            CustomPythonExecutionInjector(const CustomPythonExecutionInjector& other);

            void prepare_to_run();

            void before_run_step(int step_ix);
            void after_run_step(int step_ix);

            void before_run();
            void after_run();

            boost::python::object GetCustom_Python_Object() const { return m_custom_py_object; }
            void SetCustom_Python_Object(boost::python::object value) { m_custom_py_object = value; }
        protected:
        private:
        std::string m_script_file;
        boost::python::object m_custom_py_object;
    };
}}
#endif // CUSTOMPYTHONEXECUTIONINJECTOR_H
