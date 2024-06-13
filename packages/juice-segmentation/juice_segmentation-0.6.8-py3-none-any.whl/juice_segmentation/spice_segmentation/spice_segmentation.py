"""
Created on May 2021

@author: Claudio Munoz Crego (ESAC)

This module allows to perform a juice segmentation ck cutting


    0) We first need to define environment parameters, and where to find input and generate output
    1) Set-up original working group segments
    2) Cut segments according to highest priority: flybys, then conjunction, then communications, then default
    3) Join all the non overlapping segment and generate resulting  csv

"""

import glob
import logging
import os
import sys

from juice_segmentation.wg.wg_segmentation import WgSegmentation


def generate_spice_segmentation_non_overlapping_segment(input_dir_path, output_dir_path,
                                                        file_name='juice_sc_sat_crema_X_Y.csv',
                                                        start=None, end=None,
                                                        input_file_pattern='juice_sc_*crema_*.csv'):
    """
    Generate juice segmentation ck cutting starting from 'juice_sc_sat_*.csv trajectory dependent file

    :param input_dir_path: input directory path
    :param output_dir_path: output directory path (must exits)
    :param file_name: segmentation output file name
    :param start: period start time filter
    :param end: period end time filter
    :param input_file_pattern: pattern allowing to select input files
    """

    wg_seg_input = []

    input_file_names = glob.glob(os.path.join(input_dir_path, input_file_pattern))

    if len(input_file_names) == 0:

        logging.error('no input file mapping with expected pattern "{}" in input directory "{}"'.format(
            input_file_pattern, input_dir_path))
        logging.error('Please check it')
        sys.exit()

    for name in input_file_names:

        wg_seg_input.append(name)
        logging.debug('{}$ file found in input directory: {}'.format(input_file_pattern, name))

    json_data = \
        {
            "root_path": input_dir_path,
            "output": {"dir": output_dir_path},
            "wg_seg_input": wg_seg_input,
        }

    juice_seg = WgSegmentation(json_data, do_spice_segmentation=True)
    seg = juice_seg.seg
    wg_seg = seg.get_original_wg_seg(juice_seg.config)

    #
    # 1) Set-up original attitude segment
    # i.e. wg_att_flyby all the segment of working group "GENERIC" with name including ["_NOA", "_NPO"]
    #

    wg_att_flyby = seg.select_wgx_subset(wg_seg, wg_filter=["GENERIC"], seg_filter=["_NOA", "_NPO"])
    wg_att_conj = seg.select_wgx_subset(wg_seg, wg_filter=["GENERIC"], seg_filter=["_SUP_SOL_CONJ"])
    wg_att_comms = seg.select_wgx_subset(wg_seg, wg_filter=["GENERIC"], seg_filter=["_COMMS"])
    wg_att_default = seg.select_wgx_subset(wg_seg, wg_filter=["GENERIC"],
                                           seg_filter=["_TRANSFER", "_JUPITER_TOUR", "_GANYMEDE_PHASE"])

    # 1.2) Cut according to start and end if specified (Not None)
    if start or end:

        intervals = list(seg.get_start_end_WG1234x(wg_seg))

        if start and start > intervals[0]:
            intervals[0] = start
        if end and end < intervals[1]:
            intervals[1] = end

        wg_att_flyby = seg.select_wgx_subset_by_time(wg_att_flyby, intervals=[intervals])
        wg_att_conj = seg.select_wgx_subset_by_time(wg_att_conj, intervals=[intervals])
        wg_att_comms = seg.select_wgx_subset_by_time(wg_att_comms, intervals=[intervals])
        wg_att_default = seg.select_wgx_subset_by_time(wg_att_default, intervals=[intervals])

    #
    # 2) Cut segments according to highest priority getting block >= 30 minutes:
    #   - flybys,
    #   - then conjunction,
    #   - then communications,
    #   - then default
    #

    wg_att_default = seg.wg_substract(wg_att_default, [wg_att_flyby, wg_att_conj, wg_att_comms],
                                      segment_minimun_sec=30*60)
    wg_att_comms = seg.wg_substract(wg_att_comms, [wg_att_flyby, wg_att_conj], segment_minimun_sec=30*60)
    wg_att_conj = seg.wg_substract(wg_att_conj, [wg_att_flyby], segment_minimun_sec=30*60)

    #
    # 3) Join all the non overlapping segments in wg_att and generate resulting csv
    #

    wg_att = seg.wg_add(wg_att_flyby, [wg_att_flyby, wg_att_conj, wg_att_comms, wg_att_default])

    # Try to find crema id
    if 'Crema' in input_dir_path:
        crema_id = input_dir_path.split('Crema')[1].replace('/', '')
        file_name = file_name.replace('_X_Y', crema_id)
    elif 'crema' in input_dir_path:
        crema_id = input_dir_path.split('crema')[1].replace('/', '')
        file_name = file_name.replace('_X_Y', crema_id)
    else:
        logging.warning('output file path/name not specified as input so set to default {}'.format(file_name))

    seg.write_segment_file(file_name, [wg_att], output_dir=output_dir_path)
