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

from tabulate import tabulate


class MissionTimelineEvent(object):
    """
    Juice mission timeline Event File Handler
    """

    def __init__(self, file_input, output_dir="./"):

        self.output_dir = output_dir

        self.input_file = file_input

        self.df = self.read_event_timeline_file()

    def read_event_timeline_file(self):
        """
        Read Juice mission timeline Event File
        :return: df
        """

        col_names = ['Event name', 'event time [utc]', 'contextual info']

        df = read_file(self.input_file, header=None, col_names=col_names)

        if df.iloc[0][0].startswith('Event name'):
            df.iloc[0][0] = '#' + df.iloc[0][0]

        df['datetime (UTC)'] = pd.to_datetime(df['event time [utc]'], format="%Y-%m-%dT%H:%M:%SZ", errors='ignore')
        df['datetime (UTC)'] = df['event time [utc]']
        df = df.drop(columns=['event time [utc]'])

        return df

    def get_flyby_and_pe_events(self):
        """
        Get Flyby and PErijove sub_phases from mission timeline event file

        :return: my_events: dictionary {Flyby and PErijove} vs datetime
        """

        df2 = self.df[self.df['Event name'].str.startswith('FLYBY_') |
                      self.df['Event name'].str.startswith('PERIJOVE_')]

        my_events = {}

        for i in range(len(df2)):

            identifier = df2.iloc[i]['Event name']
            dt = df2.iloc[i]['datetime (UTC)']
            other = df2.iloc[i]['contextual info']

            if identifier.startswith('PERIJOVE_'):

                event_name = identifier.replace('PJ', '').replace('PERIJOVE_', 'PJ')

            elif identifier.startswith('FLYBY_'):

                event_name = other.split(';')[0].split()[-1]

            event_date = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')

            my_events[event_date] = event_name

        return my_events

    def get_sun_conjunctions(self, as_dico=True):
        """
        Get SUN_CONJUNCTION from mission timeline event file

        :return: return list of Sun Conjunctions periods
        """

        df2 = self.df[self.df['Event name'].str.startswith('SUN_CONJUNCTION_SUP')]

        my_tab = tabulate(df2, headers='keys', tablefmt='grid', numalign='center',
                          stralign='center',
                          showindex=False)

        if logging.DEBUG >= logging.root.level:
            print('\n' + my_tab + '\n')

        sun_conjunctions_periods = []

        start = datetime.datetime.strptime(df2.iloc[0]['datetime (UTC)'], '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.datetime.strptime(df2.iloc[-1]['datetime (UTC)'], '%Y-%m-%dT%H:%M:%SZ')

        for i in range(len(df2)):

            identifier = df2.iloc[i]['Event name']
            dt = df2.iloc[i]['datetime (UTC)']
            dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')

            if identifier.endswith('_START'):
                start = dt
            elif identifier.endswith('_END'):
                sun_conjunctions_periods.append([start, dt])

        # Check last conjunction ends; if not extend it until end
        if identifier.endswith('_START'):
            sun_conjunctions_periods.append([start, end])

        if as_dico:

            return {'SUN_CONJUNCTION_SUP': sun_conjunctions_periods}

        else:

            return sun_conjunctions_periods


def read_file(input_file, header=[0], sep=',', col_names=None):
    """
    Read csv like file

    :param header: specify header lines; default is None
    :param input_file: path of the csv file to read
    :param sep: cvs file separator (i.e, ",")
    :param col_names: list of column names; Defualt is None
    :return: df: panda data frame instance containing input data
    """

    if not os.path.exists(input_file):
        logging.error('input file "{}" not available'.format(input_file))
        sys.exit()  # event line output routine
    else:

        if col_names:

            df = pd.read_csv(input_file, sep=sep, header=None, comment='#', names=col_names)

        else:

            df = pd.read_csv(input_file, sep=sep, header=header, comment='#')

    return df
