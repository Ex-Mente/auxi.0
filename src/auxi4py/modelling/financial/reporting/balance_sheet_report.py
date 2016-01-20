from auxi.modelling.financial.des import AccountType
from tabulate import tabulate


class BalanceSheetReport:
    headers = ["Assets", " ", "Liabilities and Equity", "", "  "]

    def __init__(self, gl, end_date, currency=""):
        transactions = gl.transactions
        ledger_struct = gl.structure
        summedAssets = {}
        summedLiability = {}
        summedEquity = {}

        for t in transactions:
            if t.date <= end_date:
                cr_account_name = t.cr_account
                db_account_name = t.dt_account
                cr_account_type = ledger_struct.get_account(cr_account_name).type
                db_account_type = ledger_struct.get_account(db_account_name).type
                if cr_account_name != "":
                    if cr_account_type == AccountType.asset:
                        if cr_account_name in summedAssets: summedAssets[cr_account_name] -= t.amount
                        else: summedAssets[cr_account_name] = t.amount
                    elif cr_account_type == AccountType.liability:
                        if cr_account_name in summedLiability: summedLiability[cr_account_name] += t.amount
                        else: summedLiability[cr_account_name] = t.amount
                    elif cr_account_type == AccountType.equity:
                        if cr_account_name in summedEquity: summedEquity[cr_account_name] += t.amount
                        else: summedEquity[cr_account_name] = t.amount
                if db_account_name != "":
                    if db_account_type == AccountType.asset:
                        if db_account_name in summedAssets: summedAssets[db_account_name] += t.amount
                        else: summedAssets[db_account_name] = t.amount
                    if db_account_type == AccountType.liability:
                        if db_account_name in summedLiability: summedLiability[db_account_name] -= t.amount
                        else: summedLiability[db_account_name] = t.amount
                    if db_account_type == AccountType.equity:
                        if db_account_name in summedEquity: summedEquity[db_account_name] -= t.amount
                        else: summedEquity[db_account_name] = t.amount

        assets_count = len(summedAssets)
        lia_n_eq_count = len(summedLiability) + len(summedEquity) + 4 + 3

        assets_sum = sum(summedAssets.values())
        liabilities_sum = sum(summedLiability.values())
        equities_sum = sum(summedEquity.values())

        self.rows = []
        for i in range(0, max(assets_count, lia_n_eq_count)):
            self.rows.append(["", "", "", "", ""])
        ix = 0
        for entry in summedAssets:
            self.rows[ix][0] = entry
            self.rows[ix][1] = summedAssets[entry]
            ix += 1

        self.rows[0][2] = "Liabilities"
        self.rows[1][2] = "-----------"
        ix = 2
        for entry in summedLiability:
            self.rows[ix][2] = entry
            self.rows[ix][3] = summedLiability[entry]
            ix += 1

        self.rows[ix][2] = "Total liabilities"
        self.rows[ix][4] = liabilities_sum
        ix += 1
        self.rows[ix][2] = "-----------------"
        ix += 1
        self.rows[ix][2] = "Owners' Equity"
        ix += 1
        self.rows[ix][2] = "--------------"
        ix += 1
        for entry in summedEquity:
            self.rows[ix][2] = entry
            self.rows[ix][3] = summedEquity[entry]
            ix += 1
        self.rows[ix][2] = "Total owners' equities"
        self.rows[ix][4] = sum(summedEquity.values())

        self.rows.append(["-----", "--------", "----------------------", "", "--------"])
        self.rows.append(["Total", assets_sum, "Total", "", liabilities_sum + equities_sum])

    def _generate_report(self, tablefmt):
        return tabulate(self.rows, self.headers, tablefmt=tablefmt, numalign="right", floatfmt=".2f")

    def text(self):
        return self._generate_report("psql")

    def latex(self):
        return self._generate_report("latex")
