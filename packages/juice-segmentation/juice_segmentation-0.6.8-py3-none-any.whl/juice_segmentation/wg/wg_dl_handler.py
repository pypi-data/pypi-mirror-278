"""
Created on May 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows handle specific feature for dl segmentation files
"""

import datetime
import logging

from juice_segmentation.wg.wg_seg_basic_ops import WgSegBasicOps


class WgDlSegmentHandler(WgSegBasicOps):
    """
    This Module allows to run segmentation files
    """

    def __init__(self, mission_phases, fb_pe_events, output_dir='./'):

        self.mission_phases = mission_phases
        self.fb_pe_events = fb_pe_events

        logging.debug(f'output path: {output_dir}')

        super(WgDlSegmentHandler, self).__init__()

    def dl_extend(self, dl, periods_to_extend=[], dt_extension=8*3600):
        """
        Extend downlink until 17H summing 8h to the 9H = 2*30min slew + 8H input DL_

        :param dt_extension: Number of seconds to be added to initial DL
        :param dl: downlink segments
        :param periods_to_extend: list of period or phases where dl_ must be extended
        :return: dl: updated downlink segments
        """

        periods_to_extend = self.expand_variable_in_intervals(periods_to_extend)

        dt_to_extend = self.select_wgx_subset_by_time(dl, 'GENERIC', 'DL_', intervals=periods_to_extend)

        dl = self.wg_substract(dl, [dt_to_extend])

        dt_to_extend = self.reset_wgx_segments_start_end(dt_to_extend, end_shift=dt_extension)

        dt_to_extend = self.rename_wgx_segments(dt_to_extend, seg_new_names={'DL_': 'DL_EXT'})

        dl = self.merge_wgx_segments(dl, dt_to_extend)

        return dl

    def expand_variable_in_intervals(self, interval):
        """
        Expand periods/intervals according to

        :param interval: parameters to set interval/periods around perijoves
        :return: new_interval: list of extended periods around perijove
        """

        new_interval = []

        for p in interval:

            new_interval.append(self.expand_variable_in_interval(p['start'], p['end'], p['duration']))

        return new_interval

    def expand_variable_in_interval(self, start=None, end=None, duration=0):
        """
        Create interval/periods around perijoves using 2 of the 3 parameters
        start, end, and duration

        :param duration: period duration in seconds
        :param end: end time
        :param start: start time
        :return: [start, end]: extended period
        """

        duration = datetime.timedelta(seconds=duration)

        if start is not None:

            if isinstance(start, str):  # Check if single event and substitute by time:

                start = self.find_fb_pe_event(start)

                if start in self.fb_pe_events.keys():

                    start = self.fb_pe_events[start]

                else:

                    logging.error('Unknown Event "{}" in interval'.format(start))

        if end is not None:

            if isinstance(end, str):  # Check if single event and substitute by time:

                end = self.find_fb_pe_event(end)

                if end in self.fb_pe_events.keys():

                    end = self.fb_pe_events[end]

                else:

                    logging.error('Unknown Event "{}" in interval'.format(end))

        if duration.total_seconds() > 0:

            if start and end is None:

                end = start + duration

            elif start is None and end:

                start = end - duration

        return [start, end]

    def find_fb_pe_event(self, event):
        """
        Return first event matching with label fractal;

        :param event: event name
        :return: fb_pe: perijove mapping with event name
        """

        for fb_pe in self.fb_pe_events.keys():

            if event in fb_pe:

                logging.info('{} mapped to {} for DL_EXT set-up'.format(event, fb_pe))
                break

        return fb_pe
