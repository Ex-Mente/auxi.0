
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "CapitalLoanActivity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

// Converts a C++ vector to a python list
template <class T>
boost::python::list to_python_list(std::vector<T> vector) {
    typename std::vector<T>::iterator iter;
    boost::python::list list;
    for (iter = vector.begin(); iter != vector.end(); ++iter) {
        list.append(*iter);
    }
    return list;
}






struct CapitalLoanActivityWrapper : CapitalLoanActivity, wrapper<CapitalLoanActivity>
{
};

void export_auxi_modelling_business_CapitalLoanActivity()
{
  // Python C++ mappings



    class_<CapitalLoanActivityWrapper, CapitalLoanActivity*, bases<Activity>>("CapitalLoanActivity", """", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
    
	.def("onExecute_MeetExecutionCriteria", &CapitalLoanActivity::OnExecute_MeetExecutionCriteria, "")
    
	.def("prepare_to_run", &CapitalLoanActivity::prepare_to_run, "")
    
	.def("run", &CapitalLoanActivity::run, "")

	.add_property("date", &CapitalLoanActivity::GetDate, &CapitalLoanActivity::SetDate, """")

	.add_property("general_ledger_liability_account", make_function(&CapitalLoanActivity::GetGeneralLedgerLiabilityAccount, return_internal_reference<>()), &CapitalLoanActivity::SetGeneralLedgerLiabilityAccount, """")

	.add_property("general_ledger_expense_account", make_function(&CapitalLoanActivity::GetGeneralLedgerExpenseAccount, return_internal_reference<>()), &CapitalLoanActivity::SetGeneralLedgerExpenseAccount, """")

	.add_property("make_loan_tx_template", make_function(&CapitalLoanActivity::GetMakeLoanTxTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetMakeLoanTxTemplate, """")

	.add_property("consider_interest_tx_template", make_function(&CapitalLoanActivity::GetConsiderInterestTxTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetConsiderInterestTxTemplate, """")

	.add_property("pay_monthly_loan_amount_tx_template", make_function(&CapitalLoanActivity::GetPayMonthlyLoanAmountTxTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetPayMonthlyLoanAmountTxTemplate, """")

	.add_property("loan_amount", &CapitalLoanActivity::GetLoanAmount, &CapitalLoanActivity::SetLoanAmount, """")

	.add_property("interest_rate", &CapitalLoanActivity::GetInterestRate, &CapitalLoanActivity::SetInterestRate, """")

	.add_property("period_in_months", &CapitalLoanActivity::GetPeriodInMonths, &CapitalLoanActivity::SetPeriodInMonths, """")

	.add_property("amount_left", &CapitalLoanActivity::GetAmountLeft, """")

	.add_property("months_left", &CapitalLoanActivity::GetMonthsLeft, """")

	.add_property("monthly_payment", &CapitalLoanActivity::GetMonthlyPayment, """")

	.add_property("current_interest_amount", &CapitalLoanActivity::GetCurrentInterestAmount, """")
    ;

    //implicitly_convertible<CapitalLoanActivityWrapper*,CapitalLoanActivity*>();
    implicitly_convertible<CapitalLoanActivity*,Activity*>();
    class_<std::vector<CapitalLoanActivity*>>("CapitalLoanActivityList").def(vector_indexing_suite<std::vector<CapitalLoanActivity*>>());
}