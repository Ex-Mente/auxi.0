from prettytable import PrettyTable
from auxi.modelling.business import *


def get(transactions, start_date, end_date, currency=""):
    table = PrettyTable(["Date", "Account", "Debit (dr)", "Credit (cr)"])
    table.align["Date"] = "l"
    table.align["Account"] = "l"
    table.align["Debit (dr)"] = "r"
    table.align["Credit (cr)"] = "r"
    table.float_format = ".2"
    amount_tot = 0
    for t in transactions:
        if t.date >= start_date and t.date <= end_date:
            table.add_row([t.date, t.debitAccountName, t.amount, ""])
            if t.creditAccount == "":
                table.add_row(["", "? (Look at Capital Loan's 'Interest' Financial transaction.", "", ""])
            else:
                table.add_row(["", t.creditAccountName, "", t.amount])
            amount_tot += t.amount
    table.add_row(["", "Total (dr)", amount_tot, ""])
    table.add_row(["", "Total (cr)", "", amount_tot])
    table.sort_key("Date")
    return table
