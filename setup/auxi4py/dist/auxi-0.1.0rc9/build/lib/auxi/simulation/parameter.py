# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 08:30:29 2015

@author: Christoff Kok, Thabisani Nigel Phuthi
"""
__version__ = "0.0.0"

from auxi.modelling.business import NamedObject
from auxi.simulation.path_engine import *
from auxi.modelling.business import TimeInterval


class Parameter(NamedObject):
    def __init__(self, name, source, units, default_value, description=""):
        NamedObject.__init__(self)
        self.name = str(name)
        if description is not None:
            self.description = description
        self._source = source
        self.units = units
        self.default_value = default_value
        self._path = None

        self.value_dict_intervals = {}
        self.value_dict_dates = {}

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    def get_dt_diff(self, date_time1, date_time2, interval_type, interval_size):
        if interval_type == TimeInterval.Millisecond:
            return (date_time1.millisecond - date_time2.millisecond) * interval_size
        if interval_type == TimeInterval.Second:
            return (date_time1.second - date_time2.second) * interval_size
        if interval_type == TimeInterval.Minute:
            return (date_time1.minute - date_time2.minute) * interval_size
        if interval_type == TimeInterval.Hour:
            return (date_time1.hour - date_time2.hour) * interval_size
        if interval_type == TimeInterval.Day:
            return (date_time1.day - date_time2.day) * interval_size
        if interval_type == TimeInterval.Week:
            return (date_time1.day - date_time2.day) * 7 * interval_size
        if interval_type == TimeInterval.Month:
            return (date_time1.month - date_time2.month) * interval_size
        if interval_type == TimeInterval.Year:
            return (date_time1.year - date_time2.year) * interval_size

    def get_nearest_date_value(self, date):
        if date in self.value_dict_dates:
                return date, self.value_dict_dates[date]
        else:
            # return the previous set value
            prev_key = datetime.min
            found = False
            for key in sorted(self.value_dict_dates.keys()):
                if key > date:
                    break
                prev_key = key
                found = True
            if not found:
                return prev_key, self.default_value
            else:
                return prev_key, self.value_dict_dates[prev_key]

    def get_nearest_interval_value(self, interval):
        if interval in self.value_dict_intervals:
            return interval, self.value_dict_intervals[interval]
        else:
            # return the previous set value
            prev_key = 0
            found = False
            for key in sorted(self.value_dict_intervals.keys()):
                if key > interval:
                    break
                prev_key = key
                found = True
            if not found:
                return prev_key, self.default_value
            else:
                return prev_key, self.value_dict_intervals[prev_key]

    def get_nearest_value(self, interval, date_time,
                          interval_type, interval_size):
        if interval is None:
            if date_time is None:
                return self.default_value
            else:
                return self.get_nearest_date_value(date_time)[1]
        else:
            if date_time is None:
                return self.get_nearest_interval_value(interval)[1]
            else:
                int_ix, interval_val = self.get_nearest_interval_value(
                    interval)
                dt_ix, date_val = self.get_nearest_date_value(date_time)
                if dt_ix is None:
                    if int_ix is None:
                        return self.default_value
                    else:
                        return interval_val
                elif int_ix is None:
                    return date_val
                elif self.get_dt_diff(date_time, dt_ix, interval_type,
                                      interval_size) > int_ix * interval_size:
                    return date_val
                else:
                    return interval_val

    def value(self, date_query=None, interval=None, date_time=None,
              interval_type=None, interval_size=None, scenario=None):
        if date_query is None:
            result = self.get_nearest_value(interval, date_time, interval_type,
                                            interval_size)
        elif isinstance(date_query, datetime):
            result = self.get_nearest_value(None, date_query, interval_type,
                                            interval_size)
        else:
            try:
                val_ix = eval(str(date_query))
                if isinstance(val_ix, int):
                    result = self.get_nearest_value(val_ix, None, interval_type,
                                                    interval_size)
                else:
                    result = self.default_value
            except:
                pass

        if scenario is not None and isinstance(result, str):
            param_start_ix = result.rindex(".")
            seg_path = result[0:param_start_ix]
            seg_name = seg_path[result.index("::")+2:]
            param_path = result[param_start_ix+1:]

            if seg_name in scenario.segments:
                seg = scenario.segments[seg_name]
                if param_path in seg.parameters:
                    result = seg.parameters[param_path]._source
        return result

    def apply_value(self, seg_source, interval=None, date_time=None,
                    interval_type=None, interval_size=None, scenario=None):
        val = self.value(
            interval=interval,
            date_time=date_time,
            interval_type=interval_type,
            interval_size=interval_size,
            scenario=scenario)
        if isinstance(self._source, int):
            val = int(val)
        set_instance_value(seg_source, self.name, val)
