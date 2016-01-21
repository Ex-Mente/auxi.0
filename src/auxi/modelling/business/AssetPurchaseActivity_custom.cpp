#include "AssetPurchaseActivity.h"
#include <cmath>

using namespace auxi::modelling::business;

/*
AssetPurchaseActivity::AssetPurchaseActivity(std::string name, std::string description, int start, int end, int interval) : Activity(name, description, start, end, interval)
{
    initialize();
}
*/
AssetPurchaseActivity::AssetPurchaseActivity(std::string name, std::string description, boost::posix_time::ptime start, boost::posix_time::ptime end, int interval) : Activity(name, description, start, end, interval)
{
    initialize();
}
/*
AssetPurchaseActivity::AssetPurchaseActivity(std::string name, std::string description, boost::posix_time::ptime start, int repeat, int interval) : Activity(name, description, start, repeat, interval)
{
    initialize();
}
*/

void AssetPurchaseActivity::initialize()
{
    m_assetPurchaseTxTemplate.SetName("AssetPruchase");
    m_addDepreciationTxTemplate.SetName("Depreciation");
}


void AssetPurchaseActivity::updatePeriodicDepreciationAmount()
{
    m_periodicDepreciationAmount = (m_purchaseAmount - m_writeOffAmount) / m_monthsTillWrittenOff * m_interval;
}

void AssetPurchaseActivity::SetPurchaseAmount(double value)
{
    m_purchaseAmount = value;
    updatePeriodicDepreciationAmount();
}

void AssetPurchaseActivity::SetMonthsTillWrittenOff(double value)
{
    m_monthsTillWrittenOff = value;
    updatePeriodicDepreciationAmount();
}

bool AssetPurchaseActivity::OnExecute_MeetExecutionCriteria(int ix_period)
{
    return Activity::OnExecute_MeetExecutionCriteria(ix_period) && m_currentAssetValue > m_writeOffAmount;
}

void AssetPurchaseActivity::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    Activity::prepare_to_run(clock, totalIntervalsToRun);

    m_monthsLeft = m_monthsTillWrittenOff;
    m_amountLeft = m_purchaseAmount;
    m_currentAssetValue = m_purchaseAmount;
    updatePeriodicDepreciationAmount();
}

void AssetPurchaseActivity::run(Clock* clock, int ix_period,
                                auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_period)) return;
    // TODO: add purchase on first iteration.
    boost::posix_time::ptime currentExecutionDateTime = clock->GetDateTimeAtPeriodIndex(ix_period);

    if (ix_period == m_startPeriod)
    {
        auto t = generalLedger->create_transaction(
            m_assetPurchaseTxTemplate.GetName(),
            m_assetPurchaseTxTemplate.GetName(),
            m_assetPurchaseTxTemplate.GetCrAccount(),
            m_assetPurchaseTxTemplate.GetDtAccount(),
            path);
        t->SetDate(currentExecutionDateTime);
        t->SetCurrency(m_currency);
        t->SetAmount(std::abs(m_purchaseAmount));
    }
    else
    {
        double depreciationAmount = std::abs(std::min(std::abs(m_periodicDepreciationAmount), m_currentAssetValue - m_writeOffAmount));

        auto t = generalLedger->create_transaction(
            m_addDepreciationTxTemplate.GetName(),
            m_addDepreciationTxTemplate.GetName(),
            m_addDepreciationTxTemplate.GetCrAccount(),
            m_addDepreciationTxTemplate.GetDtAccount(),
            path);
        t->SetDate(currentExecutionDateTime + boost::gregorian::days(-1));
        t->SetCurrency(m_currency);
        t->SetAmount(depreciationAmount);

        m_currentAssetValue -= depreciationAmount;
    }
    m_monthsLeft--;
}




