from tabulate import tabulate
from auxi.modelling.financial.des import *


class GeneralLedgerStructureReport:
    headers = ["Name", "Description", "Number", "Type"]

    def __init__(self, generalLedger_structure):
        self.rows = []
        for acc in generalLedger_structure.accounts:
            self.gl_accounts_to_table("", acc)

    def gl_accounts_to_table(self, prefix, account):
        self.rows.append([prefix + account.name, account.description, account.number, account.type.name])
        for acc in account.accounts:
            self.gl_accounts_to_table("  " + prefix, acc)

    def _generate_report(self, tablefmt):
        return tabulate(self.rows, self.headers, tablefmt=tablefmt, numalign="right", floatfmt=".2f")

    def text(self):
        return self._generate_report("psql")

    def latex(self):
        return self._generate_report("latex")
