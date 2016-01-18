from tabulate import tabulate
from auxi.modelling.financial.des import *


class IncomeStatementReport:
    headers = ["", "Debit", "Credit"]

    def __init__(self, generalLedger, start_date, end_date, currency=""):
        transactions = generalLedger.transactionList
        ledger_struct = generalLedger.structure
        summedIncome = {}
        summedExpenses = {}
        for t in transactions:
            if t.date >= start_date and t.date <= end_date:
                cr_account_name = t.creditAccountName
                db_account_name = t.debitAccountName
                cr_account_type = ledger_struct.get_account(cr_account_name).type
                db_account_type = ledger_struct.get_account(db_account_name).type
                if not t.isClosingCreditAccount and not t.isClosingDebitAccount and cr_account_name != "":
                    if cr_account_type == GeneralLedgerAccountType.Revenue:
                        if cr_account_name in summedIncome: summedIncome[cr_account_name] += t.amount
                        else: summedIncome[cr_account_name] = t.amount
                    elif cr_account_type == GeneralLedgerAccountType.Expense:
                        if cr_account_name in summedExpenses: summedExpenses[cr_account_name] -= t.amount
                        else: summedExpenses[cr_account_name] = t.amount
                if not t.isClosingCreditAccount and not t.isClosingDebitAccount and db_account_name != "":
                    if db_account_type == GeneralLedgerAccountType.Revenue:
                        if db_account_name in summedIncome: summedIncome[db_account_name] -= t.amount
                        else: summedIncome[db_account_name] = t.amount
                    elif db_account_type == GeneralLedgerAccountType.Expense:
                        if db_account_name in summedExpenses: summedExpenses[db_account_name] += t.amount
                        else: summedExpenses[db_account_name] = t.amount

        sum_incomes = sum(summedIncome.values())
        sum_expenses = sum(summedExpenses.values())
        net_income = sum_incomes - sum_expenses

        self.rows = []
        self.rows.append(["Revenues", "", ""])
        self.rows.append(["--------", "", ""])
        for entry in summedIncome:
            self.rows.append([entry, summedIncome[entry], ""])
        self.rows.append(["", "", "--------"])
        self.rows.append(["GROSS REVENUES (including INTEREST income)", "", sum_incomes])
        self.rows.append(["", "", "--------"])

        self.rows.append(["Expenses", "", ""])
        self.rows.append(["--------", "", ""])
        for entry in summedExpenses:
            self.rows.append([entry, summedExpenses[entry], ""])
        self.rows.append(["", "", "--------"])
        self.rows.append(["TOTAL EXPENSES", "", "(%.2f)" % sum_expenses])
        self.rows.append(["", "", "--------"])
        if net_income < 0:
            self.rows.append(["NET INCOME", "", "(%.2f)" % abs(net_income)])
        else:
            self.rows.append(["NET INCOME", "", abs(net_income)])

    def _generate_report(self, tablefmt):
        return tabulate(self.rows, self.headers, tablefmt=tablefmt, numalign="right", floatfmt=".2f")

    def text(self):
        return self._generate_report("psql")

    def latex(self):
        return self._generate_report("latex")
