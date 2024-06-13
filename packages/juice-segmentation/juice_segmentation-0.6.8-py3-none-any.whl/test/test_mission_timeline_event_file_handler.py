"""
Created on October, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) Juice mission timeline Event files
"""


import os
import sys
import logging
import datetime
import pandas as pd

from juice_segmentation.commons.mission_timeline_event_file_handler import MissionTimelineEvent


if __name__ == '__main__':

    from esac_juice_pyutils.commons.my_log import setup_logger
    from tabulate import tabulate

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)
    # root_dir = os.path.dirname(test_dir)

    print('pwd = {}'.format(here))
    print(test_dir)

    setup_logger('debug')
    print(os.getcwd())

    print('\n-----------------------------------------------\n')

    logging.debug('Start of test')

    mission_timeline_file = '../test_files/config/crema_3.0/mission_timeline_event_file_3_0.csv'

    p = MissionTimelineEvent(mission_timeline_file)

    # my_tab = tabulate(p.df[:5], headers='keys', tablefmt='grid', numalign='center',
    #                   stralign='center',
    #                   showindex=False)
    #
    # print('\n' + my_tab + '\n')

    logging.info('\nMission Sub-phases within {}\n'.format(mission_timeline_file))
    fb = p.get_flyby_and_pe_events()
    for k,v in fb.items():
        print('\t[{}]: {}'.format(k, v))

    logging.info('\nSolar Conjunction within {}\n'.format(mission_timeline_file))
    sun_conjuntions = p.get_sun_conjunctions(False)
    for i in range(len(sun_conjuntions)):
        print('[{}]: {}'.format(i, sun_conjuntions[i]))

    sun_conjuntions = p.get_sun_conjunctions()
    for k, v in sun_conjuntions.items():
        print('[{}]: {}\n'.format(k, v))

    logging.debug('End of test')





