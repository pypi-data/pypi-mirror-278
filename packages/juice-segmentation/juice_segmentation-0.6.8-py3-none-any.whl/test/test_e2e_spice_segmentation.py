"""
Created on Jun 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to run the spice segmentation scheduler for spice
and compare them to reference output produced for trajectory crema 3.0.
There are E2E test running most of the available source code,
performing by the way a non regression test.

All the data are available on test_data_set directory

1) Run spice segmentation schedule for crema_5_0
The result is compared against a previous run

2) Run spice segmentation schedule for crema_5_0 filtering by start and end time
removing first and last segments
The result is compared against a previous run

"""
import datetime
import os
import logging
import shutil
import unittest

from juice_segmentation.spice_segmentation import input_file_pattern
from juice_segmentation.spice_segmentation.spice_segmentation \
    import generate_spice_segmentation_non_overlapping_segment

test_data_set = '../TDS/spice'
temp_dir = 'temp'
juice_spice_segmentation = 'conf_file_local_copy/crema_5_0'
juice_sc_sat_crema_X_Y = 'juice_sc_sat_crema_5_0.csv'

# disable logging during unit test
logging.disable(logging.CRITICAL)


class MyTestCase(unittest.TestCase):

    maxDiff = None

    def test_spice_segmentation(self):
        """
        Test (case 1) we have no regression when running the spice segmentation scheduler
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        input_dir = os.path.abspath(juice_spice_segmentation)
        output_ref = os.path.abspath('./')
        output_temp = os.path.abspath(temp_dir)
        start, end = None, None

        generate_spice_segmentation_non_overlapping_segment(
            input_dir, output_temp, start=start, end=end, input_file_pattern=input_file_pattern)

        tmp_values = list(open(os.path.join(temp_dir, juice_sc_sat_crema_X_Y), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, juice_sc_sat_crema_X_Y), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)

    def test_nominal_segmentation_schedule_not_including_opnav(self):
        """
        Test (case 2) we have no regression when running the spice segmentation scheduler
        and filtering by start and end time removing first and last segments
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        input_dir = os.path.abspath(juice_spice_segmentation)
        output_ref = os.path.abspath('./')
        output_temp = os.path.abspath(temp_dir)
        start = datetime.datetime.strptime("2024-08-26T11:00:00", "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime("2035-05-07T16:46:12", "%Y-%m-%dT%H:%M:%S")

        generate_spice_segmentation_non_overlapping_segment(
            input_dir, output_temp, start=start, end=end, input_file_pattern=input_file_pattern)

        output_file = os.path.join(output_temp, juice_sc_sat_crema_X_Y)
        file_ref = os.path.join(output_ref, juice_sc_sat_crema_X_Y)

        tmp_values = list(open(output_file, 'r'))
        tmp_ref = list(open(file_ref, 'r'))[1:-1]

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)
