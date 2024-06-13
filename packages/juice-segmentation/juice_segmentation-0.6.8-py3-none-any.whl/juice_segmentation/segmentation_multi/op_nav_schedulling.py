"""
Created October 2022

@author: Claudio Munoz Crego (ESAC)

This module provides the methods allowing to perform the OP_NAV (FD) scheduling
"""

import sys
import logging

from juice_segmentation.wg.wg_utils import is_mask_in_keys


def perform_op_nav_scheduling(seg, ws, seg_to_load, op_nav_insertion_rules, juice_seg,
                              fd_ope_nav, wgx_sun_conjunction, wgx_calib_original,
                              wgx_calib, partition, flag_cutted_gs_downlink=False,
                              dl_segment_minimum_sec=3*3600):
    """
    Combine WG according to given priority rules decreasing priority order for scheduling

    1) removing too short segments, as for instance DL too short

    2) Allocating Juice Moon OPE_NAV for FD and WG3 (and WG4, WG2 if needed)

    Notes: ws working group correspond to the segment_to_load for the current windows time removing WGX

    :param seg: seg object
    :param ws: wg_seg object
    :param seg_to_load: structure specifying working group + segments to load in priority order
    :param op_nav_insertion_rules: structure specifying insertion rules for OP_NAV
    :param juice_seg: object
    :param fd_ope_nav: collection of potential OP_NAV segments
    :param wgx_sun_conjunction: sun conjunction segment
    :param wgx_calib_original: original Calibration segments
    :param wgx_calib: selected calibration segments
    :param partition: current partition
    :param flag_cutted_gs_downlink: True if DL was cut by current partition; False per default
    :param dl_segment_minimum_sec: minimum duration for DL_ segment in seconds; if not removed
    :return: wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, wg_all, fd_openav_selected
    """

    ids = range(len(ws))
    for i in ids:

        if ws[i]:

            first_dl_instance = {}
            last_dl_instance = {}

            wg_to_substract = [ws[k] for k in ids if k < i]

            segment_minimum_sec = 60
            wg_i = list(ws[i].keys())[0]
            seg_i = list(ws[i][wg_i].keys())

            if 'DL_' in seg_i:

                segment_minimum_sec = dl_segment_minimum_sec

                if flag_cutted_gs_downlink:

                    # Check if DL have cut by partition (previous partition ends by DL);
                    # then if there is a DL segment at beginning of current partition
                    # do not remove it independently of is size (removing it from the segment to substract)

                    first_dl_period, first_wg_name, first_seg_name = seg.get_first_segments(ws[i])

                    if first_dl_period[0] == partition[0]:
                        # DL_ start a beginning of new partitions

                        w2s_starting_at_partition_start = False

                        for ws2sub in wg_to_substract:

                            first_w2s_period, first_w2s_name, first_w2s_name = seg.get_first_segments(ws2sub)

                            if first_w2s_period:

                                if first_w2s_period[0] == partition[0]:
                                    # Segment with higher priority at partition start

                                    w2s_starting_at_partition_start = True
                                    break

                        if not w2s_starting_at_partition_start:
                            # No segment with higher priority at partition start

                            first_dl_instance = {first_wg_name: {first_seg_name: [first_dl_period]}}

                # check if DL_ at the end of partition to not remove it
                last_dl_period, last_wg_name, last_seg_name = seg.get_last_segments(ws[i])
                if 'DL_' in last_seg_name:
                    if last_dl_period[-1] == partition[-1]:
                        # DL_ at the end of partition
                        last_dl_instance = {last_wg_name: {last_seg_name: [last_dl_period]}}
                        last_dl_instance = seg.wg_substract(last_dl_instance, wg_to_substract, segment_minimun_sec=0)
                        if last_dl_period[-1] != partition[-1]:  # in case not DL no longer at the end of partition
                            last_dl_instance = {}

            if 'WG3' in wg_i:
                segment_minimum_sec = 0

            if 'JMAG_CALROLL' in seg_i:
                del (ws[i][wg_i]['JMAG_CALROLL'])
                ws[i] = seg.wg_substract(ws[i], [wgx_calib_original])
                ws[i] = seg.merge_wgx_segments(ws[i], wgx_calib)

            ws[i] = seg.wg_substract(ws[i], wg_to_substract, segment_minimun_sec=segment_minimum_sec)

            if first_dl_instance:  # wg/seg is GENERIC/DL
                ws[i] = seg.merge_wgx_segments(ws[i], first_dl_instance)

            if last_dl_instance:
                ws[i] = seg.merge_wgx_segments(ws[i], last_dl_instance)

    wg1 = {'WG1': {}}
    wg2 = {'WG2': {}}
    wg3 = {'WG3': {}}
    wg4 = {'WG4': {}}
    wgx = {'WGX': {}}
    dl_ = {'GENERIC': {}}
    fd_nav = {'GENERIC': {}}
    fd_tcm = {'GENERIC': {}}
    fd_wol = {'GENERIC': {}}

    for i in ids:

        if ws[i]:  # not empty
            wg_i, wgi_segments = list(ws[i].items())[0]
            seg_i = list(wgi_segments.keys())

            if wg_i == "WG1":
                wg1 = seg.merge_wgx_segments(wg1, ws[i])
            elif wg_i == 'WG2':
                wg2 = seg.merge_wgx_segments(wg2, ws[i])
            elif wg_i == 'WG3':
                wg3 = seg.merge_wgx_segments(wg3, ws[i])
            elif wg_i == 'WG4':
                wg4 = seg.merge_wgx_segments(wg4, ws[i])
            elif wg_i == 'WGX':
                wgx = seg.merge_wgx_segments(wgx, ws[i])
            elif wg_i == 'GENERIC' and 'DL_' in seg_i:
                dl_ = seg.merge_wgx_segments(dl_, ws[i])
            elif wg_i == 'GENERIC' and is_mask_in_keys(seg_i, '_FD_TCM'):
                fd_tcm = seg.merge_wgx_segments(fd_tcm, ws[i])
            elif wg_i == 'GENERIC' and is_mask_in_keys(seg_i, '_FD_WOL'):
                fd_wol = seg.merge_wgx_segments(fd_wol, ws[i])
            else:
                logging.error('cannot catch working group segment: {}, {}'.format(wg_i, seg_i))
                sys.exit()

    #
    # 2) Allocating Juice Moon OPE_NAV for FD and WG3 (and WG4, WG2 if needed)
    #

    fd_openav_selected, wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_ = \
        juice_seg.schedule_ope_nav_4(wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, fd_ope_nav,
                                     wgx_sun_conjunction, fd_nav, op_nav_insertion_rules)

    wg_all = seg.wg_add(wgx, [fd_openav_selected, wg1, wg2, wg3, wg4, fd_nav, fd_tcm, fd_wol, dl_])

    return wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, wg_all, fd_openav_selected
