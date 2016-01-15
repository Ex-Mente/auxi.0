#include "AssetPurchaseActivity.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>



using namespace auxi::modelling::business;

AssetPurchaseActivity::AssetPurchaseActivity()
{
    //ctor
    initialize();
}

AssetPurchaseActivity::AssetPurchaseActivity(const AssetPurchaseActivity& other)
{
    m_date = other.m_date;
    m_generalLedgerExpenseAccount = other.m_generalLedgerExpenseAccount;
    m_generalLedgerAssetAccount = other.m_generalLedgerAssetAccount;
    m_assetPurchaseTransactionTemplate = other.m_assetPurchaseTransactionTemplate;
    m_addDepreciationTransactionTemplate = other.m_addDepreciationTransactionTemplate;
    m_purchaseAmount = other.m_purchaseAmount;
    m_writeOffAmount = other.m_writeOffAmount;
    m_monthsTillWrittenOff = other.m_monthsTillWrittenOff;
    m_periodicDepreciationAmount = other.m_periodicDepreciationAmount;
    m_amountLeft = other.m_amountLeft;
    m_monthsLeft = other.m_monthsLeft;
    m_currentAssetValue = other.m_currentAssetValue;
}

AssetPurchaseActivity::~AssetPurchaseActivity()
{

}

boost::posix_time::ptime AssetPurchaseActivity::GetDate() const { return m_date; }
void AssetPurchaseActivity::SetDate(boost::posix_time::ptime value) { m_date = value; }
auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* AssetPurchaseActivity::GetGeneralLedgerExpenseAccount() const { return m_generalLedgerExpenseAccount; }
void AssetPurchaseActivity::SetGeneralLedgerExpenseAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* value) { m_generalLedgerExpenseAccount = value; }
auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* AssetPurchaseActivity::GetGeneralLedgerAssetAccount() const { return m_generalLedgerAssetAccount; }
void AssetPurchaseActivity::SetGeneralLedgerAssetAccount(auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* value) { m_generalLedgerAssetAccount = value; }
auxi::modelling::financial::double_entry_system::TransactionTemplate& AssetPurchaseActivity::GetAssetPurchaseTransactionTemplate() { return m_assetPurchaseTransactionTemplate; }
void AssetPurchaseActivity::SetAssetPurchaseTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& value) { m_assetPurchaseTransactionTemplate = value; }
auxi::modelling::financial::double_entry_system::TransactionTemplate& AssetPurchaseActivity::GetAddDepreciationTransactionTemplate() { return m_addDepreciationTransactionTemplate; }
void AssetPurchaseActivity::SetAddDepreciationTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& value) { m_addDepreciationTransactionTemplate = value; }
double AssetPurchaseActivity::GetPurchaseAmount() const { return m_purchaseAmount; }
double AssetPurchaseActivity::GetWriteOffAmount() const { return m_writeOffAmount; }
void AssetPurchaseActivity::SetWriteOffAmount(double value) { m_writeOffAmount = value; }
double AssetPurchaseActivity::GetMonthsTillWrittenOff() const { return m_monthsTillWrittenOff; }
double AssetPurchaseActivity::GetPeriodicDepreciationAmount() const { return m_periodicDepreciationAmount; }
double AssetPurchaseActivity::GetAmountLeft() const { return m_amountLeft; }
double AssetPurchaseActivity::GetMonthsLeft() const { return m_monthsLeft; }
double AssetPurchaseActivity::GetCurrentAssetValue() const { return m_currentAssetValue; }
void AssetPurchaseActivity::SetCurrentAssetValue(double value) { m_currentAssetValue = value; }


    
    
    
namespace auxi { namespace modelling { namespace business { 
    bool operator==(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs)
    {
        return 1 == 1
	  && lhs.m_date == rhs.m_date
	  && lhs.m_generalLedgerExpenseAccount == rhs.m_generalLedgerExpenseAccount
	  && lhs.m_generalLedgerAssetAccount == rhs.m_generalLedgerAssetAccount
	  && lhs.m_assetPurchaseTransactionTemplate == rhs.m_assetPurchaseTransactionTemplate
	  && lhs.m_addDepreciationTransactionTemplate == rhs.m_addDepreciationTransactionTemplate
	  && almost_equal(lhs.m_purchaseAmount, rhs.m_purchaseAmount, 5)
	  && almost_equal(lhs.m_writeOffAmount, rhs.m_writeOffAmount, 5)
	  && almost_equal(lhs.m_monthsTillWrittenOff, rhs.m_monthsTillWrittenOff, 5)
	  && almost_equal(lhs.m_periodicDepreciationAmount, rhs.m_periodicDepreciationAmount, 5)
	  && almost_equal(lhs.m_amountLeft, rhs.m_amountLeft, 5)
	  && almost_equal(lhs.m_monthsLeft, rhs.m_monthsLeft, 5)
	  && almost_equal(lhs.m_currentAssetValue, rhs.m_currentAssetValue, 5)
	  ;
    }

    bool operator!=(const AssetPurchaseActivity& lhs, const AssetPurchaseActivity& rhs)
    {
        return 1 != 1
	  || lhs.m_date != rhs.m_date
	  || lhs.m_generalLedgerExpenseAccount != rhs.m_generalLedgerExpenseAccount
	  || lhs.m_generalLedgerAssetAccount != rhs.m_generalLedgerAssetAccount
	  || lhs.m_assetPurchaseTransactionTemplate != rhs.m_assetPurchaseTransactionTemplate
	  || lhs.m_addDepreciationTransactionTemplate != rhs.m_addDepreciationTransactionTemplate
	  || !almost_equal(lhs.m_purchaseAmount, rhs.m_purchaseAmount, 5)
	  || !almost_equal(lhs.m_writeOffAmount, rhs.m_writeOffAmount, 5)
	  || !almost_equal(lhs.m_monthsTillWrittenOff, rhs.m_monthsTillWrittenOff, 5)
	  || !almost_equal(lhs.m_periodicDepreciationAmount, rhs.m_periodicDepreciationAmount, 5)
	  || !almost_equal(lhs.m_amountLeft, rhs.m_amountLeft, 5)
	  || !almost_equal(lhs.m_monthsLeft, rhs.m_monthsLeft, 5)
	  || !almost_equal(lhs.m_currentAssetValue, rhs.m_currentAssetValue, 5)
	;
    }

    std::ostream& operator<<(std::ostream& os, const AssetPurchaseActivity& obj)
    {

        os << obj.GetName();
        return os;
    }
}
}
}
