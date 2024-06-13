"""
Created on Jun 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to test utest_wg_segment_prime_mapping

"""
import os
import pathlib
import unittest
import datetime

import juice_segmentation.wg.wg_utils as wg_utils
import juice_segmentation.wg.wg_seg_prime_mapping as wg_seg_prime_mapping
from esac_juice_pyutils.commons.my_log import setup_logger

current_location = (pathlib.Path(__file__).parent.resolve())
setup_logger('info')

# Create temporal representative OPPORTUNITY_PRIME_CORRESPONDENCE.csv for testing
OPPORTUNITY_PRIME_CORRESPONDENCE = os.path.join(current_location, "data/OPPORTUNITY_PRIME_correspondance_test.csv")

mission_timeline_event_file = os.path.join(current_location, 'data/mission_timeline_event_file_5_0_PE_FB.csv')

wgx = {
    'WG1': {
        'GANYMEDE_FLYBY_GALA': [[datetime.datetime(2030, 10, 4, 0, 0, 0), datetime.datetime(2030, 10, 5, 0, 0, 0)]]},
    'WG2': {
        'EUROPA_FB_RS': [[datetime.datetime(2030, 10, 5, 0, 0, 0), datetime.datetime(2030, 10, 6, 0, 0, 0)]]},
    'WG3': {
        'GANYMEDE_GM': [[datetime.datetime(2030, 10, 6, 0, 0, 0), datetime.datetime(2030, 10, 7, 0, 0, 0)]]},
    'WG4': {
        'JUPITER_PERIJOVE': [[datetime.datetime(2030, 10, 7, 0, 0, 0), datetime.datetime(2030, 10, 8, 0, 0, 0)]],
        'JUPITER_PHASE_MAX': [[datetime.datetime(2030, 10, 8, 0, 0, 0), datetime.datetime(2030, 10, 9, 0, 0, 0)]],
        'INCLINED_NORTH': [[datetime.datetime(2030, 10, 10, 0, 0, 0), datetime.datetime(2030, 10, 11, 0, 0, 0)]]},
    'WGX': {
        'JMAG_CALROLL': [[datetime.datetime(2030, 10, 11, 0, 0, 0), datetime.datetime(2030, 10, 12, 0, 0, 0)]]},
    'GENERIC': {
        'JUPITER_FD_WOL_FB': [[datetime.datetime(2030, 10, 12, 0, 0, 0), datetime.datetime(2030, 10, 13, 0, 0, 0)]]},
}


class MyTestCase(unittest.TestCase):

    def test_seg_opportunity_2_prime_seg(self):
        """
        Test segment to prime renaming

        - direct mapping as JMAG_CALROLL --> CAL
        - specific ones as FLYBYs and Perijoves
        - n to 1 primes as INCLINED_NORTH --> JA_INCL
        - wild-card as JUPITER_PHASE_MAX via JUPITER_PHASE_* --> JA_PH
        """

        opportunity_vs_prime, dummy = wg_utils.get_prime_names(OPPORTUNITY_PRIME_CORRESPONDENCE)

        self.assertEqual(wg_seg_prime_mapping.seg_opportunity_2_prime_seg(wgx, opportunity_vs_prime),
                         {'GENERIC': {'J_FD_WOL_FB': [[datetime.datetime(2030, 10, 12, 0, 0),
                                                       datetime.datetime(2030, 10, 13, 0, 0)]]},
                          'WG1': {'G_GPH_xx': [[datetime.datetime(2030, 10, 4, 0, 0),
                                                datetime.datetime(2030, 10, 5, 0, 0)]]},
                          'WG2': {'E_RS_xx': [[datetime.datetime(2030, 10, 5, 0, 0),
                                               datetime.datetime(2030, 10, 6, 0, 0)]]},
                          'WG3': {'G_IS_xx': [[datetime.datetime(2030, 10, 6, 0, 0),
                                               datetime.datetime(2030, 10, 7, 0, 0)]]},
                          'WG4': {'JA_INCL': [[datetime.datetime(2030, 10, 10, 0, 0),
                                               datetime.datetime(2030, 10, 11, 0, 0)]],
                                  'JA_PExx': [[datetime.datetime(2030, 10, 7, 0, 0),
                                               datetime.datetime(2030, 10, 8, 0, 0)]],
                                  'JA_PH': [[datetime.datetime(2030, 10, 8, 0, 0),
                                             datetime.datetime(2030, 10, 9, 0, 0)]]},
                          'WGX': {'CAL': [[datetime.datetime(2030, 10, 11, 0, 0),
                                           datetime.datetime(2030, 10, 12, 0, 0)]]}}

                             )

    def test_is_prime_segment(self):
        """
        check if a segment is already prime
        """

        opportunity_vs_prime, dummy = wg_utils.get_prime_names(OPPORTUNITY_PRIME_CORRESPONDENCE)

        self.assertEqual(wg_seg_prime_mapping.is_prime_segment('WG4', 'JUPITER_MONITORING', opportunity_vs_prime), False)

        self.assertEqual(wg_seg_prime_mapping.is_prime_segment('WG4', 'JA_PE34', opportunity_vs_prime), True)

        self.assertEqual(wg_seg_prime_mapping.is_prime_segment('WG2', 'E_RS_14C7', opportunity_vs_prime), True)

    # def test_reset_opportunity_2_prime_seg_mapping_using_wild_card(self,):
    #     """
    #     Test segment to prime mapping extension using wildcards
    #
    #     - direct mapping as JMAG_CALROLL --> CAL
    #     - specific ones as FLYBYs and Perijoves
    #     - n to 1 primes as INCLINED_NORTH --> JA_INCL
    #     - wild-card as JUPITER_PHASE_MAX via JUPITER_PHASE_* --> JA_PH
    #     """
    #     from collections import namedtuple
    #
    #     f = open(OPPORTUNITY_PRIME_CORRESPONDENCE, "w")
    #     f.write("""OPPORTUNITY SEGMENT WG;OPPORTUNITY SEGMENT NAME ;CORRESPONDING PRIME NAME;COMMENTS,,,,,,,,,,,,,,,,,
    #     4;JUPITER_PHASE_MAX;JA_MX;,,,,,,,,,,,,,,,,,
    #     4;JUPITER_PHASE_*;JA_PH;,,,,,,,,,,,,,,,,,
    #     """)
    #     f.close()
    #
    #     wg4 = {
    #         'WG4': {
    #             'JUPITER_PHASE_MAX': [
    #                 [datetime.datetime(2030, 10, 8, 0, 0, 0), datetime.datetime(2030, 10, 9, 0, 0, 0)]],
    #             'JUPITER_PHASE_MIN': [
    #                 [datetime.datetime(2030, 10, 10, 0, 0, 0), datetime.datetime(2030, 10, 11, 0, 0, 0)]]}
    #     }
    #
    #     opportunity_vs_prime, dummy = wg_utils.get_prime_names(OPPORTUNITY_PRIME_CORRESPONDENCE)
    #
    #     opportunity_vs_prime_keys = sorted(opportunity_vs_prime.keys())
    #
    #     self.assertEqual(wg_seg_prime_mapping.reset_opportunity_2_prime_seg_mapping_using_wild_card(
    #         wg4, opportunity_vs_prime),
    #         {'GENERIC': {},
    #          'WG1': {},
    #          'WG2': {},
    #          'WG3': {},
    #          'WG4': {'JUPITER_PHASE_*': 'JA_PH',
    #                  'JUPITER_PHASE_MAX': 'JA_MX',
    #                  'JUPITER_PHASE_MIN': 'JA_PH'},
    #          'WGX': {}}
    #                      )

