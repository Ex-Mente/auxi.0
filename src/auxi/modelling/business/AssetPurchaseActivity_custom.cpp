#include "AssetPurchaseActivity.h"
#include <cmath>

using namespace auxi::modelling::business;

void AssetPurchaseActivity::initialize()
{
    m_assetPurchaseTransactionTemplate.SetName("AssetPruchase");
    m_addDepreciationTransactionTemplate.SetName("Depreciation");
}


void AssetPurchaseActivity::updatePeriodicDepreciationAmount()
{
    m_periodicDepreciationAmount = (m_purchaseAmount - m_writeOffAmount) / m_monthsTillWrittenOff * m_executeInterval;
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

bool AssetPurchaseActivity::OnExecute_MeetExecutionCriteria(int ix_month)
{
    return Activity::OnExecute_MeetExecutionCriteria(ix_month) && m_currentAssetValue > m_writeOffAmount;
}

void AssetPurchaseActivity::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    Activity::prepare_to_run(clock, totalIntervalsToRun);

    m_monthsLeft = m_monthsTillWrittenOff;
    m_amountLeft = m_purchaseAmount;
    m_currentAssetValue = m_purchaseAmount;
    updatePeriodicDepreciationAmount();
}

void AssetPurchaseActivity::run(Clock* clock, int ix_interval,
                                auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger)
{
    if (!OnExecute_MeetExecutionCriteria(ix_interval)) return;
    // TODO: add purchase on first iteration.
    boost::posix_time::ptime currentExecutionDateTime = clock->GetDateTimeAtInterval(ix_interval);

    if (ix_interval == m_executionStartAtInterval)
    {
        auto t = generalLedger->create_transaction(
            m_assetPurchaseTransactionTemplate.GetName(),
            m_assetPurchaseTransactionTemplate.GetName(),
            m_assetPurchaseTransactionTemplate.GetCreditAccountName(),
            m_assetPurchaseTransactionTemplate.GetDebitAccountName(),
            path);
        t->SetDate(currentExecutionDateTime);
        t->SetCurrency(m_currency);
        t->SetAmount(std::abs(m_purchaseAmount));
    }
    else
    {
        double depreciationAmount = std::abs(std::min(std::abs(m_periodicDepreciationAmount), m_currentAssetValue - m_writeOffAmount));

        auto t = generalLedger->create_transaction(
            m_addDepreciationTransactionTemplate.GetName(),
            m_addDepreciationTransactionTemplate.GetName(),
            m_addDepreciationTransactionTemplate.GetCreditAccountName(),
            m_addDepreciationTransactionTemplate.GetDebitAccountName(),
            path);
        t->SetDate(currentExecutionDateTime + boost::gregorian::days(-1));
        t->SetCurrency(m_currency);
        t->SetAmount(depreciationAmount);

        m_currentAssetValue -= depreciationAmount;
    }
    m_monthsLeft--;
}




