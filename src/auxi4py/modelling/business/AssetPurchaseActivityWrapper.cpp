
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "AssetPurchaseActivity.h"

using namespace boost::python;
using namespace auxi::modelling::business;

struct AssetPurchaseActivityWrapper : AssetPurchaseActivity, wrapper<AssetPurchaseActivity>
{
    
    bool OnExecute_MeetExecutionCriteria(int executionIntervals)
    {
        if (override OnExecute_MeetExecutionCriteria = this->get_override("OnExecute_MeetExecutionCriteria"))
            return OnExecute_MeetExecutionCriteria(executionIntervals);
        return AssetPurchaseActivity::OnExecute_MeetExecutionCriteria(executionIntervals);
    }
    bool default_OnExecute_MeetExecutionCriteria(int executionIntervals) { return this->AssetPurchaseActivity::OnExecute_MeetExecutionCriteria(executionIntervals); }
};

void export_auxi_modelling_business_AssetPurchaseActivity()
{
  // Python C++ mappings

    //class_<AssetPurchaseActivity, AssetPurchaseActivity*, bases<Activity>>("AssetPurchaseActivity", init<>())
    class_<AssetPurchaseActivity, AssetPurchaseActivity*, bases<Activity>>("AssetPurchaseActivity", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    //.def("onExecute_MeetExecutionCriteria", &AssetPurchaseActivity::OnExecute_MeetExecutionCriteria, &AssetPurchaseActivityWrapper::default_OnExecute_MeetExecutionCriteria)
    .def("onExecute_MeetExecutionCriteria", &AssetPurchaseActivity::OnExecute_MeetExecutionCriteria)
	.def("prepare_to_run", &AssetPurchaseActivity::prepare_to_run)
	.def("run", &AssetPurchaseActivity::run)
	.add_property("date", &AssetPurchaseActivity::GetDate, &AssetPurchaseActivity::SetDate)
	.add_property("generalLedgerExpenseAccount", make_function(&AssetPurchaseActivity::GetGeneralLedgerExpenseAccount, return_internal_reference<>()), &AssetPurchaseActivity::SetGeneralLedgerExpenseAccount)
	.add_property("generalLedgerAssetAccount", make_function(&AssetPurchaseActivity::GetGeneralLedgerAssetAccount, return_internal_reference<>()), &AssetPurchaseActivity::SetGeneralLedgerAssetAccount)
	.add_property("assetPurchaseTransactionTemplate", make_function(&AssetPurchaseActivity::GetAssetPurchaseTransactionTemplate, return_internal_reference<>()), &AssetPurchaseActivity::SetAssetPurchaseTransactionTemplate)
	.add_property("addDepreciationTransactionTemplate", make_function(&AssetPurchaseActivity::GetAddDepreciationTransactionTemplate, return_internal_reference<>()), &AssetPurchaseActivity::SetAddDepreciationTransactionTemplate)
	.add_property("purchaseAmount", &AssetPurchaseActivity::GetPurchaseAmount, &AssetPurchaseActivity::SetPurchaseAmount)
	.add_property("writeOffAmount", &AssetPurchaseActivity::GetWriteOffAmount, &AssetPurchaseActivity::SetWriteOffAmount)
	.add_property("monthsTillWrittenOff", &AssetPurchaseActivity::GetMonthsTillWrittenOff, &AssetPurchaseActivity::SetMonthsTillWrittenOff)
	.add_property("periodicDepreciationAmount", &AssetPurchaseActivity::GetPeriodicDepreciationAmount)
	.add_property("amountLeft", &AssetPurchaseActivity::GetAmountLeft)
	.add_property("monthsLeft", &AssetPurchaseActivity::GetMonthsLeft)
	.add_property("currentAssetValue", &AssetPurchaseActivity::GetCurrentAssetValue, &AssetPurchaseActivity::SetCurrentAssetValue)
    ;

    //implicitly_convertible<AssetPurchaseActivityWrapper*,AssetPurchaseActivity*>();
    implicitly_convertible<AssetPurchaseActivity*,Activity*>();
    class_<std::vector<AssetPurchaseActivity*>>("AssetPurchaseActivityList").def(vector_indexing_suite<std::vector<AssetPurchaseActivity*>>());
}