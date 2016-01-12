from prettytable import PrettyTable
from auxi.modelling.business import *


def gl_accounts_to_table(table, prefix, account):
    table.add_row([prefix + account.name, account.description, account.accountNumber, account.type.name])
    for acc in account.generalLedgerAccountList:
        gl_accounts_to_table(table, "  " + prefix, acc)


def generalLedger_structure_to_string(generalLedger_structure):
    table = PrettyTable(["Name", "Description", "Number", "Type"])
    table.align = 'l'
    for acc in generalLedger_structure.generalLedgerAccountList:
        gl_accounts_to_table(table, "", acc)
    return table
