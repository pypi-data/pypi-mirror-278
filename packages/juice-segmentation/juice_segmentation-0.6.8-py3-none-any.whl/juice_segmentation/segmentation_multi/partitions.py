"""
Created on Sep, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle a segment partitions
"""

import datetime
import logging
import sys

from juice_segmentation.wg.wg_utils import json_str_2_datatime


def set_partitions(config, mission_phases_path, plan_start, plan_end):
    """
    Set partitions

    :param config: config parameters
    :param mission_phases_path: mission phase file path
    :param plan_start: input segmentation start time
    :param plan_end: input segmentation end time
    :return: partitions: set of partition/sub-periods,
             max_start: start time of all partitions
             max_end: end time of all partitions
    """

    from juice_segmentation.commons.mission_phases import get_mission_phases, print_mission_phases
    from esac_juice_pyutils.periods.event_period_merger import PeriodMerger
    from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers
    import datetime

    merge = PeriodMerger()

    partitions = config['partitions']

    n_partitions = len(partitions)

    partitions_gti = []

    for i in range(n_partitions):

        if 'start' not in partitions[i].keys():
            logging.warning(f'No start time for partition {i+1}; set to beginning of plan: {plan_start}')
            start = plan_start
        else:
            start = partitions[i]["start"]
            if not start:
                logging.warning(f'start time empty for partition {i+1}; set to beginning of plan: {plan_start}')
                start = plan_start

        if 'end' not in partitions[i].keys():
            logging.warning(f'No end time for partition {i+1}; set to end of plan: {plan_end}')
            end = plan_end
        else:
            end = partitions[i]["end"]
            if not end:
                logging.warning(f'end time empty for partition {i+1}; set to end of plan: {plan_end}')
                end = plan_end

        start_i = json_str_2_datatime(start, as_per_dateformat=True)
        if start_i is None:
            logging.error('bad start time in config "{}" (expected format is %Y-%m-%dT%H:%M:%SZ")'.format(start))
            sys.exit()

        end_i = json_str_2_datatime(end, as_per_dateformat=True)
        if end_i is None:
            logging.error('bad end time in config  "{}" (expected format is %Y-%m-%dT%H:%M:%SZ")'.format(end))
            sys.exit()

        if start_i is not None and end_i is not None:
            if end_i <= start_i:
                logging.error('end must be > start; Check config: (start,end) = ({}, {})'.format(start, end))
                sys.exit()

        # check partition overlap

        overlap = merge.get_event_overlap(partitions_gti, [[start_i, end_i]])
        overlap = [x for x in overlap if (x[1] - x[0]).total_seconds() > 0]

        if overlap:
            logging.error(
                'Overlap(s) between input partitions_gti: {}'.format(overlap))
            logging.error('Input partition cannot overlap; please check fix it configuration file')
            sys.exit()

        partitions_gti.append([start_i, end_i])
        partitions[i]['start'] = start_i
        partitions[i]['end'] = end_i

    mission_phases = get_mission_phases(mission_phases_path)

    max_start = partitions_gti[0][0]
    max_end = partitions_gti[-1][1]

    if max_start < mission_phases['Mission_phase_all'].start or max_end > mission_phases['Mission_phase_all'].end:
        logging.error('period [{}, {}] not within Mission_phase_all=[{}, {}]'.format(
            max_start, max_end, mission_phases['Mission_phase_all'].start, mission_phases['Mission_phase_all'].end))
        sys.exit()

    # check gap in partitions_gti
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    p = IntervalHandlers()
    gaps = p.not_intervals(partitions_gti)
    gaps = clean(gaps)

    nb_gaps = len(gaps)
    if nb_gaps > 0:
        logging.warning('There are {} gaps in input partition; please fix it'.format(nb_gaps))

        for i in range(nb_gaps):
            p = gaps[i]

            start_str = datetime.datetime.strftime(p[0], date_format)
            stop_str = datetime.datetime.strftime(p[1], date_format)
            gap_duration = p[1] - p[0]

            logging.warning('Gap {}/{}: [{} - {}]: dt = {}'.format(i + 1, nb_gaps, start_str, stop_str, gap_duration))

        logging.error('Please fix gaps between partitions_gti')
        sys.exit()

    print_mission_phases(mission_phases)

    return partitions, max_start, max_end


def clean(intervals, min_value=datetime.timedelta(seconds=1)):
    """
    Clean filtering intervals removing any interval < min_value

    :param intervals: list of periods
    :param min_value: start time
    :return: new_intervals: updated list of periods
    """

    new_intervals = []

    for p in intervals:

        if p[1] - p[0] >= min_value:
            new_intervals.append(p)

    return new_intervals


class SegmentInstance(object):
    """
    Segment Instance
    """

    def __init__(self, wg_name, segment_name, segment_period):

        self.wg = wg_name
        self.segment = segment_name
        self.period = segment_period
