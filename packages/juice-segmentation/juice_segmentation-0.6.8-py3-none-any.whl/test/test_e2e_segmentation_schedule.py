"""
Created on May 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to run the segmentation scheduler for several cases
and compare them to reference output produced for trajectory crema 5.0.
There are E2E test running most of the available source code,
performing by the way a non regression test.

All the data are available on test_data_set directory

1) Segmentation Opportunities (+ OPNAV) --> Segmentation Proposal (Prime; no overlap)
Run the nominal case segmentation_scheduler_multi_config.json which runs the segmentation scheduler
to selected from a segmentation plan proposal the prime segmentation including opnav without overlaps.
The result is compared against a previous run

2) Segmentation Opportunities (without OPNAV) --> Segmentation Proposal (Prime; no overlap)
Run the nominal case segmentation_scheduler_multi_config_no_opnav.json which runs the segmentation scheduler
to selected from a segmentation plan proposal the prime segmentation but not including opnav without overlaps.
The result is compared against a previous run of

3) Segmentation Proposal (Prime; no overlap) + OPNAV (opportunities) --> Segmentation Proposal (Prime; no overlap)
Run the update of the case 2  including opnav Segmentation_scheduler_config_file_update_multi.json
The result is compared against a previous run,
and must be in line with result of case 1
"""

import os
import logging
import shutil
import unittest

from esac_juice_pyutils.commons.json_handler import load_to_dic
from juice_segmentation.segmentation_multi.segmentation import generate_proposal_file

test_data_set = '../TDS/crema_5_0'
temp_dir = 'temp'
mission_phases_file = 'conf_file_local_copy/Mission_Phases.csv'
mission_timeline_event_file = 'conf_file_local_copy/mission_timeline_event_file_5_0.csv'
opportunity_vs_primes_file = 'conf_file_local_copy/OPPORTUNITY_PRIME_correspondance.csv'

# disable logging during unit test
logging.disable(logging.CRITICAL)


class MyTestCase(unittest.TestCase):

    def test_nominal_segmentation_schedule_including_opnav(self):
        """
        Test (case 1) we have no regression when running the segmentation scheduler to selected from a
        segmentation plan proposal the prime segmentation including opnav without overlaps
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'segmentation_scheduler_multi_config.json'

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
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(temp_dir, 'report.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'report.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)

    def test_nominal_segmentation_schedule_not_including_opnav(self):
        """
        Test (case 2) we have no regression when running the segmentation scheduler to selected from a
        segmentation plan proposal the prime segmentation not including opnav without overlaps
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'segmentation_scheduler_multi_config_no_opnav.json'

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

    def test_nominal_segmentation_schedule_update_including_opnav(self):
        """
        Test (case 3) we have no regression when running the segmentation scheduler to update from a
        segmentation plan containing prime segmentation in order to schedule opnav
        """

        here = os.getcwd()
        os.chdir(test_data_set)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'Segmentation_scheduler_config_file_update_multi.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(temp_dir, 'report.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'report.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        os.chdir(here)