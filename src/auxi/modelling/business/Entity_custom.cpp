#include "Component.h"
#include "Entity.h"
#include "IncomeRule.h"
#include "boost/date_time/gregorian/gregorian.hpp"
#include <map>
#include <algorithm>
#include <typeinfo>
#include <cmath>
#include <iostream>

using namespace auxi::modelling::business;

Component* Entity::create_component(std::string name)
{
    auto component = new Component(name, "");
    component->set_path("");
    m_componentList.push_back(component);
    return component;
}

void Entity::remove_component(std::string name)
{
    for(auto itr = m_componentList.begin(); itr != m_componentList.end(); ++itr)
    {
        if((*itr)->GetName() == name)
        {
           delete (*itr);
           m_componentList.erase(itr);
           return;
        }
    }
    throw std::out_of_range("The component: '" + name + "' does not exist in the entity's component list'.");
}

void Entity::prepare_to_run(Clock* clock, int totalIntervalsToRun)
{
    m_totalIntervalsToRun = totalIntervalsToRun;

    m_execution_end_date = clock->GetDateTimeAtInterval(totalIntervalsToRun);
    m_prev_year_end_date = clock->GetStartDateTime();
    m_curr_year_end_date = clock->GetStartDateTime() + boost::gregorian::years(1);

    auto t_List = m_generalLedger.GetTransactionList();
    for (unsigned int i = 0; i < t_List.size(); i++ )
        delete t_List[i];
    t_List.clear();
    for(auto item: m_componentList)
        item->prepare_to_run(clock, totalIntervalsToRun);
    m_negativeIncomeTaxTotal = 0;
}

double Entity::perform_year_end_procedure_gross_profit(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff)
{
    auto generalLedger_struct = m_generalLedger.GetStructure();
    double grossProfit = 0;
    for(auto iter: grossProfitAccountsToWriteOff)
    {
        auto account_name = iter.first;
        double account_val = iter.second;
        grossProfit += account_val;
        if (account_val > 0)
        {
            std::string transaction_name = "Settle the '" + account_name + "' Account";
            auto t = m_generalLedger.create_transaction(
                transaction_name,
                transaction_name,
                account_name,
                generalLedger_struct->GetGrossProfitAccount()->GetName(),
                "");
            t->SetDate(yearEndDate);
            t->SetCurrency (currency);
            t->SetAmount(std::abs(account_val));
            t->SetIsClosingCreditAccount(true);
        }
        else if (account_val < 0)
        {
            std::string transaction_name = "Settle the '" + account_name + "' Account";
            auto t = m_generalLedger.create_transaction(
                transaction_name,
                transaction_name,
                generalLedger_struct->GetGrossProfitAccount()->GetName(),
                account_name,
                "");
            t->SetDate(yearEndDate);
            t->SetCurrency(currency);
            t->SetAmount(std::abs(account_val));
            t->SetIsClosingCreditAccount(true);
        }
    }
    return grossProfit;
}

double Entity::perform_year_end_procedure_income_summary(boost::posix_time::ptime yearEndDate, Units currency, double grossProfit, std::map<std::string, double> incomeSummaryAccountsToWriteOff)
{
    auto generalLedger_struct = m_generalLedger.GetStructure();
    double incomeSummaryAmount = grossProfit;
    for(auto iter: incomeSummaryAccountsToWriteOff)
    {
        auto account_name = iter.first;
        auto account = generalLedger_struct->get_account(account_name);
        double account_val = iter.second;
        if (account_val > 0)
        {
            std::string credit_acc_name = "";
            std::string debit_acc_name = "";
            if (account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
            {
                incomeSummaryAmount -= account_val;

                credit_acc_name = account_name;
                debit_acc_name = generalLedger_struct->GetIncomeSummaryAccount()->GetName();
            }
            else
            {
                incomeSummaryAmount += account_val;

                credit_acc_name = generalLedger_struct->GetIncomeSummaryAccount()->GetName();
                debit_acc_name = account_name;
            }
            std::string transaction_name = "Settle the '" + account_name + "' Account";
            auto t = m_generalLedger.create_transaction(
                transaction_name,
                transaction_name,
                credit_acc_name,
                debit_acc_name,
                "");
            t->SetDate(yearEndDate);
            t->SetCurrency (currency);
            t->SetAmount(std::abs(account_val));
            t->SetIsClosingCreditAccount(true);

        }
        else if (account_val < 0)
        {
            std::string credit_acc_name = "";
            std::string debit_acc_name = "";
            if (account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
            {
                incomeSummaryAmount += account_val;

                credit_acc_name = generalLedger_struct->GetIncomeSummaryAccount()->GetName();
                debit_acc_name = account_name;
            }
            else
            {
                incomeSummaryAmount -= account_val;

                credit_acc_name = account_name;
                debit_acc_name = generalLedger_struct->GetIncomeSummaryAccount()->GetName();
            }

            std::string transaction_name = "Settle the '" + account_name + "' Account";
            auto t = m_generalLedger.create_transaction(
                transaction_name,
                transaction_name,
                generalLedger_struct->GetGrossProfitAccount()->GetName(),
                account_name,
                "");
            t->SetDate(yearEndDate);
            t->SetCurrency(currency);
            t->SetAmount(std::abs(account_val));
            t->SetIsClosingCreditAccount(true);
        }
    }
    return incomeSummaryAmount;
}

double Entity::perform_year_end_procedure_gross_profit_and_income_summary(boost::posix_time::ptime yearEndDate, Units currency, std::map<std::string, double> grossProfitAccountsToWriteOff, std::map<std::string, double> incomeSummaryAccountsToWriteOff)
{
    auto generalLedger_struct = m_generalLedger.GetStructure();
    double grossProfit = perform_year_end_procedure_gross_profit(yearEndDate, currency, grossProfitAccountsToWriteOff);
    double incomeSummaryAmount = perform_year_end_procedure_income_summary(yearEndDate, currency, grossProfit, incomeSummaryAccountsToWriteOff);

    // Debit the gross profit and credit the income summary account.
    if (grossProfit > 0)
    {
        std::string transaction_name = "Settle the '" + generalLedger_struct->GetGrossProfitAccount()->GetName() + "' Account";
        auto t = m_generalLedger.create_transaction(
            transaction_name,
            transaction_name,
            generalLedger_struct->GetIncomeSummaryAccount()->GetName(),
            generalLedger_struct->GetGrossProfitAccount()->GetName(),
            "");
        t->SetDate(yearEndDate);
        t->SetCurrency(currency);
        t->SetAmount(std::abs(grossProfit));
        t->SetIsClosingCreditAccount(true);
    }
    else if (grossProfit < 0)
    {
        std::string transaction_name = "Settle the '" + generalLedger_struct->GetGrossProfitAccount()->GetName() + "' Account";
        auto t = m_generalLedger.create_transaction(
            transaction_name,
            transaction_name,
            generalLedger_struct->GetGrossProfitAccount()->GetName(),
            generalLedger_struct->GetIncomeSummaryAccount()->GetName(),
            "");
        t->SetDate(yearEndDate);
        t->SetCurrency(currency);
        t->SetAmount(std::abs(grossProfit));
        t->SetIsClosingCreditAccount(true);
    }

    return incomeSummaryAmount;
}

double Entity::perform_year_end_procedure_income_tax(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount)
{
    auto generalLedger_struct = m_generalLedger.GetStructure();
    double taxableIncome = incomeSummaryAmount;
    if (m_taxRuleSet.GetRuleList().size() != 0)
    {
        // Get the income total for the year.
        //taxableIncome = currentExecutionFinancialTransactionList.Where(x => x.GetCreditAccountName() is GeneralLedgerRevenueAccount)
        //    .Sum(x => Units.Convert(x.Amount, x.Currency, currency));
        //taxableIncome -= currentExecutionFinancialTransactionList.Where(x => x.GetDebitAccountName() is GeneralLedgerRevenueAccount)
        //    .Sum(x => Units.Convert(x.Amount, x.Currency, currency));
        //taxableIncome += currentExecutionFinancialTransactionList.Where(x => x.GetCreditAccountName() is GeneralLedgerExpenseAccount)
        //    .Sum(x => Units.Convert(x.Amount, x.Currency, currency));
        //taxableIncome -= currentExecutionFinancialTransactionList.Where(x => x.GetDebitAccountName() is GeneralLedgerExpenseAccount)
        //    .Sum(x => Units.Convert(x.Amount, x.Currency, currency));

        if (m_negativeIncomeTaxTotal < 0)
        {
            m_negativeIncomeTaxTotal += taxableIncome;
            if (m_negativeIncomeTaxTotal > 0)
            {
                taxableIncome = m_negativeIncomeTaxTotal;
                m_negativeIncomeTaxTotal = 0;
            }
            else taxableIncome = 0;
        }
        else m_negativeIncomeTaxTotal = 0;

        // compute the tax
        if (taxableIncome > 0)
        {
            double tax = 0;
            for(auto taxRule: m_taxRuleSet.GetRuleList())
            {
                auto incomeTaxRule = dynamic_cast<auxi::modelling::financial::tax::IncomeRule*>(taxRule);
                if(incomeTaxRule != nullptr) // Perform tax transaction
                {
                    tax = taxableIncome * (incomeTaxRule->GetPercentage() / 100);

                    // CONSIDER THE TAX
                    auto consider_t = m_generalLedger.create_transaction(
                        "Consider Income Tax",
                        "Consider Income Tax",
                        generalLedger_struct->GetIncomeTaxPayableAccount()->GetName(),
                        generalLedger_struct->GetIncomeTaxExpenseAccount()->GetName(),
                        "");
                    consider_t->SetDate(yearEndDate);
                    consider_t->SetCurrency(currency);
                    consider_t->SetAmount(std::abs(tax));
                    // PAY THE TAX
                    auto pay_t = m_generalLedger.create_transaction(
                        "Pay Income Tax",
                        "Pay Income Tax",
                        generalLedger_struct->GetBankAccount()->GetName(),
                        generalLedger_struct->GetIncomeTaxPayableAccount()->GetName(),
                        "");
                    pay_t->SetDate(yearEndDate);
                    pay_t->SetCurrency(currency);
                    pay_t->SetAmount(std::abs(tax));
                    // SETTLE THE INCOME TAX EXPENSE ACCOUNT
                    std::string transaction_name = "Settle the '" + generalLedger_struct->GetIncomeTaxExpenseAccount()->GetName() + "' Account";
                    auto settle_t = m_generalLedger.create_transaction(
                        transaction_name,
                        transaction_name,
                        generalLedger_struct->GetIncomeTaxExpenseAccount()->GetName(),
                        generalLedger_struct->GetIncomeSummaryAccount()->GetName(),
                        "");
                    settle_t->SetDate(yearEndDate);
                    settle_t->SetCurrency(currency);
                    settle_t->SetAmount(std::abs(tax));

                    incomeSummaryAmount -= tax;
                    break;
                }
            }
        }
    }
    return incomeSummaryAmount;
}

void Entity::perform_year_end_procedure_retained_earnings(boost::posix_time::ptime yearEndDate, Units currency, double incomeSummaryAmount)
{
    auto generalLedger_struct = m_generalLedger.GetStructure();
    if (incomeSummaryAmount > 0)
    {
        std::string transaction_name = "Settle the '" + generalLedger_struct->GetIncomeSummaryAccount()->GetName() + "' Account, adjust Retained Earnings accordingly.";
        auto t = m_generalLedger.create_transaction(
            transaction_name,
            transaction_name,
            generalLedger_struct->GetRetainedEarningsAccount()->GetName(),
            generalLedger_struct->GetIncomeSummaryAccount()->GetName(),
            "");
        t->SetDate(yearEndDate);
        t->SetCurrency(currency);
        t->SetAmount(incomeSummaryAmount);
        t->SetIsClosingCreditAccount(true);
    }
    else if (incomeSummaryAmount < 0)
    {
        std::string transaction_name = "Settle the '" + generalLedger_struct->GetIncomeSummaryAccount()->GetName() + "' Account, adjust Retained Earnings accordingly.";
        auto t = m_generalLedger.create_transaction(
            transaction_name,
            transaction_name,
            generalLedger_struct->GetIncomeSummaryAccount()->GetName(),
            generalLedger_struct->GetRetainedEarningsAccount()->GetName(),
            "");
        t->SetDate(yearEndDate);
        t->SetCurrency(currency);
        t->SetAmount(incomeSummaryAmount);
        t->SetIsClosingCreditAccount(true);
    }
}

void Entity::perform_year_end_procedure(Clock * clock, int ix_interval, Units currency)
{
    if(clock->GetDateTimeAtInterval(ix_interval) >= m_curr_year_end_date || ix_interval+1 == m_totalIntervalsToRun)
    {
        auto generalLedger_struct = m_generalLedger.GetStructure();

        boost::posix_time::ptime yearStartDate = m_prev_year_end_date;
        boost::posix_time::ptime yearEndDate = m_curr_year_end_date + boost::posix_time::seconds(-1);
        //if (ix_interval == 11) yearStartDate = start_dateTime;
        //else if (ix_interval == m_totalMonthsToRun) yearStartDate = yearEndDate + boost::gregorian::months(-((ix_month%12)+1));
        //else yearStartDate = yearEndDate + boost::gregorian::years(-1);
        //yearEndDate += boost::posix_time::seconds(-1);

        m_prev_year_end_date = m_curr_year_end_date;
        m_curr_year_end_date = m_curr_year_end_date + boost::gregorian::years(1);
        if(m_curr_year_end_date > m_execution_end_date)
            m_curr_year_end_date = m_execution_end_date;

        auto grossProfitAccountsToWriteOff = std::map<std::string, double>();
        auto incomeSummaryAccountsToWriteOff = std::map<std::string, double>();
        std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> salesAccounts;
        std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> costOfSalesAccounts;
        salesAccounts = getSalesAccounts(generalLedger_struct->GetSalesAccount());
        costOfSalesAccounts = getCostOfSalesAccounts(generalLedger_struct->GetCostOfSalesAccount());

        // Construct a temporary transaction list containing all of the financial transactions plus the current executions financial transactions inside of the year start and year end date.
        auto tmp = std::vector<auxi::modelling::financial::double_entry_system::Transaction*>();
        for(auto transaction: m_generalLedger.GetTransactionList())
        {
            auto transaction_date = transaction->GetDate();
            if(transaction_date >= yearStartDate && transaction_date <= yearEndDate)
            {
                tmp.push_back(transaction);
            }
        }
        for(auto transaction: tmp)
        {
            std::string credit_account_name = transaction->GetCreditAccountName();
            std::string debit_account_name = transaction->GetDebitAccountName();
            auto credit_account = generalLedger_struct->get_account(credit_account_name);
            auto debit_account = generalLedger_struct->get_account(debit_account_name);

            if(std::find(salesAccounts.begin(), salesAccounts.end(), credit_account) != salesAccounts.end()) {

                if (grossProfitAccountsToWriteOff.count(credit_account_name)>0)
                    grossProfitAccountsToWriteOff[credit_account_name] += transaction->GetAmount();
                else grossProfitAccountsToWriteOff[transaction->GetCreditAccountName()] = transaction->GetAmount();
            }
            else if (std::find(salesAccounts.begin(), salesAccounts.end(), debit_account) != salesAccounts.end())
            {
                if (grossProfitAccountsToWriteOff.count(debit_account_name)>0)
                    grossProfitAccountsToWriteOff[debit_account_name] -= transaction->GetAmount();
                else grossProfitAccountsToWriteOff[debit_account_name] = -transaction->GetAmount();
            }
            else if (std::find(costOfSalesAccounts.begin(), costOfSalesAccounts.end(), debit_account) != costOfSalesAccounts.end())
            {
                if (grossProfitAccountsToWriteOff.count(debit_account_name)>0)
                    grossProfitAccountsToWriteOff[debit_account_name] -= transaction->GetAmount();
                else grossProfitAccountsToWriteOff[debit_account_name] = -transaction->GetAmount();
            }
            else if (std::find(costOfSalesAccounts.begin(), costOfSalesAccounts.end(), credit_account) != costOfSalesAccounts.end())
            {
                if (grossProfitAccountsToWriteOff.count(credit_account_name)>0)
                    grossProfitAccountsToWriteOff[credit_account_name] += transaction->GetAmount();
                else grossProfitAccountsToWriteOff[credit_account_name] = transaction->GetAmount();
            }
            else if(credit_account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Revenue)
            {
                if (incomeSummaryAccountsToWriteOff.count(credit_account_name)>0)
                    incomeSummaryAccountsToWriteOff[credit_account_name] += transaction->GetAmount();
                else incomeSummaryAccountsToWriteOff[credit_account_name] = transaction->GetAmount();
            }
            else if(debit_account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Revenue)
            {
                if (incomeSummaryAccountsToWriteOff.count(debit_account_name)>0)
                    incomeSummaryAccountsToWriteOff[debit_account_name] -= transaction->GetAmount();
                else incomeSummaryAccountsToWriteOff[debit_account_name] = -transaction->GetAmount();
            }
            else if(credit_account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
            {
                if (incomeSummaryAccountsToWriteOff.count(credit_account_name)>0)
                    incomeSummaryAccountsToWriteOff[credit_account_name] -= transaction->GetAmount();
                else incomeSummaryAccountsToWriteOff[credit_account_name] = -transaction->GetAmount();
            }
            else if(debit_account->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
            {
                if (incomeSummaryAccountsToWriteOff.count(debit_account_name)>0)
                    incomeSummaryAccountsToWriteOff[debit_account_name] += transaction->GetAmount();
                else incomeSummaryAccountsToWriteOff[debit_account_name] = transaction->GetAmount();
            }
        }

        double incomeSummaryAmount = perform_year_end_procedure_gross_profit_and_income_summary(yearEndDate, currency, grossProfitAccountsToWriteOff, incomeSummaryAccountsToWriteOff);
        incomeSummaryAmount = perform_year_end_procedure_income_tax(yearEndDate, currency, incomeSummaryAmount);
        perform_year_end_procedure_retained_earnings(yearEndDate, currency, incomeSummaryAmount);
    }
}

void Entity::run(Clock* clock, int ix_interval, Units currency)
{
    if(ix_interval >= m_totalIntervalsToRun) return;
    auto generalLedger_struct = m_generalLedger.GetStructure();
    if(generalLedger_struct == nullptr) return;

    for(auto item: m_componentList) item->run(clock, ix_interval, &m_generalLedger);

    perform_year_end_procedure(clock, ix_interval, currency);
}

std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> Entity::getSalesAccounts(
    auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* currentAccount,
    std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> salesAccounts)
{
    if (currentAccount->GetAccountList().size() == 0)
    {
        if(currentAccount->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Revenue)
            salesAccounts.push_back(currentAccount);
        return salesAccounts;
    }
    for(auto account: currentAccount->GetAccountList())
    {
        for(auto acc_child: getSalesAccounts(account, salesAccounts))
        {
            if(acc_child->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Revenue)
                salesAccounts.push_back(acc_child);
        }
    }
    return salesAccounts;
}

std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> Entity::getCostOfSalesAccounts(
    auxi::modelling::financial::double_entry_system::GeneralLedgerAccount* currentAccount,
    std::vector<auxi::modelling::financial::double_entry_system::GeneralLedgerAccount*> costOfSalesAccounts)
{
    if (currentAccount->GetAccountList().size() == 0)
    {
        if(currentAccount->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
            costOfSalesAccounts.push_back(currentAccount);
        return costOfSalesAccounts;
    }
    for(auto account: currentAccount->GetAccountList())
    {
        for(auto acc_child: getCostOfSalesAccounts(account, costOfSalesAccounts))
        {
            if(acc_child->GetType() == auxi::modelling::financial::double_entry_system::GeneralLedgerAccountType::Expense)
                costOfSalesAccounts.push_back(acc_child);
        }
    }
    return costOfSalesAccounts;
}

