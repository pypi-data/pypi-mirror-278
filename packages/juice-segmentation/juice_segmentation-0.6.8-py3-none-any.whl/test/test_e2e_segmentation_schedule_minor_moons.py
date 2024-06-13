"""
Created on May 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to run the segmentation scheduler for several cases
and compare them to reference output produced for trajectory crema 5.0.
There are E2E test running most of the available source code,
performing by the way a non regression test.

All the data are available on test_data_set directory

here we run the same case
Segmentation Proposal (Prime; with overlap) + minor moons (opportunities)--> Segmentation Proposal
to demonstrate
* seg_to_load can be avoided if it contains PRIME segment
* start and/or end time can be avoided in a partition; the start/end time will be take from the input segmentation plan


1) Nominal case
Run the update of the case Segmentation Proposal scheduling minor moons according to
segmentation_scheduler_config_minor_moons.json
The result is compared against a previous (reference) run.

2) seg_to_load set to []
Run the update of the case Segmentation Proposal scheduling minor moons according to
segmentation_scheduler_config_minor_moons_seg_load.json
The result is compared against a previous (reference) run,
and it is the same as case 1

3) seg_to_load set to [] and start = "" (no defined)
Run the update of the case Segmentation Proposal scheduling minor moons according to
segmentation_scheduler_config_minor_moons_no_time.json
The result is compared against a previous (reference) run,
and it is the same as case 1
"""

import os
import io
import shutil
import logging
import unittest

from esac_juice_pyutils.commons.json_handler import load_to_dic
from juice_segmentation.segmentation_multi.segmentation import generate_proposal_file

test_data_set = '../TDS/UM_CASE_4_3'
temp_dir = 'temp'
mission_phases_file = 'conf_file_local_copy/Mission_Phases.csv'
mission_timeline_event_file = 'conf_file_local_copy/mission_timeline_event_file_5_1_150lb_23_1.csv'
opportunity_vs_primes_file = 'conf_file_local_copy/OPPORTUNITY_PRIME_correspondance.csv'

# disable logging during unit test
logging.disable(logging.CRITICAL)


class MyTestCase(unittest.TestCase):

    def test_minor_mmon_segmentation_schedule_nominal(self):
        """
        Test case 1: Nominal case
        Run the update of the case Segmentation Proposal scheduling minor moons according to
        segmentation_scheduler_config_minor_moons.json
        The result is compared against a previous (reference) run.

        Segmentation Proposal (Prime; with overlap) + minor moons (opportunities)--> Segmentation Proposal
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'segmentation_scheduler_config_minor_moons.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        wg_segments_to_ignore = []
        if 'wg_segments_to_ignore' in cfg_file['main'].keys():
            wg_segments_to_ignore = cfg_file['main']["wg_segments_to_ignore"]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"],
                               wg_segments_to_ignore=wg_segments_to_ignore)

        tmp_values = list(open(os.path.join(temp_dir, 'report.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'report.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)

    def test_minor_mmon_segmentation_schedule_no_seg_to_load(self):
        """
        2) seg_to_load set to []
        Run the update of the case Segmentation Proposal scheduling minor moons according to
        segmentation_scheduler_config_minor_moons_no_time.json
        The result is compared against a previous (reference) run.

        Segmentation Proposal (Prime; with overlap) + minor moons (opportunities)--> Segmentation Proposal
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'segmentation_scheduler_config_minor_moons_seg_load.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        wg_segments_to_ignore = []
        if 'wg_segments_to_ignore' in cfg_file['main'].keys():
            wg_segments_to_ignore = cfg_file['main']["wg_segments_to_ignore"]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"],
                               wg_segments_to_ignore=wg_segments_to_ignore)

        tmp_values = list(open(os.path.join(temp_dir, 'report.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'report.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)

    def test_minor_mmon_segmentation_schedule_no_start_time(self):
        """
        3) seg_to_load set to [] and start = "" (no defined)
        Run the update of the case Segmentation Proposal scheduling minor moons according to
        segmentation_scheduler_config_minor_moons.json
        The result is compared against a previous (reference) run.

        Segmentation Proposal (Prime; with overlap) + minor moons (opportunities)--> Segmentation Proposal
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'segmentation_scheduler_config_minor_moons_no_time.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        wg_segments_to_ignore = []
        if 'wg_segments_to_ignore' in cfg_file['main'].keys():
            wg_segments_to_ignore = cfg_file['main']["wg_segments_to_ignore"]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"],
                               wg_segments_to_ignore=wg_segments_to_ignore)

        tmp_values = list(open(os.path.join(temp_dir, 'report.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'report.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)
