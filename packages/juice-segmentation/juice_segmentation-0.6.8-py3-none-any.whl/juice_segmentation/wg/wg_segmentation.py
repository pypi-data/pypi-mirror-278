"""
Created on Mars, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to test segmentation.py
"""

import os
import sys
import logging
import copy

from operator import itemgetter

from esac_juice_pyutils.commons import json_handler as my_json
from juice_segmentation.commons.mission_phases import get_mission_phases, print_mission_phases

from juice_segmentation.wg.wg_fd_handler import WgFdSegmentHandler
from juice_segmentation.wg.wg_dl_handler import WgDlSegmentHandler
from juice_segmentation.wg.wg_calib_handler import WgCalibSegmentHandler
from juice_segmentation.wg.wg_utils import set_date_vs_FB_PE_event


class WgSegmentation(object):

    def __init__(self, config_file, main_config=None, do_spice_segmentation=False):

        logging.info('Input Segments from Geopipeline')
        # for f in config_file["wg_seg_input"]:
        #     logging.info('{}'.format(f))

        if not do_spice_segmentation:
            self.main_config = main_config

            config_file['root_path'] = os.path.expandvars(config_file['root_path'])
            config_file['mission_phases'] = os.path.expandvars(config_file['mission_phases'])
            config_file['mission_timeline_event_file'] = os.path.expandvars(config_file['mission_timeline_event_file'])
            config_file['opportunity_vs_prime'] = os.path.expandvars(config_file['opportunity_vs_prime'])

        from collections import namedtuple
        eo = namedtuple('Struct', config_file.keys())(*config_file.values())
        self.config = eo

        self.output_dir = eo.output["dir"]

        if not do_spice_segmentation:

            self.file_prefix = eo.output["file_prefix"]
            self.file_sufix = eo.output["file_sufix"]

            from juice_segmentation.wg.wg_segment_handler import WgSegmentHandler

            mission_phases = get_mission_phases(eo.mission_phases)
            if logging.root.isEnabledFor(logging.DEBUG):
                print_mission_phases(mission_phases)

            date_vs_event, fb_pe_events = set_date_vs_FB_PE_event(self.config)

            self.seg = WgSegmentHandler(eo.root_path, eo.opportunity_vs_prime, mission_phases,
                                        date_vs_event, fb_pe_events,
                                        output_dir=self.output_dir, config=self.main_config)

            self.fd_seg = WgFdSegmentHandler(eo, fb_pe_events, output_dir=self.output_dir)

            self.dl_seg = WgDlSegmentHandler(mission_phases, fb_pe_events)
            self.cal_seg = WgCalibSegmentHandler(mission_phases, fb_pe_events)

        else:

            from juice_segmentation.spice_segmentation.wg_segment_handler import SpiceWgSegmentHandler

            self.seg = SpiceWgSegmentHandler(eo.root_path, output_dir=self.output_dir)

    def set_up_parameters(self, cfg_file=''):
        """
        Set up simulation parameters info according to input json file

        1) load json configuration file to x object
        2) check input parameters

        :param cfg_file: json configuration file including plot parameters
        :return: x.main: json object including inout parameters
        """

        x = my_json.load_to_object(cfg_file)

        return x.main

    def set_original_metrics(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem, create_csv=True):
        """
        Set Original metrics

        1) Set metrics
        2) For debugging purpose create original segment files

        :param wg1: windows for WG1 segments
        :param wg2: windows for WG2 segments
        :param wg3: windows for WG3 segments
        :param wg4: windows for WG4 segments
        :param wgx: windows for WGX segments (i.e. calibrations)
        :param fd_tcm: windows for TCM maneuvers
        :param fd_wol: windows for WOL maneuvers
        :param dl_:  windows for downlinks
        :param fd_navephem: WG and segments for OPE_NAV (FD moon ephemerides)
        :param fd_nav: windows for NAV maneuvers
        :param create_csv: Flag allowing to create orginale working group segment files; default=true
        """

        self.seg.set_original_metrics([wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem])

        if create_csv:
            self.seg.write_segment_files(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem,
                                         file_prefix=self.config.output["file_prefix_origin"])

    def generate_segment_and_report(self, wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem, wg_all,
                                    segment_handler=None, generate_report=True, report_order=None, create_csv=True,
                                    new_plan_name=None, other_insertion_rules=None,
                                    segment_with_dv_not_shared_by_group=[]):
        """
        Generate segments and reports

        1) Generate output without renaming for checks
           and comparison of the scheduled segments against the original segments

        2) Generate the comparison report

        3) Generate final output with segments renamed to Prime

        4) Check Gaps and if any log them

        5) Check overlaps and if any log them

        6) Check MPAD rules and if any log them

        :param segment_handler: segment handler object
        :param wg1: windows for WG1 segments
        :param wg2: windows for WG2 segments
        :param wg3: windows for WG3 segments
        :param wg4: windows for WG4 segments
        :param wgx: windows for WGX segments (i.e. calibrations)
        :param dl_:  windows for downlinks
        :param fd_nav: windows for NAV maneuvers
        :param fd_tcm: windows for TCM maneuvers
        :param fd_wol: windows for WOL maneuvers
        :param fd_navephem: WG and segments for OPE_NAV (FD moon ephemerides)
        :param wg_all: windows for all segments
        :param generate_report: flag to enforce the generation of the metrics report
        :param report_order: list of periods specifying the report order per phases/periods; defaults means by time
        :param create_csv: Flag allowing to create orginale working group segment files; default=true
        :param new_plan_name: new plan Name
        :param other_insertion_rules: rules for generic scheduling;
        use to set DATA_VOLUME for segment instance when needed (in json plan),
        :param segment_with_dv_not_shared_by_group: list of segments which scheduled subsegment DVs are not to be share
        by group but assigned for subsegment so scheduled sub-segment have a total DV_final = n * DV_initially_specified
        """

        file_sufix = self.file_sufix
        file_prefix = self.file_prefix

        seg = self.seg

        # Generate segment Files with internal names including instance numbers (mainly for debugging)

        wg_all_without_seg_renaming = copy.copy(wg_all)
        if create_csv:
            seg.write_segment_file(file_prefix + '_all_without_seg_renaming' + file_sufix, [wg_all])
            wg_all_without_fd = seg.wg_substract(wg_all, [fd_nav, fd_tcm, fd_wol, fd_navephem])
            seg.write_segment_file(file_prefix + '_all_without_seg_renaming_and_without_fd' + file_sufix,
                                   [wg_all_without_fd])

        # Set Final Metrics and generate the corresponding report
        if generate_report:
            seg.set_final_metrics_and_report([wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem],
                                             report_order)

        # Check if any overlap and report it
        seg.check_if_overlaps_within_proper_segments(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm)

        # Renaming to prime name (i.e. simplified one without instance number used by Timeline Tool)
        # And Generate Segment Files
        logging.debug('Renaming segment to prime names used by Timeline Tool')
        seg.rename_seg_2_prime([wg1, wg2, wg3, wg4, wgx, wg_all])
        seg.rename_seg_2_prime([fd_nav, fd_tcm, fd_wol, fd_navephem])
        new_segment_file = file_prefix + '_all' + file_sufix

        seg.write_segment_file(new_segment_file, [wg_all])

        if create_csv:
            seg.write_segment_files(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_tcm, fd_wol, fd_navephem, file_prefix)

        if segment_handler is not None:
            segment_csv_file = os.path.join(seg.output_dir, new_segment_file)
            # segment_handler.create_json_segment_file_from_segment_csv(segment_csv_file)
            json_filename = segment_csv_file.replace('.csv', '.json')
            wg_seg_list = sorted(seg.wg_seg_to_list([wg_all_without_seg_renaming]), key=itemgetter(1, 2))
            segment_handler.create_json_segment_file_from_list(
                wg_seg_list, json_filename,
                seg.opportunity_vs_prime,
                new_plan_name, other_insertion_rules=other_insertion_rules,
                segment_with_dv_not_shared_by_group=segment_with_dv_not_shared_by_group)

            if not create_csv:
                os.remove(segment_csv_file)

        # Check overlaps
        seg.get_and_report_gaps(wg_all)

        # Check if any overlap and report it
        logging.info('Checking for segment overlaps')
        seg.check_if_overlaps(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm)
        seg.check_if_overlaps_within_proper_segments(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm)

        # Check MPAD rules
        seg.check_mpad_rules(wg1, wg2, wg3, wg4, wgx, dl_, fd_nav, fd_wol, fd_tcm)

    def get_wgx_cal_roll(self, wgx, selection_per_phase):
        """
        Get Calibration roll segments

        :param wgx: windows for WGX segments (i.e. calibrations)
        :param selection_per_phase: selection of input calibration segment per mission phase
        :return: segment for calibration
        """

        for phase, calibs in selection_per_phase.items():

            if phase not in self.cal_seg.mission_phases.keys():
                logging.error('"{}" not in mission_phases keys()'.format(phase))
                logging.error('valid keys are: {}'.format(self.cal_seg.mission_phases.keys()))
                sys.exit()

            self.cal_seg.mission_phases[phase].call_roll = calibs

        return self.cal_seg.get_wgx_cal_roll(wgx, self.cal_seg.mission_phases)

    def schedule_ope_nav(self, wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, fd_ope_nav, wgx_sun_conjunction,
                         fd_nav,
                         wg3_ops='JUPITER_GM',
                         ja_m='JUPITER_MONITORING',
                         ja_pe='JUPITER_PERIJOVE',
                         rs='_FB_RS',
                         other_wg4_seg=['STAR_OCC', 'JUPITER_INCLINED_AURORA', 'INCLINED_NORTH', "INCLINED_SOUTH"]):
        """
        Allocate OPE_NAV on a daily basis according to rule

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
        :param dl_:  windows for downlinks
        :param fd_ope_nav: WG and segments for OPE_NAV (FD moon ephemerides)
        :param wgx_sun_conjunction: Solar Conjunction windows
        :param fd_nav: windows for NAV maneuvers
        :param other_wg4_seg: star occultation segment name filter
        :param rs: moon remote sensing segment name filter
        :param ja_pe: jypiter perijove  segment name filter
        :param ja_m:  jupiter monitoring segment name filter
        :param wg3_ops: WG3 segments allowed to insert openav
        :return: fd_navephem_selected, wg1, wg2, wg3, wg4, fd_tcm, fd_wol, dl_
        """

        seg = self.fd_seg  # self.seg

        wg1234x = seg.wg_add(wg1, [wg2, wg3, wg4, wgx])
        start, end = seg.get_start_end_WG1234x(wg1234x)

        wg3_for_ope_nav = seg.select_wgx_subset(wg3, seg_filter=[wg3_ops])
        wg3_for_ope_nav = seg.wg_substract(wg3_for_ope_nav, [wgx_sun_conjunction])

        wg4_for_ope_nav = [seg.select_wgx_subset(wg4, seg_filter=[ja_m])]

        for other_wg4 in other_wg4_seg:
            wg4_for_ope_nav.append(seg.select_wgx_subset(wg4, seg_filter=[other_wg4]))

        wg4_ju_pe = seg.select_wgx_subset(wg4, seg_filter=[ja_pe])

        wg2_for_ope_nav = [seg.select_wgx_subset(wg2, seg_filter=[rs])]

        maneuvers = seg.wg_add({}, [fd_tcm, fd_wol, dl_])
        wg_all_seg = seg.wg_add(wgx, [wg1, wg2, wg3_for_ope_nav, wg4, fd_nav, fd_tcm, fd_wol, dl_])
        fd_navephem_selected, dl_ = seg.get_fd3_ephem_periods(fd_ope_nav, wg3_for_ope_nav, dl_, maneuvers,
                                                              wg4=wg4_for_ope_nav,
                                                              wg2=wg2_for_ope_nav,
                                                              wgx=[wgx],
                                                              wg_all=wg_all_seg,
                                                              wg4_jup_pe=wg4_ju_pe,
                                                              start=start,
                                                              end=end)

        wg4 = seg.wg_substract(wg4, [fd_navephem_selected])
        wg2 = seg.wg_substract(wg2, [fd_navephem_selected])
        wg3 = seg.wg_substract(wg3, [fd_navephem_selected])
        wgx = seg.wg_substract(wgx, [fd_navephem_selected])

        return fd_navephem_selected, wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_

    def schedule_ope_nav_4(self, wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_, fd_ope_nav, wgx_sun_conjunction,
                           fd_nav,
                           my_rules):
        """
        Allocate OPE_NAV on a daily basis according to rule

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
        :param dl_:  windows for downlinks
        :param fd_ope_nav: WG and segments for OPE_NAV (FD moon ephemerides)
        :param wgx_sun_conjunction: Solar Conjunction windows
        :param fd_nav: windows for NAV maneuvers
        :param my_rules: Python structure defining OPNAV insertion rules to be applied
        :return: fd_navephem_selected, wg1, wg2, wg3, wg4, fd_tcm, fd_wol, dl_
        """

        seg = self.fd_seg  # self.seg

        wg1234x = seg.wg_add(wg1, [wg2, wg3, wg4, wgx])
        wg1234x = seg.wg_substract(wg1234x, [wgx_sun_conjunction])

        for rule in my_rules:

            wg_seg_list = []
            for wg, seg_list in rule["seg"]:
                seg_list_slots = seg.select_wgx_subset(wg1234x, wg_filter=[wg], seg_filter=seg_list)
                wg_seg_list.append(seg_list_slots)

            rule["seg_instance"] = wg_seg_list

        maneuvers = seg.wg_add({}, [fd_tcm, fd_wol, dl_])

        wg_all_seg = seg.wg_add(wg1234x, [fd_nav, fd_tcm, fd_wol, dl_])

        if my_rules:  # if rules empty then take OPNAV and DL as is

            start, end = seg.get_start_end_WG1234x(wg1234x)

            if start is None or end is None:
                logging.error('We need ALLOWED segments to insert OPNAV; check configuration file')
                sys.exit()

            fd_navephem_selected, dl_ = seg.get_fd_ephem_periods_generic(fd_ope_nav, dl_, maneuvers,
                                                                         wg_all_seg,
                                                                         my_rules,
                                                                         start=start,
                                                                         end=end)
        else:

            fd_navephem_selected = fd_ope_nav

        wg4 = seg.wg_substract(wg4, [fd_navephem_selected])
        wg2 = seg.wg_substract(wg2, [fd_navephem_selected])
        wg3 = seg.wg_substract(wg3, [fd_navephem_selected])
        wgx = seg.wg_substract(wgx, [fd_navephem_selected])

        return fd_navephem_selected, wg1, wg2, wg3, wg4, wgx, fd_tcm, fd_wol, dl_
