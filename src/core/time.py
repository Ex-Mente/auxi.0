#!/usr/bin/env python3
"""
This module provides classes to manage time.
"""

from datetime import datetime, timedelta

from enum import Enum
from dateutil.relativedelta import relativedelta

from auxi.core.objects import NamedObject

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class TimePeriod(Enum):
    """
    Represents a period in time.
    """

    millisecond = 1
    second = 2
    minute = 3
    hour = 4
    day = 5
    week = 6
    month = 7
    year = 8


class Clock(NamedObject):
    """
    Represents a clock that provices functions to manage a ticking clock based
    on a time period as well as retreive the current tick's date since the
    start date.
    """

    def __init__(self, name, description=None,
                 start_datetime=datetime.min,
                 timestep_period_duration=TimePeriod.month,
                 timestep_period_count=1):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param start_datetime: The start datetime.
        :param timestep_period_duration: The duration of each time period.
        :param timestep_period_count: The number of periods that makes up a
          timestep.
        """

        super(Clock, self).__init__(name, description)
        self.start_datetime = start_datetime
        self.timestep_period_duration = timestep_period_duration
        self.timestep_period_count = timestep_period_count
        self.timestep_ix = 0

    def tick(self):
        """
        Increment the clock's timestep index.
        """

        self.timestep_ix += 1

    def reset(self):
        """
        Resets the clock's timestep index to '0'.
        """

        self.timestep_ix = 0

    def get_datetime_at_period_ix(self, ix):
        """
        Get the datetime at a given period.

        :param period: The index of the period.

        :returns: The datetime.
        """

        if self.timestep_period_duration == TimePeriod.millisecond:
            return self.start_datetime + timedelta(milliseconds=ix)
        elif self.timestep_period_duration == TimePeriod.second:
            return self.start_datetime + timedelta(seconds=ix)
        elif self.timestep_period_duration == TimePeriod.minute:
            return self.start_datetime + timedelta(minutes=ix)
        elif self.timestep_period_duration == TimePeriod.hour:
            return self.start_datetime + timedelta(hours=ix)
        elif self.timestep_period_duration == TimePeriod.day:
            return self.start_datetime + relativedelta(days=ix)
        elif self.timestep_period_duration == TimePeriod.week:
            return self.start_datetime + relativedelta(days=ix*7)
        elif self.timestep_period_duration == TimePeriod.month:
            return self.start_datetime + relativedelta(months=ix)
        elif self.timestep_period_duration == TimePeriod.year:
            return self.start_datetime + relativedelta(years=ix)

    def get_datetime(self):
        """
        Get the clock's current datetime.

        :returns: The datetime.
        """

        return self.get_datetime_at_period_ix(self.timestep_ix)

if __name__ == "__main__":
    import unittest
    from auxi.core.time.time_test import ClockUnitTester
    unittest.main()
