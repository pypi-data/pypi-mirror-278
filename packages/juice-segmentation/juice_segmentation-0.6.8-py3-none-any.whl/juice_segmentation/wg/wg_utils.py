"""
Created on July 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) segmentation files
"""

import datetime
import logging
import os
import sys

import pandas as pd


def get_prime_names(input_file):
    """
    Read Working group (WG) corresponding table a build lookup table between prime segment and generic names

    1) parse csv file

    :param input_file: path of the input file
    :return: generic_wg_2_prime
    """

    logging.debug('Parsing OPPORTUNITY_PRIME_correspondance file: {}'.format(input_file))

    df = read_file(input_file, sep=';')

    seg_2_prime = {'WG1': {}, 'WG2': {}, 'WG3': {}, 'WG4': {}, 'WGX': {}, 'GENERIC': {}}
    mult_segs_2_prime = {'WG1': [], 'WG2': [], 'WG3': [], 'WG4': [], 'WGX': [], 'GENERIC': []}

    for i in range(len(df)):

        segment_mapping = df.iloc[i]

        if str(segment_mapping[0]) in ['1', '2', '3', '4', 'X', 'GENERIC']:

            check_record(i, df)

            wg_label = 'WG{}'.format(segment_mapping[0])
            if segment_mapping[0] == 'GENERIC':
                wg_label = segment_mapping[0]

            seg_name_opportunity = df.iloc[i][1]
            seg_name_prime = df.iloc[i][2]

            if ',' in seg_name_opportunity:
                segment_opps = seg_name_opportunity.split(',')
                mult_segs_2_prime[wg_label].append([segment_opps, seg_name_prime])
                for segment_opp in segment_opps:
                    seg_2_prime[wg_label][segment_opp] = seg_name_prime
            else:
                seg_2_prime[wg_label][seg_name_opportunity] = seg_name_prime

    # Check if duplicated values in dico
    for wg in seg_2_prime:
        logging.debug('WG: {}'.format(wg))
        find_duplicated_values_in_dic(seg_2_prime[wg])

    return seg_2_prime, mult_segs_2_prime


def get_segments_type_original(input_file):
    """
    return all original (opportunity) segment types

    1) parse csv file

    :param input_file: path of the input file
    :return: generic_wg_2_prime
    """

    seg_2_prime, mult_segs_2_prime = get_prime_names(input_file)

    segment_types = {}

    for wg in seg_2_prime.keys():

        if wg not in segment_types.keys():

            segment_types[wg] = []

        for seg in seg_2_prime[wg].keys():

            segment_types[wg].append(seg)

    for wg in mult_segs_2_prime.keys():

        if wg not in segment_types.keys():
            segment_types[wg] = []

        for ele in mult_segs_2_prime[wg]:

            seg_list = ele[0]
            segment_types[wg].extend(seg_list)

    return segment_types


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

        df = pd.read_csv(input_file, sep=sep, header=header, comment='#')

    return df


def find_duplicated_values_in_dic(original_dict):
    """
    Check if duplicated mapping in OPPORTUNITY_PRIME_correspondance.csv

    :param original_dict: opportunity segment to prime mapping
    :return:
    """

    reverse_dict = {}
    for key, value in original_dict.items():

        if len(value) > 1:
            logging.debug("key: {} has multiple values: {}".format(key, value))

        if value in reverse_dict.keys():
            reverse_dict[value].append(key)
        else:
            reverse_dict[value] = [key]

    for key, value in reverse_dict.items():
        if len(value) > 1:
            logging.debug("key: {} has multiple values: {}".format(key, value))


def check_record(i, df):
    """
    Check if invalid record in OPPORTUNITY_PRIME_correspondance.csv

    :param i: df record
    :param df: panda data frame containing OPPORTUNITY_PRIME_correspondance mapping
    :return:
    """

    rec = df.iloc[i]

    wg = str(rec[0])
    segment_names = '{}'.format(rec[1])
    # segment_output_name = str(rec[2])

    line = wg + ';' + segment_names + ';;'

    # if not isinstance(rec[2], str):
    segment_output_name = str(rec[2])
    if segment_output_name == 'nan':
        logging.error('missing value for renamed segment ("$;;") in "{}'.format(
            line))


def set_date_vs_FB_PE_event(config_param):
    """
    Set mapping between FB_PE events and dates

    :param config_param: path of configuration file
    :return: date_vs_event, fb_pe_events
    """

    from juice_segmentation.commons.mission_timeline_event_file_handler import MissionTimelineEvent

    root_dir = config_param.root_path

    mission_timeline_event_file_path = os.path.expandvars(config_param.mission_timeline_event_file)
    if not os.path.exists(mission_timeline_event_file_path):
        mission_timeline_event_file_path = os.path.join(root_dir, mission_timeline_event_file_path)

    if not os.path.exists(mission_timeline_event_file_path):
        logging.error('file does not exists: {}'.format(mission_timeline_event_file_path))

    mission_timeline_event = MissionTimelineEvent(mission_timeline_event_file_path)
    date_vs_event = mission_timeline_event.get_flyby_and_pe_events()

    fb_pe_events = dict(map(reversed, date_vs_event.items()))

    return date_vs_event, fb_pe_events


def datetime2utc_json(date_time, dateformat='%Y-%m-%dT%H:%M:%S.%f'):
    """
    Translates a date time from datetime to utc string
                            "2030-05-27T09:15:00.000Z"
    :param date_time:
    :param dateformat:
    :return:
    """
    str_date_time = datetime.datetime.strftime(date_time, dateformat)
    str_date_time = str_date_time[:-3] + 'Z'

    return str_date_time


def json_str_2_datatime(str_date, dateformat=['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ'],
                        as_per_dateformat=False):
    """
    Translates a string date time to datetime
                            "2030-05-27T09:15:00.000Z"
    :param str_date: date string
    :param dateformat: lsit of date string format
    :param as_per_dateformat: only parse if in dateformat
    :return:
    """

    from dateutil.parser import parse

    eps_datetime_formats = dateformat

    dt = None

    error_value = ''

    for dt_format in eps_datetime_formats:

        try:

            dt = datetime.datetime.strptime(str_date, dt_format)

            if dt:
                break

        except IOError as e:
            logging.debug(("I/O error({0}): {1}".format(e.errno, e.strerror)))

        except ValueError:
            error_value = 'Bad date time format "{}"; Expected format is "{}"'.format(
                str_date, datetime.datetime.strftime(datetime.datetime.now(), dt_format))

    if not as_per_dateformat:  # Try to parse it anyway

        try:

            if dt is None:
                dt = parse(str_date)

        except IOError as e:
            logging.debug(("I/O error({0}): {1}".format(e.errno, e.strerror)))

        except ValueError:
            error_value = 'Bad date time format "{}"; Expected format is "{}"'.format(
                str_date, datetime.datetime.strftime(datetime.datetime.now(), dt_format))

    if dt is None:
        logging.debug('Cannot parse "{}" to datetime format!'.format(str_date))
        if error_value:
            logging.debug(error_value)

    return dt


def is_mask_in_keys(keys, value):

    for ele in keys:

        if value in ele:

            return True

    return False
