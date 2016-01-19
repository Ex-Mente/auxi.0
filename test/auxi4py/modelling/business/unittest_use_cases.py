import sys
import datetime
from auxi.modelling.financial.calculation_engines import *
from auxi.modelling.financial.des import *
from auxi.modelling.financial.tax import *
from auxi.modelling.financial.balance_sheet_report import BalanceSheetReport
from auxi.modelling.financial.income_statement_report import IncomeStatementReport
from auxi.modelling.financial.financial_transactions_report import FinancialTransactionsReport
from auxi.modelling.business import *
import unittest

test_string_value = "Test"
test_int_value = 3
test_double_value = 5.3
test_datetime_value = datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

#-----------------------------------------------
#//
#//    Entity Unit Test
#//
#-----------------------------------------------
class Test_UseCases(unittest.TestCase):

  def test_use_case_simple_model(self):

    # Set up the financial objects
    calc_eng = FinancialCalculationEngine()
    calc_eng.name = "My_Financial_Calculation_Engine"

    gl_struct = calc_eng.create_generalLedgerStructure("My_general_ledger_structure_a")

    operating_revenues_account = gl_struct.create_account("Operating","031",  GeneralLedgerAccountType.Revenue)
    ferrochrome_sales_account = operating_revenues_account.create_account("FerrochromeSales", "010", GeneralLedgerAccountType.Revenue)

    tem = TimeBasedModel()
    tem.name = "MyTimeBasedModel"
    tem.currency.name = "Rand"
    tem.currency.symbol = "ZAR"
    tem.totalIntervalsToRun = 18


    tem.clock.name = "ClockA"
    tem.clock.timeStepInterval = TimeInterval.Day

    #Set up business structure and add activities
    # Initiate business
    smelter_company = tem.create_entity("FerrochromeSmelterCompany")
    smelter_company.description = "The overall smelter business"
    smelter_company.generalLedger.structure = gl_struct

    # Sales
    sales_department = smelter_company.create_component("SalesDepartment")


    ferrochrome_sales = BasicActivity()
    ferrochrome_sales.name = "Sale"
    ferrochrome_sales.totalIntervalsToRun = 12
    ferrochrome_sales.executeInterval = 1
    ferrochrome_sales.currency.name = "Rand"
    ferrochrome_sales.currency.symbol = "ZAR"
    ferrochrome_sales.amount = 1000.0
    ferrochrome_sales.transactionTemplate.name = "Sale"
    ferrochrome_sales.transactionTemplate.creditAccountName = ferrochrome_sales_account.name
    ferrochrome_sales.transactionTemplate.debitAccountName = gl_struct.bankAccount.name
    sales_department.activityList.append(ferrochrome_sales)

    tem.run()

    balance_sheet = BalanceSheetReport(smelter_company.generalLedger, datetime.datetime.strptime("2017-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
    print(balance_sheet.text())
    income_statement = IncomeStatementReport(smelter_company.generalLedger, datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime("2018-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
    print(income_statement.text())

    financial_transactions = FinancialTransactionsReport(smelter_company.generalLedger.transactionList, datetime.datetime.strptime("2015-02-15 13:37:01", "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime("2017-02-17 13:37:01", "%Y-%m-%d %H:%M:%S"))
    #print(financial_transactions.text())

    from auxi.modelling.financial.classes_report import GeneralLedgerStructureReport
    gl_struct_report = GeneralLedgerStructureReport(gl_struct)
    print(gl_struct_report.text())

    # 12 months' transactions = 12 transaction. + 2 transactions for year end.
    self.assertEqual(len(smelter_company.generalLedger.transactionList), 14)


if __name__ == '__main__':
    unittest.main()
