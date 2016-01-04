#ifndef CUSTOMPYTHONMODEL_H
#define CUSTOMPYTHONMODEL_H

#include <cmath>
#include "Model.h"

namespace auxi { namespace py
{
    using namespace auxi::core;

    class CustomPythonModel : public Model
    {
        public:
            //static std::string type() { return "CustomPythonModel"; }; // Rather use type_id?

            CustomPythonModel();
            CustomPythonModel(int id) : m_id(id) {};
            ~CustomPythonModel();
            CustomPythonModel(const CustomPythonModel& other);

            friend bool operator==(const CustomPythonModel& lhs, const CustomPythonModel& rhs);

            bool IsValid() const { return true; }
            CustomPythonModel* Clone() const { return new CustomPythonModel(*this); }

            char const* test() { return "Yeah!!!"; }
            void execute_serial();
            int Id() const { return m_id; }
            void Id(int id) { m_id = id; }
            std::string PythonExecutionCode() const { return m_pythonExecutionCode; }
            void  PythonExecutionCode(std::string pythonExecutionCode) { m_pythonExecutionCode = pythonExecutionCode; }
        protected:
        private:
        int m_id;
        std::string m_pythonExecutionCode;
    };
}}
#endif // CUSTOMPYTHONMODEL_H
