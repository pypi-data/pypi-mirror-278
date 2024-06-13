"""
Created on May, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) segmentation files
"""

import logging
import os
import sys

from juice_segmentation.report.segmentation_report import SegmentationReportFilter
from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps


class SpiceWgSegmentHandler(WgSegBasicOps):
    """
    Class to handle segmentation
    """

    def __init__(self, root_dir, output_dir='./', config={}):
        """
        1) Check root_dir is defined.
        2) Check output directory is defined

        :param root_dir: base directory for intputs
        :param output_dir: output directory path
        """

        self.config = config

        if not os.path.exists(root_dir):
            logging.error('root_dir path not valid: {}'.format(root_dir))
            sys.exit()

        self.root_dir = root_dir

        self.output_dir = self.check_and_set_up_output_dir(output_dir)

    def get_original_wg_seg(self, config_param, add_prime_name=True):
        """
        Get original segments using input configuration parameter object

        1) Read all segment files from Geopipeline and store them by WG/SEG in  new_wg_seg
        2) Number WG1,2,3,4 segment instance appending  "_<instance_counter>" at the en of segment identifier
        2) add_primes IDS to segment label when needed

        :param config_param: path of configuration file
        :param add_prime_name: optional flag to allow the opportunity segment name to the corresponding prime names
        :return: new_wg_seg: original segments object
        """

        root_dir = config_param.root_path

        new_wg_seg = {}
        for wg_file in config_param.wg_seg_input:
            logging.info('{} original segments loading ...'.format(wg_file))

            file_name = os.path.join(root_dir, wg_file)

            wg_seg = self.get_wgx(file_name)
            new_wg_seg = self.wg_add(new_wg_seg, [wg_seg])

        for wg_key, wg in new_wg_seg.items():

            if wg_key in ['WGX', 'WG1', 'WG2', 'WG3', 'WG4']:
                wg_seg = self.select_wgx_subset(new_wg_seg, wg_filter=[wg_key])
                new_wg_seg[wg_key] = self.split_wgx_per_instance(wg_seg)[wg_key]  # new_wg_seg

        return new_wg_seg

    def get_original_segments_wg_all(self, config_param, add_prime_name=False):
        """
        Get original segments using input configuration parameter object

        1) Get 3 types of original segments 'DL_', 'FD_' and others
        2) add_primes IDS to segment label when needed

        :param config_param: path of configuration file
        :param add_prime_name: optional flag to allow the opportunity segment name to the corresponding prime names
        :return: new_wg_seg: original segments object
        """

        root_dir = config_param.root_path

        for wg_file in config_param.wg_all:
            logging.info('{} original segments loading ...'.format(wg_file))

            file_name = os.path.join(root_dir, wg_file)

            wg_seg = self.get_wgx(file_name)
            new_wg_seg = wg_seg

        if add_prime_name:
            new_wg_seg = self.mapp_prime_name2(config_param, new_wg_seg)

        return new_wg_seg

    def get_original_segments_mal_vis(self, config_param, add_prime_name=False):
        """
        Get original segments using input configuration parameter object

        1) Get 3 types of original segments 'DL_', 'FD_' and others
        2) add_primes IDS to segment label when needed

        :param config_param: path of configuration file
        :param add_prime_name: optional flag to allow the opportunity segment name to the corresponding prime names
        :return: new_wg_seg: original segments object
        """

        root_dir = config_param.root_path

        for wg_file in config_param.wg_mal_visibity:
            logging.info('{} original segments loading ...'.format(wg_file))

            file_name = os.path.join(root_dir, wg_file)

            wg_seg = self.get_wgx(file_name)
            new_wg_seg = wg_seg

        if add_prime_name:
            new_wg_seg = self.mapp_prime_name2(config_param, new_wg_seg)

        return new_wg_seg

    def get_original_segments(self, config_param, add_prime_name=True):
        """
        Get original segments using input configuration parameter object

        1) Get 3 types of original segments 'DL_', 'FD_' and others
        2) add_primes IDS to segment label when needed

        :param config_param: path of configuration file
        :param add_prime_name: optional flag to allow the opportunity segment name to the corresponding prime names
        :return: new_wg_seg: original segments object
        """

        root_dir = config_param.root_path

        new_wg_seg = {}
        for wg_seg in config_param.WG_SEG:

            wg_key = list(wg_seg.keys())[0]
            wg_file_path = wg_seg[wg_key]

            logging.info('{} original segments loading ...'.format(wg_key))
            # print(wg_key)

            file_name = os.path.join(root_dir, wg_file_path)

            if 'DL_' in wg_key:

                new_wg_seg[wg_key] = self.get_wgx(file_name)
                new_wg_seg[wg_key] = self.select_wgx_subset(new_wg_seg[wg_key], wg_filter=["GENERIC"])
                if len(list(new_wg_seg[wg_key].keys())) == 0:
                    logging.error('DL segment should be GENERIC in file: {}'.format(file_name))
                    logging.error('Please fix it!')
                    sys.exit()

            elif 'FD_' in wg_key:

                new_wg_seg[wg_key] = self.get_wgx(file_name)
                new_wg_seg[wg_key] = self.select_wgx_subset(new_wg_seg[wg_key], wg_filter=["GENERIC"])
                if len(list(new_wg_seg[wg_key].keys())) == 0:
                    logging.error('FD segment should be GENERIC in file: {}'.format(file_name))
                    logging.error('Please fix it!')
                    sys.exit()

            elif 'WGX' in wg_key:

                new_wg_seg[wg_key] = self.get_wgx(file_name)
                new_wg_seg[wg_key] = self.select_wgx_subset(new_wg_seg[wg_key], wg_filter=["WGX"])

            else:

                new_wg_seg[wg_key] = self.get_wgx_per_instance(file_name)
                new_wg_seg[wg_key] = self.select_wgx_subset(new_wg_seg[wg_key], wg_filter=[wg_key])

                # self.print_segment_details(new_wg_seg[wg_key])
            logging.info('{} original segments loaded!'.format(wg_key))

        if add_prime_name:
            new_wg_seg = self.mapp_prime_name(config_param, new_wg_seg)

        return new_wg_seg

    def check_if_overlaps(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm):
        """
        Checking if overlaps

        1) Set all_wg = all but fd_tcm wg

        :param wg1: working group 1 object including segments
        :param wg2: working group 2 object including segments
        :param wg3: working group 3 object including segments
        :param wg4: working group 4 object including segments
        :param wgx: working group x object including segments
        :param dl_: downlink object including segments
        :param fd_nav: flight Dynamic navigation object including segments
        :param fd_wol: flight Dynamic wheel of loading object including segments
        :param fd_tcm: flight Dynamic rcm object including segments
        """
        all_wg = [wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol]

        logging.info('Checking if overlaps between segments ...')

        logging.debug('fd_tcm')
        self.get_all_wg_overlaps(fd_tcm, all_wg)
        all_wg.pop(-1)
        logging.debug('fd_wol')
        self.get_all_wg_overlaps(fd_wol, all_wg)
        all_wg.pop(-1)
        logging.debug('fd_nav')
        self.get_all_wg_overlaps(fd_nav, all_wg)
        all_wg.pop(-1)
        logging.debug('dl_')
        self.get_all_wg_overlaps(dl_, all_wg)
        all_wg.pop(-1)
        logging.debug('wgx')
        self.get_all_wg_overlaps(wgx, all_wg)
        all_wg.pop(0)
        logging.debug('wg1')
        self.get_all_wg_overlaps(wg1, all_wg)
        all_wg.pop(0)
        logging.debug('wg2')
        self.get_all_wg_overlaps(wg2, all_wg)
        all_wg.pop(1)
        logging.debug('wg4')
        self.get_all_wg_overlaps(wg4, all_wg)
        # seg.get_all_wg_overlaps(fd_nav, all_wg)
        # list_of_wg = [wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem]

        # seg.get_all_wg_overlaps(fd_tcm, [{wg1}, {wg2}, {wg3}, {wg4}, {wgx}, {dl_}, {fd_wol}])

    def check_if_overlaps_within_proper_segments(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm):
        """
        Checking if Overlaps within_proper segments

        :param wg1: working group 1 object including segments
        :param wg2: working group 2 object including segments
        :param wg3: working group 3 object including segments
        :param wg4: working group 4 object including segments
        :param wgx: working group x object including segments
        :param dl_: downlink object including segments
        :param fd_nav: flight Dynamic navigation object including segments
        :param fd_wol: flight Dynamic wheel of loading object including segments
        :param fd_tcm: flight Dynamic rcm object including segments
        """
        logging.info('Checking if overlaps within segments ...')

        self.get_overlaps_within_proper_wg(fd_tcm)
        logging.debug('fd_wol')
        self.get_overlaps_within_proper_wg(fd_wol)
        logging.debug('fd_nav')
        self.get_overlaps_within_proper_wg(fd_nav)
        logging.debug('dl_')
        self.get_overlaps_within_proper_wg(dl_)
        logging.debug('wgx')
        self.get_overlaps_within_proper_wg(wgx)
        logging.debug('wg1')
        self.get_overlaps_within_proper_wg(wg1)
        logging.debug('wg2')
        self.get_overlaps_within_proper_wg(wg2)
        logging.debug('wg3')
        self.get_overlaps_within_proper_wg(wg3)
        logging.debug('wg4')
        self.get_overlaps_within_proper_wg(wg4)

    def set_original_metrics(self, list_of_wg):
        """
        Set_up Metrics

        :param list_of_wg:
        """

        self.metrics_wg_orig = self.my_metrics.report_wg_metrics_per_phases(list_of_wg, self.mission_phases)
        self.metrics_seg_types_orig = self.my_metrics.report_segment_metrics_per_types_and_per_phases(
            list_of_wg, self.mission_phases)
        # self.metrics_seg_types_orig = self.my_metrics.report_segment_metrics_per_types_and_per_phases(
        #     list_of_wg, self.mission_phases, self.segments_opportunity_types)

    def set_final_metrics_and_report(self, list_of_wg, report_order=None):
        """
        Set final Metrics and create Segment Metrics Report

        :param list_of_wg: list of working groups
        :param report_order: parameter to set the reporting section order
        """

        metrics_wg = self.my_metrics.report_wg_metrics_per_phases(list_of_wg, self.mission_phases)
        metrics_seg_types = self.my_metrics.report_segment_metrics_per_types_and_per_phases(
            list_of_wg, self.mission_phases)
        # metrics_seg_types = self.my_metrics.report_segment_metrics_per_types_and_per_phases(
        #     list_of_wg, self.mission_phases, self.segments_opportunity_types)

        new_wg_metrics = \
            self.my_metrics.create_wg_ratio_metrics_per_phases(self.metrics_wg_orig, metrics_wg, self.mission_phases)

        new_seg_types_metrics = self.my_metrics.create_seg_types_ratio_metrics_per_phases(
            self.metrics_seg_types_orig, metrics_seg_types, self.mission_phases)

        my_report = SegmentationReportFilter(self.mission_phases, report_order, output_dir=self.output_dir)
        my_report.create_report(new_wg_metrics, new_seg_types_metrics, self.config)

    def check_and_set_up_output_dir(self, output_dir):
        """
        Check as setup output directory

        :param output_dir: output directory path
        :return: output_dir
        """

        if self.root_dir[-1] == '/':
            self.root_dir = self.root_dir[:-1]

        self.output_dir = output_dir
        if not os.path.exists(output_dir):

            logging.info('output_dir does not exist: {}'.format(self.root_dir))
            logging.info('Checking if base dir exist and create subdirectory in affirmative case')

            base_directory = os.path.dirname(self.output_dir)

            if not os.path.exists(base_directory):

                logging.error('base_directory directory does not exist; Please check it: {}'.format(base_directory))
                sys.exit()

            else:
                sub_directory = os.path.basename(self.output_dir)
                logging.debug('Creating subdirectory {} in {}'.format(sub_directory, base_directory))
                os.mkdir(self.output_dir)
                logging.info('Output subdirectory {} created in {}'.format(sub_directory, base_directory))

        return self.output_dir

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
