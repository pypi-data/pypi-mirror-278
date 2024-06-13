"""
Created on Jun 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to test utest_wg_segment_prime_mapping

"""

import os
import pathlib
import unittest
import datetime
from collections import namedtuple

import juice_segmentation.wg.wg_utils as wg_utils
from esac_juice_pyutils.commons.my_log import setup_logger

current_location = (pathlib.Path(__file__).parent.resolve())
setup_logger('info')

# Create temporal representative OPPORTUNITY_PRIME_CORRESPONDENCE.csv for testing
OPPORTUNITY_PRIME_CORRESPONDENCE = os.path.join(current_location, "data/OPPORTUNITY_PRIME_correspondance_test.csv")

# f = open(OPPORTUNITY_PRIME_CORRESPONDENCE, "w")
# f.write("""OPPORTUNITY SEGMENT WG;OPPORTUNITY SEGMENT NAME ;CORRESPONDING PRIME NAME;COMMENTS,,,,,,,,,,,,,,,,,
# 1;GANYMEDE_FLYBY_GALA;G_GPH_xx;xx: name of the flyby (crema name: 2G2),,,,,,,,,,,,,,,,,
# 2;EUROPA_FB_RS;E_RS_xx;xx: name of the flyby (crema name: 6E1),,,,,,,,,,,,,,,,,
# 3;GANYMEDE_GM;G_IS_xx;xx: name of the flyby (crema name: 2G2),,,,,,,,,,,,,,,,,
# 4;JUPITER_PERIJOVE;JA_PExx;xx: reference number of the perijove (1 to 50). E.g. JA_PE46,,,,,,,,,,,,,,,,,
# 4;JUPITER_PHASE_*;JA_PH;,,,,,,,,,,,,,,,,,
# 4;INCLINED_NORTH,INCLINED_SOUTH;JA_INCL;,,,,,,,,,,,,,,,,
# X;JMAG_CALROLL;CAL;,,,,,,,,,,,,,,,,,
# GENERIC;JUPITER_FD_WOL_FB;J_FD_WOL_FB;,,,,,,,,,,,,,,,,,
# """)
# f.close()

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
        'JUPITER_PHASE_*': [[datetime.datetime(2030, 10, 8, 0, 0, 0), datetime.datetime(2030, 10, 9, 0, 0, 0)]],
        'INCLINED_NORTH': [[datetime.datetime(2030, 10, 10, 0, 0, 0), datetime.datetime(2030, 10, 11, 0, 0, 0)]]},
    'WGX': {
        'JMAG_CALROLL': [[datetime.datetime(2030, 10, 11, 0, 0, 0), datetime.datetime(2030, 10, 12, 0, 0, 0)]]},
    'GENERIC': {
        'JUPITER_FD_WOL_FB': [[datetime.datetime(2030, 10, 12, 0, 0, 0), datetime.datetime(2030, 10, 13, 0, 0, 0)]]},
}


class MyTestCase(unittest.TestCase):
    maxDiff = None

    def test_get_prime_names(self):
        """
        Test seg2prime mapp generation from input file
        """

        self.assertEqual(wg_utils.get_prime_names(OPPORTUNITY_PRIME_CORRESPONDENCE),
                         ({'GENERIC': {'JUPITER_FD_WOL_FB': 'J_FD_WOL_FB'},
                           'WG1': {'GANYMEDE_FLYBY_GALA': 'G_GPH_xx'},
                           'WG2': {'EUROPA_FB_RS': 'E_RS_xx'},
                           'WG3': {'GANYMEDE_GM': 'G_IS_xx'},
                           'WG4': {'INCLINED_NORTH': 'JA_INCL',
                                   'INCLINED_SOUTH': 'JA_INCL',
                                   'JUPITER_PERIJOVE': 'JA_PExx',
                                   'JUPITER_PHASE_*': 'JA_PH'},
                           'WGX': {'JMAG_CALROLL': 'CAL'}},
                          {'GENERIC': [],
                           'WG1': [],
                           'WG2': [],
                           'WG3': [],
                           'WG4': [[['INCLINED_NORTH', 'INCLINED_SOUTH'], 'JA_INCL']],
                           'WGX': []}))

    def test_get_segments_type_original(self):
        """
        Test get_segments_type_original which allows to extract list of original segment
        """

        self.assertEqual(wg_utils.get_segments_type_original(OPPORTUNITY_PRIME_CORRESPONDENCE),
                         {'GENERIC': ['JUPITER_FD_WOL_FB'],
                          'WG1': ['GANYMEDE_FLYBY_GALA'],
                          'WG2': ['EUROPA_FB_RS'],
                          'WG3': ['GANYMEDE_GM'],
                          'WG4': ['JUPITER_PERIJOVE',
                                  'JUPITER_PHASE_*',
                                  'INCLINED_NORTH',
                                  'INCLINED_SOUTH',
                                  'INCLINED_NORTH',
                                  'INCLINED_SOUTH'],
                          'WGX': ['JMAG_CALROLL']})

    def test_set_date_vs_FB_PE_event(self):
        """
        Test set_date_vs_FB_PE_event which allows mapp flyby and Perijoves
        """

        config = {'root_path': './',
                  'mission_timeline_event_file': mission_timeline_event_file}

        config_param = namedtuple('Struct', config.keys())(*config.values())

        self.assertEqual(wg_utils.set_date_vs_FB_PE_event(config_param),
                         ({datetime.datetime(2031, 7, 21, 7, 14, 23): '1G1',
                          datetime.datetime(2031, 7, 21, 20, 50, 23): 'PJ1',
                          datetime.datetime(2032, 2, 13, 23, 4, 50): '2G2',
                          datetime.datetime(2032, 2, 14, 14, 20, 17): 'PJ2',
                          datetime.datetime(2032, 4, 11, 4, 14, 26): '3G3',
                          datetime.datetime(2032, 4, 11, 22, 47, 32): 'PJ3',
                          datetime.datetime(2032, 5, 9, 18, 34, 32): '4G4',
                          datetime.datetime(2032, 5, 10, 14, 44, 34): 'PJ4',
                          datetime.datetime(2032, 6, 2, 1, 35, 42): 'PJ5',
                          datetime.datetime(2032, 6, 2, 21, 30, 34): '5G5',
                          datetime.datetime(2032, 6, 18, 9, 50, 9): 'PJ6',
                          datetime.datetime(2032, 6, 21, 0, 37, 42): '6C1',
                          datetime.datetime(2032, 7, 2, 15, 20, 15): 'PJ7',
                          datetime.datetime(2032, 7, 2, 16, 22, 25): '7E1',
                          datetime.datetime(2032, 7, 16, 21, 19, 34): 'PJ8',
                          datetime.datetime(2032, 7, 16, 22, 17, 57): '8E2',
                          datetime.datetime(2032, 7, 29, 1, 49, 28): '9C2',
                          datetime.datetime(2032, 7, 31, 15, 20, 3): 'PJ9',
                          datetime.datetime(2032, 8, 14, 18, 13, 55): '10C3',
                          datetime.datetime(2032, 8, 17, 5, 44, 15): 'PJ10',
                          datetime.datetime(2032, 9, 8, 7, 1, 44): 'PJ11',
                          datetime.datetime(2032, 9, 10, 19, 24, 45): '11C4',
                          datetime.datetime(2032, 9, 24, 21, 33, 24): 'PJ12',
                          datetime.datetime(2032, 9, 27, 11, 59, 26): '12C5',
                          datetime.datetime(2032, 10, 11, 12, 25, 53): 'PJ13',
                          datetime.datetime(2032, 10, 14, 4, 28, 19): '13C6',
                          datetime.datetime(2032, 10, 28, 1, 47, 25): 'PJ14',
                          datetime.datetime(2032, 10, 30, 20, 53, 6): '14C7',
                          datetime.datetime(2032, 11, 13, 13, 53, 36): 'PJ15',
                          datetime.datetime(2032, 11, 16, 13, 16, 8): '15C8',
                          datetime.datetime(2032, 11, 30, 0, 45, 10): 'PJ16',
                          datetime.datetime(2032, 12, 3, 5, 36, 32): '16C9',
                          datetime.datetime(2032, 12, 13, 14, 20, 36): 'PJ17',
                          datetime.datetime(2032, 12, 27, 12, 25, 27): 'PJ18',
                          datetime.datetime(2033, 1, 10, 10, 18, 4): 'PJ19',
                          datetime.datetime(2033, 1, 24, 8, 6, 40): 'PJ20',
                          datetime.datetime(2033, 2, 7, 5, 42, 15): 'PJ21',
                          datetime.datetime(2033, 2, 21, 3, 7, 22): 'PJ22',
                          datetime.datetime(2033, 2, 24, 16, 8): '17C10',
                          datetime.datetime(2033, 3, 10, 2, 13, 14): 'PJ23',
                          datetime.datetime(2033, 3, 13, 8, 31, 8): '18C11',
                          datetime.datetime(2033, 3, 31, 20, 48, 29): 'PJ24',
                          datetime.datetime(2033, 4, 22, 3, 20): 'PJ25',
                          datetime.datetime(2033, 5, 10, 16, 8, 57): '19C12',
                          datetime.datetime(2033, 5, 13, 15, 35, 54): 'PJ26',
                          datetime.datetime(2033, 6, 1, 18, 4, 5): 'PJ27',
                          datetime.datetime(2033, 6, 4, 18, 37, 57): '20C13',
                          datetime.datetime(2033, 6, 18, 6, 57, 14): 'PJ28',
                          datetime.datetime(2033, 6, 21, 11, 1, 19): '21C14',
                          datetime.datetime(2033, 7, 5, 4, 35, 56): 'PJ29',
                          datetime.datetime(2033, 7, 8, 3, 23, 28): '22C15',
                          datetime.datetime(2033, 7, 22, 1, 6, 48): 'PJ30',
                          datetime.datetime(2033, 7, 24, 19, 45, 47): '23C16',
                          datetime.datetime(2033, 8, 7, 20, 28, 54): 'PJ31',
                          datetime.datetime(2033, 8, 10, 12, 13, 44): '24C17',
                          datetime.datetime(2033, 8, 28, 20, 27, 36): 'PJ32',
                          datetime.datetime(2033, 9, 18, 17, 3, 9): 'PJ33',
                          datetime.datetime(2033, 10, 9, 13, 23, 15): 'PJ34',
                          datetime.datetime(2033, 10, 30, 9, 50): 'PJ35',
                          datetime.datetime(2033, 11, 1, 22, 59, 43): '25C18',
                          datetime.datetime(2033, 11, 26, 23, 27, 20): 'PJ36',
                          datetime.datetime(2033, 11, 27, 6, 22, 15): '26G6',
                          datetime.datetime(2033, 12, 13, 6, 52, 14): 'PJ37',
                          datetime.datetime(2033, 12, 29, 20, 24, 21): 'PJ38',
                          datetime.datetime(2034, 1, 14, 18, 38, 52): '27G7',
                          datetime.datetime(2034, 1, 15, 16, 23, 31): 'PJ39',
                          datetime.datetime(2034, 1, 27, 3, 5, 8): 'PJ40',
                          datetime.datetime(2034, 2, 7, 13, 55, 32): 'PJ41',
                          datetime.datetime(2034, 2, 15, 0, 7, 43): '28C19',
                          datetime.datetime(2034, 2, 18, 5, 44, 7): 'PJ42',
                          datetime.datetime(2034, 3, 7, 12, 41, 3): 'PJ43',
                          datetime.datetime(2034, 3, 24, 21, 1, 23): 'PJ44',
                          datetime.datetime(2034, 4, 11, 5, 32, 48): 'PJ45',
                          datetime.datetime(2034, 4, 28, 13, 36, 19): 'PJ46',
                          datetime.datetime(2034, 5, 1, 22, 25, 5): '29C20',
                          datetime.datetime(2034, 5, 11, 0, 40, 6): 'PJ47',
                          datetime.datetime(2034, 5, 24, 2, 46, 13): 'PJ48',
                          datetime.datetime(2034, 6, 6, 6, 53, 16): '30G8',
                          datetime.datetime(2034, 6, 6, 14, 11, 28): 'PJ49',
                          datetime.datetime(2034, 6, 18, 1, 58, 9): 'PJ50',
                          datetime.datetime(2034, 6, 24, 5, 14, 44): '31C21',
                          datetime.datetime(2034, 6, 30, 17, 17, 39): 'PJ51',
                          datetime.datetime(2034, 7, 12, 7, 52, 5): '32G9',
                          datetime.datetime(2034, 7, 12, 15, 20, 1): 'PJ52',
                          datetime.datetime(2034, 7, 24, 1, 58, 56): 'PJ53',
                          datetime.datetime(2034, 8, 4, 12, 53, 54): 'PJ54',
                          datetime.datetime(2034, 8, 15, 23, 57, 29): 'PJ55',
                          datetime.datetime(2034, 8, 27, 11, 12, 54): 'PJ56',
                          datetime.datetime(2034, 9, 7, 18, 2, 57): '33G10',
                          datetime.datetime(2034, 9, 8, 0, 5, 38): 'PJ57',
                          datetime.datetime(2034, 9, 18, 17, 47, 3): 'PJ58',
                          datetime.datetime(2034, 9, 29, 6, 48, 16): '34G11',
                          datetime.datetime(2034, 9, 29, 13, 42, 47): 'PJ59',
                          datetime.datetime(2034, 10, 9, 14, 11, 46): 'PJ60',
                          datetime.datetime(2034, 10, 19, 15, 1, 36): 'PJ61',
                          datetime.datetime(2034, 10, 29, 15, 45, 38): 'PJ62',
                          datetime.datetime(2034, 11, 8, 16, 30, 53): 'PJ63',
                          datetime.datetime(2034, 11, 18, 22, 0, 34): '35G12',
                          datetime.datetime(2034, 11, 18, 23, 16, 8): 'PJ64',
                          datetime.datetime(2034, 11, 28, 17, 19, 2): 'PJ65',
                          datetime.datetime(2034, 12, 8, 6, 17, 48): 'PJ66',
                          datetime.datetime(2034, 12, 18, 13, 30, 49): 'PJ67'},
                         {'10C3': datetime.datetime(2032, 8, 14, 18, 13, 55),
                          '11C4': datetime.datetime(2032, 9, 10, 19, 24, 45),
                          '12C5': datetime.datetime(2032, 9, 27, 11, 59, 26),
                          '13C6': datetime.datetime(2032, 10, 14, 4, 28, 19),
                          '14C7': datetime.datetime(2032, 10, 30, 20, 53, 6),
                          '15C8': datetime.datetime(2032, 11, 16, 13, 16, 8),
                          '16C9': datetime.datetime(2032, 12, 3, 5, 36, 32),
                          '17C10': datetime.datetime(2033, 2, 24, 16, 8),
                          '18C11': datetime.datetime(2033, 3, 13, 8, 31, 8),
                          '19C12': datetime.datetime(2033, 5, 10, 16, 8, 57),
                          '1G1': datetime.datetime(2031, 7, 21, 7, 14, 23),
                          '20C13': datetime.datetime(2033, 6, 4, 18, 37, 57),
                          '21C14': datetime.datetime(2033, 6, 21, 11, 1, 19),
                          '22C15': datetime.datetime(2033, 7, 8, 3, 23, 28),
                          '23C16': datetime.datetime(2033, 7, 24, 19, 45, 47),
                          '24C17': datetime.datetime(2033, 8, 10, 12, 13, 44),
                          '25C18': datetime.datetime(2033, 11, 1, 22, 59, 43),
                          '26G6': datetime.datetime(2033, 11, 27, 6, 22, 15),
                          '27G7': datetime.datetime(2034, 1, 14, 18, 38, 52),
                          '28C19': datetime.datetime(2034, 2, 15, 0, 7, 43),
                          '29C20': datetime.datetime(2034, 5, 1, 22, 25, 5),
                          '2G2': datetime.datetime(2032, 2, 13, 23, 4, 50),
                          '30G8': datetime.datetime(2034, 6, 6, 6, 53, 16),
                          '31C21': datetime.datetime(2034, 6, 24, 5, 14, 44),
                          '32G9': datetime.datetime(2034, 7, 12, 7, 52, 5),
                          '33G10': datetime.datetime(2034, 9, 7, 18, 2, 57),
                          '34G11': datetime.datetime(2034, 9, 29, 6, 48, 16),
                          '35G12': datetime.datetime(2034, 11, 18, 22, 0, 34),
                          '3G3': datetime.datetime(2032, 4, 11, 4, 14, 26),
                          '4G4': datetime.datetime(2032, 5, 9, 18, 34, 32),
                          '5G5': datetime.datetime(2032, 6, 2, 21, 30, 34),
                          '6C1': datetime.datetime(2032, 6, 21, 0, 37, 42),
                          '7E1': datetime.datetime(2032, 7, 2, 16, 22, 25),
                          '8E2': datetime.datetime(2032, 7, 16, 22, 17, 57),
                          '9C2': datetime.datetime(2032, 7, 29, 1, 49, 28),
                          'PJ1': datetime.datetime(2031, 7, 21, 20, 50, 23),
                          'PJ10': datetime.datetime(2032, 8, 17, 5, 44, 15),
                          'PJ11': datetime.datetime(2032, 9, 8, 7, 1, 44),
                          'PJ12': datetime.datetime(2032, 9, 24, 21, 33, 24),
                          'PJ13': datetime.datetime(2032, 10, 11, 12, 25, 53),
                          'PJ14': datetime.datetime(2032, 10, 28, 1, 47, 25),
                          'PJ15': datetime.datetime(2032, 11, 13, 13, 53, 36),
                          'PJ16': datetime.datetime(2032, 11, 30, 0, 45, 10),
                          'PJ17': datetime.datetime(2032, 12, 13, 14, 20, 36),
                          'PJ18': datetime.datetime(2032, 12, 27, 12, 25, 27),
                          'PJ19': datetime.datetime(2033, 1, 10, 10, 18, 4),
                          'PJ2': datetime.datetime(2032, 2, 14, 14, 20, 17),
                          'PJ20': datetime.datetime(2033, 1, 24, 8, 6, 40),
                          'PJ21': datetime.datetime(2033, 2, 7, 5, 42, 15),
                          'PJ22': datetime.datetime(2033, 2, 21, 3, 7, 22),
                          'PJ23': datetime.datetime(2033, 3, 10, 2, 13, 14),
                          'PJ24': datetime.datetime(2033, 3, 31, 20, 48, 29),
                          'PJ25': datetime.datetime(2033, 4, 22, 3, 20),
                          'PJ26': datetime.datetime(2033, 5, 13, 15, 35, 54),
                          'PJ27': datetime.datetime(2033, 6, 1, 18, 4, 5),
                          'PJ28': datetime.datetime(2033, 6, 18, 6, 57, 14),
                          'PJ29': datetime.datetime(2033, 7, 5, 4, 35, 56),
                          'PJ3': datetime.datetime(2032, 4, 11, 22, 47, 32),
                          'PJ30': datetime.datetime(2033, 7, 22, 1, 6, 48),
                          'PJ31': datetime.datetime(2033, 8, 7, 20, 28, 54),
                          'PJ32': datetime.datetime(2033, 8, 28, 20, 27, 36),
                          'PJ33': datetime.datetime(2033, 9, 18, 17, 3, 9),
                          'PJ34': datetime.datetime(2033, 10, 9, 13, 23, 15),
                          'PJ35': datetime.datetime(2033, 10, 30, 9, 50),
                          'PJ36': datetime.datetime(2033, 11, 26, 23, 27, 20),
                          'PJ37': datetime.datetime(2033, 12, 13, 6, 52, 14),
                          'PJ38': datetime.datetime(2033, 12, 29, 20, 24, 21),
                          'PJ39': datetime.datetime(2034, 1, 15, 16, 23, 31),
                          'PJ4': datetime.datetime(2032, 5, 10, 14, 44, 34),
                          'PJ40': datetime.datetime(2034, 1, 27, 3, 5, 8),
                          'PJ41': datetime.datetime(2034, 2, 7, 13, 55, 32),
                          'PJ42': datetime.datetime(2034, 2, 18, 5, 44, 7),
                          'PJ43': datetime.datetime(2034, 3, 7, 12, 41, 3),
                          'PJ44': datetime.datetime(2034, 3, 24, 21, 1, 23),
                          'PJ45': datetime.datetime(2034, 4, 11, 5, 32, 48),
                          'PJ46': datetime.datetime(2034, 4, 28, 13, 36, 19),
                          'PJ47': datetime.datetime(2034, 5, 11, 0, 40, 6),
                          'PJ48': datetime.datetime(2034, 5, 24, 2, 46, 13),
                          'PJ49': datetime.datetime(2034, 6, 6, 14, 11, 28),
                          'PJ5': datetime.datetime(2032, 6, 2, 1, 35, 42),
                          'PJ50': datetime.datetime(2034, 6, 18, 1, 58, 9),
                          'PJ51': datetime.datetime(2034, 6, 30, 17, 17, 39),
                          'PJ52': datetime.datetime(2034, 7, 12, 15, 20, 1),
                          'PJ53': datetime.datetime(2034, 7, 24, 1, 58, 56),
                          'PJ54': datetime.datetime(2034, 8, 4, 12, 53, 54),
                          'PJ55': datetime.datetime(2034, 8, 15, 23, 57, 29),
                          'PJ56': datetime.datetime(2034, 8, 27, 11, 12, 54),
                          'PJ57': datetime.datetime(2034, 9, 8, 0, 5, 38),
                          'PJ58': datetime.datetime(2034, 9, 18, 17, 47, 3),
                          'PJ59': datetime.datetime(2034, 9, 29, 13, 42, 47),
                          'PJ6': datetime.datetime(2032, 6, 18, 9, 50, 9),
                          'PJ60': datetime.datetime(2034, 10, 9, 14, 11, 46),
                          'PJ61': datetime.datetime(2034, 10, 19, 15, 1, 36),
                          'PJ62': datetime.datetime(2034, 10, 29, 15, 45, 38),
                          'PJ63': datetime.datetime(2034, 11, 8, 16, 30, 53),
                          'PJ64': datetime.datetime(2034, 11, 18, 23, 16, 8),
                          'PJ65': datetime.datetime(2034, 11, 28, 17, 19, 2),
                          'PJ66': datetime.datetime(2034, 12, 8, 6, 17, 48),
                          'PJ67': datetime.datetime(2034, 12, 18, 13, 30, 49),
                          'PJ7': datetime.datetime(2032, 7, 2, 15, 20, 15),
                          'PJ8': datetime.datetime(2032, 7, 16, 21, 19, 34),
                          'PJ9': datetime.datetime(2032, 7, 31, 15, 20, 3)}))
