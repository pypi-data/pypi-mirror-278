"""
Created on August 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to test wg_segment_handler

"""

import unittest
import datetime

from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps
from esac_juice_pyutils.commons.my_log import setup_logger

setup_logger('info')

wg1_seg = {'WG1': {
    'EUROPA_FLYBY_1': [
        [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]],
    'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2), datetime.datetime(2030, 10, 20, 4, 48, 2)]],
    'EUROPA_FLYBY_3GM_2': [
        [datetime.datetime(2030, 10, 19, 8, 48, 2), datetime.datetime(2030, 10, 20, 0, 48, 2)]],
    'EUROPA_FLYBY_3GM_1': [
        [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 18, 57, 22)]],
    'EUROPA_RPWI_PASSIVRAD_1': [
        [datetime.datetime(2030, 10, 5, 10, 45), datetime.datetime(2030, 10, 5, 11, 10)]]
}
}

OPPORTUNITY_PRIME_correspondance = '../../test_files/config/OPPORTUNITY_PRIME_correspondance.csv'
mission_phases = '../../test_files/config/crema_3.2/Mission_phases.txt'
segment_handler = WgSegBasicOps()


class MyTestCase(unittest.TestCase):

    def test_get_wg_sub(self):
        """
        Test segment subtraction function is working as expected.
        """

        wg2_seg = {'WG2': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]],
            'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2), datetime.datetime(2030, 10, 20, 1, 0, 0)]],
            'EUROPA_FLYBY_3GM_1': [
                [datetime.datetime(2030, 10, 5, 9, 0, 0), datetime.datetime(2030, 10, 5, 10, 0, 0)],
                [datetime.datetime(2030, 10, 5, 12, 0, 0), datetime.datetime(2030, 10, 5, 14, 0, 0)]],
            'EUROPA_FLYBY_GALA_1': [
                [datetime.datetime(2030, 10, 19, 8, 48, 2), datetime.datetime(2030, 10, 20, 0, 48, 2)]],
        }
        }

        self.assertEqual(segment_handler.get_wg_sub(wg1_seg, wg1_seg), {'WG1': {}})

        self.assertEqual(segment_handler.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 10, 00, 1)]]}}
        )

        self.assertEqual(segment_handler.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 10, 0, 1)]]}}
        )

        self.assertEqual(segment_handler.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 19, 4, 48, 2), datetime.datetime(2030, 10, 20, 4, 48, 2)]]}},
            {'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 19, 0, 48, 2), datetime.datetime(2030, 10, 20, 1, 0, 0)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 20, 1, 0, 0), datetime.datetime(2030, 10, 20, 4, 48, 2)]]}}
        )

        self.assertEqual(segment_handler.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 18, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 5, 9, 0, 0), datetime.datetime(2030, 10, 5, 10, 0, 0)],
                    [datetime.datetime(2030, 10, 5, 12, 0, 0), datetime.datetime(2030, 10, 5, 14, 0, 0)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 9, 0, 0)],
                    [datetime.datetime(2030, 10, 5, 10, 0, 0), datetime.datetime(2030, 10, 5, 12, 0, 0)],
                    [datetime.datetime(2030, 10, 5, 14, 0, 0), datetime.datetime(2030, 10, 5, 18, 57, 22)]]}}
        )

        # All tests together
        self.assertEqual(segment_handler.get_wg_sub(wg1_seg, wg2_seg), {'WG1': {
            'EUROPA_FLYBY_1': [[datetime.datetime(2030, 10, 4, 22, 57, 22),
                                datetime.datetime(2030, 10, 5, 9, 0)],
                               [datetime.datetime(2030, 10, 5, 10, 0),
                                datetime.datetime(2030, 10, 5, 10, 0, 1)]],
            'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 20, 1, 0),
                                datetime.datetime(2030, 10, 20, 4, 48, 2)]],
            'EUROPA_FLYBY_3GM_1': [[datetime.datetime(2030, 10, 5, 2, 57, 22),
                                    datetime.datetime(2030, 10, 5, 9, 0)],
                                   [datetime.datetime(2030, 10, 5, 10, 0),
                                    datetime.datetime(2030, 10, 5, 10, 0, 1)]]}})

    def test_select_wgx_subset(self):
        """
        Test Working Group (WG) and/or segments subset extraction from a given wgx
        """

        self.assertEqual(segment_handler.select_wgx_subset(wg1_seg, wg_filter=['WG1'], seg_filter=['EUROPA_FLYBY_2']),
                         {'WG1': {'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2),
                                                      datetime.datetime(2030, 10, 20, 4, 48, 2)]]}})

        self.assertEqual(segment_handler.select_wgx_subset(wg1_seg, seg_filter=['EUROPA_FLYBY_2']),
                         {'WG1': {'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2),
                                                      datetime.datetime(2030, 10, 20, 4, 48, 2)]]}})

    def test_set_wgx_segments(self):
        """
        Test Working Group (WG) and/or segments subset addition and overwriting from a given wgx
        """

        self.assertEqual(segment_handler.add_wgx_segments(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}
        )

        self.assertEqual(segment_handler.add_wgx_segments(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 5, 10, 00, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
                'WG2': {
                    'EUROPA_FLYBY_2': [
                        [datetime.datetime(2030, 10, 5, 10, 00, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}})
