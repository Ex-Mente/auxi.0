# -*- coding: utf-8 -*-
"""
This module provides a clock class that provides functions to manage a
ticking clock based on a time period as well as retreive the current tick's
date since the start date.\n

@name: clock
@author: Ex Mente Technologies (Pty) Ltd
"""

from enum import Enum
from datetime import datetime
from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"


class TimePeriod(Enum):
    millisecond = 1
    second = 2
    minute = 3
    hour = 4
    day = 5
    week = 6
    month = 7
    year = 8


class Clock(NamedObject):
    """Represents a clock."""
    timestep_ix = 0

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 start_datetime=datetime.min,
                 timestep_period_duration=TimePeriod.month,
                 timestep_period_count=1):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param start_datetime: The start datetime.
        :param timestep_period_duration: The duration of each time period.
        :param timestep_period_count: The number of periods that makes up a timestep.
        """
        super().__init__(name, description)
        self.start_datetime = start_datetime
        self.timestep_period_duration = timestep_period_duration
        self.timestep_period_count = timestep_period_count

    def tick(self):
        self.timestep_ix += 1

    def reset(self):
        self.timestep_ix = 0

    def get_datetime_at_period_ix(self, ix):
        if self.timestep_period_duration == TimePeriod.milliseconds:
            return self.start_datetime + datetime.timedelta(milliseconds=ix)
        elif self.timestep_period_duration == TimePeriod.seconds:
            return self.start_datetime + datetime.timedelta(seconds=ix)
        elif self.timestep_period_duration == TimePeriod.minutes:
            return self.start_datetime + datetime.timedelta(minutes=ix)
        elif self.timestep_period_duration == TimePeriod.hours:
            return self.start_datetime + datetime.timedelta(hours=ix)
        elif self.timestep_period_duration == TimePeriod.days:
            return self.start_datetime + datetime.timedelta(days=ix)
        elif self.timestep_period_duration == TimePeriod.days:
            return self.start_datetime + datetime.timedelta(days=ix*7)
        elif self.timestep_period_duration == TimePeriod.months:
            return self.start_datetime + datetime.timedelta(months=ix)
        elif self.timestep_period_duration == TimePeriod.years:
            return self.start_datetime + datetime.timedelta(years=ix)

    def get_datetime(self):
        return self.get_datetime_at_period_ix(self.timestep_ix)
