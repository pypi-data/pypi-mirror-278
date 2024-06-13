"""
Created on May 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to run the segmentation scheduler for several cases
and compare them to reference output produced for trajectory crema 5.0.
There are E2E test running most of the available source code,
performing by the way a non regression test.

All the data are available on test_data_set directory

"""
import copy
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

os.chdir(test_data_set)


class MyTestCase(unittest.TestCase):

    def test_segmentation_schedule_including_opnav_dl_3h(self):
        """
        Test (case 1) we insert opnav with minimum DL duration of 3H
        """

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'conf_cut_dl_template.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        cfg_file['main']["dl_segment_minimum_sec"] = 3 * 3600
        cfg_file['main']["partitions"][0]["op_nav_insertion_rules"] = [{
                "seg": [["WG3", ["JUPITER_GM"]]],
                "rules": ["adjacent_to_man_1h30m", "anywhere_2h", "anywhere_cutting_DL_1h30m"]}]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(
            temp_dir, 'segmentation_proposal_crema_5_0_all_without_seg_renaming.csv'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'segmentation_proposal_test_1.csv'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

    def test_segmentation_schedule_including_opnav_dl_4h(self):
        """
        Test (case 2) we insert opnav with minimum DL duration of 4H
        * first DL is removed since its duration is 3H
        * the second "DL_,2034-06-25T06:07:47Z,2034-06-25T15:07:11Z,,GENERIC" has a 9 hours duration
        """

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'conf_cut_dl_template.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        cfg_file['main']["dl_segment_minimum_sec"] = 4 * 3600
        cfg_file['main']["partitions"][0]["op_nav_insertion_rules"] = [{
                "seg": [["WG3", ["JUPITER_GM"]]],
                "rules": ["adjacent_to_man_1h30m", "anywhere_2h", "anywhere_cutting_DL_1h30m"]}]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(
            temp_dir, 'segmentation_proposal_crema_5_0_all_without_seg_renaming.csv'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'segmentation_proposal_test_2.csv'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

    def test_segmentation_schedule_including_opnav_dl_4h_anywhere_2h(self):
        """
        Test (case 3) we insert opnav with minimum DL duration of 4H usign rules anywhere_2h
        * first DL is removed since its duration is 3H
        * the second "DL_,2034-06-25T06:07:47Z,2034-06-25T15:07:11Z,,GENERIC" has a 9 hours duration

        """

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'conf_cut_dl_template.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        cfg_file['main']["dl_segment_minimum_sec"] = 4 * 3600
        cfg_file['main']["partitions"][0]["op_nav_insertion_rules"] = [{
            "seg": [["WG3", ["JUPITER_GM"]]],
            "rules": ["anywhere_2h"]}]

        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(
            temp_dir, 'segmentation_proposal_crema_5_0_all_without_seg_renaming.csv'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'segmentation_proposal_test_3.csv'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)
    def test_segmentation_schedule_including_opnav_dl_4h_2_partitions(self):
        """
        Test (case 5) we insert opnav with minimum DL duration of 4H
        * first DL is removed since its duration is 3H
        * The partition cut the DL "DL_,2034-06-25T06:07:47Z,2034-06-25T15:07:11Z,,GENERIC" of 9 hours
        * split the partition in 2, in partition one DL <= 4 hours but not to be removed if continue in next partition

        """

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'conf_cut_dl_template.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        cfg_file['main']["dl_segment_minimum_sec"] = 4 * 3600
        cfg_file['main']["partitions"].append(copy.copy(cfg_file['main']["partitions"][0]))
        cfg_file['main']["partitions"][0]["end"] = "2034-06-25T10:06:47Z"
        cfg_file['main']["partitions"][1]["start"] = "2034-06-25T10:06:47Z"
        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(
            temp_dir, 'segmentation_proposal_crema_5_0_all_without_seg_renaming.csv'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'segmentation_proposal_test_5.csv'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

    def test_segmentation_schedule_including_opnav_dl_4h_2_partitions_2(self):
        """
        Test (case 5) we insert opnav with minimum DL duration of 4H
        * first DL is removed since its duration is 3H
        * The partition cut the DL "DL_,2034-06-25T06:07:47Z,2034-06-24T08:00:00Z,,GENERIC"
        * split the partition in 2, in partition one DL <= 4 hours must be removed since not at the end of partitions

        """

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        config_file = 'conf_cut_dl_template.json'

        cfg_file = load_to_dic(config_file)
        input_file = cfg_file['main']["input_segmentation_file_path"]
        output_ref = cfg_file['main']["output_dir"]

        # set input in cfg_file to avoid the need o gitlab conf repository
        cfg_file['main']["mission_phases"] = mission_phases_file
        cfg_file['main']["mission_timeline_event_file"] = mission_timeline_event_file
        cfg_file['main']["opportunity_vs_prime"] = opportunity_vs_primes_file

        cfg_file['main']["dl_segment_minimum_sec"] = 4 * 3600
        cfg_file['main']["partitions"].append(copy.copy(cfg_file['main']["partitions"][0]))
        cfg_file['main']["partitions"][0]["end"] = "2034-06-24T08:00:00Z"
        cfg_file['main']["partitions"][1]["start"] = "2034-06-24T08:00:00Z"
        generate_proposal_file(input_file,
                               temp_dir,
                               cfg_file['main'],
                               create_csv=cfg_file['main']["create_csv"])

        tmp_values = list(open(os.path.join(
            temp_dir, 'segmentation_proposal_crema_5_0_all_without_seg_renaming.csv'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, 'segmentation_proposal_test_6.csv'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)