__version__ = "0.1.0"

from auxi.core import NamedObject
from auxi.modelling.business import TimeBasedModel
from auxi.modelling.business import Clock
from auxi.modelling.business import Entity
from auxi.modelling.business import Component
from auxi.modelling.business import Activity
from auxi.modelling.business import BasicActivity
from auxi.modelling.business import CapitalLoanActivity
from auxi.modelling.business import CustomPythonActivity
from auxi.modelling.business import TimeInterval
from auxi.simulation.custom_python_object import *


NamedObject.is_param = lambda self, p: False

TimeBasedModel.is_param = lambda self, p: p in ['entityList',
                                                'totalIntervalsToRun',
                                                'clock']

Clock.is_param = lambda self, p: p in ['timeStepIntervalCount',
                                       'timeStepInterval',
                                       'startDateTime']

Entity.is_param = lambda self, p: p in ['componentList',
                                        'generalLedger',
                                        'taxRuleSet',
                                        'variableGroupList']

Component.is_param = lambda self, p: p in ['activityList',
                                           'componentList',
                                           'variableGroupList']

Activity.is_param = lambda self, p: p in ['executeInterval',
                                          'executionEndAtInterval',
                                          'executionStartAtInterval']

BasicActivity.is_param = lambda self, p: p in ['executeInterval',
                                               'executionEndAtInterval',
                                               'executionStartAtInterval',
                                               'amount',
                                               'date']

CapitalLoanActivity.is_param = lambda self, p: p in ['executeInterval',
                                                     'executionEndAtInterval',
                                                     'executionStartAtInterval',
                                                     'loanAmount',
                                                     'date',
                                                     'interestRate',
                                                     'periodInMonths',
                                                     'amountLeft',
                                                     'monthsLeft',
                                                     'monthlyPayment',
                                                     'currentInterestAmount']

CustomPythonActivity.is_param = lambda self, p: p in ['custom_python_object']


def run_Entity(self, segment):
    self.prepare_to_run()


def prepare_to_run_TimebasedModel(self, scenario):
    scenario.apply_parameter_values(0,
                                    self.clock.startDateTime,
                                    self.clock.timeStepInterval,
                                    1)
    self.prepare_to_run()


TimeBasedModel.prepare_to_run_from_scenario = prepare_to_run_TimebasedModel


def run_TimebasedModel(self, scenario):
    self.prepare_to_run_from_scenario(scenario)
    for ix in range(0, self.totalIntervalsToRun):
        # Apply the scenario's parameter values for this iteration before
        #   executing this month.
        scenario.apply_parameter_values(ix,
                                        self.clock.getDateTimeAtInterval(ix),
                                        self.clock.timeStepInterval,
                                        1)

        for entity in self.entityList:
            entity.run(self.clock, ix, self.currency)

TimeBasedModel.run_from_scenario = run_TimebasedModel
