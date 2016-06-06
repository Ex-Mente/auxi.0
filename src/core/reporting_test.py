#!/usr/bin/env python3
"""
This module contains code used to test core reporting classes.
"""

import unittest
import os.path

from auxi.core.reporting import ReportFormat, Report


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ReportingUnitTester(unittest.TestCase):
    """
    The unit tester for the class being tested.
    """

    def setUp(self):
        self.object = Report([["cola", "colb"], [1, 2]])
        self.object_w_file = Report([["cola", "colb"], [1, 2]], "./test")

    def tearDown(self):
        del self.object

    def test_render_without_file(self):
        """
        Test whether a value is returned when a report is rendered in a
        string format. And wether any of the other formats throw an error.
        """

        self.object.render(format=ReportFormat.printout)
        self.object.render(format=ReportFormat.latex)
        self.object.render(format=ReportFormat.txt)
        self.object.render(format=ReportFormat.csv)

        self.assertEqual(
            len(self.object.render(format=ReportFormat.string)) > 0,
            True)

        self.object.render(format=ReportFormat.matplotlib)
        self.object.render(format=ReportFormat.png)

    def test_render_with_file(self):
        """
        Test whether a value is returned when a report is rendered in a
        string format. And wether any of the other formats throw an error.
        """

        file_name = self.object_w_file.output_path
        self.object_w_file.render(format=ReportFormat.printout)
        self.object_w_file.render(format=ReportFormat.latex)
        os.path.isfile(file_name + '.tex')
        os.remove(file_name + '.tex')
        self.object_w_file.render(format=ReportFormat.txt)
        os.path.isfile(file_name + '.txt')
        os.remove(file_name + '.txt')
        self.object_w_file.render(format=ReportFormat.csv)
        os.path.isfile(file_name + '.csv')
        os.remove(file_name + '.csv')

        self.assertEqual(
            len(self.object_w_file.render(format=ReportFormat.string)) > 0,
            True)

        self.object_w_file.render(format=ReportFormat.matplotlib)
        self.object_w_file.render(format=ReportFormat.png)


if __name__ == '__main__':
    unittest.main()
