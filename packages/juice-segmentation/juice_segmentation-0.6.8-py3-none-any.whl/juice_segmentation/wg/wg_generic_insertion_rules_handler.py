"""
Created on October 2022

@author: Claudio Munoz Crego (ESAC)

This Module allows handle generic segmentation insertion and scheduling rules
"""

import datetime
import logging

from esac_juice_pyutils.periods.event_period_merger import PeriodMerger
from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers
from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps


def schedule_generic(wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_,
                     fd_ope_nav, wgx_sun_conjunction, fd_nav,
                     my_rules, seg_to_insert, seg_allowed):
    """
    Allocate seg on a daily basis according to rule

    Note: We try to allocate one and only one slot per OPE_NAV (segment form FD)
    of 1:30H if adjacent to a manoeuvre else 2:00H following the rules:

    1) Try to allocate in a WG3 segment
    1.1) a slot of 1:30 H Adjacent to a manoeuvre
    1.2) if not possible, a slot of 2:00 H within WG3
    1.3) if not possible, and there is a slot adjacent to a DL, cut the downlink to allocate the slot
    2) if not possible
    2.1) try the same (as 1)for WG3 + WG4[JUPITER_MONITORING]
    2.2) try the same for WG3 + WG4[JUPITER_MONITORING  + STELLAR_OCC]
    2.3) try the same for WG3 + WG4[JUPITER_MONITORING  + STELLAR_OCC+ JUPITER_PERIJOVE]
    3) if not possible for WG3 + WG4[JUPITER_MONITORING  + STELLAR_OCC+ JUPITER_PERIJOVE] + WG2[FB_RS]
    3.1) a slot of 1:30 H Adjacent to a manoeuvre
    3.2) if not possible, and there is a slot adjacent to a DL, cut the downlink to allocate the slot
    3.3) if not possible, a slot of 2:00 H within WG2
    Finally if one OPNAV not allocated inform user raising the corresponding Warning



    :param wg1: windows for WG1 segments
    :param wg2: windows for WG2 segments
    :param wg3: windows for WG3 segments
    :param wg4: windows for WG4 segments
    :param wgx: windows for WGX segments (i.e. calibrations)
    :param fd_tcm: windows for TCM maneuvers
    :param fd_wol: windows for WOL maneuvers
    :param dl_:  windows for downlink
    :param seg_to_insert: WG and segments for OPE_NAV (FD moon ephemerides)
    :param wgx_sun_conjunction: Solar Conjunction windows
    :param fd_nav: windows for NAV maneuvers
    :param my_rules: Python structure defining OPNAV insertion rules to be applied
    :param fd_ope_nav: FD operational navcam instances
    :param seg_allowed: segment allowed
    :return: fd_navephem_selected, wg1, wg2, wg3, wg4, fd_tcm, fd_wol, dl_
    """

    seg = WgGenericSegmentHandler()

    wg1234x = seg.wg_add(wg1, [wg2, wg3, wg4, wgx])
    wg1234x = seg.wg_substract(wg1234x, [wgx_sun_conjunction])

    start, end = seg.get_start_end_WG1234x(wg1234x)

    wg_seg_list = []
    for wg, seg_list in my_rules["seg"]:
        seg_list_slots = seg.select_wgx_subset(wg1234x, wg_filter=[wg], seg_filter=seg_list)
        wg_seg_list.append(seg_list_slots)

    my_rules["seg_instance"] = wg_seg_list

    maneuvers = seg.wg_add({}, [fd_tcm, fd_wol, dl_, fd_ope_nav])

    if my_rules:  # if rules empty then

        # for r in other_insertion_rules:
        #     r['selected'] = []
        #     for [wg, wg_segments] in r:
        #         for seg in wg_segments:
        #             segments_to_add = seg.join_wg_segments_at_given_time(wgx, part_other, partition[0])
        #             r['selected'] = seg.merge_wgx_segments(r['selected'], segments_to_add)

        seg_selected, dl_ = seg.get_generic_periods2insert(seg_to_insert, seg_allowed, dl_, maneuvers,
                                                           my_rules,
                                                           start=start,
                                                           end=end)

    wg4 = seg.wg_substract(wg4, [seg_selected])
    wg3 = seg.wg_substract(wg3, [seg_selected])
    wg2 = seg.wg_substract(wg2, [seg_selected])
    wg1 = seg.wg_substract(wg1, [seg_selected])
    wgx = seg.wg_substract(wgx, [seg_selected])

    wg4 = seg.merge_wgx_segments(wg4, seg.select_wgx_subset(seg_selected, wg_filter=['WG4']))
    wg3 = seg.merge_wgx_segments(wg3, seg.select_wgx_subset(seg_selected, wg_filter=['WG3']))
    wg2 = seg.merge_wgx_segments(wg2, seg.select_wgx_subset(seg_selected, wg_filter=['WG2']))
    wg1 = seg.merge_wgx_segments(wg1, seg.select_wgx_subset(seg_selected, wg_filter=['WG1']))
    wgx = seg.merge_wgx_segments(wgx, seg.select_wgx_subset(seg_selected, wg_filter=['WGX']))

    return wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_


class WgGenericSegmentHandler(WgSegBasicOps):
    """
    This Module allows to run segmentation files
    """

    def __init__(self, output_dir='./'):

        super(WgGenericSegmentHandler, self).__init__()

    def get_generic_periods2insert(self, seg_to_insert, seg_allowed, downlink, maneuver_slots, scheduling_rules,
                                   start=None,
                                   end=None):
        """
        Calculate jupiter moon (Gan, Eur, Cal) FD ephemerides between 2 downlink

        Note: We try to allocate one and only one slot per OPE_NAV (segment form FD)
        of 1:30 H if adjacent to a manoeuvre else 2H following the rules :

        :param seg_to_insert: WG and segments for FD moon ephemerides
        :param downlink: WG and segments for downlink
        :param seg_allowed: segments allowed
        :param scheduling_rules: Structure defining the list of rules to be applied for segments
        :param start: Absolute start
        :param end: Absolute end
        :param wgx: windows for WGX segments (i.e. calibrations)
        :return: selected_ephem: selected instances of WG and segments for FD moon ephemerides
        """

        selected_ephem = {}

        for rule in scheduling_rules["rules"]:

            keys = list(rule.keys())

            if 'datetime_patterns' in keys:  # Try to find of 1 hour

                slot_duration = rule['datetime_patterns']['duration']
                slot_repetition = rule['datetime_patterns']['repetition']
                simulation_step = rule['datetime_patterns']['simulation_step']

                # wg_seg_allowed_i = self.clean_wgx_segments(seg_allowed, segment_minimun_sec=slot_duration)
                wg_seg_to_insert_i = self.clean_wgx_segments(seg_to_insert, segment_minimun_sec=slot_duration)
                flag, seg_select = self.get_overlaps(wg_seg_to_insert_i, seg_allowed, log_silence=True)
                # seg_select_i = self.clean_wgx_segments(seg_select, segment_minimun_sec=slot_duration)

                # schedule
                tmp, tmp_group, final_slots = self.get_potential_slots(
                    seg_select, slot_repetition, slot_duration, simulation_step)
                # get windows of potential consecutive periods
                # seg_select_i_group = self.remove_gaps_wgx_segments(seg_select_i, slot_repetition - slot_duration)

                final_seg = self.select_wgx_subset_by_time(seg_select, intervals=final_slots)

                selected_ephem = self.merge_wgx_segments(selected_ephem, final_seg)

        # self.merge_wgx_segments(selected_ephem, selected_ephem)

        return selected_ephem, downlink

    def get_potential_slots(self, seg_allowed, slot_repetition, min_duration, simulation_step):
        """
        Get periods where min_duration <= t_seg_instance_i - t_seg_instance_j <= max_duration
        Return periods where the condition is true for each t_i

        :param seg_allowed: Working Group object
        :return: overlap_flag: Flag stating if there are overlap between segments
                 new_wg_base: Working Group object including all overlapps
        """

        potential_slots = []
        for wg, wg_seg in seg_allowed.items():
            for seg, list_periods in wg_seg.items():
                potential_slots.extend(list_periods)

        dt = datetime.timedelta(seconds=slot_repetition)
        dt_duration = datetime.timedelta(seconds=min_duration)

        p = IntervalHandlers()

        merge = PeriodMerger()

        potential_slots = p.merge_intervals(potential_slots)

        extended_potential_slots = []
        for seg_instance in potential_slots:
            extended_potential_slots.append([seg_instance[0] - dt, seg_instance[1] - dt])
            extended_potential_slots.append([seg_instance[0] + dt, seg_instance[1] + dt])

        overlap = merge.get_event_overlap(extended_potential_slots, potential_slots)

        new_potential_slots = p.merge_intervals(overlap)
        new_potential_slots = [x for x in new_potential_slots if (x[1] - x[0]).total_seconds() >= min_duration]

        if len(new_potential_slots) > 0:
            new_potential_groups = self.remove_gaps(new_potential_slots, datetime.timedelta(
                seconds=slot_repetition - min_duration))
        else:
            new_potential_groups = []

        final_slots = []
        for start_group, end_group in new_potential_groups:

            logging.info('Period: [{} - {}]:'.format(start_group, end_group))
            opps = self.explore_coverage(
                new_potential_slots, start_group, end_group, dt_duration, dt, step=simulation_step)
            final_slots.append(opps[2])

            # max_ok = 0
            #
            # for i in range(16):
            #     t = start_group + datetime.timedelta(hours=i)
            #
            #     count = 0
            #     number_t = 0
            #     best_opps = []
            #     opps = []
            #
            #     logging.info('\tPeriod: [{} - {}]: {}'.format(t, end_group, i))
            #     while t <= end_group and t + dt_duration <= end_group:
            #         my_period = [t, t+dt_duration]
            #         number_t += 1
            #         overlap = merge.get_event_overlap([[t, t+dt_duration]], new_potential_slots)
            #
            #         if len(overlap) == 1:
            #             duration = overlap[0][1] - overlap[0][0]
            #             if duration == dt_duration:
            #                 opps.append([overlap[0][1] - overlap[0][0]])
            #                 logging.info('\t [{} - {}]: ok'.format(t, t + dt_duration))
            #                 count += 1
            #             else:
            #                 logging.warning('\t\t[{} - {}]: missed segment < {}'.format(
            #                 t, t + dt_duration, dt_duration))
            #         else:
            #             logging.warning('\t\t[{} - {}]: missed segment; no overlap'.format(t, t + dt_duration))
            #
            #         t += dt
            #
            #     if count > max_ok:
            #         max_ok = count
            #         maximize_i = i
            #         maximize_number_t = number_t
            #         best_opps = opps
            #
            # logging.info('---> best sol is {} / {} for {}'.format(max_ok, maximize_number_t,  maximize_i))

        final_slots = [item for sublist in final_slots for item in sublist]
        final_slots = p.merge_intervals(final_slots)

        return new_potential_slots, new_potential_groups, final_slots

    def explore_coverage(self, potential_slots, start_group, end_group, dt_duration, dt, step=3600):

        slots = []

        max_ok = 0
        # best_opps = []

        for [p_start, p_end] in sorted(potential_slots):

            if start_group <= p_start <= end_group and start_group <= p_end <= end_group:
                slots.append([p_start, p_end])

        for [p_start, p_end] in slots:

            nb_step = int((p_end - p_start).total_seconds() / step)

            for i in range(nb_step):

                t0 = p_start + datetime.timedelta(seconds=i*step)
                t = t0
                # count = 0
                # number_t = 0
                # opps = []

                logging.debug('\tPeriod: [{} - {}]: {}'.format(t, end_group, i))

                count, number_t, opps = self.simulate_coverage(slots, t, start_group, end_group, dt_duration, dt)

                if count > max_ok:
                    max_ok = count
                    maximize_start = t0
                    maximize_number_t = number_t
                    # best_opps = opps

        # Calculate statistics
        coverage_percent = round(max_ok / maximize_number_t * 100, 2)
        group_duration = end_group - start_group
        logging.info('---> Best sol is {} / {} for {}; coverage {}%; duration: {}'.format(
            max_ok, maximize_number_t, maximize_start, coverage_percent, group_duration))

        opps = self.simulate_coverage(
            slots, maximize_start, start_group, end_group, dt_duration, dt, log_details=True)

        return opps

    def simulate_coverage(self, slots, t, start_group, end_group, dt_duration, dt, log_details=False):

        merge = PeriodMerger()

        count = 0
        number_t = 0
        opps = []

        if log_details:
            logging.info('\tPeriod: [{} - {}]:'.format(t, end_group))

        while t <= end_group and t + dt_duration <= end_group:
            # my_period = [t, t + dt_duration]
            number_t += 1
            overlap = merge.get_event_overlap([[t, t + dt_duration]], slots)

            if len(overlap) == 1:
                duration = overlap[0][1] - overlap[0][0]
                if duration == dt_duration:
                    opps.append([overlap[0][0], overlap[0][1]])
                    if log_details:
                        logging.info('\t [{} - {}]: ok'.format(t, t + dt_duration))
                    count += 1
                else:
                    if log_details:
                        logging.warning('\t\t[{} - {}]: missed segment {}< {}'.format(
                            t, t + dt_duration, duration, dt_duration))
            else:
                if log_details:
                    logging.warning('\t\t[{} - {}]: missed segment; no overlap'.format(t, t + dt_duration))

            t += dt

        return count, number_t, opps

    def get_potential_wg_seg_slots(self, wg_base, wg2, slot_repetition, min_duration, max_duration, log_silence=False):
        """
        Get periods where min_duration <= t_seg_instance_i - t_seg_instance_j <= max_duration
        Return periods where the condition is true for each t_i

        :param wg_base: Working Group object
        :param wg2: Working Group object
        :param log_silence: flag to avoid logging if set to true
        :return: overlap_flag: Flag stating if there are overlap between segments
                 new_wg_base: Working Group object including all overlapps
        """
        dt = datetime.timedelta(seconds=slot_repetition)

        p = IntervalHandlers()

        merge = PeriodMerger()

        new_wg_base = {}

        # overlap_flag = False

        for wg in wg_base.keys():
            new_wg_base[wg] = {}
            for seg in sorted(wg_base[wg].keys()):
                new_wg_base[wg][seg] = []
                seg_wg = []

                # seg_duration = (seg[1] - seg[0]).total_seconds()
                # t_i = [seg[0] + i for i in seg_duration]

                # extended_seg_wg = [[seg_instance[0] - dt, seg_instance[1] + dt] for seg_instance in wg_base[wg][seg]]
                extended_seg_wg = []
                for seg_instance in wg_base[wg][seg]:

                    extended_seg_wg.append([seg_instance[0] - dt, seg_instance[1] - dt])
                    extended_seg_wg.append([seg_instance[0] + dt, seg_instance[1] + dt])

                for sub_wg in wg2.keys():

                    for sub_seg in wg2[sub_wg].keys():

                        # sub_seg_duration = (sub_seg[1] - sub_seg[0]).total_seconds()

                        # t_j = [sub_seg[0] + j for j in sub_seg_duration]

                        overlap = merge.get_event_overlap(extended_seg_wg, wg2[sub_wg][sub_seg])
                        # overlap = p.intervals_clean(overlap, min_interval=1)  # to remove 0 intervals
                        overlap = [x for x in overlap if (x[1] - x[0]).total_seconds() >= min_duration]
                        if overlap:

                            if not log_silence:
                                logging.warning(
                                    'Overlap(s) between {} {} and {} {}'.format(wg, seg, sub_wg, sub_seg))
                                for over_instance in overlap:
                                    logging.warning('==> {}'.format(self.datetime_list_2_str_list([over_instance])))

                            seg_wg.extend(overlap)
                            # overlap_flag = True

                if seg_wg:
                    new_wg_base[wg][seg] = p.merge_intervals(seg_wg)

        for wg in new_wg_base:
            seg_keys = list(new_wg_base[wg].keys())
            for k in seg_keys:
                if not new_wg_base[wg][k]:
                    logging.debug('instance {} {} deleted!'.format(wg, k))
                    del (new_wg_base[wg][k])

        return new_wg_base

    def remove_gaps(self, intervals, max_gap_sec):
        """
        Clean interval segments joining segments with gap duration <= seg_min

        :param intervals: list of windows
        :param max_gap_sec: The maximum acceptable gap between values;
        Consecutive values with Intervals smaller than max_gaps will be combined into a single interval.
        Default: 0   (any gap keeps intervals separate)
        :return: new_wg_base: working group segment updated
        """

        new_interval = []

        len_intervals = len(intervals)

        start = intervals[0][0]
        current_interval = intervals[0]

        for i in range(1, len_intervals):

            gap = intervals[i][0] - intervals[i-1][1]

            if gap <= max_gap_sec:
                current_interval = [start, intervals[i][1]]

            else:

                new_interval.append(current_interval)

                if i + 1 <= len_intervals:
                    start = intervals[i][0]
                    current_interval = intervals[i]
                else:
                    current_interval = None

        if current_interval:  # to get last interval

            new_interval.append(current_interval)

        return new_interval
