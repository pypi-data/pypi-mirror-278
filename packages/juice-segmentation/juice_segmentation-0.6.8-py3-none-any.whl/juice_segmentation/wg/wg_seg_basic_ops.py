"""
Created on september, 2019

@author: Claudio Munoz Crego (ESAC)

This Module is Wg class
"""

import logging
import os
import copy
import sys
import pandas as pd
import datetime

from operator import itemgetter

import esac_juice_pyutils.commons.tds as tds

from esac_juice_pyutils.periods.event_period_merger import PeriodMerger
from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers


class WgSegBasicOps(object):
    """
    The class include basic functionality for Working Groups Segment Handling
    """

    def add_wgx_segments(self, wg_base, wg_to_set):
        """
        Add or Overwrite wb_base segments with wg_to_set ones

        :param wg_base: baseline working group
        :param wg_to_set: wg_seg containing segments to be set or reset
        """

        for wg in wg_to_set:

            if wg not in wg_base.keys():
                wg_base[wg] = {}
                # logging.debug('{} added'.format(wg))

            for seg in sorted(wg_to_set[wg]):

                if seg not in wg_base[wg].keys():

                    wg_base[wg][seg] = wg_to_set[wg][seg]
                    # logging.debug('{} added'.format(seg))

                else:

                    wg_base[wg][seg] = wg_to_set[wg][seg]
                    # logging.debug('{} updated'.format(seg))

        return wg_base

    def wg_add(self, wg_base, list_of_wg_to_add, segment_minimun_sec=0):
        """
        Add or Overwrite wb_base segments with a list of list_of_wg_to_add

        :param wg_base: baseline working group
        :param list_of_wg_to_add: list of wg_seg containing segments to be add
        :param segment_minimun_sec: optional parameter allowing to remove any periods <=  segment_minimun_sec
        """

        new_wg_base = copy.deepcopy(wg_base)

        for wg in list_of_wg_to_add:
            new_wg_base = self.add_wgx_segments(new_wg_base, wg)

        if segment_minimun_sec > 0:
            new_wg_base = self.clean_wgx_segments(new_wg_base, segment_minimun_sec=segment_minimun_sec)

        return new_wg_base

    def wg_substract(self, wg_base, list_of_wg_to_substract, segment_minimun_sec=0):
        """
        Remove periods from wg_base instances overlapping with  list_of_wg_to_substract

        :param wg_base: baseline working group
        :param list_of_wg_to_substract: list of wg containing periods to be avoided in wg_base
        :param segment_minimun_sec: optional parameter allowing to remove any periods <=  segment_minimun_sec
        :return: new_wg_base: wg_base(periods) - list_of_wg_to_substract(periods)
        """

        new_wg_base = copy.deepcopy(wg_base)

        for wg in list_of_wg_to_substract:
            new_wg_base = self.get_wg_sub(new_wg_base, wg)

        new_wg_base = self.clean_wgx_segments(new_wg_base, segment_minimun_sec=segment_minimun_sec)

        return new_wg_base

    def get_wg_sub(self, wg_base, wg_to_substract, log_silence=True, date_format='%Y-%m-%dT%H:%M:%S'):
        """
        Remove periods from wg_base instances overlapping with wg_to_substract

        :param wg_base: baseline working group
        :param wg_to_substract: wg containing periods to be avoided in wg_base
        :param log_silence: flag to avoid logging if set to true
        :param date_format: datetime format used for logging
        :return: new_wg_base: wg_base(periods) - wg_to_substract(periods)
        """

        merge = PeriodMerger()

        new_wg_base = {}

        for wg in wg_base.keys():
            new_wg_base[wg] = {}
            for seg in sorted(wg_base[wg].keys()):
                seg_wg = wg_base[wg][seg]

                for sub_wg in wg_to_substract.keys():

                    for sub_seg in wg_to_substract[sub_wg].keys():

                        seg_wg = merge.get_event_sub(seg_wg, wg_to_substract[sub_wg][sub_seg])

                        if not log_silence:

                            overlap = merge.get_event_overlap(wg_base[wg][seg], wg_to_substract[sub_wg][sub_seg])
                            overlap = [x for x in overlap if (x[1] - x[0]).total_seconds() > 0]  # remove 0 intervals

                            if overlap:
                                overlap_str = self.datetime_list_2_str_list(overlap)
                                seg_wg1_str = self.datetime_list_2_str_list(wg_base[wg][seg])
                                seg_wg_str = self.datetime_list_2_str_list(seg_wg)
                                wg_to_substract_str = self.datetime_list_2_str_list(wg_to_substract[sub_wg][sub_seg])

                                logging.debug(
                                    'Overlap {} between {} {} and {} {}'.format(overlap_str, wg, seg, sub_wg, sub_seg))

                                logging.debug('{} - {} ==> {}'.format(seg_wg1_str, wg_to_substract_str, seg_wg_str))

                        if not seg_wg:  # Segment is empty
                            break

                new_wg_base[wg][seg] = seg_wg

        for wg in new_wg_base:
            seg_keys = list(new_wg_base[wg].keys())
            for k in seg_keys:
                if not new_wg_base[wg][k]:
                    # logging.debug('instance {} {} deleted!'.format(wg, k))
                    del (new_wg_base[wg][k])

        return new_wg_base

    def remove_seg_if_overlapping(self, wg_base, wg_to_chek):
        """
        Remove segments in wg_base instances overlapping with segments in wg_to_chek

        :param wg_base: baseline working group
        :param wg_to_chek:
        :return: new_wg_base: wg_base(periods) - wg_to_substract(periods)
        """

        from esac_juice_pyutils.periods.event_period_merger import PeriodMerger

        merge = PeriodMerger()

        for wg in wg_base.keys():

            for seg in sorted(wg_base[wg].keys()):

                for sub_wg in sorted(wg_to_chek.keys()):

                    for sub_seg in wg_to_chek[sub_wg].keys():

                        for i in reversed(range(len(wg_base[wg][seg]))):

                            seg_instance = wg_base[wg][seg][i]

                            overlap = merge.get_event_overlap([seg_instance], wg_to_chek[sub_wg][sub_seg])

                            if overlap:
                                overlap_str = self.datetime_list_2_str_list(overlap)

                                logging.info(
                                    'Overlap {0} between {1} {2} and {3} {4} ==> {1} {2} removed'.format(
                                        overlap_str, wg, seg, sub_wg, sub_seg))

                                del (wg_base[wg][seg][i])

                    if not wg_base[wg][seg]:
                        del (wg_base[wg][seg])

        return wg_base

    def datetime_list_2_str_list(self, wg_seg, date_format='%Y-%m-%dT%H:%M:%S'):
        """
        convert datetime list of datetime periods to a list of periods with date in format date_format

        :param wg_seg: working group segment
        :param date_format: datetime format
        :return: wg_seg_str
        """
        wg_seg_str = [[tds.datetime2utc(s, date_format), tds.datetime2utc(e, date_format)] for [s, e] in wg_seg]

        return wg_seg_str

    def merge_wgx_segments(self, wg_base, wg2):
        """
        Merge segments in wg_base merging wg_base and wg_to_check wg/seg/intervals

        :param wg_base: baseline working group
        :param wg2: wg to merge
        :return: new_wg_base: wg_base(periods) - wg_to_substract(periods)
        """

        p = IntervalHandlers()

        new_wg_base = copy.deepcopy(wg_base)

        wg_keys = wg_base.keys()

        wg2_keys_in_wg_keys = [x for x in wg2.keys() if x in wg_keys]
        wg2_keys_not_in_wg_keys = [x for x in wg2.keys() if x not in wg_keys]

        for k in wg2_keys_not_in_wg_keys:
            new_wg_base[k] = wg2[k]

        for wg in sorted(wg2_keys_in_wg_keys):

            wg2_seg_key_in_wg_seg_keys = [x for x in wg2[wg].keys() if x in wg_base[wg].keys()]
            wg2_seg_key_not_in_wg_seg_keys = [x for x in wg2[wg].keys() if x not in wg_base[wg].keys()]

            for k in wg2_seg_key_not_in_wg_seg_keys:
                new_wg_base[wg][k] = wg2[wg][k]

            for k in wg2_seg_key_in_wg_seg_keys:
                all_seg_instances = wg_base[wg][k] + wg2[wg][k]
                new_wg_base[wg][k] = p.merge_intervals(all_seg_instances)

        return new_wg_base

    def join_wg_segments_at_given_time(self, wg_base, wg2, join_time):
        """
        Join Segment at a given time

        :param wg_base:
        :param wg2:
        :param join_time:
        :return:
        """

        new_wg_base = copy.deepcopy(wg_base)

        wg_keys = wg_base.keys()

        wg2_keys_in_wg_keys = [x for x in wg2.keys() if x in wg_keys]
        wg2_keys_not_in_wg_keys = [x for x in wg2.keys() if x not in wg_keys]

        for k in wg2_keys_not_in_wg_keys:
            new_wg_base[k] = wg2[k]

        for wg in sorted(wg2_keys_in_wg_keys):

            wg2_seg_key_in_wg_seg_keys = [x for x in wg2[wg].keys() if x in wg_base[wg].keys()]
            wg2_seg_key_not_in_wg_seg_keys = [x for x in wg2[wg].keys() if x not in wg_base[wg].keys()]

            for k in wg2_seg_key_not_in_wg_seg_keys:
                new_wg_base[wg][k] = wg2[wg][k]

            for k in wg2_seg_key_in_wg_seg_keys:

                j_start = 0

                for i in range(len(wg_base[wg][k])):

                    if wg_base[wg][k][i][1] == join_time:

                        for j in range(j_start, len(wg2[wg][k])):

                            if wg2[wg][k][j][0] == join_time:

                                new_wg_base[wg][k][i][1] = wg2[wg][k][j][1]  # extend segment instance
                                break

                            else:

                                new_wg_base[wg][k].append(wg2[wg][k][j])

                        j_start = j + 1

                new_wg_base[wg][k].extend(wg2[wg][k][j_start:])  # add remaining segment
                new_wg_base[wg][k] = sorted(new_wg_base[wg][k], key=itemgetter(0, 1))

        return new_wg_base

    def select_wgx_subset(self, wg_seg, wg_filter=[], seg_filter=[]):
        """
        Extract a subset of Working Group (WG) and/or segments from a given wgx

        :param wg_seg: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter: list of labels to filter input wg_seg per segment type
        :return: new_wg_seg:  working group segment
        """

        new_seg_wg = {}

        wks_keys = wg_seg.keys()
        if wg_filter:
            wks_keys = [k for k in wg_seg.keys() if k in wg_filter]

        for wg in wks_keys:

            new_seg_wg[wg] = {}

            if not seg_filter:
                seg_filter = wg_seg[wg].keys()

            for seg in wg_seg[wg].keys():

                for label in seg_filter:

                    if label in seg:
                        new_seg_wg[wg][seg] = wg_seg[wg][seg]

        return new_seg_wg

    def remove_wgx_subset(self, wg_seg, wg_filter=[], seg_filter=[]):
        """
        Remove a subset of Working Group (WG) and/or segments from a given wgx

        :param wg_seg: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter: list of labels to filter input wg_seg per segment type
        :return: new_wg_seg:  working group segment
        """

        new_seg_wg = {}

        wks_keys = wg_seg.keys()
        if wg_filter:
            wks_keys = [k for k in wg_seg.keys() if k in wg_filter]

        for wg in wg_seg.keys():
            if wg not in wks_keys:
                new_seg_wg[wg] = wg_seg[wg]

        for wg in wks_keys:

            new_seg_wg[wg] = {}

            if not seg_filter:
                seg_filter = wg_seg[wg].keys()

            for seg in wg_seg[wg].keys():

                label_in_seg_filter = False
                for label in seg_filter:

                    if label in seg:
                        label_in_seg_filter = True

                if not label_in_seg_filter:
                    new_seg_wg[wg][seg] = wg_seg[wg][seg]

        return new_seg_wg

    def select_wgx_subset_by_mission_phases(self, wg_base, wg_filter=[], seg_filter=[], mission_phases=[]):
        """
        Extract a subset of Working Group (WG) and/or segments from a given wgx and for a given list of intervals

        :param wg_base: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter: list of labels to filter input wg_seg per segment type
        :param mission_phases: list of objects including mission phases id and periods
        :return: new_wg_seg:  working group segment
        """

        mission_phases_intervals = []

        for phase in mission_phases:
            mission_phases_intervals.append([phase.start, phase.end])

        if mission_phases_intervals:

            return self.select_wgx_subset_by_time(wg_base, wg_filter, seg_filter, mission_phases_intervals)

        else:

            logging.error('No mission phases intervals defined!')
            sys.exit()

    def get_first_segments(self, wg_base, wg_filter=[], seg_filter_orig=[]):

        """
        Return the first segment of Working Group (WG) and/or segments

        :param wg_base: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter_orig: list of labels to filter input wg_seg per segment type
        :return: last_seg_instance_prev, last_wg, last_seg: the last segment period [start,end], WG and segment name
        """

        first_seg_instance_prev = None
        first_wg = None
        first_seg = None

        wks_keys = list(wg_base.keys())

        if wg_filter:
            wks_keys = [k for k in wg_base.keys() if k in wks_keys]

        for wg in wks_keys:
            seg_filter = seg_filter_orig

            if not seg_filter:
                seg_filter = wg_base[wg].keys()

            for seg in sorted(wg_base[wg].keys()):

                for label in seg_filter:

                    if label in seg:

                        first_seg_instance = wg_base[wg][seg][0]

                        if first_seg_instance_prev:

                            if first_seg_instance[0] < first_seg_instance_prev[0]:
                                first_seg_instance_prev = first_seg_instance
                                first_wg = wg
                                first_seg = label

                        else:

                            first_seg_instance_prev = first_seg_instance
                            first_wg = wg
                            first_seg = label

        return first_seg_instance_prev, first_wg, first_seg

    def get_last_segments(self, wg_base, wg_filter=[], seg_filter_orig=[]):

        """
        Return the last segment of Working Group (WG) and/or segments

        :param wg_base: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter_orig: list of labels to filter input wg_seg per segment type
        :return: last_seg_instance_prev, last_wg, last_seg: the last segment period [start,end], WG and segment name
        """

        last_seg_instance_prev = None
        last_wg = None
        last_seg = None

        wks_keys = list(wg_base.keys())

        if wg_filter:
            wks_keys = [k for k in wg_base.keys() if k in wks_keys]

        for wg in wks_keys:
            seg_filter = seg_filter_orig

            if not seg_filter:
                seg_filter = wg_base[wg].keys()

            for seg in sorted(wg_base[wg].keys()):

                for label in seg_filter:

                    if label in seg:

                        if len(wg_base[wg][seg]) == 0:
                            print(wg, seg)

                        last_seg_instance = wg_base[wg][seg][-1]

                        if last_seg_instance_prev:

                            if last_seg_instance[1] > last_seg_instance_prev[1]:
                                last_seg_instance_prev = last_seg_instance
                                last_wg = wg
                                last_seg = label

                        else:

                            last_seg_instance_prev = last_seg_instance
                            last_wg = wg
                            last_seg = label

        return last_seg_instance_prev, last_wg, last_seg

    def select_wgx_subset_by_time(self, wg_base, wg_filter=[], seg_filter_orig=[], intervals=[],
                                  only_overllaping_periods=True):
        """
        Extract a subset of Working Group (WG) and/or segments from a given wgx and for a given list of intervals

        :param wg_base: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter_orig: list of labels to filter input wg_seg per segment type
        :param intervals: list of time intervals [[start, end], ...]
        :param only_overllaping_periods: by default return only the overlaping segment part
        :return: new_wg_seg:  working group segment
        """

        merge = PeriodMerger()

        new_seg_wg = copy.deepcopy(wg_base)

        wks_keys = list(new_seg_wg.keys())

        if wg_filter:
            wks_keys = [k for k in new_seg_wg.keys() if k in wks_keys]

        for wg in wks_keys:

            seg_filter = seg_filter_orig

            if not seg_filter:
                seg_filter = new_seg_wg[wg].keys()

            for seg in sorted(new_seg_wg[wg].keys()):

                for label in seg_filter:

                    if label in seg:

                        for i in reversed(range(len(new_seg_wg[wg][seg]))):

                            overlap = merge.get_event_overlap([new_seg_wg[wg][seg][i]], intervals)

                            if overlap:

                                # logging.debug('{} {} selected'.format(wg, seg))
                                if only_overllaping_periods:
                                    new_seg_wg[wg][seg][i] = overlap[0]

                            else:

                                del (new_seg_wg[wg][seg][i])

                if not new_seg_wg[wg][seg]:
                    del (new_seg_wg[wg][seg])

        return new_seg_wg

    def is_segment_within_time(self, wg_base, wg_filter=[], seg_filter=[], intervals=[]):
        """
        Check if is segment(s) intervals

        :param wg_base: working group segment (input)
        :param wg_filter: list of labels to filter input wg_seg per wg type
        :param seg_filter: list of labels to filter input wg_seg per segment type
        :param intervals: list of time intervals [[start, end], ...]
        :return: new_wg_seg:  working group segment
        """

        wg_seg = self.select_wgx_subset_by_time(wg_base, wg_filter, seg_filter, intervals)

        flag = False
        for wg in wg_seg:

            if len(list(wg_seg[wg])) > 0:
                flag = True
                break

        return flag

    def get_instances_of_wg_seg(self, wg_base, wg_id, seg_id, interval_numbers=[]):
        """
        get a subset of instance numbers for a given  Working Group (WG) and segment

        :param wg_base: working group segment (input)
        :param wg_id: working group identifier
        :param seg_id: segment identifier
        :param interval_numbers:
        :return: new_wg_seg:  working group segment
        """

        new_seg_wg = {wg_id: {seg_id: []}}

        nb_of_intervals = len(wg_base[wg_id][seg_id])

        for i in interval_numbers:

            if i >= nb_of_intervals:

                logging.warning('There is/are only {} intervals for {}:{}'.format(
                    nb_of_intervals, wg_id, seg_id))

                for j in range(nb_of_intervals):
                    print('\t{}: [{} - {}]'.format(j, wg_base[wg_id][seg_id][j][0], wg_base[wg_id][seg_id][j][1]))

                break

            else:

                new_seg_wg[wg_id][seg_id].append(wg_base[wg_id][seg_id][i])
                logging.debug('Segment {}:{}:{} selected!'.format(wg_id, seg_id, i))

        return new_seg_wg

    def get_intervals_of_wg_seg(self, wg_base, wg_id, seg_id):
        """
        get all intervals for a given  Working Group (WG) and segment

        :param wg_base: working group segment (input)
        :param wg_id: working group identifier
        :param seg_id: segment identifier
        :return: new_wg_seg:  working group segment
        """

        return wg_base[wg_id][seg_id]

    def clean_wgx_segments(self, wg_base, segment_minimun_sec=3 * 3600):
        """
        Clean wb_base segments removing segment with un duration < seg_min

        :param wg_base: baseline working group
        :param segment_minimun_sec: minimum duration for segment
        :return: wg_base: working group segment updated
        """

        segment_minimun = datetime.timedelta(seconds=segment_minimun_sec)

        wg_keys = list(wg_base.keys())
        for wg in wg_keys:

            if not wg_base[wg]:
                del (wg_base[wg])

            else:

                wg_seg_keys = sorted(wg_base[wg].keys())
                for seg in wg_seg_keys:

                    if not wg_base[wg][seg]:
                        del (wg_base[wg][seg])

                    else:
                        for i in reversed(range(len(wg_base[wg][seg]))):

                            (start, end) = tuple(wg_base[wg][seg][i])

                            if (end - start) < segment_minimun:
                                del (wg_base[wg][seg][i])
                                logging.debug(f'{wg} {seg}: [{start} - {end}] '
                                              f'Segment too short < {segment_minimun_sec} sec')
                            elif start == end:
                                del (wg_base[wg][seg][i])
                                logging.debug(f'{wg} {seg}: [{start} - {end}] Segment deleted start = end!')

        # After removing segment duration < segment_minimun_sec remove working group and segment empty
        wg_keys = list(wg_base.keys())
        for wg in wg_keys:

            wg_seg_keys = sorted(wg_base[wg].keys())
            for seg in wg_seg_keys:

                if not wg_base[wg][seg]:
                    del (wg_base[wg][seg])

            if not wg_base[wg]:
                del (wg_base[wg])

        return wg_base

    def remove_gaps_wgx_segments(self, wg_base, segment_gap_max_sec):
        """
        Clean wb_base segments joining segments with gap duration <= seg_min

        :param wg_base: baseline working group
        :param segment_gap_max_sec: The maximum acceptable gap between values;
        Consecutive values with Intervals smaller than max_gaps will be combined into a single interval.
        Default: 0   (any gap keeps intervals separate)
        :return: new_wg_base: working group segment updated
        """

        segment_gap_max = datetime.timedelta(seconds=segment_gap_max_sec)
        new_wg_base = {}

        wg_keys = list(wg_base.keys())
        for wg in wg_keys:

            new_wg_base[wg] = {}

            wg_seg_keys = sorted(wg_base[wg].keys())
            for seg in wg_seg_keys:

                new_wg_base[wg][seg] = []

                intervals = wg_base[wg][seg]
                len_intervals = len(intervals)

                start = intervals[0][0]
                current_interval = intervals[0]

                for i in range(1, len_intervals):

                    gap = intervals[i][0] - intervals[i - 1][1]

                    if gap <= segment_gap_max:
                        current_interval = [start, intervals[i][1]]

                    else:
                        new_wg_base[wg][seg].append(current_interval)
                        if i + 1 <= len_intervals:
                            start = intervals[i][0]
                            current_interval = intervals[i]
                        else:
                            current_interval = None

                if current_interval:  # to get last interval

                    new_wg_base[wg][seg].append(current_interval)

        return new_wg_base

    def reset_wgx_segments_start_end(self, wg_base, start_shift=0, end_shift=0, duration=0,
                                     segment_minimun_sec=3 * 3600):
        """
        Reset start and end with all segments from wg_base with a duration > seg_min

        :param wg_base: baseline working group
        :param start_shift: number of seconds to shift segments start
        :param end_shift: number of seconds to shift segments start
        :param duration: minimum duration
        :param segment_minimum_sec: minimum duration for segment
        :return: wg_base: working group segment updated
        """

        segment_minimun = datetime.timedelta(seconds=segment_minimun_sec)
        start_shift = datetime.timedelta(seconds=start_shift)
        if end_shift:
            end_shift = datetime.timedelta(seconds=end_shift)

        duration = datetime.timedelta(seconds=duration)

        new_wg_base = {}

        for wg in wg_base.keys():

            new_wg_base[wg] = {}

            for seg in sorted(wg_base[wg].keys()):

                for i in range(len(wg_base[wg][seg])):

                    (start, end) = tuple(wg_base[wg][seg][i])

                    if (end - start) >= segment_minimun:

                        if seg not in new_wg_base[wg].keys():
                            new_wg_base[wg][seg] = []

                        if end_shift:

                            new_period = [start + start_shift, end + end_shift]

                        else:

                            new_period = [start + start_shift, start + start_shift + duration]

                        new_wg_base[wg][seg].append(new_period)

        return new_wg_base

    def rename_wgx_segments(self, wg_base, seg_new_names={}, wg_new_names={}):
        """
        Rename WG and segments

        :param wg_base: baseline working group
        :param seg_new_names: dictionary includes the mapping for segments to rename
        :param wg_new_names: dictionary includes the mapping for working groups to rename
        :return: wg_new_names: dictionary includes segments to rename
        """

        new_wg_base = {}

        for wg in wg_base.keys():

            new_wg = wg
            if wg in wg_new_names:
                new_wg = wg_new_names[wg]

            new_wg_base[new_wg] = {}

            for seg in sorted(wg_base[wg].keys()):

                new_seg = seg
                if seg in seg_new_names:
                    new_seg = seg_new_names[seg]

                new_wg_base[wg][new_seg] = wg_base[wg][seg]

        return new_wg_base

    def print_segment_details(self, wg_seg):
        """
        Print segment details

        :param wg_seg: working group segment
        :return:
        """

        for wg in wg_seg:
            if not wg_seg[wg]:
                logging.info('There are no segment instances for {}'.format(wg))
            else:
                print(wg)
                for seg in wg_seg[wg]:
                    print('\t{}: {}'.format(seg, wg_seg[wg][seg]))

    def get_no_overlaps(self, wg_base, wg2, log_silence=True):
        """
        Get WG/segments windows wg_base not overlapping with WG2,

        :param wg_base: Working Group object
        :param wg2: Working Group object
        :param log_silence: flag to avoid logging if set to true
        :return: no_overlap_flag: Flag stating if there are overlap between segments
                 no_overlap_wg_base: Working Group including all not wg_base segments not overlapped by wg2 segments
        """

        overlaps = self.get_overlaps(wg_base, wg2)[1]
        no_overlaps = self.get_wg_sub(wg_base, overlaps)

        no_overlap_flag = False
        for wg in no_overlaps:
            for seg in sorted(no_overlaps[wg].keys()):
                if len(seg) > 0:
                    no_overlap_flag = True
                    break

        return no_overlap_flag, no_overlaps

    def get_start_end_WG1234x(self, wg_base):
        """
        Get absolute start and end of WG 1,2,3,4,5

        :param wg_base: Working Group object
        :return: start,end
        """

        p = IntervalHandlers()

        list_all = []

        for k_wg, wg in wg_base.items():

            for k_seg, seg in wg.items():
                list_all.extend(seg)

        list_all = p.merge_intervals(list_all)

        if len(list_all):

            start = list_all[0][0]
            end = list_all[-1][-1]

        else:
            logging.warning('There are no segments in current partition!')

            start = None
            end = None

        return start, end

    def get_and_report_gaps(self, wg_base, date_format='%Y-%m-%dT%H:%M:%SZ'):
        """
        Report Gaps in Segmentation Schedule

        :param date_format: datetime format
        :param wg_base: Working Group object
        :return: gaps: list of gaps
        """

        p = IntervalHandlers()

        list_all = []

        for k_wg, wg in wg_base.items():

            for k_seg, seg in wg.items():
                list_all.extend(seg)

        list_all = p.merge_intervals(list_all)

        gaps = p.not_intervals(list_all)

        nb_gaps = len(gaps)
        if nb_gaps > 0:

            logging.warning('There are {} gaps in Final Scheduled  Segmentation'.format(nb_gaps))

        else:

            logging.info('There are no gaps in Final Scheduled  Segmentation!')

        for i in range(nb_gaps):
            p = gaps[i]

            start_str = datetime.datetime.strftime(p[0], date_format)
            stop_str = datetime.datetime.strftime(p[1], date_format)
            gap_duration = p[1] - p[0]

            logging.warning('Gap {}/{}: [{} - {}]: dt = {}'.format(i + 1, nb_gaps, start_str, stop_str, gap_duration))

        return gaps

    def get_overlaps(self, wg_base, wg2, log_silence=False):
        """
        Get overlaps between WGs,
        Return the wg_base/segments/intervals overlapped by wg2/segments/intervals

        :param wg_base: Working Group object
        :param wg2: Working Group object
        :param log_silence: flag to avoid logging if set to true
        :return: overlap_flag: Flag stating if there are overlap between segments
                 new_wg_base: Working Group object including all overlapps
        """

        p = IntervalHandlers()

        merge = PeriodMerger()

        new_wg_base = {}

        overlap_flag = False

        for wg in wg_base.keys():
            new_wg_base[wg] = {}
            for seg in sorted(wg_base[wg].keys()):
                new_wg_base[wg][seg] = []
                seg_wg = []

                for sub_wg in wg2.keys():

                    for sub_seg in wg2[sub_wg].keys():

                        overlap = merge.get_event_overlap(wg_base[wg][seg], wg2[sub_wg][sub_seg])
                        # to remove 0 intervals use "overlap = p.intervals_clean(overlap, min_interval=1)"
                        overlap = [x for x in overlap if (x[1] - x[0]).total_seconds() > 0]  # to remove 0 intervals
                        if overlap:

                            if not log_silence:
                                logging.warning(
                                    'Overlap(s) between {} {} and {} {}'.format(wg, seg, sub_wg, sub_seg))
                                for over_instance in overlap:
                                    logging.warning('==> {}'.format(self.datetime_list_2_str_list([over_instance])))

                            seg_wg.extend(overlap)
                            overlap_flag = True

                if seg_wg:
                    new_wg_base[wg][seg] = p.merge_intervals(seg_wg)

        for wg in new_wg_base:
            seg_keys = list(new_wg_base[wg].keys())
            for k in seg_keys:
                if not new_wg_base[wg][k]:
                    # logging.debug('instance {} {} deleted!'.format(wg, k))
                    del (new_wg_base[wg][k])

        return overlap_flag, new_wg_base

    def get_all_wg_overlaps(self, wg_base, list_of_wg, log_silence=False):
        """
        Get overlaps between a given wg and a list of wg

        :param wg_base: Working Group object
        :param list_of_wg: list of Working Group object
        :param log_silence: flag to avoid logging if set to true
        :return: any_overlap_flag: true is there is any overlap
        """

        any_overlap_flag = False

        for ele in list_of_wg:
            overlap_flag, new_wg_base = self.get_overlaps(wg_base, ele, log_silence=log_silence)

            if overlap_flag:

                any_overlap_flag = True

                if not log_silence:
                    logging.warning('{} overlap with {} = {}'.format(wg_base.keys(), ele.keys(), overlap_flag))

        return any_overlap_flag

    def get_overlaps_within_proper_wg(self, wg_base):
        """
        Get overlaps between WG

        :param wg_base: the input working group object
        :return: overlap_flag
        """

        from esac_juice_pyutils.periods.event_period_merger import PeriodMerger

        merge = PeriodMerger()

        overlap_flag = False

        for wg in wg_base.keys():

            for seg in sorted(wg_base[wg].keys()):

                for sub_seg in sorted(wg_base[wg].keys()):

                    if seg != sub_seg:

                        overlap = merge.get_event_overlap(wg_base[wg][seg], wg_base[wg][sub_seg])
                        overlap = [x for x in overlap if (x[1] - x[0]).total_seconds() > 0]

                        if overlap:

                            logging.warning(
                                '{0} : Overlap(s) between segments {1} {2} '.format(wg, seg, sub_seg))
                            for over_instance in overlap:
                                logging.warning('==> {}'.format(self.datetime_list_2_str_list([over_instance])))

                            overlap_flag = True

        return overlap_flag

    def get_total_seconds_intervals(self, intervals):
        """
        Get total of seconds of a list of periods

        :return: total_time: the total number of seconds in intervals
        """

        total_time = sum([(x[1] - x[0]) for x in intervals]).total_seconds()

        return total_time

    def get_wgx(self, input_file):
        """
        Read Working group (WG) file and return a list of list of values

        1) Parse csv file
        2) For each record
        2.1) Check start < end; if not ignore the record and log the corresponding log message
        2.2) Check if duplicated record; if not ignore the record and log the corresponding log message
        3) Add counter to instance for each segment type

        :param input_file: path of the input file
        :return: seg_wg: working group segment object with segment type instance numbered
        """

        df = read_file(input_file)

        values = []
        for i in range(len(df)):
            # values.append(list(df.ix[i]))
            values.append(list(df.iloc[i]))

        values = sorted(values, key=itemgetter(2, 3))

        date_format = '%Y-%m-%dT%H:%M:%SZ'
        expectec_wg = ['WGX', 'WG1', 'WG2', 'WG3', 'WG4', 'GENERIC']

        seg_wg = {}
        for i in range(len(values)):

            line = values[i]
            seg = line[0]
            wg = line[4]

            if wg not in expectec_wg:
                logging.error('unexpected WG "{}" in field {}, line {} of file {}'.format(
                    wg, 4 + 1, i + 1, input_file))
                logging.error('WG must be in {}; Please fix it!'.format(expectec_wg))
                sys.exit()

            try:
                start = datetime.datetime.strptime(line[1], date_format)
                end = datetime.datetime.strptime(line[2], date_format)
            except Exception as error:

                logging.debug(error)

                try:
                    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    start = datetime.datetime.strptime(line[1], date_format)
                    end = datetime.datetime.strptime(line[2], date_format)

                except Exception as error:
                    logging.error('Cannot parse {} contents; Please check it'.format(input_file))
                    logging.debug(error, exc_info=True)
                    sys.exit()

            start_str = datetime.datetime.strftime(start, date_format)
            stop_str = datetime.datetime.strftime(end, date_format)

            if start >= end:
                logging.warning(
                    '(Start >= end) for period {} of Instance "{}:{}"; line {} of file {}; ignored!'.format(
                        [start_str, stop_str], wg, seg, i + 1, input_file))
                continue

            if wg not in seg_wg.keys():
                seg_wg[wg] = {seg: [[start, end]]}
            elif seg not in seg_wg[wg].keys():
                seg_wg[wg][seg] = [[start, end]]
            else:
                if [start, end] in seg_wg[wg][seg]:
                    index_all_occurrence = [j + 1 for j, x in enumerate(values[:i]) if str(x) == str(line)]
                    logging.warning(
                        '{} {}: Instance {} line {} already defined in line(s) {}; file {} ignored!'.format(
                            wg, seg, [start_str, stop_str], i + 1, index_all_occurrence, input_file))
                else:
                    seg_wg[wg][seg].append([start, end])

        return seg_wg

    def get_wgx_per_instance(self, input_file):
        """
        Read Working group (WG) file and return a list of values

        :param input_file: path of the input file
        :return: seg_wg per instance
        """

        wgx = self.get_wgx(input_file)
        seg_wg = self.split_wgx_per_instance(wgx)

        return seg_wg

    def split_wgx_per_instance(self, wg_base):
        """
        Split working per instance

        :param wg_base: working group segment
        :return: new_wg_seg: working group segment
        """

        new_wg_seg = {}

        for wg in wg_base:
            new_wg_seg[wg] = {}
            for seg in wg_base[wg]:

                my_periods = sorted(wg_base[wg][seg])

                if seg not in self.opportunity_vs_prime[wg].keys():

                    wild_card = get_prime_for_wildcard(seg, self.opportunity_vs_prime[wg].keys())
                    if not wild_card:
                        logging.debug('{}: {} not defined in OPPORTUNITY_PRIME_Correspondance table'.format(wg, seg))

                    new_wg_seg[wg][seg] = my_periods

                elif 'xx' in self.opportunity_vs_prime[wg][seg]:

                    for i in range(len(my_periods)):
                        new_wg_seg[wg]['{}_{}'.format(seg, i + 1)] = [[my_periods[i][0], my_periods[i][1]]]

                else:

                    new_wg_seg[wg][seg] = my_periods

        return new_wg_seg

    def get_fd_seg(self, input_file):
        """
        Read Flight Dynamic (FD) segment file and return a list of list of values

        :param input_file: path of the input file
        :return: seg_wg working group segment
        """

        return self.get_wgx(input_file)

    def wg_seg_to_list(self, wg_seg, date_format='%Y-%m-%dT%H:%M:%SZ'):
        """
        Convert working group segment to list of segments

        Note: [[seg, start, end, , wg], ...]

        :param wg_seg: working group segment object
        :param date_format: date time format for segments' start and end
        :return: wg_seg_list
        """

        csv_data = []

        for wgx in wg_seg:

            for wg in wgx:

                for seg in wgx[wg]:

                    periods_str = self.datetime_list_2_str_list(wgx[wg][seg], date_format)

                    for [start, end] in periods_str:
                        csv_data.append([seg, start, end, '', wg])

        return csv_data

    def write_segment_file(self, file_name, wg_seg, output_dir=None, date_format='%Y-%m-%dT%H:%M:%SZ'):
        """
        Write Working Group Segment Files

        :param file_name: ouput file name
        :param wg_seg: working group segment object
        :param output_dir: output directory path
        :param date_format: date time format for segments' start and end
        """

        if output_dir is None:
            output_dir = self.output_dir

        csv_data = self.wg_seg_to_list(wg_seg, date_format=date_format)

        file_path = os.path.join(output_dir, file_name)

        csv_data = sorted(csv_data, key=itemgetter(1, 0, 2))

        write_segment_file(file_path, csv_data)

    def write_segment_files(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem,
                            file_prefix, file_sufix='.csv'):
        """

        Create Timeline file for all og Working Group Segments

        :param wg1: windows for WG1 segments
        :param wg2: windows for WG2 segments
        :param wg3: windows for WG3 segments
        :param wg4: windows for WG4 segments
        :param wgx: windows for WGX segments (i.e. calibrations)
        :param fd_tcm: windows for TCM maneuvers
        :param fd_wol: windows for WOL maneuvers
        :param dl_:  windows for downlinks
        :param fd_nav: windows for NAV maneuvers
        :param fd_navephem:
        :param wg_all: windows for all working group and segment
        :param file_sufix: output file suffix
        :param file_prefix: output file prefix

        """
        # Write Segments
        # seg.write_segment_file(file_prefix + '_all' + file_sufix, [wg_all])
        self.write_segment_file(file_prefix + '_WG1' + file_sufix, [wg1])
        self.write_segment_file(file_prefix + '_WG2' + file_sufix, [wg2])
        self.write_segment_file(file_prefix + '_WG3' + file_sufix, [wg3])
        self.write_segment_file(file_prefix + '_WG4' + file_sufix, [wg4])
        self.write_segment_file(file_prefix + '_WGX' + file_sufix, [wgx])
        self.write_segment_file(file_prefix + '_DL' + file_sufix, [dl_])
        self.write_segment_file(file_prefix + '_FD' + file_sufix, [fd_nav, fd_tcm, fd_wol, fd_navephem])


def get_prime_for_wildcard(label, list_of_wild_card):
    """
    Return first wild_card mapping if any
    Else None

    :param label: a string to compare
    :param list_of_wild_card:
    :return:
    """

    import fnmatch

    wild_card_keys = [k for k in list_of_wild_card if '*' in k or '?' in k]
    for wild_card in wild_card_keys:
        if fnmatch.fnmatch(label, wild_card):
            return wild_card

    return None


def read_file(input_file, header=None):
    """
    Read csv like file

    :param header: specify header lines; default is None
    :param input_file: path of the csv file to read
    :return: df: panda data frame instance containing input data
    """

    if not os.path.exists(input_file):
        logging.error('input file "{}" not available'.format(input_file))
        sys.exit()  # event line output routine
    else:

        df = pd.read_csv(input_file, sep=',', header=header, comment='#')

    return df


def write_segment_file(csv_file, csv_data):
    """
    Write csv data file

    :param csv_file: csv file
    :param csv_data: csd data
    """

    f = open(csv_file, 'w')

    for row in csv_data:
        line = ','.join(tuple(row)) + '\n'

        f.write(line)

    f.close()
    logging.info('new segment file created: {}'.format(csv_file))
