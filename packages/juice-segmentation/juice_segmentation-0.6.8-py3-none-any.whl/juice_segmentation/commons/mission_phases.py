"""
Created on July, 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) mission phase files
"""

import datetime
import logging
import os
import sys

import pandas as pd


class MissionPhase(object):
    """
    Mission Phase
    """

    def __init__(self, id, descr, start, end):
        self.id = id
        self.description = descr
        self.start = start
        self.end = end
        self.call_roll = []

    def to_string(self):
        return '{} ; [{} - {}]; {}; '.format(self.id, self.start, self.end, self.description)


class MissionPhases(object):
    """
    List of mission phases
    """

    pass


def get_mission_phases(input_file):
    """
    Read Working mission_phase file

    1) parse csv file

    :param input_file: path of the input file
    :return: generic_wg_2_prime
    """

    df = read_file(input_file, sep=',')

    mission_phases = {}

    for i in range(len(df)):
        identifier = df.iloc[i][0]
        description = df.iloc[i][1]
        start = parse_date_time(df.iloc[i][2])  # datetime.datetime.strptime(df.iloc[i][2], '%d/%m/%y')
        end = parse_date_time(df.iloc[i][3])  # datetime.datetime.strptime(df.iloc[i][3], '%d/%m/%y')

        mission_phases[identifier] = MissionPhase(identifier, description, start, end)

    return mission_phases


def print_mission_phases(phases):
    """
    Print mission Phases to standard output

    :param phases: phase and sub_phases
    """

    logging.info('Juice Mission Phases')
    for m in phases.keys():
        print('\t{}'.format(phases[m].to_string()))


def parse_date_time(str_date):
    """
        Parse date time

    :param str_date: date time provided a a string
    :return:
    """
    """
    Parse Mission phases period date time format to datetime object

    1) Try some specific format first
    2) use datetutils wich support most common formats
    :return:
    """

    from dateutil.parser import parse

    dt = None

    try:

        if dt is None:
            dt = parse(str_date)

    except IOError as e:
        logging.debug(("I/O error({0}): {1}".format(e.errno, e.strerror)))

    except ValueError:
        logging.debug(f'Bad date time format "{str_date}"')

    if dt is None:
        logging.debug('Cannot parse "{}" to datetime format!'.format(str_date))

    return dt


def read_file(input_file, header=[0], sep=','):
    """
    Read csv like file

    :param sep:
    :param header: specify header lines; default is None
    :param input_file: path of the csv file to read
    :return: df: panda data frame instance containing input data
    """

    if not os.path.exists(input_file):
        logging.error('input file "{}" not available'.format(input_file))
        sys.exit()  # event line output routine
    else:

        df = pd.read_csv(input_file, sep=sep, header=header, comment='#', engine='python')

    return df


if __name__ == '__main__':
    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    print(here)
    print(test_dir)

    setup_logger('debug')
    print(os.getcwd())

    print('\n-----------------------------------------------\n')

    logging.debug('Start of test')

    mission_phases = get_mission_phases('../test_files/config/crema_3.2/Mission_phases.txt')

    logging.debug('End of test')
