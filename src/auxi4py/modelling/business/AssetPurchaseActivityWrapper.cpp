
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "TransactionTemplate.h"
#include "Clock.h"
#include "AssetPurchaseActivity.h"

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






struct AssetPurchaseActivityWrapper : AssetPurchaseActivity, wrapper<AssetPurchaseActivity>
{
};

void export_auxi_modelling_business_AssetPurchaseActivity()
{
  // Python C++ mappings



    class_<AssetPurchaseActivityWrapper, AssetPurchaseActivity*, bases<Activity>>("AssetPurchaseActivity", """", init<std::string, optional<std::string, boost::posix_time::ptime, boost::posix_time::ptime, int> >())
	.def(self == self)


    //.def(init<std::string, optional<std::string, int, int, int> >())


    //.def(init<std::string, optional<std::string, boost::posix_time::ptime, boost::posix_time::ptime, int> >())


    //.def(init<std::string, optional<std::string, boost::posix_time::ptime, int, int> >())


	.def("onExecute_MeetExecutionCriteria", &AssetPurchaseActivity::OnExecute_MeetExecutionCriteria, "")

	.def("prepare_to_run", &AssetPurchaseActivity::prepare_to_run, "")

	.def("run", &AssetPurchaseActivity::run, "")


	.add_property("date", &AssetPurchaseActivity::GetDate, &AssetPurchaseActivity::SetDate, """")

	.add_property("general_ledger_expense_account", make_function(&AssetPurchaseActivity::GetGeneralLedgerExpenseAccount, return_internal_reference<>()), &AssetPurchaseActivity::SetGeneralLedgerExpenseAccount, """")

	.add_property("general_ledger_asset_account", make_function(&AssetPurchaseActivity::GetGeneralLedgerAssetAccount, return_internal_reference<>()), &AssetPurchaseActivity::SetGeneralLedgerAssetAccount, """")

	.add_property("asset_purchase_tx_template", make_function(&AssetPurchaseActivity::GetAssetPurchaseTxTemplate, return_internal_reference<>()), &AssetPurchaseActivity::SetAssetPurchaseTxTemplate, """")

	.add_property("add_depreciation_tx_template", make_function(&AssetPurchaseActivity::GetAddDepreciationTxTemplate, return_internal_reference<>()), &AssetPurchaseActivity::SetAddDepreciationTxTemplate, """")

	.add_property("purchase_amount", &AssetPurchaseActivity::GetPurchaseAmount, &AssetPurchaseActivity::SetPurchaseAmount, """")

	.add_property("write_off_amount", &AssetPurchaseActivity::GetWriteOffAmount, &AssetPurchaseActivity::SetWriteOffAmount, """")

	.add_property("months_till_written_off", &AssetPurchaseActivity::GetMonthsTillWrittenOff, &AssetPurchaseActivity::SetMonthsTillWrittenOff, """")

	.add_property("periodic_depreciation_amount", &AssetPurchaseActivity::GetPeriodicDepreciationAmount, """")

	.add_property("amount_left", &AssetPurchaseActivity::GetAmountLeft, """")

	.add_property("months_left", &AssetPurchaseActivity::GetMonthsLeft, """")

	.add_property("current_asset_value", &AssetPurchaseActivity::GetCurrentAssetValue, &AssetPurchaseActivity::SetCurrentAssetValue, """")
    ;

    //implicitly_convertible<AssetPurchaseActivityWrapper*,AssetPurchaseActivity*>();
    implicitly_convertible<AssetPurchaseActivity*,Activity*>();
    class_<std::vector<AssetPurchaseActivity*>>("AssetPurchaseActivityList").def(vector_indexing_suite<std::vector<AssetPurchaseActivity*>>());
}