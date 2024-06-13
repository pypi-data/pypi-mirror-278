"""
Created on August 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to test wg_segment_handler

"""

import unittest
import datetime

from juice_segmentation.wg.wg_segment_handler import WgSegmentHandler
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
segment_handler = WgSegmentHandler('./', OPPORTUNITY_PRIME_correspondance, mission_phases)


class MyTestCase(unittest.TestCase):

    def test_shift_fd_navfb(self):
        """
        Test all FD_NAV_FB against FD_WOL

        :return:
        """

        pass

        # wol = {'GENERIC': {
        #     'JUPITER_FD_WOL': [
        #         [datetime.datetime(2030, 9, 14, 14, 25, 30), datetime.datetime(2030, 9, 14, 14, 55, 30)],
        #         [datetime.datetime(2030, 9, 15, 14, 22, 00), datetime.datetime(2030, 9, 15, 14, 52, 00)],
        #         [datetime.datetime(2030, 9, 16, 14, 18, 40), datetime.datetime(2030, 9, 16, 14, 48, 40)]]}}
        #
        # nav = {'GENERIC': {
        #     'JUPITER_FD_NAV_FB': [
        #         [datetime.datetime(2030, 9, 13, 11, 55, 30), datetime.datetime(2030, 9, 13, 14, 25, 30)],
        #         [datetime.datetime(2030, 9, 14, 11, 55, 30), datetime.datetime(2030, 9, 14, 14, 25, 30)],
        #         [datetime.datetime(2030, 9, 15, 10, 22, 00), datetime.datetime(2030, 9, 15, 12, 52, 00)],
        #         [datetime.datetime(2030, 9, 16, 11, 18, 40), datetime.datetime(2030, 9, 16, 13, 48, 40)]]}}

        # self.assertEqual(shift_fd_navfb(nav, wol),
        #                  {'GENERIC': {
        #                      'JUPITER_FD_NAV_FB': [
        #                          [datetime.datetime(2030, 9, 14, 11, 55, 30),
        #                           datetime.datetime(2030, 9, 14, 14, 25, 30)],
        #                          [datetime.datetime(2030, 9, 15, 11, 52, 00),
        #                           datetime.datetime(2030, 9, 15, 14, 22, 00)],
        #                          [datetime.datetime(2030, 9, 16, 11, 48, 40),
        #                           datetime.datetime(2030, 9, 16, 14, 18, 40)]]}})

    # def test_shift_fd_wol(self):
    #     """
    #     Test all FD_WOL against DL
    #
    #     JUPITER_FD_WOL	2030-10-08T11:05:21Z	2030-10-08T13:05:21Z
    #     DL_	2030-10-08T13:05:21Z	2030-10-08T21:05:21Z
    #
    #     JUPITER_FD_WOL	2030-10-11T10:55:27Z	2030-10-11T12:55:27Z
    #     DL_	2030-10-11T12:55:31Z	2030-10-11T20:55:31Z
    #
    #     JUPITER_FD_WOL	2030-10-14T10:45:33Z	2030-10-14T12:45:33Z
    #     DL_	2030-10-14T12:45:31Z	2030-10-14T20:45:31Z
    #
    #     :return:
    #     """
    #
    #     wol = {'GENERIC': {
    #         'JUPITER_FD_WOL': [
    #             [datetime.datetime(2030, 10, 8, 11, 5, 21), datetime.datetime(2030, 10, 8, 13, 5, 21)],
    #             [datetime.datetime(2030, 10, 11, 10, 55, 27), datetime.datetime(2030, 10, 11, 12, 55, 27)],
    #             [datetime.datetime(2030, 10, 14, 10, 45, 33), datetime.datetime(2030, 10, 14, 12, 45, 33)]]}}
    #
    #     dl = {'GENERIC': {
    #         'DL_': [
    #             [datetime.datetime(2030, 10, 7, 13, 8, 21), datetime.datetime(2030, 10, 7, 21, 5, 21)],
    #             [datetime.datetime(2030, 10, 8, 13, 5, 21), datetime.datetime(2030, 10, 8, 21, 5, 21)],
    #             [datetime.datetime(2030, 10, 9, 13, 1, 51), datetime.datetime(2030, 10, 13, 21, 1, 51)],
    #             [datetime.datetime(2030, 10, 10, 12, 58, 51), datetime.datetime(2030, 10, 10, 21, 58, 51)],
    #             [datetime.datetime(2030, 10, 11, 12, 55, 31), datetime.datetime(2030, 10, 11, 20, 55, 31)],
    #             [datetime.datetime(2030, 10, 14, 12, 45, 31), datetime.datetime(2030, 10, 14, 20, 45, 31)]]}}
    #
    #     self.assertEqual(shift_fd_wol(wol, dl),
    #                      {'GENERIC': {
    #                          'JUPITER_FD_WOL': [
    #                              [datetime.datetime(2030, 10, 8, 11, 5, 21),
    #                               datetime.datetime(2030, 10, 8, 13, 5, 21)],
    #                              [datetime.datetime(2030, 10, 11, 10, 55, 27),
    #                               datetime.datetime(2030, 10, 11, 12, 55, 31)],
    #                              [datetime.datetime(2030, 10, 14, 10, 45, 33),
    #                               datetime.datetime(2030, 10, 14, 12, 45, 31)]]}})
