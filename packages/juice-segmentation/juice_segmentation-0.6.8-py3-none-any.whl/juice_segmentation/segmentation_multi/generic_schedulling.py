"""
Created October 2022

@author: Claudio Munoz Crego (ESAC)

This module provides the methods allowing to perform the generic scheduling
"""

import sys
import logging

from juice_segmentation.wg.wg_utils import is_mask_in_keys
from juice_segmentation.wg.wg_generic_insertion_rules_handler import schedule_generic


def perform_generic_scheduling(rule, seg, ws, seg_to_load, seg_to_insert, seg_allowed,
                               fd_ope_nav, wgx_sun_conjunction, wgx_calib_original,
                               wgx_calib, partition, flag_cutted_gs_downlink=False):
    """
    Combine WG according to given priority rules decreasing priority order for scheduling


    2) Allocating specified segment according the rules

    :param rule: insertion rule
    :param seg: seg object
    :param ws: wg_seg object
    :param seg_to_load: structure specifying working group + segments to load in priority order
    :param seg_to_insert: segment available to insert
    :param seg_allowed: Segment allowed for insertion
    :param fd_ope_nav: collection of potential OP_NAV segments
    :param wgx_sun_conjunction: sun conjunction segment
    :param wgx_calib_original: original Calibration segments
    :param wgx_calib: selected calibration segments
    :param partition: current partition
    :param flag_cutted_gs_downlink: True if DL was cut by current partition; False per default.
    :return: wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, wg_all, fd_openav_selected
    """

    ids = range(len(ws))
    for i in ids:

        if ws[i]:

            first_dl_instance = None

            wg_to_substract = [ws[k] for k in ids if k < i]

            segment_minimun_sec = 60
            wg_i = list(ws[i].keys())[0]
            seg_i = list(ws[i][wg_i].keys())
            if 'DL_' in seg_i:
                segment_minimun_sec = 3 * 3600

                if flag_cutted_gs_downlink:

                    # Check if DL have cut by partition (previous partition ends by DL);
                    # then if there is a DL segment at beginning of current partition
                    # do not remove it independently of is size (removing it from the segment too substract)

                    first_dl_period, first_wg_name, first_seg_name = seg.get_first_segments(ws[i])

                    if first_dl_period[0] == partition[0]:  # DL_ start a beginning of new partitions

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

            if 'WG3' in wg_i:
                segment_minimun_sec = 0

            if 'JMAG_CALROLL' in seg_i:
                del (ws[i][wg_i]['JMAG_CALROLL'])
                ws[i] = seg.wg_substract(ws[i], [wgx_calib_original])
                ws[i] = seg.merge_wgx_segments(ws[i], wgx_calib)

            ws[i] = seg.wg_substract(ws[i], wg_to_substract, segment_minimun_sec=segment_minimun_sec)

            if first_dl_instance:  # wg/seg is GENERIC/DL

                ws[i] = seg.merge_wgx_segments(ws[i], first_dl_instance)

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

        [wg_i, seg_i] = seg_to_load[i]

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
    # 2) Allocating segment as per rules
    #
    wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_ = \
        schedule_generic(wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_,
                         fd_ope_nav, wgx_sun_conjunction, fd_nav,
                         rule, seg_to_insert, seg_allowed)

    wg_all = seg.wg_add(wgx, [fd_ope_nav, wg1, wg2, wg3, wg4, fd_nav, fd_tcm, fd_wol, dl_])

    return wg1, wg2, wg3, wg4, wgx, dl_, wg_all
