#!/usr/bin/env python3
"""
This module provides classes to create reports.
"""

from io import StringIO

from enum import Enum
import csv
from tabulate import tabulate

from auxi.core.objects import Object

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ReportFormat(Enum):
    """
    Represents the format the report should be outputted as.
    """

    printout = 1,
    latex = 2,
    txt = 3,
    csv = 4,
    string = 5,
    matplotlib = 6,
    png = 7


class Report(Object):
    """
    Base class for all auxi reports.
    """

    def __init__(self, data_source, output_path=None):
        self.data_source = data_source
        self.output_path = output_path

    def _generate_table_(self):
        return []

    def _render_matplotlib_(self, png=False):
        pass

    def render(self, format=ReportFormat.printout):
        """
        Render the report in the specified format

        :param format: The format. The default format is to print
          the report to the console.

        :returns: If the format was set to 'string' then a string
          representation of the report is returned.
        """

        table = self._generate_table_()
        if(format == ReportFormat.printout):
            print(tabulate(table, headers="firstrow", tablefmt="simple"))
        elif (format == ReportFormat.latex):
            self._render_latex_(table)
        elif (format == ReportFormat.txt):
            self._render_txt_(table)
        elif (format == ReportFormat.csv):
            self._render_csv_(table)
        elif (format == ReportFormat.string):
            return str(tabulate(table, headers="firstrow", tablefmt="simple"))
        elif (format == ReportFormat.matplotlib):
            self._render_matplotlib_()
            pass
        elif (format == ReportFormat.png):
            if self.output_path is None:
                self._render_matplotlib_()
            else:
                self._render_matplotlib_(True)
            pass

    def _render_latex_(self, table):
        if self.output_path is not None:
            with open(self.output_path + '.tex', 'w') as f:
                f.write(
                    tabulate(table, headers="firstrow", tablefmt="latex"))
        else:
            print(tabulate(table, headers="firstrow", tablefmt="latex"))

    def _render_txt_(self, table):
        if self.output_path is not None:
            with open(self.output_path + '.txt', 'w') as f:
                f.write(
                    tabulate(table, headers="firstrow", tablefmt="simple"))
        else:
            print(tabulate(table, headers="firstrow", tablefmt="simple"))

    def _render_csv_(self, table):
        if self.output_path is not None:
            with open(self.output_path + '.csv', 'w') as f:
                csv.writer(f, lineterminator='\n').writerows(table)
        else:
            with StringIO() as f:
                csv.writer(f, lineterminator='\n').writerows(table)
                print(f.getvalue())


if __name__ == "__main__":
    import unittest
    from reporting_test import ReportingUnitTester
    unittest.main()
