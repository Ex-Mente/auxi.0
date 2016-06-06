#!/usr/bin/env python3
"""
This module provides classes to manage currencies.
"""

from datetime import datetime

from enum import Enum

from auxi.core.helpers import get_date
from auxi.core.reporting import Report as ReportBase

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ReportType(Enum):
    """
    Represents a report type, e.g. balance sheet or income statement.
    """

    balance_sheet = 1,
    income_statement = 2,
    transaction_list = 3,
    cash_flow = 4


class Report(ReportBase):
    """
    Base class for reports.

    :param data_source: The object to report on.
    :param output_path: The path to write the report file to.
    """

    def __init__(self, data_source, output_path=None):
        super(Report, self).__init__(data_source, output_path)


class GeneralLedgerStructure(Report):
    """
    Report on a general ledger structure.

    :param data_source: The object to report on.
    :param output_path: The path to write the report file to.
    """

    def __init__(self, data_source, output_path=None):
        super(GeneralLedgerStructure, self).__init__(data_source, output_path)

    def _gl_accounts_to_table_(self, table, account, prefix=''):
        table.append([account.account_type.name,
                      prefix + account.number,
                      account.name, account.description])
        for acc in sorted(account.accounts, key=lambda a: a.number):
            self._gl_accounts_to_table_(
                table, acc, account.number + '/')

    def _generate_table_(self):
        table = [["Type", "Number", "Name", "Description"]]

        i = [a for a in self.data_source.accounts if a.number.startswith('I')]
        for acc in sorted(i, key=lambda a: a.number):
            self._gl_accounts_to_table_(table, acc)

        b = [a for a in self.data_source.accounts if a.number.startswith('B')]
        for acc in sorted(b, key=lambda a: a.number):
            self._gl_accounts_to_table_(table, acc)
        return table


class TransactionList(Report):
    """
    Report on a list of transactions.

    :param data_source: The object to report on.
    :param end: The start date to generate the report for.
    :param end: The end date to generate the report for.
    :param component_path: The path of the component to filter the report's
      transactions by.
    :param output_path: The path to write the report file to.
    """

    # TODO: Generate transaction for a component at a path only.

    def __init__(self, data_source, start=datetime.min.date(),
                 end=datetime.max.date(), component_path="",
                 output_path=None):
        self.start_date = get_date(start)
        self.end_date = get_date(end)
        self.component_path = component_path
        super(TransactionList, self).__init__(data_source, output_path)

    def _generate_table_(self):
        table = [["Date", "Source", "Tx Name", "Debit Account",
                  "Credit Account", "Amount", "Description"]]
        amount_tot = 0
        tx_list = self.data_source.transactions
        for t in sorted(tx_list, key=lambda v: v.tx_date):
            if not t.source.startswith(self.component_path):
                continue
            if t.tx_date >= self.start_date and \
               t.tx_date <= self.end_date:
                if t.source.endswith(t.name):
                    name = ''
                else:
                    name = t.name
                table.append([t.tx_date, t.source, name,
                              t.dt_account, t.cr_account,
                              "%.2f" % t.amount,
                              "" if t.description is None else t.description])
                amount_tot += t.amount
        table.append(["", "", "Total", "", "", "%.2f" % amount_tot, ""])
        return table


class BalanceSheet(Report):
    """
    Report a balance sheet of a general ledger.

    :param data_source: The object to report on.
    :param end: The end date to generate the report for.
    :param output_path: The path to write the report file to.
    """
    # TODO: Generate transaction for a component at a path only.

    def __init__(self, data_source, end=datetime.max.date(), output_path=None):
        """
        """
        self.end_date = get_date(end)
        super(BalanceSheet, self).__init__(data_source, output_path)

    def _sum_amounts_per_account_(self):
        gls = self.data_source.structure
        summedAssets = {}
        summedLiability = {}
        summedEquity = {}

        for t in self.data_source.transactions:
            if t.tx_date <= self.end_date:
                cr_account_type = gls.get_account(t.cr_account).account_type
                dt_account_type = gls.get_account(t.dt_account).account_type
                if cr_account_type == AccountType.asset:
                    if t.cr_account in summedAssets:
                        summedAssets[t.cr_account] -= t.amount
                    else:
                        summedAssets[t.cr_account] = -t.amount
                elif cr_account_type == AccountType.liability:
                    if t.cr_account in summedLiability:
                        summedLiability[t.cr_account] += t.amount
                    else:
                        summedLiability[t.cr_account] = t.amount
                elif cr_account_type == AccountType.equity:
                    if t.cr_account in summedEquity:
                        summedEquity[t.cr_account] += t.amount
                    else:
                        summedEquity[t.cr_account] = t.amount
                if dt_account_type == AccountType.asset:
                    if t.dt_account in summedAssets:
                        summedAssets[t.dt_account] += t.amount
                    else:
                        summedAssets[t.dt_account] = t.amount
                elif dt_account_type == AccountType.liability:
                    if t.dt_account in summedLiability:
                        summedLiability[t.dt_account] -= t.amount
                    else:
                        summedLiability[t.dt_account] = -t.amount
                elif dt_account_type == AccountType.equity:
                    if t.dt_account in summedEquity:
                        summedEquity[t.dt_account] -= t.amount
                    else:
                        summedEquity[t.dt_account] = -t.amount

        return summedAssets, summedLiability, summedEquity

    def _generate_table_(self):
        table = [["Assets", " ", "Liabilities and Equity", "", "  "]]

        sumAssets, sumLiability, sumEquity = self._sum_amounts_per_account_()

        assets_count = len(sumAssets)
        lia_n_eq_count = len(sumLiability) + len(sumEquity) + 4 + 3

        assets_sum = sum(sumAssets.values())
        liabilities_sum = sum(sumLiability.values())
        equities_sum = sum(sumEquity.values())

        rows = []
        for i in range(0, max(assets_count, lia_n_eq_count)):
            rows.append(["", "", "", "", ""])
        ix = 0
        for entry in sumAssets:
            rows[ix][0] = entry
            rows[ix][1] = "%.2f" % sumAssets[entry]
            ix += 1

        rows[0][2] = "Liabilities"
        rows[1][2] = "-----------"
        ix = 2
        for entry in sumLiability:
            rows[ix][2] = entry
            rows[ix][3] = "%.2f" % sumLiability[entry]
            ix += 1

        rows[ix][2] = "Total liabilities"
        rows[ix][4] = "%.2f" % liabilities_sum
        ix += 1
        rows[ix][2] = "-----------------"
        ix += 1
        rows[ix][2] = "Owners' Equity"
        ix += 1
        rows[ix][2] = "--------------"
        ix += 1
        for entry in sumEquity:
            rows[ix][2] = entry
            rows[ix][3] = "%.2f" % sumEquity[entry]
            ix += 1
        rows[ix][2] = "Total owners' equities"
        rows[ix][4] = "%.2f" % sum(sumEquity.values())

        rows.append(["-----", "--------", "----------------------", "",
                     "--------"])
        rows.append(["Total", "%.2f" % assets_sum, "Total", "",
                     "%.2f" % (liabilities_sum + equities_sum)])

        [table.append(row) for row in rows]

        return table


class IncomeStatement(Report):
    """
    Report an income statement of a general ledger.

    :param data_source: The object to report on.
    :param end: The start date to generate the report for.
    :param end: The end date to generate the report for.
    :param component_path: The path of the component to filter the report's
      transactions by.
    :param output_path: The path to write the report file to.
    """
    # TODO: Generate transaction for a component at a path only.

    def __init__(self, data_source, start=datetime.min.date(),
                 end=datetime.max.date(), component_path="", output_path=None):
        """
        """
        self.start_date = get_date(start)
        self.end_date = get_date(end)
        self.component_path = component_path
        super(IncomeStatement, self).__init__(data_source, output_path)

    def _sum_amounts_per_account_(self):
        gls = self.data_source.structure
        summedIncome = {}
        summedExpenses = {}
        for t in self.data_source.transactions:
            if not t.source.startswith(self.component_path):
                continue
            if t.tx_date >= self.start_date and t.tx_date <= self.end_date:
                cr_account_type = gls.get_account(t.cr_account).account_type
                dt_account_type = gls.get_account(t.dt_account).account_type
                if not t.is_closing_cr_account and \
                   not t.is_closing_dt_account and t.cr_account != "":
                    if cr_account_type == AccountType.revenue:
                        if t.cr_account in summedIncome:
                            summedIncome[t.cr_account] += t.amount
                        else:
                            summedIncome[t.cr_account] = t.amount
                    elif cr_account_type == AccountType.expense:
                        if t.cr_account in summedExpenses:
                            summedExpenses[t.cr_account] -= t.amount
                        else:
                            summedExpenses[t.cr_account] = t.amount
                if not t.is_closing_cr_account and \
                   not t.is_closing_dt_account and t.dt_account != "":
                    if dt_account_type == AccountType.revenue:
                        if t.dt_account in summedIncome:
                            summedIncome[t.dt_account] -= t.amount
                        else:
                            summedIncome[t.dt_account] = t.amount
                    elif dt_account_type == AccountType.expense:
                        if t.dt_account in summedExpenses:
                            summedExpenses[t.dt_account] += t.amount
                        else:
                            summedExpenses[t.dt_account] = t.amount
        return summedIncome, summedExpenses

    def _generate_table_(self):
        summedIncome, summedExpenses = self._sum_amounts_per_account_()

        sum_incomes = sum(summedIncome.values())
        sum_expenses = sum(summedExpenses.values())
        net_income = sum_incomes - sum_expenses

        table = [["", "Debit", "Credit"]]
        table.append(["Revenues", "", ""])
        table.append(["--------", "", ""])
        for entry in summedIncome:
            table.append([entry, "", "%.2f" % summedIncome[entry]])
        table.append(["", "", ""])
        table.append(["Cost of Sales", "", ""])
        table.append(["-------------", "", ""])
        cos_sum = 0
        for entry in summedExpenses:
            if entry.startswith('Cost of Sales'):
                cos_sum += summedExpenses[entry]
                table.append([entry, "%.2f" % summedExpenses[entry], ""])
        table.append(["", "", "--------"])
        table.append(["Gross Revenues (including interest income)",
                     "", "%.2f" % (sum_incomes - cos_sum)])
        table.append(["", "", "--------"])

        table.append(["Expenses", "", ""])
        table.append(["--------", "", ""])
        for entry in summedExpenses:
            if not entry.startswith('Cost of Sales'):
                table.append([entry, "%.2f" % summedExpenses[entry], ""])
        table.append(["", "--------", ""])
        table.append(["Total Expenses", "%.2f" % (sum_expenses - cos_sum), ""])
        table.append(["", "--------", "--------"])
        if net_income < 0:
            table.append(["Net Income", "", "(%.2f)" % abs(net_income)])
        else:
            table.append(["Net Income", "", "%.2f" % abs(net_income)])
        return table


from auxi.modelling.financial.des import AccountType


if __name__ == "__main__":
    import unittest
    from auxi.modelling.reporting import GeneralLedgerStructureUnitTester
    from auxi.modelling.reporting import TransactionListUnitTester
    from auxi.modelling.reporting import BalanceSheetUnitTester
    from auxi.modelling.reporting import IncomeStatementUnitTester
    unittest.main()
