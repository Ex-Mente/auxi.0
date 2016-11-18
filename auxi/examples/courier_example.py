from datetime import datetime
from dateutil.relativedelta import relativedelta

from auxi.core.time import TimePeriod
from auxi.modelling.business.models import TimeBasedModel
from auxi.modelling.business.basic import BasicActivity, BasicLoanActivity
from auxi.modelling.financial.des import GeneralLedgerStructure
from auxi.core.reporting import ReportFormat

# Create general ledger structure and accounts.
gl_structure = GeneralLedgerStructure("Courier GL Structure")

gl_structure["Long Term Borrowing"].create_account("Loan", "0000")
gl_structure["Expense"].create_account("Interest Expense", "0000")
gl_structure["Fixed Assets"].create_account("Vehicle Asset", "0000")
gl_structure["Sales"].create_account("Sales Delivery", "0000")
gl_structure["Cost of Sales"].create_account("Fuel", "0000")
gl_structure["Expense"].create_account("Wages", "0000")

# Create the business model, entity and components.
start_datetime = datetime(2016, 2, 1)
end_datetime = datetime(2021, 1, 1)

model = TimeBasedModel("Business Model", start_datetime=start_datetime,
                       period_duration=TimePeriod.month, period_count=61)

courier_company = model.create_entity("CourierZA", gl_structure=gl_structure)
ops = courier_company.create_component("Operations")
hr = courier_company.create_component("HR")

# Create activities
loan = BasicLoanActivity("Loan",
    bank_account="Bank/Default", loan_account="Long Term Borrowing/Loan",
    interest_account="Expense/Interest Expense",
    amount=200000, interest_rate=0.15, start=start_datetime, duration=36,
    interval=1)
ops.add_activity(loan)

purchase_vehicle = BasicActivity("Purchase Vehicle",
    dt_account="Fixed Assets/Vehicle Asset", cr_account="Bank/Default",
    amount=177000, start=start_datetime, end=start_datetime + relativedelta(months=1),
    interval=1)
ops.add_activity(purchase_vehicle)

make_delivery_sale = BasicActivity("Make Delivery",
    dt_account="Bank/Default", cr_account="Sales/Sales Delivery",
    amount=15000, start=start_datetime, end=end_datetime, interval=1)
ops.add_activity(make_delivery_sale)

pay_delivery_costs = BasicActivity("Pay for Fuel",
    dt_account="Cost of Sales/Fuel", cr_account="Bank/Default",
    amount=1000, start=start_datetime, end=end_datetime, interval=1)
ops.add_activity(pay_delivery_costs)

pay_wages = BasicActivity("Pay Wages", dt_account="Expense/Wages", cr_account="Bank/Default",
    amount=10000, start=start_datetime, end=end_datetime, interval=1)
hr.add_activity(pay_wages)

# Run the model
model.run()

# Print the reports.
#courier_company.gl.balance_sheet(format=ReportFormat.latex, output_path="balance_sheet.tex")
#courier_company.gl.income_statement(format=ReportFormat.latex, output_path="income_statement.tex")
courier_company.gl.transaction_list(component_path=ops.path)
courier_company.gl.balance_sheet()
courier_company.gl.income_statement(component_path=hr.path)
