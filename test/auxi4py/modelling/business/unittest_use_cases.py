import datetime
#from auxi.modelling.financial.calculation_engines import *
from auxi.modelling.financial.des import *
from auxi.modelling.financial.tax import *
from auxi.modelling.financial.balance_sheet_report import BalanceSheetReport
from auxi.modelling.financial.income_statement_report import IncomeStatementReport
from auxi.modelling.financial.financial_transactions_report import FinancialTransactionsReport
from auxi.modelling.business import *

#TODO: document all classes, methods, properties and fields.
##### TODO ######
### to_string ###
#################

def create_financial_objects():
    """
    Create the calculation engine and general ledger structure for the model.
    """
    #TODO: Give FinancialCalculationEngine contructor a default of None for description.

    #gl_struct = GeneralLedgerStructure("GeneralLedgerStructureA") #fin_ce.create_generalLedgerStructure("GeneralLedgerStructureA")
    gl_struct = GeneralLedgerStructure("GeneralLedgerStructureA",
                                 description="",
                                 json_path="")

    operating_revenues_account = gl_struct.create_account("Operating","031",  AccountType.revenue)
    operating_revenues_account.create_account("FerrochromeSales", "010")

    return gl_struct


def create_model():
    """
    Create and configure the business model.
    """

    #tem = TimeBasedModel("MyTimeBasedModel", "")

    tem = TimeBasedModel("MyTimeBasedModel",
                         description="",
                         start_date=datetime.datetime.strptime("2016-01-01 12:23:44", "%Y-%m-%d %H:%M:%S"),
                         period_duration=TimePeriod.month,
                         period_count=60)
    #TODO: Remove currency property. It must be on business entity.
    #tem.currency.name = "South African Rand"
    #tem.currency.symbol = "ZAR"

    #TODO: replace the term "interval" with "period" throughout.
    #tem.totalIntervalsToRun = 60 #TODO: rename to "interval_count", move property to clock
    #tem.clock.timeStepInterval = TimePeriod.month #TODO: rename to "interval_size"
    #tem.clock.start_date_time = datetime.datetime.strptime("2016-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

    return tem


def configure_business(tem, gl_struct):
    """
    Set up business structure and add activities.
    """

    # configure business
    co = tem.create_entity("SamancorChrome") #TODO: add description with default None
    co.description = "The Samancor Chrome company."
    co.gl.structure = gl_struct #TODO: add this to create_entity

    sales_department = co.create_component("Sales")  #TODO: add description with default None
    sales_department.description = "Sales department."

    # create activities
    tx_template = TransactionTemplate("Sale", description="Sale", debit_account=gl_struct.bank.name, credit_account="FerrochromeSales")
    # datetime.datetime.strptime("2016-04-17 13:37:01", "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime("2017-04-17 13:37:01", "%Y-%m-%d %H:%M:%S"), 1, 1000, tx_template

    ferrochrome_sales = BasicActivity("Sale",
                                      description="Sale of ferrochrome product",
                                      start=datetime.datetime.strptime("2016-04-17 13:37:01", "%Y-%m-%d %H:%M:%S"),
                                      end=datetime.datetime.strptime("2017-04-17 13:37:01", "%Y-%m-%d %H:%M:%S"),
                                      interval=1,
                                      amount=1000,
                                      tx_template=tx_template) #TODO: add description with default None
    #ferrochrome_sales.total_intervals_to_run = 12 #TODO: rename to "interval_count"
    #ferrochrome_sales.execute_interval = 1
    #ferrochrome_sales.executionEndAtInterval = 1
    #ferrochrome_sales.currency.name = "Rand"
    #ferrochrome_sales.currency.symbol = "ZAR"
    #ferrochrome_sales.amount = 1000.0
    #ferrochrome_sales.tx_template.name = "Sale" #TODO: rename to "tx_template"
    #ferrochrome_sales.tx_template.cr_account = "FerrochromeSales" #TODO: account names must have a pathing mechanism
    #ferrochrome_sales.tx_template.dt_account = gl_struct.bank.name #TODO> rename "dt_account_name"
    sales_department.activities.append(ferrochrome_sales)

    return co


def print_reports(co, gl_struct):
    balance_sheet = BalanceSheetReport(co.gl, datetime.datetime.strptime("2017-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
    print(balance_sheet.text()) # TODO: add balance sheet heading
    income_statement = IncomeStatementReport(co.gl, datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime("2018-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
#    print(income_statement.text()) # TODO: add income statement heading

    financial_transactions = FinancialTransactionsReport(co.gl.transactions, datetime.datetime.strptime("2015-02-15 13:37:01", "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime("2017-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
    print(financial_transactions.latex()) # TODO: add heading

    from auxi.modelling.financial.classes_report import GeneralLedgerStructureReport
    gl_struct_report = GeneralLedgerStructureReport(gl_struct)
    print(gl_struct_report.text()) #TODO: fix. it does not show hierarchical structure


gl_struct = create_financial_objects()
tem = create_model()
company = configure_business(tem, gl_struct)
print(tem.entities[0].name, len(tem.entities[0].gl.transactions))
tem.run()
print_reports(company, gl_struct)
