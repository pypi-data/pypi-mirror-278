"""
Created on september 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to compute wg and segment metrics
"""

import datetime
import logging
from operator import itemgetter

import numpy as np

from esac_juice_pyutils.periods.event_period_merger import PeriodMerger
from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers


class Metrics(object):
    """
    The class include basic functionality to calculate metrics corresponding to  Working Groups Segment Handling
    """

    def __init__(self, start=None, end=None):

        if start and end:

            self.total_time = (end - start)
            logging.info('[{}: {}] <=> {}'.format(start, end, self.total_time))

    def check_overlap_within_seg_type(self, wg_seg):
        """
         Cehck if there are overlaps within a given segment type

         :param wg_seg: working group segment
         :param interval: optional period of time to filter working group segment interval
         """

        p = IntervalHandlers()
        pm = PeriodMerger()

        wg_seg_metric = {}

        for wg in wg_seg:

            wg_seg_metric[wg] = {}

            if not wg_seg[wg]:

                logging.debug(f'There are no segment instances for {wg}')

            else:

                for seg in wg_seg[wg]:

                    wg_seg_metric[wg][seg] = p.merge_intervals(wg_seg[wg][seg])
                    # logging.debug('\t[{}:{}]: {}'.format(wg, seg, wg_seg_metric[wg][seg]))

                    nb = len(wg_seg[wg][seg])
                    if len(wg_seg_metric[wg][seg]) < nb:

                        count_overlaps = 0
                        record_overlaps = []
                        for i in range(nb):
                            for j in range(i + 1, nb):
                                wg_tmp = wg_seg[wg][seg]

                                overlap = pm.get_period_overlap(wg_tmp[i], wg_tmp[j])
                                if overlap:
                                    if (overlap[1] - overlap[0]).total_seconds() > 0:  # avoid 0 seconds overlaps
                                        count_overlaps += 1
                                        record_overlaps.append(('{}:[{} - {}]'.format(
                                            count_overlaps, overlap[0], overlap[1])))

                        if count_overlaps > 0:
                            logging.warning('{} Overlap(s) within {} {}'.format(count_overlaps, wg, seg))
                            for i in range(count_overlaps):
                                print('\t{}'.format(record_overlaps[i]))

    def get_wg_seg_intervals(self, wg_seg, interval=None):
        """
        Get total time per wg and segment

        :param wg_seg: working group segment
        :param interval: optional period of time to filter working group segment interval
        :return: wg_seg_metric: a working group segment without overlapping
        """

        p = IntervalHandlers()
        pm = PeriodMerger()

        wg_seg_metric = {}

        for wg in wg_seg:

            wg_seg_metric[wg] = {}

            if not wg_seg[wg]:

                logging.debug('There are no segment instances for {}'.format(wg))

            else:

                for seg in wg_seg[wg]:

                    wg_seg_metric[wg][seg] = p.merge_intervals(wg_seg[wg][seg])
                    # logging.debug('\t[{}:{}]: {}'.format(wg, seg, wg_seg_metric[wg][seg]))

                    if interval:
                        wg_seg_metric[wg][seg] = pm.get_event_overlap(wg_seg_metric[wg][seg], [interval])
                        if not wg_seg_metric[wg][seg]:
                            del (wg_seg_metric[wg][seg])

        return wg_seg_metric

    def get_wg_seg_metrics(self, wg_seg, report_as_dico=True):
        """
        Get total time per wg and segment
        providing the total 'Sum Of times' for each WG, or segment types for GENERIC WG

        For Generic WG, we use the segment type name instead GENERIC

        :param wg_seg: working group segment
        :param report_as_dico: flag to report metrics as dico
        :return: metrics_wg, wg_seg_metric: wg and segment metrics
        """

        from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers

        p = IntervalHandlers()

        metrics_wg = [['Working Group', 'Sum Of times']]

        wg_seg_metric = {}

        for wg in wg_seg:

            wg_group_time_coverage = []
            wg_seg_metric[wg] = {}

            if not wg_seg[wg]:

                logging.info('There are no segment instances for {}'.format(wg))

            else:

                for seg in wg_seg[wg]:

                    seg_time_coverage = p.merge_intervals(wg_seg[wg][seg])
                    wg_group_time_coverage.extend(seg_time_coverage)

                    wg_seg_metric[wg][seg] = datetime.timedelta(seconds=0)

                    dt = 0
                    for [start, stop] in seg_time_coverage:
                        dt += (stop - start).total_seconds()

                    wg_seg_metric[wg][seg] = dt

                    # logging.debug('\t[{}:{}]: {}'.format(wg, seg, wg_seg_metric[wg][seg]))

        # report time per WG only as list of list where first list include headers
        for wg, seg_list in wg_seg_metric.items():

            wg_sum = 0
            for seg in seg_list:
                wg_sum += seg_list[seg]

            metrics_wg.append([wg, wg_sum])

        return metrics_wg, wg_seg_metric

    def report_wg_metrics(self, list_of_wg, interval=None, report_as_dico=True):
        """
        Create Timeline file for a list of Working Group Segments
        providing the total 'Sum Of times' for each WG, or segment types for GENERIC WG

        For Generic WG, we use the segment type name instead GENERIC

        :param list_of_wg: list of WG
        :param interval: optional period of time to filter working group segment interval
        :param report_as_dico: flag to report metrics as dico
        :return: metrics_wg: a working group segment without overlapping
        """

        from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers

        p = IntervalHandlers()

        metrics_wg = [['Working Group', 'Sum Of times']]

        for wg in list_of_wg:

            self.check_overlap_within_seg_type(wg)
            wg_seg_metrics = self.get_wg_seg_intervals(wg, interval)

            wg_group_time_coverage = []
            for wg_seg in wg_seg_metrics.keys():

                if 'GENERIC' == wg_seg:

                    for seg, seg_time_coverage in wg_seg_metrics[wg_seg].items():
                        # print(wg_seg, seg, wg_seg_metrics[wg_seg][seg])

                        # seg_time_coverage = wg_seg_metrics[wg_seg][seg]
                        # wg_group_time_coverage.extend(seg_time_coverage)

                        wg_sum = 0
                        for [start, stop] in p.merge_intervals(seg_time_coverage):
                            wg_sum += (stop - start).total_seconds()

                        metrics_wg.append([seg, wg_sum])

                else:

                    for seg in wg_seg_metrics[wg_seg]:
                        # print(wg_seg, seg, wg_seg_metrics[wg_seg][seg])

                        seg_time_coverage = wg_seg_metrics[wg_seg][seg]
                        wg_group_time_coverage.extend(seg_time_coverage)

                    wg_sum = 0
                    for [start, stop] in p.merge_intervals(wg_group_time_coverage):
                        wg_sum += (stop - start).total_seconds()

                    metrics_wg.append([wg_seg, wg_sum])

        if report_as_dico:

            metrics_wg_as_dico = {}
            for ele in metrics_wg[1:]:  # remove Title

                metrics_wg_as_dico[ele[0]] = ele[1]

            metrics_wg = metrics_wg_as_dico

        return metrics_wg

    def report_wg_metrics_per_phases(self, list_of_wg, mission_phases):
        """
        Create Timeline file for a list of Working Group Segments

        :param list_of_wg: list of WG
        :param mission_phases: mission phases
        :return: metrics_per_phases: metrics per mission phases
        """

        metrics_per_phases = {}

        for phase in mission_phases:

            interval = [mission_phases[phase].start, mission_phases[phase].end]
            metrics_per_phases[phase] = self.report_wg_metrics(list_of_wg, interval)

        return metrics_per_phases

    def get_segment_types_metrics(self, list_of_wg, interval=None):
        """
        Create Timeline file for a list of Working Group Segments
        providing the total 'Sum Of times' for each WG and segment type,

        :param list_of_wg: list of WG
        :param segments_opportunity_types: segment opportunity types
        :param interval: sub windows
        :return: metrics_wg_seg_type: WG and segment metrics
        """

        from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers

        p = IntervalHandlers()

        metrics_wg_seg_type = [['Working Group', 'Segment Type', 'Sum Of times']]

        metrics_wg_seg_type_as_dico = {}

        for wg in list_of_wg:

            wg_seg_metrics = self.get_wg_seg_intervals(wg, interval)

            for wg_seg in wg_seg_metrics.keys():

                if wg_seg not in list(metrics_wg_seg_type_as_dico.keys()):
                    metrics_wg_seg_type_as_dico[wg_seg] = {}

                for seg_type, seg_time_coverage in wg_seg_metrics[wg_seg].items():

                    seg_type_sum = 0
                    for [start, stop] in p.merge_intervals(seg_time_coverage):
                        seg_type_sum += (stop - start).total_seconds()

                    metrics_wg_seg_type.append([wg_seg, seg_type, seg_type_sum])

                    if seg_type not in list(metrics_wg_seg_type_as_dico[wg_seg].keys()):

                        metrics_wg_seg_type_as_dico[wg_seg][seg_type] = seg_type_sum

                    else:

                        metrics_wg_seg_type_as_dico[wg_seg][seg_type] += seg_type_sum

        return metrics_wg_seg_type_as_dico

    def report_segment_metrics_per_types_and_per_phases(self, list_of_wg, mission_phases):
        """
        Create Timeline file for a list of Working Group Segments

        :param list_of_wg: list of WG
        :param mission_phases: mission phases or sub-periods
        :return: metrics_per_phases
        """

        metrics_per_phases = {}

        for phase in mission_phases:
            interval = [mission_phases[phase].start, mission_phases[phase].end]

            metrics_per_phases[phase] = self.get_segment_types_metrics(list_of_wg, interval)
            # metrics_per_phases[phase] = \
            # self.get_segment_types_metrics(list_of_wg, segments_opportunity_types, interval)

        return metrics_per_phases

    def create_wg_ratio_metrics(self, metrics_wg_orig, metrics_wg, total_seconds):
        """
        Create orig/cutted working group ratio metrics

        :param total_seconds: number of seconds for the given period
        :param metrics_wg_orig: dico providing sum of segments per WG,
        or per segment type for GENERIC WG at the beginning
        :param metrics_wg: dico providing sum of segments per WG, or per segment type for GENERIC WG at the end
        """

        new_wg_metrics = [['Working Group', 'Opportunities', 'Selected',
                           '% Selected', '% Selected/Total']]

        keys_metrics_wg = list(metrics_wg.keys())

        for wg, sum_of_time in metrics_wg_orig.items():

            m_orig = datetime.timedelta(seconds=sum_of_time)
            m_time_selected = datetime.timedelta(seconds=0)
            percent_selected = 0

            if sum_of_time > 0 and wg in keys_metrics_wg:
                percent_selected = round(metrics_wg[wg] / sum_of_time * 100, ndigits=2)
                m_time_selected = datetime.timedelta(seconds=metrics_wg[wg])

            m_orig = datetime.timedelta(seconds=np.ceil(m_orig.total_seconds()))
            m_time_selected = datetime.timedelta(seconds=np.ceil(m_time_selected.total_seconds()))

            percent_cutted_against_total = round(m_time_selected.total_seconds() / total_seconds * 100, ndigits=3)

            new_wg_metrics.append([wg, m_orig, m_time_selected, percent_selected, percent_cutted_against_total])

        # Adding Total
        m = new_wg_metrics[2:]
        total = ['Total'] + new_wg_metrics[1][1:]
        for row in m:
            for i_col in range(1, len(row)):
                total[i_col] += row[i_col]

        if total[1].total_seconds() > 0:
            total[3] = round(total[2].total_seconds() / total[1].total_seconds() * 100., ndigits=2)
        else:
            total[3] = 0.00

        total[4] = round(total[4], ndigits=3)

        new_wg_metrics.append(total)

        return new_wg_metrics

    def create_wg_ratio_metrics_per_phases(self, metrics_wg_orig, metrics_wg, mission_phases):
        """
        Create orig/cutted working group ratio metrics per for all mission phases.

        :param mission_phases:
        :param metrics_wg_orig:
        :param metrics_wg:
        :return:
        """

        metrics_per_phases = {}

        for phase in mission_phases:
            total_seconds = (mission_phases[phase].end - mission_phases[phase].start).total_seconds()
            if total_seconds > 0:
                metrics_per_phases[phase] = self.create_wg_ratio_metrics(
                    metrics_wg_orig[phase], metrics_wg[phase], total_seconds)

        return metrics_per_phases

    def create_seg_types_ratio_metrics(self, metrics_wg_orig, metrics_wg, total_seconds):
        """
        Create orig/cutted working group ratio metrics

        Note: table is rearranged (sorted) by WG and Segment type in alphanumeric order

        :param total_seconds: number of seconds for the given period
        :param metrics_wg_orig: dico providing sum of segments per WG,
        or per segment type for GENERIC WG at the beginning
        :param metrics_wg: dico providing sum of segments per WG, or per segment type for GENERIC WG at the end
        :return:
        """

        new_wg_metrics_header = [['Working Group', 'Segment Type', 'Opportunities', 'Selected',
                                  '% Selected', '% Selected/Total']]

        keys_metrics_wg = list(metrics_wg.keys())

        new_wg_metrics = []

        for wg, ele in metrics_wg_orig.items():

            for seg, sum_of_time in ele.items():

                m_orig = datetime.timedelta(seconds=sum_of_time)
                m_selected = datetime.timedelta(seconds=0)
                percent_selected = 0.

                if sum_of_time > 0:
                    if wg in keys_metrics_wg and seg in metrics_wg[wg].keys():
                        percent_selected = round(metrics_wg[wg][seg] / sum_of_time * 100, ndigits=2)
                        m_selected = datetime.timedelta(seconds=metrics_wg[wg][seg])

                m_orig = datetime.timedelta(seconds=np.ceil(m_orig.total_seconds()))
                m_selected = datetime.timedelta(seconds=np.ceil(m_selected.total_seconds()))

                percent_cutted_against_total = round(m_selected.total_seconds() / total_seconds * 100, ndigits=3)

                new_wg_metrics.append([wg, seg, m_orig, m_selected, percent_selected, percent_cutted_against_total])

        new_wg_metrics = new_wg_metrics_header + sorted(new_wg_metrics,
                                                        key=itemgetter(0, 1))  # sort by WG and segment type

        # Adding Total
        if len(new_wg_metrics) > 1:
            total = [''] + ['Total'] + new_wg_metrics[1][2:]
            for row in new_wg_metrics[2:]:
                for i_col in range(2, len(row)):
                    total[i_col] += row[i_col]

            if total[2].total_seconds() > 0:
                total[4] = round(total[3].total_seconds() / total[2].total_seconds() * 100., ndigits=2)
            else:
                total[4] = 0.00

            total[5] = round(total[5], ndigits=3)

            new_wg_metrics.append(total)

        return new_wg_metrics

    def create_seg_types_ratio_metrics_per_phases(self, metrics_wg_orig, metrics_wg, mission_phases):
        """
        Create orig/cutted segment types  group ratio metrics for all mission phases.

        :param mission_phases:
        :param metrics_wg_orig:
        :param metrics_wg:
        :return:
        """

        metrics_per_phases = {}

        for phase in mission_phases:
            total_seconds = (mission_phases[phase].end - mission_phases[phase].start).total_seconds()

            metrics_per_phases[phase] = self.create_seg_types_ratio_metrics(
                metrics_wg_orig[phase], metrics_wg[phase], total_seconds)

        return metrics_per_phases
