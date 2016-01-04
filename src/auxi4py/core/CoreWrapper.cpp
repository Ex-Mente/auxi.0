/*
    TODO:
    :New
    Used normal pointers to work around this. Shared pointers give this error.
    :Old
    Used a workaround (not a solution): A class wrapper containing a cast method to address the following issue:
     - Inheritance Still not working correctly: Cannot downcast. That is Get a Model object from C++ but I want it as a CustomPythonModel in Python.
        http://stackoverflow.com/questions/18720165/smart-pointer-casting-in-boostpython
        http://www.boost.org/doc/libs/1_56_0/libs/python/doc/v2/class.html#HeldType
        http://code.activestate.com/lists/python-cplusplus-sig/6746/
        http://stackoverflow.com/questions/26354480/boost-python-polymorhpism-down-casting-issue
*/
#ifndef COREWRAPPER_CPP
#define COREWRAPPER_CPP

#include "Object.h"
#include "NamedObject.h"
#include "IndexedNamedObject.h"
#include "VariableGroup.h"
#include "Variable.h"
#include "ScalarVariable.h"
#include "CalculationEngine.h"
#include "Model.h"
#include "ModelingProject.h"
#include "CustomPythonModel.h"
//#include "CustomPythonExecutionInjector.h"
#include "stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>

using namespace auxi::core;
using namespace auxi::py;

//----------------------------------------------------- CLASS WRAPPERS -------------------------------------------------------------//
/*class VariableWrap : public Variable, public boost::python::wrapper<Variable> {
public:
  void ValueString(std::string val) {
    if (boost::python::override ValueString = this->get_override("ValueString"))
      ValueString(val);
    Variable::ValueString(val);
  }
  void default_ValueString(std::string val) {return this->Variable::ValueString(val);}

  void DefaultValueString(std::string val) {
    if (boost::python::override DefaultValueString = this->get_override("DefaultValueString"))
      DefaultValueString(val);
    Variable::DefaultValueString(val);
  }
  void default_DefaultValueString(std::string val) {return this->Variable::DefaultValueString(val);}
};
template<typename ScalarT>
class ScalarVariableWrap : public ScalarVariable<ScalarT> , public boost::python::wrapper<ScalarVariable<ScalarT>> {
public:
    static ScalarVariable<ScalarT>* cast(Variable* const& v) { return std::dynamic_pointer_cast<ScalarVariable<ScalarT>>(v); }
};
class CustomPythonModelWrap : public CustomPythonModel, public boost::python::wrapper<CustomPythonModel> {
public:
    static std::shared_ptr<CustomPythonModel> cast(std::shared_ptr<Model> const& v) { return std::dynamic_pointer_cast<CustomPythonModel>(v); }
};*/

//------------------------------------------------------ PYTHON MODULE -------------------------------------------------------------//

template<class T>
void export_ScalarVariable(std::string name) {

    using namespace boost::python;
    class_<ScalarVariable<T>,ScalarVariable<T>*, bases<Variable>>(name.c_str(), init<>())
        .def(self == self)
        //.def("cast", &ScalarVariableWrap<T>::cast)
        //.staticmethod("cast")
        .add_property("value", &ScalarVariable<T>::GetValue, &ScalarVariable<T>::SetValue)
        .add_property("defaultValue", &ScalarVariable<T>::GetDefaultValue, &ScalarVariable<T>::SetDefaultValue)
    ;

   implicitly_convertible<ScalarVariable<T>*,Variable*>();
}

static long get_usecs(boost::posix_time::time_duration const& d)
{
  static long resolution
    = boost::posix_time::time_duration::ticks_per_second();
  long fracsecs = d.fractional_seconds();
  if (resolution > 1000000)
    return fracsecs / (resolution / 1000000);
  else
    return fracsecs * (1000000 / resolution);
}


/* Convert ptime to/from python */
struct ptime_to_python_datetime
{
    static PyObject* convert(boost::posix_time::ptime const& pt)
    {
        boost::gregorian::date date = pt.date();
        boost::posix_time::time_duration td = pt.time_of_day();
        return PyDateTime_FromDateAndTime((int)date.year(),
					  (int)date.month(),
					  (int)date.day(),
					  td.hours(),
					  td.minutes(),
					  td.seconds(),
					  get_usecs(td));
    }
};


struct ptime_from_python_datetime
{
     ptime_from_python_datetime()
     {
         boost::python::converter::registry::push_back(
             &convertible,
             &construct,
             boost::python::type_id<boost::posix_time::ptime > ());
     }

     static void* convertible(PyObject * obj_ptr)
     {
       if ( ! PyDateTime_Check(obj_ptr))
	 return 0;
       return obj_ptr;
     }

     static void construct(
         PyObject* obj_ptr,
         boost::python::converter::rvalue_from_python_stage1_data * data)
     {
       PyDateTime_DateTime const* pydate
	 = reinterpret_cast<PyDateTime_DateTime*>(obj_ptr);

       // Create date object
       boost::gregorian::date _date(PyDateTime_GET_YEAR(pydate),
				    PyDateTime_GET_MONTH(pydate),
				    PyDateTime_GET_DAY(pydate));

       // Create time duration object
       boost::posix_time::time_duration
	 _duration(PyDateTime_DATE_GET_HOUR(pydate),
		   PyDateTime_DATE_GET_MINUTE(pydate),
		   PyDateTime_DATE_GET_SECOND(pydate),
		   0);
       // Set the usecs value
       _duration += boost::posix_time::microseconds(PyDateTime_DATE_GET_MICROSECOND(pydate));

       // Create posix time object
       void* storage = (
			(boost::python::converter::rvalue_from_python_storage<boost::posix_time::ptime>*)
			data)->storage.bytes;
       new (storage)
	 boost::posix_time::ptime(_date, _duration);
       data->convertible = storage;
     }
};


/* Convert time_duration to/from python */
struct tduration_to_python_delta
{
    static PyObject* convert(boost::posix_time::time_duration d)
    {
      long days = d.hours() / 24;
      if (days < 0)
	days --;
      long seconds = d.total_seconds() - days*(24*3600);
      long usecs = get_usecs(d);
      if (days < 0)
	usecs = 1000000-1 - usecs;
      return PyDelta_FromDSU(days, seconds, usecs);
    }
};


/* Should support the negative values, but not the special boost time
   durations */
struct tduration_from_python_delta
{
     tduration_from_python_delta()
     {
         boost::python::converter::registry::push_back(
             &convertible,
             &construct,
             boost::python::type_id<boost::posix_time::time_duration>());
     }

     static void* convertible(PyObject * obj_ptr)
     {
       if ( ! PyDelta_Check(obj_ptr))
	 return 0;
       return obj_ptr;
     }

     static void construct(
         PyObject* obj_ptr,
         boost::python::converter::rvalue_from_python_stage1_data * data)
     {
       PyDateTime_Delta const* pydelta
	 = reinterpret_cast<PyDateTime_Delta*>(obj_ptr);

       long days = pydelta->days;
       bool is_negative = (days < 0);
       if (is_negative)
	 days = -days;

       // Create time duration object
       boost::posix_time::time_duration
	 duration = boost::posix_time::hours(24)*days
	            + boost::posix_time::seconds(pydelta->seconds)
	            + boost::posix_time::microseconds(pydelta->microseconds);
       if (is_negative)
	 duration = duration.invert_sign();

       void* storage = (
			(boost::python::converter::rvalue_from_python_storage<boost::posix_time::time_duration>*)
			data)->storage.bytes;
       new (storage)
	 boost::posix_time::time_duration(duration);
       data->convertible = storage;
     }
};

BOOST_PYTHON_MODULE(core)
{

    using namespace boost::python;

    // Converters
    PyDateTime_IMPORT;

    ptime_from_python_datetime();
    to_python_converter<const boost::posix_time::ptime,ptime_to_python_datetime>();

    tduration_from_python_delta();
    to_python_converter<const boost::posix_time::time_duration,tduration_to_python_delta>();

    // Set the document generation options
    boost::python::docstring_options local_docstring_options(true, true, false);

    //*****************************************************************************************************************************//
    //** Module Settings
    // map the 'sim' namespace to a sub-module
    // make "from mypackage.Util import <whatever>" work
    //object simModule(handle<>(borrowed(PyImport_AddModule("emsim.sim"))));
    // make "from mypackage import Util" work
    //scope().attr("sim") = simModule;
    // set the current scope to the new sub-module
    //scope sim_scope = simModule;


    //*****************************************************************************************************************************//
    //** Import this sub-modules' classes and enums
    //-----------------------------------------------------------------------------------------------------------------------------
    class_<Object, boost::noncopyable>("Object", no_init)
        .def_readwrite("project", &Object::project)
        //.def("isValid", &Object::IsValid)
        //.def("clone", &Object::Clone, return_value_policy<manage_new_object>())
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<NamedObject, bases<Object>, boost::noncopyable>("NamedObject", init<>())
        .add_property("name", &NamedObject::GetName, &NamedObject::SetName, "The name of the object. This is used to uniquely identify the object in auxi.")
        .add_property("description", &NamedObject::GetDescription, &NamedObject::SetDescription, "A description of the object.")
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<ExecutionObject, bases<NamedObject>, boost::noncopyable>("ExecutionObject", no_init)
        .add_property("name", &ExecutionObject::GetName, &ExecutionObject::SetName, "The name of the object. This is used to uniquely identify the object in auxi.")
        .add_property("description", &ExecutionObject::GetDescription, &ExecutionObject::SetDescription, "A description of the object.")
        .def("execute", &ExecutionObject::execute_serial)
        .def("execute_parallel", &ExecutionObject::execute_parallel)
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<IndexedNamedObject, bases<NamedObject>, boost::noncopyable>("IndexedNamedObject", no_init)
        .add_property("index", &IndexedNamedObject::GetIndex, &IndexedNamedObject::SetIndex, "The index of the object.")
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<Units,Units*, bases<NamedObject>, bases<NamedObject>>("Units", init<>())
        .def(self == self)
        .add_property("symbol", &Units::GetSymbol, &Units::SetSymbol, "The symbol of the unit.")
        .add_property("quantity", &Units::GetQuantity, &Units::SetQuantity, "The quantity the unit represents.")
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<VariableGroup, bases<NamedObject>>("VariableGroup", init<>())
        .def(self == self)
        .add_property("variableGroupList", make_function(&VariableGroup::GetVariableGroupList, return_internal_reference<1>()))
        .add_property("variableList", make_function(&VariableGroup::GetVariableList, return_internal_reference<1>()))
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<Variable,Variable*, bases<NamedObject>, boost::noncopyable>("Variable", init<>())
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    export_ScalarVariable<int>("ScalarVariableInt");
    export_ScalarVariable<float>("ScalarVariableFloat");
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<CalculationEngine,CalculationEngine*, bases<NamedObject>, boost::noncopyable>("CalculationEngine", no_init)
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    class_<Model,Model*, bases<ExecutionObject>, boost::noncopyable>("Model", no_init)
    ;
    //-----------------------------------------------------------------------------------------------------------------------------//
    ;
    class_<ModelingProject,ModelingProject*, bases<NamedObject>>("ModelingProject", init<>())
        .def(self == self)
        .add_property("variableGroupList", make_function(&ModelingProject::GetVariableGroupList, return_internal_reference<1>()))
        .add_property("calculationEngineList", make_function(&ModelingProject::GetCalculationEngineList, return_internal_reference<1>()))
        .add_property("modelList", make_function(&ModelingProject::GetModelList, return_internal_reference<1>()))
    ;
    //-----------------------------------------------------------------------------------------------------------------------------
    int (CustomPythonModel::*GetId)() const = &CustomPythonModel::Id;
    void (CustomPythonModel::*SetId)(int) = &CustomPythonModel::Id;
    std::string (CustomPythonModel::*GetPythonExecutionCode)() const = &CustomPythonModel::PythonExecutionCode;
    void (CustomPythonModel::*SetPythonExecutionCode)(std::string) = &CustomPythonModel::PythonExecutionCode;
    class_<CustomPythonModel, CustomPythonModel*, bases<Model>>("CustomPythonModel")
        .def(self == self)
        .def("test", &CustomPythonModel::test)
        .def("execute", &CustomPythonModel::execute_serial)
        .add_property("id", GetId, SetId)
        .add_property("pythonCode", GetPythonExecutionCode, SetPythonExecutionCode)
    ;

    /*class_<CustomPythonExecutionInjector, CustomPythonExecutionInjector*, bases<ExecutionInjector>>("CustomPythonExecutionInjector")
        .def("prepare_to_run", &CustomPythonExecutionInjector::prepare_to_run)
        .def("before_run_step", &CustomPythonExecutionInjector::before_run_step)
        .def("after_run_step", &CustomPythonExecutionInjector::after_run_step)
        .def("before_run", &CustomPythonExecutionInjector::before_run)
        .def("after_run", &CustomPythonExecutionInjector::after_run)
        .add_property("m_custom_py_object", &CustomPythonExecutionInjector::GetCustom_Python_Object, &CustomPythonExecutionInjector::SetCustom_Python_Object)
    ;*/
    //----------------------------------- PARENT CHAIN DECLARATIONS (CONVERTIBLE DECLARATION) -------------------------------------//
    implicitly_convertible<CustomPythonModel*,Model*>();
    //implicitly_convertible<CustomPythonExecutionInjector*,ExecutionInjector*>();
    //------------------------------------------------------------ LISTS ----------------------------------------------------------//
    class_<std::vector<VariableGroup> >("VariableGroupList_non_pointer")
        .def(vector_indexing_suite<std::vector<VariableGroup> >());
    class_<std::vector<VariableGroup*> >("VariableGroupList")
        .def(vector_indexing_suite<std::vector<VariableGroup*> >());
    class_<std::vector<Variable*> >("VariableList")
        .def(vector_indexing_suite<std::vector<Variable*> >());
    class_<std::vector<CalculationEngine*> >("CalculationEngineList")
        .def(vector_indexing_suite<std::vector<CalculationEngine*> >());
    class_<std::vector<Model*> >("ModelList")
        .def(vector_indexing_suite<std::vector<Model*> >());
    //class_<std::vector<std::shared_ptr<Model>> >("ModelList")
    //    .def(vector_indexing_suite<std::vector<std::shared_ptr<Model>> >())
}

/*
BOOST_PYTHON_MODULE(_sim)
{
    // Set the document generation options
    boost::python::docstring_options local_docstring_options(true, true, false);

    // Export the C++ sim namespace
    export_sim();
}*/
#endif // COREWRAPPER_CPP
