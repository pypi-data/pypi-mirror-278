"""
Created on August 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to test wg_segment_handler

"""

import unittest
import datetime

from juice_segmentation.report.metrics import Metrics

(start, end) = (datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1))
metrics = Metrics(start, end)

wg1 = {
    'WG1': {
        'CALLISTO_FLYBY_3GM_1': [
            [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)],
            [datetime.datetime(2030, 10, 6, 0, 0, 0), datetime.datetime(2030, 10, 6, 1, 0, 0)],
            [datetime.datetime(2030, 10, 6, 0, 30, 0), datetime.datetime(2030, 10, 6, 1, 0, 0)]]},
    'WG2': {
        'EUROPA_FLYBY_1': [
            [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 12, 0, 2)]]},
    'WG3': {
        'JUPITER_PERIJOVE_1': [
            [datetime.datetime(2031, 10, 4, 2, 0, 0), datetime.datetime(2031, 10, 4, 2, 10, 0)]]}}


class MyTestCase(unittest.TestCase):

    def test_get_wg_seg_intervals_1(self):
        """
        Test total time per wg and segment
        """

        self.assertEqual(metrics.get_wg_seg_intervals(wg1),
                         {'WG1': {
                             'CALLISTO_FLYBY_3GM_1': [
                                 [datetime.datetime(2030, 10, 4, 22, 57, 22),
                                  datetime.datetime(2030, 10, 5, 22, 57, 22)],
                                 [datetime.datetime(2030, 10, 6, 0, 0, 0),
                                  datetime.datetime(2030, 10, 6, 1, 0, 0)]]},
                             'WG2': {
                                 'EUROPA_FLYBY_1': [
                                     [datetime.datetime(2030, 10, 5, 10, 0, 1),
                                      datetime.datetime(2030, 10, 5, 12, 0, 2)]]},
                             'WG3': {
                                 'JUPITER_PERIJOVE_1': [
                                     [datetime.datetime(2031, 10, 4, 2, 0, 0),
                                      datetime.datetime(2031, 10, 4, 2, 10, 0)]]}})

    def test_get_wg_seg_intervals_2(self):
        """
        Test total time per wg and segment
        """

        self.assertEqual(metrics.get_wg_seg_intervals(wg1,
                                                      interval=[datetime.datetime(2030, 10, 6, 0, 0, 0),
                                                                datetime.datetime(2030, 10, 7, 0, 0, 0)]),
                         {'WG1': {
                             'CALLISTO_FLYBY_3GM_1': [
                                 [datetime.datetime(2030, 10, 6, 0, 0, 0),
                                  datetime.datetime(2030, 10, 6, 1, 0, 0)]]},
                             'WG2': {},
                             'WG3': {}})

    def test_get_segment_types_metrics(self):
        """
        Test total time per wg and segment type
        """

        self.assertEqual(metrics.get_segment_types_metrics([wg1]),
                         {'WG1': {'CALLISTO_FLYBY_3GM_1': 90000.0},
                          'WG2': {'EUROPA_FLYBY_1': 7201.0},
                          'WG3': {'JUPITER_PERIJOVE_1': 600.0}})

    def test_get_wg_seg_metrics(self):
        """
        Test total time per wg and segment
        """

        wg1 = {
            'WG1': {
                'CALLISTO_FLYBY_3GM_1': [
                    [datetime.datetime(2030, 10, 4, 22, 57, 22), datetime.datetime(2030, 10, 5, 22, 57, 22)],
                    [datetime.datetime(2030, 10, 6, 0, 0, 0), datetime.datetime(2030, 10, 6, 1, 0, 0)]]},
            'WG2': {
                'EUROPA_FLYBY_1': [
                    [datetime.datetime(2030, 10, 5, 10, 0, 1), datetime.datetime(2030, 10, 5, 12, 0, 2)]]},
            'WG3': {
                'JUPITER_PERIJOVE_1': [
                    [datetime.datetime(2031, 10, 4, 2, 0, 0), datetime.datetime(2031, 10, 4, 2, 10, 0)]]}}

        self.assertEqual(metrics.get_wg_seg_metrics(wg1, report_as_dico=False),
                         ([['Working Group', 'Sum Of times'],
                           ['WG1', 90000.0],
                           ['WG2', 7201.0],
                           ['WG3', 600.0]],
                          {'WG1': {'CALLISTO_FLYBY_3GM_1': 90000.0},
                           'WG2': {'EUROPA_FLYBY_1': 7201.0},
                           'WG3': {'JUPITER_PERIJOVE_1': 600.0}}))

    def test_get_wg_seg_metric_wgx(self):
        """
        Test total time per wg and segment for wgx
        """

        wgx = {'GENERIC': {
            'DL_': [
                [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 22, 57, 22)],
                [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 17, 22, 00)],
                [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 16, 25, 00)]],
            'FD_WOL_WGX': [
                [datetime.datetime(2030, 9, 14, 13, 55, 30), datetime.datetime(2030, 9, 14, 14, 25, 30)],
                [datetime.datetime(2030, 9, 15, 13, 52, 0), datetime.datetime(2030, 9, 15, 14, 22, 0)]]}}

        self.assertEqual(metrics.get_wg_seg_metrics(wgx),
                         ([['Working Group', 'Sum Of times'],
                           ['GENERIC', 52692.0]],
                          {'GENERIC': {'DL_': 49092.0, 'FD_WOL_WGX': 3600.0}}))

        self.assertEqual(metrics.get_wg_seg_metrics(wgx)[0],
                         ([['Working Group', 'Sum Of times'],
                           ['GENERIC', 52692.0]]))

        self.assertEqual(metrics.get_wg_seg_metrics(wgx)[1],
                         ({'GENERIC': {'DL_': 49092.0, 'FD_WOL_WGX': 3600.0}}))
