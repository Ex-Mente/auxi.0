# -*- coding: utf-8 -*-
"""
This module provides an activity class that that serves as a base class
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
    path = ""
    start_period_ix = -1
    end_period_ix = -1
    period_count = -1
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
        super().__init__(name, description)
        self.start_datetime = start
        self.end_datetime = end
        self.interval = interval

    def set_path(self, parent_path):
        """Set the path of this activity. The name is added to the given path.

        :param parent_path: The path of its parent.
        """
        self.path = parent_path + "/" + self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        ix = self.path.rfind('/')
        if ix == -1:
            self.path = value
        else:
            self.path = self.path[:ix] + value

    def _meet_exection_criteria(self, ix_period):
        if self.interval != 0 and (ix_period+1) % self.interval != 0:
            return False
        return ix_period >= start_period_ix and ix_period + self.interval <= end_period_ix

    def prepare_to_run(self, clock, period_count):
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
