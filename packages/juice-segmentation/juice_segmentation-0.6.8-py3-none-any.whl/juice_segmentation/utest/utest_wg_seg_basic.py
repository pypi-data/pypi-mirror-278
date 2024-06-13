"""
Created on August 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to test wg_segment_handler

"""

import unittest
import datetime

from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps

wg_seg_basic = WgSegBasicOps()

wg1_seg = {'WG1': {
    'EUROPA_FLYBY_1': [
        [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]],
    'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2), datetime.datetime(2030, 10, 20, 4, 48, 2)]],
    'EUROPA_FLYBY_3GM_2': [
        [datetime.datetime(2030, 10, 19, 8, 48, 2), datetime.datetime(2030, 10, 20, 0, 48, 2)]],
    'EUROPA_FLYBY_3GM_1': [
        [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 18, 57, 22)]],
    'EUROPA_RPWI_PASSIVRAD_1': [
        [datetime.datetime(2030, 10, 5, 10, 45), datetime.datetime(2030, 10, 5, 11, 10)]]}
}


class MyTestCase(unittest.TestCase):

    def test_get_wg_sub(self):
        """
        Test segment subtraction function is working as expected.
        :return:
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

        self.assertEqual(wg_seg_basic.get_wg_sub(wg1_seg, wg1_seg), {'WG1': {}})

        self.assertEqual(wg_seg_basic.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 10, 0, 1)]]}}
        )

        self.assertEqual(wg_seg_basic.get_wg_sub(
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

        self.assertEqual(wg_seg_basic.get_wg_sub(
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

        self.assertEqual(wg_seg_basic.get_wg_sub(
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
        self.assertEqual(wg_seg_basic.get_wg_sub(wg1_seg, wg2_seg), {'WG1': {
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

    def test_get_wg_sub_and_clean(self):
        """
        Test segment subtraction function is working as expected including cleanup using segment_minimun_sec
        * check that empty segments are removed
        * check that segment < segment_minimun_sec = 60 seconds (for instance are removed)
        :return:
        """

        self.assertEqual(wg_seg_basic.get_wg_sub(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {}}
        )

    def test_get_wg_substract_and_clean(self):
        """
        Test segment subtraction function is working as expected including cleanup using segment_minimun_sec
        * check that empty segments are removed
        * check that segment < segment_minimun_sec = 60 seconds (for instance are removed)
        :return:
        """

        self.assertEqual(wg_seg_basic.wg_substract(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            [{'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}]),
            {}
        )

        self.assertEqual(wg_seg_basic.wg_substract(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            [{'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 56, 22)]]}}]),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 22, 56, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}
            }
        )

        self.assertEqual(wg_seg_basic.wg_substract(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            [{'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 56, 22)]]}}],
            segment_minimun_sec=60),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 22, 56, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}
            }
        )

        self.assertEqual(wg_seg_basic.wg_substract(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            [{'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 56, 22)]]}}],
            segment_minimun_sec=61),
            {}
        )

    def test_select_wgx_subset(self):
        """
        Test Working Group (WG) and/or segments subset extraction from a given wgx
        :return:
        """

        self.assertEqual(wg_seg_basic.select_wgx_subset(wg1_seg, wg_filter=['WG1'], seg_filter=['EUROPA_FLYBY_2']),
                         {'WG1': {'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2),
                                                      datetime.datetime(2030, 10, 20, 4, 48, 2)]]}})

        self.assertEqual(wg_seg_basic.select_wgx_subset(wg1_seg, seg_filter=['EUROPA_FLYBY_2']),
                         {'WG1': {'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2),
                                                      datetime.datetime(2030, 10, 20, 4, 48, 2)]]}})

    def test_remove_select_wgx_subset(self):
        """
        Test Working Group (WG) and/or segments subset extraction from a given wgx
        :return:
        """

        self.assertEqual(wg_seg_basic.remove_wgx_subset(wg1_seg, wg_filter=['WG1'],
                                                        seg_filter=['EUROPA_FLYBY_1', 'EUROPA_FLYBY_3GM']),
                         {'WG1': {
                             'EUROPA_FLYBY_2': [[datetime.datetime(2030, 10, 19, 4, 48, 2),
                                                 datetime.datetime(2030, 10, 20, 4, 48, 2)]],
                             'EUROPA_RPWI_PASSIVRAD_1': [[datetime.datetime(2030, 10, 5, 10, 45),
                                                          datetime.datetime(2030, 10, 5, 11, 10)]]
                         }})

        self.assertEqual(wg_seg_basic.remove_wgx_subset(wg1_seg, wg_filter=['WG1'],
                                                        seg_filter=['EUROPA_FLY']),
                         {'WG1': {
                             'EUROPA_RPWI_PASSIVRAD_1': [[datetime.datetime(2030, 10, 5, 10, 45),
                                                          datetime.datetime(2030, 10, 5, 11, 10)]]
                         }})

        self.assertEqual(wg_seg_basic.remove_wgx_subset(
            {'WG1': {
                'EUROPA_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 18, 57, 22)]]},
                'WG2': {
                    'EUROPA_FLYBY_3GM_1': [
                        [datetime.datetime(2030, 10, 5, 9, 0, 0), datetime.datetime(2030, 10, 5, 10, 0, 0)]]}},
            wg_filter=['WG2'], seg_filter=['EUROPA_FLY']),
            {'WG1': {
                'EUROPA_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 5, 2, 57, 22), datetime.datetime(2030, 10, 5, 18, 57, 22)]]},
                'WG2': {}}
        )

    def test_add_wgx_segments(self):
        """
        Test Working Group (WG) and/or segments subset addition and overwriting from a given wgx
        """

        self.assertEqual(wg_seg_basic.add_wgx_segments(
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

        self.assertEqual(wg_seg_basic.add_wgx_segments(
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}},
            {'WG2': {
                'EUROPA_FLYBY_2': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}),
            {'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
                'WG2': {
                    'EUROPA_FLYBY_2': [
                        [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}})

    def test_remove_seg_if_overlapping(self):
        """
        Test segment are removed in wg_base instances when overlapping with segments in wg_to_check


        For instance JMAG_CALROLL in wgx when overlapping with segments PERIJOVE or FLYBY
        """

        wg1_seg = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}

        wg4_seg = {'WG4': {
            'JUPITER_PERIJOVE_PJ6': [
                [datetime.datetime(2030, 9, 15, 9, 16, 51), datetime.datetime(2030, 9, 16, 10, 19, 21)]]}}

        wgx_seg = {'WGX': {
            'JMAG_CALROLL': [
                [datetime.datetime(2030, 9, 4, 22, 57, 22), datetime.datetime(2030, 11, 5, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 22, 57, 22), datetime.datetime(2030, 9, 16, 22, 57, 22)]]}}

        self.assertEqual(wg_seg_basic.remove_seg_if_overlapping(wgx_seg, wg1_seg),
                         {'WGX':
                             {'JMAG_CALROLL': [[
                                 datetime.datetime(2030, 9, 15, 22, 57, 22),
                                 datetime.datetime(2030, 9, 16, 22, 57, 22)]]}})

        self.assertEqual(wg_seg_basic.remove_seg_if_overlapping(wgx_seg, wg4_seg), {'WGX': {}})

    def test_reset_wgx_segments_start_end(self):
        """
        Test Reset start and end with all segments from  wg_base with un duration > seg_min

        For instance for:
        - wol before DL_
        - to reduce DL_ duration
        """

        dl_ = {'GENERIC': {
            'DL_': [
                [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 17, 22, 00)],
                [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 16, 25, 00)]]}}

        fd_wol = wg_seg_basic.reset_wgx_segments_start_end(dl_, start_shift=-30 * 60, duration=30 * 60)
        self.assertEqual(wg_seg_basic.reset_wgx_segments_start_end(dl_, start_shift=-30 * 60, duration=30 * 60),
                         {'GENERIC': {
                             'DL_': [
                                 [datetime.datetime(2030, 9, 14, 13, 55, 30),
                                  datetime.datetime(2030, 9, 14, 14, 25, 30)],
                                 [datetime.datetime(2030, 9, 15, 13, 52, 0),
                                  datetime.datetime(2030, 9, 15, 14, 22, 0)]]}})

        self.assertEqual(wg_seg_basic.rename_wgx_segments(fd_wol, seg_new_names={'DL_': 'FD_WOL_WGX'}),
                         {'GENERIC': {
                             'FD_WOL_WGX': [
                                 [datetime.datetime(2030, 9, 14, 13, 55, 30),
                                  datetime.datetime(2030, 9, 14, 14, 25, 30)],
                                 [datetime.datetime(2030, 9, 15, 13, 52, 0),
                                  datetime.datetime(2030, 9, 15, 14, 22, 0)]]}})

    def test_select_wgx_subset_by_phases(self):
        """
        Test the extraction of a subset of Working Group (WG) and/or segments
        from a given wgx and for a given list of intervals
        """

        from juice_segmentation.commons.mission_phases import MissionPhase

        mission_phase = MissionPhase('Phase_2', '...',
                                     datetime.datetime(2030, 9, 15, 0, 0, 0),
                                     datetime.datetime(2030, 9, 16, 0, 0, 0))

        dl_ = {'GENERIC': {
            'DL_': [
                [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 17, 22, 00)],
                [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 16, 25, 00)]]}}

        self.assertEqual(wg_seg_basic.select_wgx_subset_by_mission_phases(dl_, mission_phases=[mission_phase]),
                         {'GENERIC': {
                             'DL_': [[datetime.datetime(2030, 9, 15, 14, 22, 00),
                                      datetime.datetime(2030, 9, 15, 17, 22, 00)]]}})

    def test_select_wgx_subset_by_time(self):
        """
        Test the extraction of a subset of Working Group (WG) and/or segments
        from a given wgx and for a given list of intervals
        :return:
        """

        dl_ = {'GENERIC': {
            'DL_': [
                [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 17, 22, 00)],
                [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 16, 25, 00)]]}}

        self.assertEqual(wg_seg_basic.select_wgx_subset_by_time(dl_, intervals=[
            [datetime.datetime(2030, 9, 15, 0, 0, 0), datetime.datetime(2030, 9, 15, 17, 22, 00)]]),
                         {'GENERIC': {
                             'DL_': [[datetime.datetime(2030, 9, 15, 14, 22, 00),
                                      datetime.datetime(2030, 9, 15, 17, 22, 00)]]}})

        self.assertEqual(wg_seg_basic.select_wgx_subset_by_time(dl_, intervals=[
            [datetime.datetime(2031, 9, 15, 0, 0, 0), datetime.datetime(2031, 9, 15, 17, 22, 00)]]),
                         {'GENERIC': {}})

    def test_get_instances_of_wg_seg(self):
        """
        Test selection of a subset of instance numbers for a given  Working Group (WG) and segment
        """

        dl_ = {'GENERIC': {
            'DL_': [
                [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 17, 22, 00)],
                [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 16, 25, 00)]]}}

        self.assertEqual(wg_seg_basic.get_instances_of_wg_seg(dl_, 'GENERIC', 'DL_', interval_numbers=[0, 2]),
                         {'GENERIC': {
                             'DL_': [
                                 [datetime.datetime(2030, 9, 14, 14, 25, 30),
                                  datetime.datetime(2030, 9, 14, 22, 57, 22)],
                                 [datetime.datetime(2030, 9, 16, 14, 18, 40),
                                  datetime.datetime(2030, 9, 16, 16, 25, 00)]]}})

    def test_merge_wgx_segments(self):
        """
        Test merging segments in wg_base merging wg_base and wg_to_chek wg/seg/intervals
        """

        wg1 = {
            'WG1': {
                'CALLISTO_FLYBY_3GM': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}

        wg2 = {
            'WG1': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 12, 5, 22, 57, 22)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 22, 0, 1), datetime.datetime(2030, 11, 5, 22, 57, 22)]]},
            'WG3': {
                'JUPITER_CPS': [
                    [datetime.datetime(2031, 10, 4, 22, 57, 22), datetime.datetime(2031, 10, 5, 10, 0, 1)]]}}

        self.assertEqual(wg_seg_basic.merge_wgx_segments(wg1, wg2),
                         {'WG1': {
                             'CALLISTO_FLYBY_3GM': [
                                 [datetime.datetime(2030, 10, 4, 22, 57, 22),
                                  datetime.datetime(2030, 10, 5, 22, 57, 22)]],
                             'EUROPA_FLYBY_1': [
                                 [datetime.datetime(2030, 10, 4, 22, 57, 22),
                                  datetime.datetime(2030, 12, 5, 22, 57, 22)]]},
                             'WG2': {
                                 'EUROPA_FLYBY_1': [
                                     [datetime.datetime(2030, 10, 5, 10, 0, 1),
                                      datetime.datetime(2030, 11, 5, 22, 57, 22)]]},
                             'WG3': {
                                 'JUPITER_CPS': [
                                     [datetime.datetime(2031, 10, 4, 22, 57, 22),
                                      datetime.datetime(2031, 10, 5, 10, 0, 1)]]}})

    def test_get_wg_overlaps(self):
        """
        Test wg/segment/interval overlaps

        1) check WG1/CALLISTO_FLYBY_3GM interval is overlapped by a wg2 segment (actually EUROPA_FLYBY_1 one)
        2) check WG1/segment/intervals are not overlapped by WG3 ones
        """

        wg_seg_basic = WgSegBasicOps()

        wg1 = {
            'WG1': {
                'CALLISTO_FLYBY_3GM': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}

        wg2 = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 12, 5, 22, 57, 22)]]}}

        wg3 = {'WG3': {
            'JUPITER_CPS': [
                [datetime.datetime(2031, 10, 4, 22, 57, 22), datetime.datetime(2031, 10, 5, 10, 00, 1)]]}}

        self.assertEqual(wg_seg_basic.get_overlaps(wg1, wg2), (True, {
            'WG1': {
                'CALLISTO_FLYBY_3GM': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
            'WG2': {'EUROPA_FLYBY_1': [[datetime.datetime(2030, 10, 5, 10, 0, 1),
                                        datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}))

        self.assertEqual(wg_seg_basic.get_overlaps(wg1, wg3), (False, {'WG1': {}, 'WG2': {}}))

    def test_get_wg_no_overlaps(self):
        """
        Test wg/segment/interval no overlaps

        1) check WG1/segment/intervals not overlapped by a wg2 segments (actually WG1:CALLISTO_FLYBY_3GM ones)
        2) check WG1/segment/intervals  not overlapped by wg3 segments (actually WG1:CALLISTO_FLYBY_3GM first one )
        """

        wg1 = {
            'WG1': {
                'CALLISTO_FLYBY_3GM': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)],
                    [datetime.datetime(2030, 11, 4, 22, 57, 22), datetime.datetime(2030, 11, 5, 22, 57, 22)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}

        wg2 = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 12, 5, 22, 0, 0)]]}}

        wg21 = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 20, 0, 0)]]}}

        wg22 = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 11, 4, 23, 0, 0)]]}}

        self.assertEqual(wg_seg_basic.get_no_overlaps(wg1, wg2), (False, {'WG1': {}, 'WG2': {}}))
        self.assertEqual(wg_seg_basic.get_no_overlaps(wg1, wg21),
                         (True, {'WG1': {'CALLISTO_FLYBY_3GM': [
                             [datetime.datetime(2030, 10, 5, 20, 0),
                              datetime.datetime(2030, 10, 5, 22, 57, 22)],
                             [datetime.datetime(2030, 11, 4, 22, 57, 22),
                              datetime.datetime(2030, 11, 5, 22, 57, 22)]]},
                             'WG2': {'EUROPA_FLYBY_1': [
                                 [datetime.datetime(2030, 10, 5, 20, 0, 0),
                                  datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}))

        self.assertEqual(wg_seg_basic.get_no_overlaps(wg1, wg22),
                         (True, {'WG1': {'CALLISTO_FLYBY_3GM': [
                             [datetime.datetime(2030, 11, 4, 23, 0, 0),
                              datetime.datetime(2030, 11, 5, 22, 57, 22)]]},
                             'WG2': {}}))

    def test_get_all_wg_overlaps(self):
        """
        Test wg/segment/interval overlaps
        """

        wg1 = {
            'WG1': {
                'CALLISTO_FLYBY_3GM': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 22, 57, 22)]]}}

        wg2 = {'WG1': {
            'EUROPA_FLYBY_1': [
                [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 12, 5, 22, 57, 22)]]}}

        wg3 = {'WG3': {
            'JUPITER_CPS': [
                [datetime.datetime(2031, 10, 4, 22, 57, 22), datetime.datetime(2031, 10, 5, 10, 0, 1)]]}}

        self.assertEqual(wg_seg_basic.get_all_wg_overlaps(wg1, [wg2, wg3]), True)
        self.assertEqual(wg_seg_basic.get_all_wg_overlaps(wg3, [wg1, wg2]), False)

    def test_join_wg_segments_at_given_time(self):
        """

        Test join wg/segment/interval at a given time
        """

        join_time = datetime.datetime(2033, 5, 23, 19, 0, 0)

        wg4 = {'WG4': {
            'JUPITER_MONITORING': [
                [datetime.datetime(2033, 5, 23, 9, 38, 51), join_time],
                [datetime.datetime(2033, 5, 23, 9, 52, 11), join_time],
                [datetime.datetime(2033, 5, 23, 17, 12, 11), join_time]]}}

        next_wg4 = {'WG4': {
            'JUPITER_MONITORING': [
                [join_time, datetime.datetime(2033, 5, 23, 19, 38, 51)],
                [join_time, datetime.datetime(2033, 5, 23, 19, 52, 11)],
                [join_time, datetime.datetime(2033, 5, 24, 3, 12, 11)]]}}

        wg4_join = {'WG4': {
            'JUPITER_MONITORING': [
                [datetime.datetime(2033, 5, 23, 9, 38, 51), datetime.datetime(2033, 5, 23, 19, 38, 51)],
                [datetime.datetime(2033, 5, 23, 9, 52, 11), datetime.datetime(2033, 5, 23, 19, 52, 11)],
                [datetime.datetime(2033, 5, 23, 17, 12, 11), datetime.datetime(2033, 5, 24, 3, 12, 11)]]}}

        self.assertEqual(wg_seg_basic.join_wg_segments_at_given_time(wg4, next_wg4, join_time), wg4_join)

    def test_remove_gaps_wgx_segments(self):
        """
        Test cleanup of wb_base segments joining segments with gap duration <= seg_min
        """

        max_gap_time_sec = 36 * 3600

        wg2 = {'WG2': {
            'JUPITER_MONITORING': [
                [datetime.datetime(2033, 5, 23, 00, 00, 00), datetime.datetime(2033, 5, 23, 13, 00, 00)],
                [datetime.datetime(2033, 5, 25, 00, 00, 11), datetime.datetime(2033, 5, 25, 12, 30, 00)],
                [datetime.datetime(2033, 5, 27, 00, 00, 00), datetime.datetime(2033, 5, 27, 14, 00, 00)],
                [datetime.datetime(2033, 6, 23, 00, 00, 00), datetime.datetime(2033, 6, 23, 13, 00, 00)],
                [datetime.datetime(2033, 6, 25, 00, 00, 11), datetime.datetime(2033, 6, 25, 12, 30, 00)],
                [datetime.datetime(2033, 7, 23, 00, 00, 00), datetime.datetime(2033, 7, 23, 13, 00, 00)],
            ]}}

        wg2_result = {'WG2': {
            'JUPITER_MONITORING': [
                [datetime.datetime(2033, 5, 23, 00, 00, 00), datetime.datetime(2033, 5, 27, 14, 00, 00)],
                [datetime.datetime(2033, 6, 23, 00, 00, 00), datetime.datetime(2033, 6, 25, 12, 30, 00)],
                [datetime.datetime(2033, 7, 23, 00, 00, 00), datetime.datetime(2033, 7, 23, 13, 00, 00)],
            ]}}

        self.assertEqual(wg_seg_basic.remove_gaps_wgx_segments(wg2, max_gap_time_sec), wg2_result)
