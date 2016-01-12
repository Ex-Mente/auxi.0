
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "CapitalLoanActivity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct CapitalLoanActivityWrapper : CapitalLoanActivity, wrapper<CapitalLoanActivity>
{
    
    bool OnExecute_MeetExecutionCriteria(int executionInterval)
    {
        if (override OnExecute_MeetExecutionCriteria = this->get_override("OnExecute_MeetExecutionCriteria"))
            return OnExecute_MeetExecutionCriteria(executionInterval);
        return CapitalLoanActivity::OnExecute_MeetExecutionCriteria(executionInterval);
    }
    bool default_OnExecute_MeetExecutionCriteria(int executionInterval) { return this->CapitalLoanActivity::OnExecute_MeetExecutionCriteria(executionInterval); }
};

void export_auxi_modelling_business_CapitalLoanActivity()
{
  // Python C++ mappings

    //class_<CapitalLoanActivity, CapitalLoanActivity*, bases<Activity>>("CapitalLoanActivity", init<>())
    class_<CapitalLoanActivity, CapitalLoanActivity*, bases<Activity>>("CapitalLoanActivity", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    //.def("onExecute_MeetExecutionCriteria", &CapitalLoanActivity::OnExecute_MeetExecutionCriteria, &CapitalLoanActivityWrapper::default_OnExecute_MeetExecutionCriteria)
    .def("onExecute_MeetExecutionCriteria", &CapitalLoanActivity::OnExecute_MeetExecutionCriteria)
	.def("prepare_to_run", &CapitalLoanActivity::prepare_to_run)
	.def("run", &CapitalLoanActivity::run)
	.add_property("date", &CapitalLoanActivity::GetDate, &CapitalLoanActivity::SetDate)
	.add_property("generalLedgerLiabilityAccount", make_function(&CapitalLoanActivity::GetGeneralLedgerLiabilityAccount, return_internal_reference<>()), &CapitalLoanActivity::SetGeneralLedgerLiabilityAccount)
	.add_property("generalLedgerExpenseAccount", make_function(&CapitalLoanActivity::GetGeneralLedgerExpenseAccount, return_internal_reference<>()), &CapitalLoanActivity::SetGeneralLedgerExpenseAccount)
	.add_property("makeLoanTransactionTemplate", make_function(&CapitalLoanActivity::GetMakeLoanTransactionTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetMakeLoanTransactionTemplate)
	.add_property("considerInterestTransactionTemplate", make_function(&CapitalLoanActivity::GetConsiderInterestTransactionTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetConsiderInterestTransactionTemplate)
	.add_property("payMonthlyLoanAmountTransactionTemplate", make_function(&CapitalLoanActivity::GetPayMonthlyLoanAmountTransactionTemplate, return_internal_reference<>()), &CapitalLoanActivity::SetPayMonthlyLoanAmountTransactionTemplate)
	.add_property("loanAmount", &CapitalLoanActivity::GetLoanAmount, &CapitalLoanActivity::SetLoanAmount)
	.add_property("interestRate", &CapitalLoanActivity::GetInterestRate, &CapitalLoanActivity::SetInterestRate)
	.add_property("periodInMonths", &CapitalLoanActivity::GetPeriodInMonths, &CapitalLoanActivity::SetPeriodInMonths)
	.add_property("amountLeft", &CapitalLoanActivity::GetAmountLeft)
	.add_property("monthsLeft", &CapitalLoanActivity::GetMonthsLeft)
	.add_property("monthlyPayment", &CapitalLoanActivity::GetMonthlyPayment)
	.add_property("currentInterestAmount", &CapitalLoanActivity::GetCurrentInterestAmount)
    ;

    //implicitly_convertible<CapitalLoanActivityWrapper*,CapitalLoanActivity*>();
    implicitly_convertible<CapitalLoanActivity*,Activity*>();
    class_<std::vector<CapitalLoanActivity*>>("CapitalLoanActivityList").def(vector_indexing_suite<std::vector<CapitalLoanActivity*>>());
}