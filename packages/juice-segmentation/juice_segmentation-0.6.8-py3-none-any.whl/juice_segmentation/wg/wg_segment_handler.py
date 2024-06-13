"""
Created on July 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) segmentation files
"""

import copy
import logging
import os
import sys
import fnmatch

import juice_segmentation.wg.wg_utils as wg_prime_segments
from juice_segmentation.report.metrics import Metrics
from juice_segmentation.report.segmentation_report import SegmentationReportFilter
from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps
import juice_segmentation.wg.wg_seg_prime_mapping as wg_seg_prime_mapping
from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers

class WgSegmentHandler(WgSegBasicOps):
    """
    Class to handle segmentation
    """

    def __init__(self, root_dir, opportunity_vs_prime, mission_phases, date_vs_event, fb_pe_events,
                 output_dir='./', config={}):
        """
        1) Check root_dir is defined.
        2) Check output directory is defined
        3) Parse opportunity_vs_prime_file annd get the corresponding mapping in dictionaries

        :param root_dir: base directory for intputs
        :param opportunity_vs_prime: path of the opportunity versus prime file
        :param output_dir: output directory path
        """

        if not os.path.exists(root_dir):
            logging.error('root_dir path not valid: {}'.format(root_dir))
            sys.exit()

        self.root_dir = root_dir

        self.output_dir = self.check_and_set_up_output_dir(output_dir)

        self.config = config

        opportunity_vs_prime_file_path = opportunity_vs_prime
        if os.path.exists(opportunity_vs_prime_file_path):
            opportunity_vs_prime_file_path = os.path.expandvars(opportunity_vs_prime_file_path)
        else:
            opportunity_vs_prime_file_path = os.path.join(root_dir, opportunity_vs_prime)

        self.opportunity_vs_prime, self.mult_segs_2_prime = \
            wg_prime_segments.get_prime_names(opportunity_vs_prime_file_path)

        self.mission_phases = mission_phases

        self.segments_opportunity_types = wg_prime_segments.get_segments_type_original(opportunity_vs_prime_file_path)

        if 'All phases' in list(self.mission_phases.keys()):

            (start, end) = (self.mission_phases['All phases'].start, self.mission_phases['All phases'].end)
            self.my_metrics = Metrics(start, end)

        else:

            self.my_metrics = Metrics()

        self.metrics_wg_orig = None
        self.metrics_seg_types_orig = None

        self.date_vs_event, self.fb_pe_events = (date_vs_event, fb_pe_events)

    def __get_config_property(self, name, default_value):
        """
        Get the configuration property value

        :param name: property name
        :param default_value: default value of the property
        :return if the property is set in the config returns its value, if not the default value.
        """
        if name in list(self.config.keys()):
            return self.config[name]

        return default_value
        

    def get_original_wg_seg(self, config_param, add_prime_name=True):
        """
        Get original segments using input configuration parameter object

        1) Read all segment files from Geopipeline and store them by WG/SEG in  new_wg_seg
        2) Number WG1,2,3,4 segment instance appending  "_<instanc2_counter>" at the en of segment identifier
        2) add_primes IDS to segment label when needed

        :param config_param: path of configuration file
        :param add_prime_name: optional flag to allow the opportunity segment name to the corresponding prime names
        :return: new_wg_seg: original segments object
        """

        root_dir = config_param.root_path

        new_wg_seg = {}
        for wg_file in config_param.wg_seg_input:
            logging.info('{} original segments loading ...'.format(wg_file))

            if os.path.exists(wg_file):
                file_name = wg_file
            else:
                file_name = os.path.join(root_dir, wg_file)

            wg_seg = self.get_wgx(file_name)
            new_wg_seg = self.wg_add(new_wg_seg, [wg_seg])

        for wg_key, wg in new_wg_seg.items():

            if wg_key in ['WGX', 'WG1', 'WG2', 'WG3', 'WG4']:
                wg_seg = self.select_wgx_subset(new_wg_seg, wg_filter=[wg_key])
                new_wg_seg[wg_key] = self.split_wgx_per_instance(wg_seg)[wg_key]  # new_wg_seg

        if add_prime_name:
            new_wg_seg = self.mapp_prime_name2(config_param, new_wg_seg)

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

        for wg_file in config_param.wg_seg_input:
            logging.info('{} original segments loading ...'.format(wg_file))

            if os.path.exists(wg_file):
                file_name = wg_file  # os.path.join(root_dir, wg_file)
            else:
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

    def mapp_prime_name2(self, config_param, wg_base):
        """
        Replace opportunity instance counter by flyby or perijove label when overlap
        is and only if needed (This mean having a _xx extension in opportunity file)

        Note: Since a segment can contain both Perijove and Flyby ensure sub-phase label start by P,
        and Flyby not.

        :param config_param: path of configuration file
        :param new_wg: Working Group segments object using opportunity names
        :return: new_wg: Working Group segments object using prime names
        """

        new_wg = copy.deepcopy(wg_base)

        opportunity_vs_prime_xx = self.get_opportunity_vs_prime_xx()

        date_vs_event = self.date_vs_event

        for wg in wg_base:

            for seg in wg_base[wg]:

                wg_seg = wg_base[wg][seg]

                # print('{}, {}, {}: {}'.format(wg_type, wg, seg, new_wg[wg_type][wg][seg]))
                # print(len(new_wg[wg_type][wg][seg]))

                if wg_seg:

                    prime_name = '_'.join(seg.split('_')[:-1])
                    if prime_name in opportunity_vs_prime_xx[wg]:

                        seg_start = wg_seg[0][0]
                        seg_end = wg_seg[0][1]

                        for event_date in sorted(date_vs_event.keys()):

                            if event_date > seg_end:
                                break

                            if seg_start <= event_date <= seg_end:

                                if '_PE' in seg:

                                    if date_vs_event[event_date].startswith('P'):
                                        new_seg = '_'.join(seg.split('_')[:-1]) + '_' \
                                                  + date_vs_event[event_date].replace('PJ', 'PE')

                                        new_wg[wg][new_seg] = new_wg[wg].pop(seg)
                                        break

                                elif '_FB' in seg or '_FLYBY' in seg:

                                    if not date_vs_event[event_date].startswith('P'):
                                        new_seg = '_'.join(seg.split('_')[:-1]) + '_' + date_vs_event[event_date]
                                        logging.debug('{}: {} ----> {}'.format(wg, seg, new_seg))
                                        new_wg[wg][new_seg] = new_wg[wg].pop(seg)

                                        break

                                else:

                                    new_seg = '_'.join(seg.split('_')[:-1]) + '_' + date_vs_event[event_date]

                                    new_wg[wg][new_seg] = new_wg[wg].pop(seg)
                                    break

        # Check for Flyby or perijoves not assigned to crema perijove or flyby
        seg_to_delete = []
        for wg in wg_base:

            for seg in new_wg[wg]:

                fb_pe = seg.split('_')[-1]

                if '_PE' in seg:

                    if fb_pe.replace('PE', 'PJ') not in self.fb_pe_events.keys():

                        logging.warning('The Perijove corresponding to this seg is not in current crema; '
                                        f'removing {wg}: {seg}')
                        if logging.DEBUG >= logging.root.level:
                            for period in new_wg[wg][seg]:
                                print(f'\t[{period[0]} - {period[1]}]')

                        seg_to_delete.append([wg, seg])

                elif '_FB' in seg or '_FLYBY' in seg:

                    if fb_pe[0].isdigit() and fb_pe not in self.fb_pe_events.keys():

                        logging.debug('The flyby corresponding to this seg is not in current crema; '
                                        f'removing {wg}: {seg}')
                        if logging.DEBUG >= logging.root.level:
                            for period in new_wg[wg][seg]:
                                print(f'\t[{period[0]} - {period[1]}]')

                        seg_to_delete.append([wg, seg])

        for (wg, seg) in seg_to_delete:

            new_wg[wg].pop(seg)

        return new_wg

    def rename_mult2_prime_seg(self, wgx):
        """
        Rename segment opportunities to prime segment names when defined.

        Note: if not defined (i.e. DL_) maintain the old name.

        :param wgx: working group x object including segments
        :return: wgx: updated working group x object including segments
        """

        new_wgx = {}
        seg_to_clean = []

        for wg in wgx:

            new_wgx[wg] = {}

            mult_segs_2_prime = self.mult_segs_2_prime[wg]

            if mult_segs_2_prime == []:
                continue

            seg_values = list(wgx[wg].items())

            for opp_seg_names, prime_name in mult_segs_2_prime:

                new_segment_list = []

                for opp_seg_name in opp_seg_names:

                    for seg, val in seg_values:

                        if opp_seg_name in seg:
                            # logging.debug(': multi >>> {} vs {}'.format(seg, opp_seg_name))

                            new_segment_list.extend(val)
                            seg_to_clean.append(seg)

                new_wgx[wg][prime_name] = new_segment_list

        if seg_to_clean:
            sub_wgx_to_delete = self.select_wgx_subset(wgx, seg_filter=seg_to_clean)

            wgx = self.get_wg_sub(wgx, sub_wgx_to_delete)

            wgx = self.add_wgx_segments(wgx, new_wgx)

        return wgx

    def rename_seg_2_prime(self, wg_seg_list):
        """
        Rename segments to corresponding prime name

        :param wg: working group segments
        :return: new_wg_seg_list: new working group segments
        """

        new_wg_seg_list = []

        for wg_seg in wg_seg_list:
            wg_seg_prime_mapping.reset_opportunity_2_prime_seg_mapping_using_wild_card(
                wg_seg, self.opportunity_vs_prime)
            wgx = wg_seg_prime_mapping.seg_opportunity_2_prime_seg(wg_seg, self.opportunity_vs_prime)

            new_wg_seg_list.append(wgx)

        return new_wg_seg_list

    def get_opportunity_vs_prime_xx(self):
        """
        Get the list of prime segment to be stamped with Flyby or Perijove Identifier
        :return opportunity_vs_prime_xx, a dictionary containing the list of original segment for each Working group
        """

        opportunity_vs_prime_xx = {}

        for wg in self.opportunity_vs_prime:

            opportunity_vs_prime_xx[wg] = []

            for seg in self.opportunity_vs_prime[wg]:

                prime_name = self.opportunity_vs_prime[wg][seg]

                if prime_name.endswith('xx'):
                    opportunity_vs_prime_xx[wg].append(seg)

        return opportunity_vs_prime_xx

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

    def check_mpad_rules(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm):
        """
        Checking mpad rules

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
        logging.info('Checking MPAD rules ...')

        self.check_mpad_downlink_rules(dl_)


    def check_mpad_downlink_rules(self, wg_base):
        """
        Checking mpad downlink constraints:
         - Maximum period without downlink
         - Minimum downlink segment duration

        :param wg_base: working group containing all downlink segments
        """        

        # Default value is 4 hours in seconds
        dl_segment_minimum_sec = self.__get_config_property('dl_segment_minimum_sec', 4 * 3600)   

        # Default value is 48 hours in seconds
        dl_maximun_gap_sec = self.__get_config_property('dl_maximun_gap_sec', 48 * 3600)  


        p = IntervalHandlers()
        list_all = []
        for wg in wg_base.values():
            for seg_group in wg.values():
                for seg in seg_group:
                    start, end = seg
                    duration = (end - start).total_seconds() 
                    if duration < dl_segment_minimum_sec:
                        logging.warning(f'MPAD rule violation: Minimun DL segment duration {duration} '
                                        f'[min {dl_segment_minimum_sec} secs] @ {start}')
                    list_all.append(seg)

        list_all = p.merge_intervals(list_all)
        gaps = p.not_intervals(list_all)
        for [gap_start, gap_end] in gaps:
                duration = (gap_end - gap_start).total_seconds() 
                if duration > dl_maximun_gap_sec:
                    logging.warning(f'MPAD rule violation: Gap between DL {duration} '
                                    f'[max {dl_maximun_gap_sec} secs] @ {gap_start}')

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

        :param list_of_wg:
        :param report_order:
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

        my_report = SegmentationReportFilter(self.mission_phases, report_order,
                                             output_dir=self.output_dir,
                                             config=self.config)
        my_report.create_report(new_wg_metrics, new_seg_types_metrics)

    def check_and_set_up_output_dir(self, output_dir):

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
                            file_prefix, file_suffix='.csv'):
        """

        Create Timeline file for all og Working Group Segments

        :param wg1: working group 1 object including segments
        :param wg2: working group 2 object including segments
        :param wg3: working group 3 object including segments
        :param wg4: working group 4 object including segments
        :param wgx: working group x object including segments
        :param dl_: downlink object including segments
        :param fd_nav: flight Dynamic navigation object including segments
        :param fd_wol: flight Dynamic wheel of loading object including segments
        :param fd_tcm: flight Dynamic rcm object including segments
        :param fd_navephem: FD navcam ephemerides
        :param wg_all: all working group [1, 2, 3, 4, x]
        :param file_prefix: output file prefix
        :param file_suffix:  output file suffix
        :return:
        """

        # seg.write_segment_file(file_prefix + '_all' + file_suffix, [wg_all])
        self.write_segment_file(file_prefix + '_WG1' + file_suffix, [wg1])
        self.write_segment_file(file_prefix + '_WG2' + file_suffix, [wg2])
        self.write_segment_file(file_prefix + '_WG3' + file_suffix, [wg3])
        self.write_segment_file(file_prefix + '_WG4' + file_suffix, [wg4])
        self.write_segment_file(file_prefix + '_WGX' + file_suffix, [wgx])
        self.write_segment_file(file_prefix + '_DL' + file_suffix, [dl_])
        self.write_segment_file(file_prefix + '_FD' + file_suffix, [fd_nav, fd_tcm, fd_wol, fd_navephem])
