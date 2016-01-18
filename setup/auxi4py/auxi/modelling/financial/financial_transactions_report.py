from tabulate import tabulate
from auxi.modelling.financial.des import *


class FinancialTransactionsReport:
    headers = ["Date", "Account", "Debit (dr)", "Credit (cr)"]

    def __init__(self, transactions, start_date, end_date, currency=""):
        self.rows = []
        amount_tot = 0
        for t in transactions:
            if t.date >= start_date and t.date <= end_date:
                self.rows.append([t.date, t.debitAccountName, t.amount, ""])
                if t.creditAccountName == "":
                    self.rows.append(["", "? (Look at Capital Loan's 'Interest' Financial transaction.)", "", ""])
                else:
                    self.rows.append(["", t.creditAccountName, "", t.amount])
                amount_tot += t.amount
        self.rows.append(["", "Total (dr)", amount_tot, ""])
        self.rows.append(["", "Total (cr)", "", amount_tot])

    def _generate_report(self, tablefmt):
        return tabulate(self.rows, self.headers, tablefmt=tablefmt, numalign="right", floatfmt=".2f")

    def text(self):
        return self._generate_report("psql")

    def latex(self):
        return self._generate_report("latex")
