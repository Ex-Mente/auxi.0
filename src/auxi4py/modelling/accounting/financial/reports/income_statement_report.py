from prettytable import PrettyTable
from auxi.modelling.business import *


def get(generalLedger, start_date, end_date, currency=""):
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

    table = PrettyTable(["", "Debit", "Credit"])
    table.align[""] = "l"
    table.align["Debit"] = "r"
    table.align["Credit"] = "r"
    table.float_format = ".2"
    table.add_row(["Revenues", "", ""])
    table.add_row(["--------", "", ""])
    for entry in summedIncome:
        table.add_row([entry, summedIncome[entry], ""])
    table.add_row(["", "", "--------"])
    table.add_row(["GROSS REVENUES (including INTEREST income)", "", sum_incomes])
    table.add_row(["", "", "--------"])

    table.add_row(["Expenses", "", ""])
    table.add_row(["--------", "", ""])
    for entry in summedExpenses:
        table.add_row([entry, summedExpenses[entry], ""])
    table.add_row(["", "", "--------"])
    table.add_row(["TOTAL EXPENSES", "", "(%.2f)" % sum_expenses])
    table.add_row(["", "", "--------"])
    if net_income < 0:
        table.add_row(["NET INCOME", "", "(%.2f)" % abs(net_income)])
    else:
        table.add_row(["NET INCOME", "", abs(net_income)])
    return table
