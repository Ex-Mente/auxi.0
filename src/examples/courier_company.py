
from datetime import datetime

from auxi.core.time import TimePeriod
from auxi.modelling.business.models import TimeBasedModel
from auxi.modelling.business.basic import BasicActivity
from auxi.modelling.financial.des import GeneralLedgerStructure

print("\033[32mStart.\033[38m")
print()
print("\033[33mConfigure the model\033[38m")
print()

# -----------------------------------------------------------------------------
# Set up the financial objects
# -----------------------------------------------------------------------------
gl_structure = GeneralLedgerStructure(
    "Courier GL Structure",
    description="Courier General Ledger Structure")

# -----------------------------------------------------------------------------
# Accounts

# Vehicle
vehicle_asset_acc = gl_structure["Fixed Assets"].create_account(
    "Vehicle Asset",
    "0000")
vehicle_loan_acc = gl_structure["Long Term Borrowing"].create_account(
    "Vehicle Loan",
    "0000")
vehicle_maintenance_acc = gl_structure["Expense"].create_account(
    "Vehicle Maintenace",
    number="0000")

# Sales operations
sales_acc = gl_structure["Sales"].create_account(
    "Sales Delivery",
    "0000")
cos_acc = gl_structure["Cost of Sales"].create_account(
    "Cos Delivery",
    "0000")

# Wages
vehicle_maintenance_acc = gl_structure["Expense"].create_account(
    "Wages",
    number="0000")


# -----------------------------------------------------------------------------
# Set up the business objects
# -----------------------------------------------------------------------------

start_datetime = datetime(2016, 2, 1)
end_datetime = datetime(2021, 2, 1)

# Create the model.
model = TimeBasedModel(
    "Business Model",
    description="The business model.",
    start_datetime=start_datetime,
    period_duration=TimePeriod.month,
    period_count=60)

# Create the entity (organisation).
courier_company = model.create_entity(
    "CourierZA",
    gl_structure=gl_structure,
    description="Courier company in South Africa")

# Create the different business components.
ops = courier_company.create_component(
    "Operations",
    description="General business operations")
hr = courier_company.create_component(
    "HR",
    description="Human Resources")


# -----------------------------------------------------------------------------
# Activities

# Vehicle purchase activity
purchase_vehicle = BasicActivity(
    "Purchase Vehicle",
    description="Purchase a vehicle on a Loan",
    dt_account="Fixed Assets/Vehicle Asset",
    cr_account="Bank/Default",
    amount=20000,
    start=start_datetime,
    end=end_datetime,
    interval=1)
ops.add_activity(purchase_vehicle)
# Vehicle Loan activity
pay_vehicle_loan = BasicActivity(
    "Pay vehicle loan",
    description="Pay the vehicle loan",
    dt_account="Long Term Borrowing/Vehicle Loan",
    cr_account="Bank/Default",
    amount=2000,
    start=start_datetime,
    end=end_datetime,
    interval=1)
ops.add_activity(pay_vehicle_loan)

# Vehicle maintenance activity
pay_vehicle_maintenance = BasicActivity(
    "Pay Vehicle Maintenance",
    description="Pay the vehicle maintenance",
    dt_account="Expense/Vehicle Maintenace",
    cr_account="Bank/Default",
    amount=4000,
    start=start_datetime,
    end=end_datetime,
    interval=3)
ops.add_activity(pay_vehicle_loan)

# Make a delivery sale activity
make_delivery_sale = BasicActivity(
    "Make delivery",
    description="Get Sales from a delivery",
    dr_account="Bank/Default",
    cr_account="Sales/Sales Delivery",
    amount=5000,
    start=start_datetime,
    end=end_datetime,
    interval=1)
ops.add_activity(make_delivery_sale)
# Pay for delivery costs
pay_delivery_costs = BasicActivity(
    "Pay delivery costs",
    description="Pay the delivery costs",
    dt_account="Cost Of Sales/Cos Delivery",
    cr_account="Bank/Default",
    amount=5000,
    start=start_datetime,
    end=end_datetime,
    interval=1)
ops.add_activity(pay_delivery_costs)

# pay wages for employees
pay_wages = BasicActivity(
    "Pay Wages",
    description="Pay Wages",
    dt_account="Expenses/Wages",
    cr_account="Bank/Default",
    amount=10000,
    start=start_datetime,
    end=end_datetime,
    interval=1)
hr.add_activity(pay_wages)

# -----------------------------------------------------------------------------
# Run the model
# -----------------------------------------------------------------------------

print()
print("\033[33mRun the model\033[38m")
print()

model.run()

print
print("\033[33mRESULTS\033[38m")
print
print

# Todo: Print results
print
print
print("\033[32mThe End.\033[38m")
