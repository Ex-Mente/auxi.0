from prettytable import PrettyTable
from auxi.modelling.financial.des import GeneralLedgerAccountType
from auxi.modelling.business import *


def get(generalLedger, end_date, currency=""):
    transactions = generalLedger.transactionList
    ledger_struct = generalLedger.structure
    table = PrettyTable(["Assets", " ", "Liabilities and Equity", "", "  "])
    table.align["Assets"] = "l"
    table.align[" "] = "r"
    table.align["Liabilities and Equity"] = "l"
    table.align[""] = "r"
    table.align["  "] = "r"
    table.float_format = ".2"
    summedAssets = {}
    summedLiability = {}
    summedEquity = {}

    for t in transactions:
        if t.date <= end_date:
            cr_account_name = t.creditAccountName
            db_account_name = t.debitAccountName
            cr_account_type = ledger_struct.get_account(cr_account_name).type
            db_account_type = ledger_struct.get_account(db_account_name).type
            if cr_account_name != "":
                if cr_account_type == GeneralLedgerAccountType.Asset:
                    if cr_account_name in summedAssets: summedAssets[cr_account_name] -= t.amount
                    else: summedAssets[cr_account_name] = t.amount
                elif cr_account_type == GeneralLedgerAccountType.Liability:
                    if cr_account_name in summedLiability: summedLiability[cr_account_name] += t.amount
                    else: summedLiability[cr_account_name] = t.amount
                elif cr_account_type == GeneralLedgerAccountType.Equity:
                    if cr_account_name in summedEquity: summedEquity[cr_account_name] += t.amount
                    else: summedEquity[cr_account_name] = t.amount
            if db_account_name != "":
                if db_account_type == GeneralLedgerAccountType.Asset:
                    if db_account_name in summedAssets: summedAssets[db_account_name] += t.amount
                    else: summedAssets[db_account_name] = t.amount
                if db_account_type == GeneralLedgerAccountType.Liability:
                    if db_account_name in summedLiability: summedLiability[db_account_name] -= t.amount
                    else: summedLiability[db_account_name] = t.amount
                if db_account_type == GeneralLedgerAccountType.Equity:
                    if db_account_name in summedEquity: summedEquity[db_account_name] -= t.amount
                    else: summedEquity[db_account_name] = t.amount

    assets_count = len(summedAssets)
    lia_n_eq_count = len(summedLiability) + len(summedEquity) + 4 + 3

    assets_sum = sum(summedAssets.values())
    liabilities_sum = sum(summedLiability.values())
    equities_sum = sum(summedEquity.values())

    rows = []
    for i in range(0, max(assets_count, lia_n_eq_count)):
        rows.append(["", "", "", "", ""])
    ix = 0
    for entry in summedAssets:
        rows[ix][0] = entry
        rows[ix][1] = summedAssets[entry]
        ix += 1

    rows[0][2] = "Liabilities"
    rows[1][2] = "-----------"
    ix = 2
    for entry in summedLiability:
        rows[ix][2] = entry
        rows[ix][3] = summedLiability[entry]
        ix += 1

    rows[ix][2] = "Total liabilities"
    rows[ix][4] = liabilities_sum
    ix += 1
    rows[ix][2] = "-----------------"
    ix += 1
    rows[ix][2] = "Owners' Equity"
    ix += 1
    rows[ix][2] = "--------------"
    ix += 1
    for entry in summedEquity:
        rows[ix][2] = entry
        rows[ix][3] = summedEquity[entry]
        ix += 1
    rows[ix][2] = "Total owners' equities"
    rows[ix][4] = sum(summedEquity.values())

    rows.append(["-----", "--------", "----------------------", "", "--------"])
    rows.append(["Total", assets_sum, "Total", "", liabilities_sum + equities_sum])

    [table.add_row(row) for row in rows]

    return str(table)
