"""
Created on May 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows handle FD segmentation files
"""

import datetime
import logging
from operator import itemgetter

import numpy as np

from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps


class WgFdSegmentHandler(WgSegBasicOps):
    """
    This Module allows to run segmentation files
    """

    def __init__(self, eo, fb_pe_events, output_dir='./'):

        root_dir = eo.root_path

        logging.debug(f'root path: {root_dir}')
        logging.debug(f'output path: {output_dir}')
        # opportunity_vs_prime = eo.opportunity_vs_prime
        # mission_phases = eo.mission_phases

        self.fb_pe_events = fb_pe_events

        super(WgFdSegmentHandler, self).__init__()

    def get_fd_ephem_periods_generic(self, ope_nav, downlink, maneuver_slots, wg_all, my_rules, start=None, end=None):
        """
        Calculate jupiter moon (Gan, Eur, Cal) FD ephemerides between 2 downlink

        Note: We try to allocate one and only one slot per OPE_NAV (segment form FD)
        of 1:30 H if adjacent to a manoeuvre else 2H following the rules :

        :param ope_nav: Working Group and segments for FD moon ephemerides
        :param downlink: Working Group and segments for downlink
        :param wg_all: all segments
        :param my_rules: Structure defining the list of rules to be applied for segments
        :param start: Absolute start
        :param end: Absolute end
        :param wgx: windows for WGX segments (i.e. calibrations)
        :return: selected_ephem: selected instances of WG and segments for FD moon ephemerides
        """

        dt_slew = datetime.timedelta(seconds=1800)
        dt_60min = datetime.timedelta(seconds=3600)

        selected_ephem = {'GENERIC': {}}

        potential_slots = []
        for k, list_periods in ope_nav['GENERIC'].items():
            potential_slots.extend(list_periods)

        for [p_start, p_end] in sorted(potential_slots):

            if start:
                if p_end < start:
                    logging.debug(' {} < {} < {}'.format(start, [p_start, p_end], end))
                    continue
            if end:
                if p_start > end:
                    logging.debug(' {} < {} < {}'.format(start, [p_start, p_end], end))
                    break

            p_start = p_start + datetime.timedelta(seconds=1)
            p_end = p_end - datetime.timedelta(seconds=1)

            potential_ephem = self.select_wgx_subset_by_time(ope_nav, intervals=[[p_start, p_end]])
            potential_ephem = self.wg_substract(potential_ephem, [maneuver_slots], segment_minimun_sec=1)

            is_allocated = False
            wg_base = {}  # set to empty WG-Segment by default
            for rule in my_rules:

                if "seg_base" in rule.keys():
                    wg_base = rule["seg_base"]

                wg_seg = rule["seg_instance"]

                is_allocated, selected_ephem, downlink = \
                    self.schedule_ope_nav_wg(wg_base, wg_seg, potential_ephem, selected_ephem, downlink,
                                             maneuver_slots, dt_slew, dt_60min,
                                             rule["rules"])

                wg_base = self.wg_add(wg_base, wg_seg)

                if is_allocated:
                    break

            selected_ephem = self.merge_wgx_segments(selected_ephem, selected_ephem)

            if not is_allocated:  # LOG non allocated daily OPE_NAV:

                for k, v in potential_ephem['GENERIC'].items():
                    if v[0][1] - v[0][0] >= dt_60min:
                        logging.warning(
                            'Cannot allocate OPE_NAV in WG3 + WG4: {}: [{} - {}]'.format(k, v[0][0], v[0][1]))

                        overlaps = self.select_wgx_subset_by_time(wg_all, intervals=[[v[0][0], v[0][1]]])
                        list_of_overlaps_with = []
                        for wg in overlaps.keys():
                            for seg in overlaps[wg].keys():
                                for p in overlaps[wg][seg]:
                                    # if p[1] - p[0] < dt_60min * 2:
                                    list_of_overlaps_with.append('\t|[{} - {}] | {} | {} |'.format(
                                        p[0], p[1], wg, seg))

                        if logging.DEBUG >= logging.root.level:
                            for ev in sorted(list_of_overlaps_with):
                                print(ev)

        return selected_ephem, downlink

    def is_man_before_interval(self, maneuver_slots, start):
        """
        Check if maneuver before current period

        :param maneuver_slots: maneuver periods
        :param start: start time
        :return: is_man_before: flag indicating if maneuver before current period
        """

        dt_1sec = datetime.timedelta(seconds=1)

        is_man_before = self.is_segment_within_time(maneuver_slots, intervals=[[start - dt_1sec, start]])

        return is_man_before

    def is_man_after_interval(self, maneuver_slots, end):
        """
        Check if maneuver after current period

        :param maneuver_slots: maneuver periods
        :param start: start time
        :param end: end time
        :return: is_man_before: flag indicating if maneuver before current period
        """

        dt_1sec = datetime.timedelta(seconds=1)

        is_man_after = self.is_segment_within_time(maneuver_slots, intervals=[[end, end + dt_1sec]])

        return is_man_after

    def is_adjacent_to_manoeuvre(self, maneuver_slots, start, end, dt_slew):
        """
        Check if maneuver adjacent current period

        :param maneuver_slots: maneuver periods
        :param start: start time
        :param end: end time
        :param dt_slew: slew in seconds
        :return: is_man_before: flag indicating if maneuver before current period
        """

        dt_60min = datetime.timedelta(seconds=3600)

        op_nav_opportunity = [start, end]

        is_man_before = self.is_man_before_interval(maneuver_slots, start)
        is_man_after = self.is_man_before_interval(maneuver_slots, end)

        if is_man_before and is_man_after and end - start == dt_60min:

            pass  # op_nav_opportunity of 1 hour of duration between 2 manoeuvres (ideal case not happening)

        elif is_man_before and end - start >= dt_60min + dt_slew:

            op_nav_opportunity = [start, start + dt_60min + dt_slew]

        elif is_man_after and end - start >= dt_60min + dt_slew:

            op_nav_opportunity = [end - dt_60min - dt_slew, end]

        else:

            op_nav_opportunity = []

        return op_nav_opportunity

    def is_adjacent_to_downlink(self, dl, start, end, dt_slew):
        """
        Check if downlink adjacent current period
        and cut downlink to insert the slot

        :param dl: downlink periods
        :param start: start time
        :param start: end time
        :param dt_slew: slew in seconds
        :return: op_nav_opportunity: new opnav
        """

        dt_60min = datetime.timedelta(seconds=3600)

        op_nav_opportunity = [start, end]

        is_man_before = self.is_man_before_interval(dl, start)
        is_man_after = self.is_man_before_interval(dl, end)

        if is_man_before and is_man_after and end - start == dt_60min:

            pass  # op_nav_opportunity of 1 hour of duration between 2 manoeuvres (ideal case not happening)

        elif is_man_before:

            op_nav_opportunity = [end - dt_60min - dt_slew, end]

        elif is_man_after:

            op_nav_opportunity = [start, start + dt_60min + dt_slew]

        else:

            op_nav_opportunity = []

        return op_nav_opportunity

    def get_slot_adjacent_with_man(self, maneuver_slots, op_nav_select, selected_ephem, dt_slew):
        """
        Get a slot adjacent to a manoeuvre if possible

        :param maneuver_slots: Working group segment including maneuver periods
        :param op_nav_select: operation nav
        :param selected_ephem: selected ephemerides slots
        :param dt_slew: slew period
        :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides
        """

        is_allocated = False

        for k, op in op_nav_select['GENERIC'].items():

            for i in range(len(op)):

                t_ref = op_nav_select['GENERIC'][k][i]

                opp = self.is_adjacent_to_manoeuvre(maneuver_slots, t_ref[0], t_ref[1], dt_slew)

                if opp:
                    is_allocated = True
                    break

            if is_allocated:

                if k not in selected_ephem['GENERIC']:
                    selected_ephem['GENERIC'][k] = [opp]
                else:
                    selected_ephem['GENERIC'][k].append(opp)
                break

        return is_allocated, selected_ephem

    def get_slot_adjacent_with_dl_and_complete(self, downlink, op_nav_select, selected_ephem, dt_slew):
        """
        Get a slot adjacent to a DL and cut DL to allocate it

        :param downlink: Working group segment including downlink periods
        :param op_nav_select: operation nav
        :param selected_ephem: selected ephemerides slots
        :param dt_slew: slew period
        :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides,
                 downlink: updated DL segments
        """

        is_allocated = False

        for k, op in op_nav_select['GENERIC'].items():

            for i in range(len(op)):

                t_ref = op_nav_select['GENERIC'][k][i]

                opp = self.is_adjacent_to_downlink(downlink, t_ref[0], t_ref[1], dt_slew)

                if opp:
                    is_allocated = True
                    break

            if is_allocated:

                if k not in selected_ephem['GENERIC']:
                    selected_ephem['GENERIC'][k] = [opp]
                else:
                    selected_ephem['GENERIC'][k].append(opp)
                break

        downlink = self.get_wg_sub(downlink, selected_ephem)

        return is_allocated, selected_ephem, downlink

    def schedule_ope_nav_wg_2(self, wg_base, wgi, potential_ephem, selected_ephem, downlink, maneuver_slots, dt_slew,
                              dt_60min, scheduling_rules=[]):
        """
        Try to schedule/insert OPNAV slots following scheduling rules

        :param wg_base: Working group segment baseline
        :param wgi: Working group segment
        :param potential_ephem: potential ephemeride slots
        :param selected_ephem: selected ephemeride slots
        :param downlink: Working group segment including downlink periods
        :param maneuver_slots: Working group segment including maneuver periods
        :param dt_slew: slew time step
        :param dt_60min: 60 minutes
        :param scheduling_rules: scheduling rules
        :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides,
                 downlink: updated DL segments
        """

        is_allocated = False

        for i in range(len(wgi)):

            wg_sub = self.wg_add(wg_base, wgi[0:i + 1])

            flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
            op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

            if 'GENERIC' not in op_nav_select.keys():  # no available slots
                continue

            for scheduling_rule in scheduling_rules:

                if scheduling_rule == 'adjacent_to_man_1h30m':  # Try to find a slot adjacent to a manoeuvre

                    is_allocated, selected_ephem = self.get_slot_adjacent_with_man(
                        maneuver_slots, op_nav_select, selected_ephem, dt_slew)

                    if is_allocated:
                        break

                elif scheduling_rule == 'anywhere_2h':  # Try to select a 2 hours slot within WG3

                    is_allocated, selected_ephem = get_slot_of_2hours(
                        op_nav_select, selected_ephem, dt_60min)

                    if is_allocated:
                        break

                elif scheduling_rule == 'anywhere_cutting_DL_1h30m':
                    # if adjacent to downlink(DL) them cut DL to allocate it. downlink

                    is_allocated, selected_ephem, downlink = self.get_slot_adjacent_with_dl_and_complete(
                        downlink, op_nav_select, selected_ephem, dt_slew)

                    if is_allocated:
                        break

        return is_allocated, selected_ephem, downlink

    def schedule_ope_nav_wg(self, wg_base, wgi, potential_ephem, selected_ephem, downlink, maneuver_slots, dt_slew,
                            dt_60min, scheduling_rules=[]):
        """
        Try to schedule/insert OPNAV slots following scheduling rules

        :param wg_base: Working group segment baseline
        :param wgi: Working group segment
        :param potential_ephem: potential ephemeride slots
        :param selected_ephem: selected ephemeride slots
        :param downlink: Working group segment including downlink periods
        :param maneuver_slots: Working group segment including maneuver periods
        :param dt_slew: slew time step
        :param dt_60min: 60 minutes
        :param scheduling_rules: scheduling rules
        :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides,
                 downlink: updated DL segments
        """

        is_allocated = False

        for scheduling_rule in scheduling_rules:

            if scheduling_rule == 'adjacent_to_man_1h30m':  # Try to find a slot adjacent to a manoeuvre

                for i in range(len(wgi)):

                    wg_sub = self.wg_add(wg_base, wgi[0:i + 1])

                    flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                    op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                    if 'GENERIC' in op_nav_select.keys():

                        is_allocated, selected_ephem = self.get_slot_adjacent_with_man(
                            maneuver_slots, op_nav_select, selected_ephem, dt_slew)

                        if is_allocated:
                            break

            elif scheduling_rule == 'anywhere_2h':  # Try to select a 2 hours slot within WG3

                for i in range(len(wgi)):  # Finally try to find a slot of 2 hours

                    wg_sub = self.wg_add(wg_base, wgi[0:i + 1])

                    flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                    op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                    if 'GENERIC' in op_nav_select.keys():

                        is_allocated, selected_ephem = get_slot_of_2hours(
                            op_nav_select, selected_ephem, dt_60min)

                        if is_allocated:
                            break

            elif scheduling_rule == 'anywhere_cutting_DL_1h30m':
                # if adjacent to downlink(DL) them cut DL to allocate it. downlink

                for i in range(len(wgi)):  # Finally try to find a slot of 2 hours

                    wg_sub = self.wg_add(wg_base, wgi[0:i + 1])

                    flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                    op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                    if 'GENERIC' in op_nav_select.keys():
                        is_allocated, selected_ephem, downlink = self.get_slot_adjacent_with_dl_and_complete(
                            downlink, op_nav_select, selected_ephem, dt_slew)

                    if is_allocated:
                        break

            # Try schedule/insert OPNAV within Jupiter Perijove slots following scheduling rules

            elif scheduling_rule == 'perijove_adjacent_to_man_1h30m':  # Try to find a slot adjacent to a manoeuvre

                for i in range(len(wgi)):

                    for wg in list(wgi[i].keys()):

                        for pe_id, slots in wgi[i][wg].items():  # try to find slots adjacent to a manoeuvre

                            if not self.is_perijove_segment(pe_id):
                                continue

                            wg_sub = self.wg_add(wg_base, [{wg: {pe_id: slots}}])

                            flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                            op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                            if 'GENERIC' in op_nav_select.keys():

                                ephem_man = self.get_all_slots_adjacent_with_man(
                                    maneuver_slots, op_nav_select, dt_slew)

                                if ephem_man['GENERIC']:
                                    selected_ephem = self.get_open_nav_as_far_as_possible_perijove(
                                        pe_id, selected_ephem, ephem_man)
                                    is_allocated = True
                                    break

                    if is_allocated:
                        break

                if is_allocated:
                    break

            elif scheduling_rule == 'perijove_as_far_as_possible_2h':  # Try to select a 2 hours slot within WG3

                for i in range(len(wgi)):

                    for wg in list(wgi[i].keys()):

                        for pe_id, slots in wgi[i][wg].items():  # try to find a slot of 2 hours

                            if not self.is_perijove_segment(pe_id):
                                continue

                            wg_sub = self.wg_add(wg_base, [{wg: {pe_id: slots}}])

                            flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                            op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                            if 'GENERIC' in op_nav_select.keys():

                                ephem_2hours = get_all_slot_of_2hours(op_nav_select, dt_60min)

                                if ephem_2hours['GENERIC']:
                                    selected_ephem = \
                                        self.get_open_nav_as_far_as_possible_perijove(
                                            pe_id, selected_ephem, ephem_2hours)

                                    is_allocated = True
                                    break

                        if is_allocated:
                            break

                    if is_allocated:
                        break

            elif scheduling_rule == 'perijove_anywhere_cutting_DL_1h30m':
                # if adjacent to downlink(DL) them cut DL to allocate it. downlink

                for i in range(len(wgi)):  # try to find aa slot of 1H30

                    for wg in list(wgi[i].keys()):

                        for pe_id, slots in wgi[i][wg].items():

                            if not self.is_perijove_segment(pe_id):
                                continue

                            wg_sub = self.wg_add(wg_base, [{wg: {pe_id: slots}}])

                            flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                            op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                            if 'GENERIC' in op_nav_select.keys():

                                ephem_dl_cut, downlink = self.get_all_slot_adjacent_with_dl_and_complete(
                                    downlink, op_nav_select, dt_slew)

                                if ephem_dl_cut['GENERIC']:
                                    selected_ephem = self.get_open_nav_as_far_as_possible_perijove(
                                        pe_id, selected_ephem, ephem_dl_cut)

                                    downlink = self.get_wg_sub(downlink, selected_ephem)

                                    is_allocated = True
                                    break

                        if is_allocated:
                            break

                    if is_allocated:
                        break

            if is_allocated:
                break

        return is_allocated, selected_ephem, downlink

    # def allocate_ope_nav_wg(self, wg_base, wgi, potential_ephem, selected_ephem, downlink, maneuver_slots, dt_slew,
    #                         dt_60min, is_allocated=False):
    #     """
    #     Try to allocate ope_nav in wg_base + other_wg
    #
    #     1) For wg in wg_base,  wg_base + other_wg[0], ...
    #     2) a slot of 1:30 H Adjacent to a manoeuvre
    #     3) if not possible, a slot of 2:00 H within WG3
    #     4) if not possible, and there is a slot adjacent to a DL, cut the downlink to allocate the slot
    #
    #     :param wg_base:
    #     :param wgi:
    #     :param potential_ephem:
    #     :param maneuver_slots:
    #     :param dt_slew:
    #     :param dt_60min:
    #     :param is_allocated:
    #     :return:
    #     """
    #     # logging.debug('cannot insert OPE_NAV in WG3: {}'.format(potential_ephem))
    #
    #     for i in range(len(wgi)):  # First try to find a slot adjacent to a manoeuvre
    #
    #         wg_sub = self.wg_add(wg_base, wgi[0:i + 1])
    #
    #         flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
    #         op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)
    #
    #         if 'GENERIC' in op_nav_select.keys():
    #
    #             # print(op_nav_select['GENERIC'])
    #
    #             is_allocated, selected_ephem = self.get_slot_adjacent_with_man(
    #                 maneuver_slots, op_nav_select, selected_ephem, dt_slew)
    #
    #             if is_allocated:
    #                 break
    #
    #     if not is_allocated:  # Then try to select a 2 hours slot within WG3
    #
    #         for i in range(len(wgi)):  # Finally try to find a slot of 2 hours
    #
    #             wg_sub = self.wg_add(wg_base, wgi[0:i + 1])
    #
    #             flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
    #             op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)
    #
    #             if 'GENERIC' in op_nav_select.keys():
    #
    #                 is_allocated, selected_ephem = get_slot_of_2hours(
    #                     op_nav_select, selected_ephem, dt_60min)
    #
    #             if is_allocated:
    #                 break
    #
    #     if not is_allocated:  # if adjacent to downlink(DL) them cut DL to allocate it. downlink
    #
    #         for i in range(len(wgi)):  # Finally try to find a slot of 2 hours
    #
    #             wg_sub = self.wg_add(wg_base, wgi[0:i + 1])
    #
    #             flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
    #             op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)
    #
    #             if 'GENERIC' in op_nav_select.keys():
    #
    #                 is_allocated, selected_ephem, downlink = self.get_slot_adjacent_with_dl_and_complete(
    #                     downlink, op_nav_select, selected_ephem, dt_slew)
    #
    #             if is_allocated:
    #                 break
    #
    #     return is_allocated, selected_ephem, downlink

    def allocate_ope_nav_wg_ja_pe(self, wg_base, wg4_jupiter_pe, potential_ephem, selected_ephem, downlink,
                                  maneuver_slots,
                                  dt_slew, dt_60min, is_allocated=False):
        """
        Try to allocate ope_nav in wg4 in JUPITER_PERIJOVE taking the solution more distant from PE

        1) For wg in wg_base,  wg_base + other_wg[0], ...
        2) a slot of 1:30 H Adjacent to a manoeuvre
        3) if not possible, a slot of 2:00 H within WG3
        4) if not possible, and there is a slot adjacent to a DL, cut the downlink to allocate the slot

        :param wg_base:
        :param wg4_jupiter_pe: Working group 4 and jupyter perijove segments
        :param potential_ephem: potential ephemerides
        :param maneuver_slots: maneuver segments (TCM, WOL)
        :param dt_slew: slew time step
        :param dt_60min: 60 minutes
        :param is_allocated: flag indicating if current opnav is allocated
        :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides,
                 downlink: updated DL segments
        """
        # logging.debug('cannot insert OPE_NAV in WG3: {}'.format(potential_ephem))

        for pe_id, slots in wg4_jupiter_pe['WG4'].items():  # find slots adjacent to a manoeuvre

            # if not str(pe_id).startswith('JUPITER_PERIJOVE_PE'):
            #     continue

            pe_slots = {'WG4': {pe_id: slots}}
            wg_sub = self.wg_add(wg_base, [pe_slots])

            flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
            op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

            if 'GENERIC' in op_nav_select.keys():

                ephem_man = self.get_all_slots_adjacent_with_man(
                    maneuver_slots, op_nav_select, dt_slew)

                if ephem_man['GENERIC']:
                    selected_ephem = self.get_open_nav_as_far_as_possible_perijove(pe_id, selected_ephem, ephem_man)

                    is_allocated = True
                    break

        if not is_allocated:  # if adjacent to downlink(DL) them cut DL to allocate it. downlink

            for pe_id, slots in wg4_jupiter_pe['WG4'].items():  # Finally try to find a slot of 2 hours

                # if not str(pe_id).startswith('JUPITER_PERIJOVE_PE'):
                #     continue

                wg_sub = self.wg_add(wg_base, [{'WG4': {pe_id: slots}}])

                flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                if 'GENERIC' in op_nav_select.keys():

                    ephem_2hours = get_all_slot_of_2hours(op_nav_select, dt_60min)

                    if ephem_2hours['GENERIC']:
                        selected_ephem = \
                            self.get_open_nav_as_far_as_possible_perijove(pe_id, selected_ephem, ephem_2hours)

                        is_allocated = True
                        break

        if not is_allocated:  # if adjacent to downlink(DL) them cut DL to allocate it. downlink

            for pe_id, slots in wg4_jupiter_pe['WG4'].items():  # Finally try to find a slot of 2 hours

                wg_sub = self.wg_add(wg_base, [{'WG4': {pe_id: slots}}])

                flag, op_nav_select = self.get_overlaps(potential_ephem, wg_sub, log_silence=True)
                op_nav_select = self.clean_wgx_segments(op_nav_select, segment_minimun_sec=3600)

                if 'GENERIC' in op_nav_select.keys():

                    ephem_dl_cut, downlink = self.get_all_slot_adjacent_with_dl_and_complete(
                        downlink, op_nav_select, dt_slew)

                    if ephem_dl_cut['GENERIC']:
                        selected_ephem = self.get_open_nav_as_far_as_possible_perijove(pe_id, selected_ephem,
                                                                                       ephem_dl_cut)

                        downlink = self.get_wg_sub(downlink, selected_ephem)

                        is_allocated = True
                        break

        return is_allocated, selected_ephem, downlink

    def get_all_slots_adjacent_with_man(self, maneuver_slots, op_nav_select, dt_slew):
        """
        Get all slots adjacent to a manoeuvre if possible

        :param maneuver_slots: Working group segment including maneuver periods
        :param op_nav_select: operation nav
        :param dt_slew: slew period
        :return: selected_opportunities: selected opportunities
        """

        selected_opportunities = {'GENERIC': {}}

        for k, op in op_nav_select['GENERIC'].items():

            for i in range(len(op)):

                t_ref = op_nav_select['GENERIC'][k][i]

                opp = self.is_adjacent_to_manoeuvre(maneuver_slots, t_ref[0], t_ref[1], dt_slew)

                if opp:

                    if k not in selected_opportunities['GENERIC']:
                        selected_opportunities['GENERIC'][k] = [opp]
                    else:
                        selected_opportunities['GENERIC'][k].append(opp)
                    break

        return selected_opportunities

    def get_all_slot_adjacent_with_dl_and_complete(self, downlink, op_nav_select, dt_slew):
        """
        Get all slots adjacent to a DL anc cut DL to allocate it

        :param downlink: Working group segment including downlink periods
        :param op_nav_select: operation nav
        :param selected_ephem: selected ephemerides slots
        :param dt_slew: slew period
        :return: selected_opportunities: selected opportunities,
                 downlink: updated DL segments
        """

        selected_opportunities = {'GENERIC': {}}

        for k, op in op_nav_select['GENERIC'].items():

            for i in range(len(op)):

                t_ref = op_nav_select['GENERIC'][k][i]

                opp = self.is_adjacent_to_downlink(downlink, t_ref[0], t_ref[1], dt_slew)

                if opp:

                    if k not in selected_opportunities.keys():
                        selected_opportunities['GENERIC'][k] = [opp]
                    else:
                        selected_opportunities['GENERIC'][k].append(opp)
                    break

        return selected_opportunities, downlink

    def get_open_nav_as_far_as_possible_perijove(self, pe_id, selected_ephem, potential_windows_for_opnav):
        """
        Get OPEN_NAV as far as possible from a perijove identifier
        (i.e perijove, moon flyby closest approach)

        :param pe_id: perijove identifier
        :param selected_ephem: selected ephemerides slots
        :param potential_windows_for_opnav: list of slots available for OPNAV insertion
        :return: selected_ephem: selected ephemerids
        """

        pe_id_date_time = self.get_perijove_data_time(pe_id)
        opp_nav_key, opps = get_open_nav_as_far_as_possible(pe_id_date_time, potential_windows_for_opnav['GENERIC'])

        if opp_nav_key not in selected_ephem['GENERIC'].keys():

            selected_ephem['GENERIC'][opp_nav_key] = [opps]

        else:

            selected_ephem['GENERIC'][opp_nav_key].append(opps)

        return selected_ephem

    def is_perijove_segment(self, segment_name):
        """
        Check if current segment is within perijove segment

        :param segment_name: segment id
        :return: is_perijove: flag indicating if current segment is within perijove segment
        """

        is_perijove = False

        if str(segment_name).startswith('JUPITER_PERIJOVE_PE') or str(segment_name).startswith('JA_PE'):

            is_perijove = True

        return is_perijove

    def get_perijove_data_time(self, segment_name):
        """
        Get perijove date_time

        :param segment_name: segment id
        :return: pe_id_date_time: perijove datetime
        """

        if str(segment_name).startswith('JUPITER_PERIJOVE_PE'):

            pe_id_key = segment_name.replace('JUPITER_PERIJOVE_PE', 'PJ')
            # print('pe_id_key: {}'.format(pe_id_key))

        elif str(segment_name).startswith('JA_PE'):

            pe_id_key = segment_name.replace('JA_PE', 'PJ')

        else:

            return None

        pe_id_date_time = self.fb_pe_events[pe_id_key]

        return pe_id_date_time


def get_open_nav_as_far_as_possible(ref_time, selected_ephem):
    """
    Get OPEN_NAV as far as possible from a given time
    (i.e perijove, moon flyby closest approach)

    :param ref_time: a datetime
    :param selected_ephem: selected ephemerides slots
    :return: seg_name: segment name,
             slot: period corresponding to segment name
    """

    max_dt = datetime.timedelta(seconds=0)

    slot = None

    for k, opportunity in selected_ephem.items():

        for s, e in sorted(opportunity):

            if abs(s - ref_time) >= abs(e - ref_time):
                nearest_border = e
            else:
                nearest_border = s

            if abs(nearest_border - ref_time) > max_dt:
                max_dt = abs(nearest_border - ref_time)
                slot = [s, e]
                seg_name = k

    return seg_name, slot


def get_all_slot_of_2hours(op_nav_select, dt_60min):
    """
    Get all slots of 2 hours if possible

    :param op_nav_select: selected opnav
    :param dt_60min: 60 minute duration
    :return: selected_opportunities: periods selected
    """

    selected_opportunities = {'GENERIC': {}}

    for k, op in op_nav_select['GENERIC'].items():

        for i in range(len(op)):

            t_ref = op_nav_select['GENERIC'][k][i]

            if t_ref[1] - t_ref[0] >= 2 * dt_60min:

                opp = [t_ref[0], t_ref[0] + 2 * dt_60min]

                if k not in selected_opportunities['GENERIC']:
                    selected_opportunities['GENERIC'][k] = [opp]
                else:
                    selected_opportunities['GENERIC'][k].append(opp)

                opp = [t_ref[1] - 2 * dt_60min, t_ref[1]]
                selected_opportunities['GENERIC'][k].append(opp)

    return selected_opportunities


def get_slot_of_2hours(op_nav_select, selected_ephem, dt_60min):
    """
    Get a slot of 2 hours if possible

    :param op_nav_select: selected opnav
    :param selected_ephem: selected ephemerides slots
    :param dt_60min: 60 minute duration
    :return: is_allocated: flag indicating it the current opnav have been allocated,
                 selected_ephem: selected ephmerides,
    """

    is_allocated = False

    for k, op in op_nav_select['GENERIC'].items():

        for i in range(len(op)):

            t_ref = op_nav_select['GENERIC'][k][i]

            if t_ref[1] - t_ref[0] >= 2 * dt_60min:
                opp = [t_ref[0], t_ref[0] + 2 * dt_60min]
                is_allocated = True
                break

        if is_allocated:
            if k not in selected_ephem['GENERIC']:
                selected_ephem['GENERIC'][k] = [opp]
            else:
                selected_ephem['GENERIC'][k].append(opp)
            break

    return is_allocated, selected_ephem


def get_fd_potential_slots(downlink):
    """
    Get potential daily slots between Malargue downlink

    :param downlink: Working group segment including downlink periods
    :return: potential_slots: potential periods
    """

    dl_ = downlink['GENERIC']['DL_']
    potential_slots = []
    dt_16_hours = datetime.timedelta(hours=16)
    dt_24_hours = datetime.timedelta(hours=24)
    start = dl_[0][0] - dt_16_hours

    for i in range(len(dl_)):

        end = dl_[i][0]
        slot_period = end - start

        if slot_period <= dt_24_hours:
            potential_slots.append([start, end])

        else:
            n_slot = slot_period.total_seconds() / 3600 / 24
            n_slot = int(n_slot)
            for k in range(n_slot):
                slot_start = start + k * dt_24_hours
                end_slot = start + (k + 1) * dt_24_hours
                potential_slots.append([slot_start, end_slot])

            potential_slots.append([end_slot, end])

        start = dl_[i][1]

    potential_slots = sorted(potential_slots)

    return potential_slots


def shift_fd_navfb(fd_navfb, fd_wol):
    """
    Check all FD_NAV_FB against FD_WOL
        enforce FD_NAV_FB start 2 hours and 30 minutes before FD_WOL and ends when FD_WOL start
        remove FD_NAV_FB if the corresponding wol

    :param fd_navfb: FD NAV periods
    :param fd_wol: WOL periods
    :return: new_fd_navfb: updated FD NAV periods
    """

    wol = [['wol', [x[0], x[1]]] for x in fd_wol['GENERIC']['JUPITER_FD_WOL']]
    nav = [['nav', [x[0], x[1]]] for x in fd_navfb['GENERIC']['JUPITER_FD_NAV_FB']]

    fd = nav + wol
    fd = sorted(fd, key=itemgetter(1), reverse=True)

    dt_2h30min = datetime.timedelta(hours=2, minutes=30)

    fd_range = range(1, len(fd))

    # print('fd_range= {}; len(fd) = {}', fd_range[-1], len(fd))

    to_del = []
    for i in fd_range:

        if fd[i][0] == 'nav':

            if fd[i - 1][0] == 'nav':
                to_del.append(i)

            else:  # 'wol'

                if fd[i][1][1] != fd[i - 1][1][0]:
                    fd[i][1][1] = fd[i - 1][1][0]
                    fd[i][1][0] = fd[i - 1][1][0] - dt_2h30min

    fd = [x for i, x in enumerate(fd) if i not in to_del]

    new_fd_navfb_intervals = [x[1] for x in fd if x[0] == 'nav']
    new_fd_navfb_intervals = sorted(new_fd_navfb_intervals)  # , key=itemgetter(0, 1))

    new_fd_navfb = {'GENERIC': {'JUPITER_FD_NAV_FB': new_fd_navfb_intervals}}

    return new_fd_navfb


def shift_fd_wol(fd_wol, dl_, max_sep_to_correct=60):
    """
    Check all FD_WOL against DL_
        enforce FD_WOL ends when DL_ starts

    :param fd_wol: WOL periods
    :param dl_:
    :param max_sep_to_correct: default 60 seconds
    :return:
    """

    dateformat = '%Y-%m-%dT%H:%M:%S'

    max_sep_to_correct_dt = datetime.timedelta(seconds=max_sep_to_correct)

    dl = [['dl', [x[0], x[1]]] for x in dl_['GENERIC']['DL_']]
    wol = [['wol', [x[0], x[1]]] for x in fd_wol['GENERIC']['JUPITER_FD_WOL']]

    fd = wol + dl
    fd = sorted(fd, key=itemgetter(1), reverse=False)

    fd_range = range(1, len(fd))

    for i in fd_range:

        if fd[i][0] == 'dl':

            if fd[i - 1][0] == 'wol':

                if fd[i][1][0] != fd[i - 1][1][1]:

                    if np.abs(fd[i][1][0] - fd[i - 1][1][1]) <= max_sep_to_correct_dt:
                        logging.debug('[{}, {}] ends reset to "{}" to coincide the dL start [{},{}]'.format(
                            datetime.datetime.strftime(fd[i - 1][1][0], dateformat),
                            datetime.datetime.strftime(fd[i - 1][1][1], dateformat),
                            datetime.datetime.strftime(fd[i][1][0], dateformat),
                            datetime.datetime.strftime(fd[i][1][0], dateformat),
                            datetime.datetime.strftime(fd[i][1][1], dateformat),
                        ))

                        fd[i - 1][1][1] = fd[i][1][0]

    fd = [x for i, x in enumerate(fd)]

    fd_wol_internal = [x[1] for x in fd if x[0] == 'wol']
    fd_wol_internal = sorted(fd_wol_internal)

    new_fd_navfb = {'GENERIC': {'JUPITER_FD_WOL': fd_wol_internal}}

    return new_fd_navfb
