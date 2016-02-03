# -*- coding: utf-8 -*-
"""
This module provides an activity class that serves as a base class
for business activities.\n

@name: activity
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Activity(NamedObject):
    """Represents an activity base class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 start=datetime.min,
                 end=datetime.max,
                 interval=1):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param start: The datetime the activity should be started.
        :param end: The datetime the activity should be run until.
        :param interval: The interval of the activity.
        """
        self._parent_path = ""
        super().__init__(name, description)
        self.start_datetime = start
        self.end_datetime = end
        self.interval = interval
        self.start_period_ix = -1
        self.end_period_ix = -1
        self.period_count = -1

    def set_parent_path(self, value):
        self._parent_path = value
        self.path = value + r'/' + self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.path = self._parent_path + r'/' + self.name

    def _meet_execution_criteria(self, ix_period):
        if self.interval != 0 and (ix_period+1) % self.interval != 0:
            return False
        return ix_period >= self.start_period_ix and ix_period + self.interval <= self.end_period_ix

    def prepare_to_run(self, clock, period_count):
        """Prepare the activity for execution.

        :param clock: The clock containing the execution start time and execution period information.
        :param period_count: The total amount of periods this activity will be requested to be run for.
        """
        if self.start_period_ix == -1 and self.start_datetime != datetime.min:
            # Set the Start period index
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.start_datetime:
                    self.start_period_ix = i
                    break
        if self.start_period_ix == -1:
            self.start_period_ix = 0
        if self.period_count == -1 and self.end_datetime != datetime.max:
            # Set the Start date
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.end_datetime:
                    self.period_count = i - self.start_period_ix
                    break
        if self.period_count != -1:
            self.end_period_ix = self.start_period_ix + self.period_count
        else:
            self.end_period_ix = self.start_period_ix + period_count
