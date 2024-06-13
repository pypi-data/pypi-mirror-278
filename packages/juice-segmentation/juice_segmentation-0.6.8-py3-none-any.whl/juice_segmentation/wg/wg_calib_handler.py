"""
Created on May 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows handle specific feature for Calibration segmentation instances
"""

import datetime
import logging

from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps


class WgCalibSegmentHandler(WgSegBasicOps):
    """
    This Module allows to run segmentation files
    """

    def __init__(self, mission_phases, fb_pe_events, output_dir='./'):

        self.mission_phases = mission_phases
        self.fb_pe_events = fb_pe_events

        super(WgCalibSegmentHandler, self).__init__()

    # def get_wgx_cal_roll(self, wgx, selection_per_phase):
    #     """
    #     Get Calibration roll segments
    #
    #     :param wgx:  windows for WGX segments (i.e. calibrations)
    #     :param selection_per_phase: set of JMAG Calibration roll pero phase
    #     :return: selected JMAG Calibration rolls
    #     """
    #
    #     for phase, calibs in selection_per_phase.items():
    #         self.mission_phases[phase].call_roll = calibs
    #
    #     return self.get_wgx_cal_roll(wgx, self.mission_phases)

    def get_wgx_cal_roll(self, wgx, mission_phases):
        """
        Return a working group segment including the call_roll specified in mission_phase call_roll list

        :param mission_phases: Dictionary including the mission phases periods
        :param wgx: working group segment including calibrations
        :return: wgx_calib: a working group segment object including the selected calibration
        """

        wgx_calib = {}

        if not wgx:  # empty: there is no WGX segment; then no calibrations

            return wgx_calib

        for phase in mission_phases.keys():

            interval = [mission_phases[phase].start, mission_phases[phase].end]

            wgx_calib_subset = self.select_wgx_subset_by_time(wgx, intervals=[interval])

            if wgx_calib_subset["WGX"]:

                for seg in wgx_calib_subset["WGX"].keys():

                    if 'CAL' in seg:

                        wgx_calib_subset = self.get_instances_of_wg_seg(
                            wgx_calib_subset, "WGX", seg, interval_numbers=mission_phases[phase].call_roll)

                        if seg == 'JMAG_CALROLL':

                            for i in range(len(wgx_calib_subset["WGX"]['JMAG_CALROLL'])):
                                wgx_calib_subset["WGX"]['JMAG_CALROLL'][i] \
                                    = self.select_jmag_call_period_around_perijove(
                                    wgx_calib_subset["WGX"]['JMAG_CALROLL'][i])

                        wgx_calib = self.merge_wgx_segments(wgx_calib, wgx_calib_subset)

                        if 'JMAG_CALROLL' in wgx_calib_subset["WGX"]:
                            if len(wgx_calib_subset["WGX"]['JMAG_CALROLL']) > 0:
                                subset_periods = [[s - e] for [s,e] in wgx_calib_subset["WGX"]['JMAG_CALROLL']]
                                logging.info(f'[{phase}: {mission_phases[phase].description}]: '
                                             f'instance WGX:{seg} included in timeline: {subset_periods}')

                        # segment detail available using seg.print_segment_details(wgx_calib)

        return wgx_calib

    def select_jmag_call_period_around_perijove(self, calib_instance, delta_dt_seconds=6 * 3600):
        """
        Select Calibration  +/- 6 hour around perijove

        1) find perijove within CALROLL (if no perijove within CALROLL raise an error)
        2) cut CALL +/- 6 hours around perijove

        Note: if the -/+ 6 hours exceed the CALROLL period then cut itt to the CALROLL limit
        and raise a warning log.


        :param wgx_calib_instance: calibration full window
        :return: calib: +/- 6 hour around perijove
        """

        dt = datetime.timedelta(seconds=delta_dt_seconds)

        flag = False
        for k, t in self.fb_pe_events.items():

            if str(k).startswith('P'):

                if calib_instance[0] <= t <= calib_instance[1]:

                    if calib_instance[0] <= t - dt:

                        calib_instance[0] = t - dt
                        dt_0 = dt

                    else:

                        dt_0 = t - calib_instance[0]
                        logging.warning('Perijove [{}] - 6H out of calibration slot [{} - {}]; Set to - {}'.format(
                            t, calib_instance[0], calib_instance[1], dt_0))

                    if calib_instance[1] >= t + dt:

                        calib_instance[1] = t + dt
                        dt_1 = dt

                    else:

                        dt_1 = calib_instance[1] - t
                        logging.warning('Perijove [{}] + 6H out of calibration slot [{} - {}]; Set to + {}'.format(
                            t, calib_instance[0], calib_instance[1], dt_1))

                    logging.info('Calibration set [- {}; + {}] around {}[{}]: [{} - {}]'.format(
                        dt_0, dt_1, k, t, calib_instance[0], calib_instance[1]))

                    flag = True

                    break

        if not flag:

            logging.error('Cannot found perijove within calibration period: [{} - {}]'.format(
                calib_instance[0], calib_instance[1]))

        return calib_instance
