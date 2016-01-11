#ifndef MODELING_BUSINESS_WRAPPER_CPP
#define MODELING_BUSINESS_WRAPPER_CPP

#include "../../core/stdWrapperCode.h"
#include <boost/python/operators.hpp>
#include <boost/date_time/posix_time/posix_time_types.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <datetime.h>
#include "CustomPythonActivity.h"

using namespace boost::python;

void export_core();

// Export the C++ sim.modelling.stock namespace
void export_auxi_modelling_accounting_stock_StockLedgerAccount();
void export_auxi_modelling_accounting_stock_StockLedgerStructure();
void export_auxi_modelling_accounting_stock_StockTransaction();
void export_auxi_modelling_accounting_stock_StockTransactionTemplate();
void export_auxi_modelling_accounting_stock_StockCalculationEngine();
void export_auxi_modelling_accounting_stock_StockLedger();

// Export the C++ sim.modelling.financial namespace
void export_auxi_modelling_accounting_financial_GeneralLedgerAccount();
void export_auxi_modelling_accounting_financial_GeneralLedgerStructure();
void export_auxi_modelling_accounting_financial_TaxRule();
void export_auxi_modelling_accounting_financial_TaxRuleSet();
void export_auxi_modelling_accounting_financial_IncomeTaxRule();
void export_auxi_modelling_accounting_financial_SalesTaxRule();
void export_auxi_modelling_accounting_financial_CapitalGainsTaxRule();
void export_auxi_modelling_accounting_financial_Transaction();
void export_auxi_modelling_accounting_financial_TransactionTemplate();
void export_auxi_modelling_accounting_financial_FinancialCalculationEngine();
void export_auxi_modelling_accounting_financial_GeneralLedger();

// Export the C++ sim.modelling.business namespace
void export_auxi_modelling_business_Activity();
void export_auxi_modelling_business_Component();
void export_auxi_modelling_business_Entity();
void export_auxi_modelling_business_BasicActivity();
void export_auxi_modelling_business_AssetPurchaseActivity();
void export_auxi_modelling_business_CapitalLoanActivity();
void export_auxi_modelling_business_Clock();
void export_auxi_modelling_business_TimeBasedModel();



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

BOOST_PYTHON_MODULE(business)
{

    using namespace auxi::py;

    // Converters
    PyDateTime_IMPORT;

    ptime_from_python_datetime();
    to_python_converter<const boost::posix_time::ptime,ptime_to_python_datetime>();

    tduration_from_python_delta();
    to_python_converter<const boost::posix_time::time_duration,tduration_to_python_delta>();

    // Set the document generation options
    boost::python::docstring_options local_docstring_options(true, true, false);

    //export_core();

    // Export the C++ auxi.modelling.accounting.stock namespace
    export_auxi_modelling_accounting_stock_StockLedgerAccount();
    export_auxi_modelling_accounting_stock_StockLedgerStructure();
    export_auxi_modelling_accounting_stock_StockTransaction();
    export_auxi_modelling_accounting_stock_StockTransactionTemplate();
    export_auxi_modelling_accounting_stock_StockCalculationEngine();
    export_auxi_modelling_accounting_stock_StockLedger();

    // Export the C++ auxi.modelling.accounting.financial namespace
    export_auxi_modelling_accounting_financial_GeneralLedgerAccount();
    export_auxi_modelling_accounting_financial_GeneralLedgerStructure();
    export_auxi_modelling_accounting_financial_TaxRule();
    export_auxi_modelling_accounting_financial_TaxRuleSet();
    export_auxi_modelling_accounting_financial_IncomeTaxRule();
    export_auxi_modelling_accounting_financial_SalesTaxRule();
    export_auxi_modelling_accounting_financial_CapitalGainsTaxRule();
    export_auxi_modelling_accounting_financial_Transaction();
    export_auxi_modelling_accounting_financial_TransactionTemplate();
    export_auxi_modelling_accounting_financial_FinancialCalculationEngine();
    export_auxi_modelling_accounting_financial_GeneralLedger();

    // Export the C++ auxi.modelling.business namespace
    export_auxi_modelling_business_Activity();
    export_auxi_modelling_business_Component();
    export_auxi_modelling_business_Entity();
    export_auxi_modelling_business_BasicActivity();
    export_auxi_modelling_business_AssetPurchaseActivity();
    export_auxi_modelling_business_CapitalLoanActivity();
    export_auxi_modelling_business_Clock();
    export_auxi_modelling_business_TimeBasedModel();

     //-----------------------------------------------------------------------------------------------------------------------------
    class_<CustomPythonActivity, CustomPythonActivity*, bases<Activity>>("CustomPythonActivity")
        .def("execute", &CustomPythonActivity::execute_serial)
        .add_property("script", &CustomPythonActivity::GetScriptFile, &CustomPythonActivity::SetScriptFile)
        .add_property("start_datetime", &CustomPythonActivity::GetStartDateTime)
        .add_property("ix_interval", &CustomPythonActivity::GetIXInterval)
        .add_property("generalLedger", make_function(&CustomPythonActivity::GetGeneralLedger, return_internal_reference<>()))
        .add_property("custom_python_object", &CustomPythonActivity::GetCustom_Python_Object, &CustomPythonActivity::SetCustom_Python_Object)
    ;
    //----------------------------------- PARENT CHAIN DECLARATIONS (CONVERTIBLE DECLARATION) -------------------------------------//
    implicitly_convertible<CustomPythonActivity*,Activity*>();
}

#endif // MODELING_CHEMAPP_WRAPPER_CPP


