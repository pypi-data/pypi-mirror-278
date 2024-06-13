"""
Created on October 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to report juice_segmentation metrics
"""

import logging
import os
import sys
from operator import itemgetter

import numpy as np

from juice_segmentation.report.rst_report import RstReport


class SegmentationReportFilter(object):
    """
    This class allows to report Segmentation simulation Metrics
    """

    def __init__(self, mission_phases, report_order=None, output_dir='./', config=None):

        self.output_dir = output_dir
        self.plots_path = os.path.join(output_dir, 'plots')
        if not os.path.exists(self.plots_path):
            os.mkdir(self.plots_path)
            logging.debug(f'Missing "plots" subdirectory created: {self.plots_path}')

        self.mission_phases = mission_phases

        self.config = config
        if config is None:
            self.config = {}

        self.report_order = report_order
        self.check_and_reset_report_order()

        self.total_time = None
        if 'All phases' in list(self.mission_phases.keys()):
            (self.start, self.end) = (mission_phases['All phases'].start, mission_phases['All phases'].end)
            self.total_time = (self.end - self.start)

    def check_and_reset_report_order(self):
        """
        Check and reset reporting order

        1) if None: set to mission_phase ones ordered by time
        2) Check sub_period are defined as input, if not raise an error and stop execution

        """

        tmp = []
        for k, o in self.mission_phases.items():
            tmp.append([k, o.start, o.end])

        tmp = list(np.array(sorted(tmp, key=itemgetter(1, 2, 0))).T[0])

        if self.report_order is None:

            self.report_order = tmp

        for sub_period in self.report_order:

            if sub_period not in tmp:

                logging.error('period "{}" not defined in in input'.format(sub_period))
                logging.error('cannot be reported; please fix it')
                sys.exit()

    def create_report(self, wg_ratio_metrics, wg_seg_radio_metrics=None):
        """
        Creates Soa reports

        :param wg_ratio_metrics: wg metrics
        :param wg_seg_radio_metrics: wg wg_seg_radio_metrics
        """

        logging.info('Start report')

        proc_report = RstReport(self.plots_path, out='rst', output_path=os.path.abspath(self.output_dir))
        title = 'Juice Segmentation Summary Report'
        objective_summary = \
            "This report includes metrics corresponding to the merging/cutting " \
            "according given rules of wg segment needed for the science planning"
        proc_report.print_summary_intro(title, objective_summary)

        proc_report.write_text('\n* Trajectory is crema_3.2')

        if self.total_time:
            proc_report.write_text('\n* the operation duration is [{}: {}] <=> {}'.format(
                self.start, self.end, self.total_time))

        proc_report.write_head_section('Working group times')

        # proc_report.write_text('Note: In this section "cut" means "Sum of selected segment from original ones",
        #                        and then:\n'
        #                        '\n* "cut/orig %": "cut against the corresponding original segment" '
        #                        '\n* "cut/total %": "cut against the total time of the corresponding phase(s)"\n')

        proc_report.write_text(
            'Note: In this section "cutted" means "Sum of selected segment from original ones", and then:\n'
            '\n* "Opportunities": Sum of all the segment opportunity windows'
            '\n* "Selected": Sum of all the segment instances windows selected'
            '\n* "% Selected": % of selected instance against the original segment opportunity windows'
            '\n* "% Selected/Total": % of selected instance against the total time allowed for a given phases"')

        for phase in self.report_order:

            phase_description = self.mission_phases[phase].description
            (start, end) = (self.mission_phases[phase].start, self.mission_phases[phase].end)
            call_roll = self.mission_phases[phase].call_roll

            proc_report.write_head_subsection('{}: {}'.format(phase, phase_description))
            proc_report.write_text('\n[{}: {}] <=> {}\n'.format(start, end, end-start))
            proc_report.write_text('\n{} calibration'.format(len(call_roll)))
            proc_report.write_text(': instances {} of the phase\n\n'.format(len(call_roll)))

            if len(wg_seg_radio_metrics[phase]) > 1:   # do not print empty tables

                proc_report.print_rst_table(wg_ratio_metrics[phase])

                percent_table = {}
                fd = 0

                for line in wg_ratio_metrics[phase][1:-1]:
                    if 'FD' in line[0]:
                        fd += float(line[-1])
                    else:
                        percent_table[line[0]] = float(line[-1])

                percent_table['J_FD'] = round(fd, ndigits=3)
                if sum(percent_table.values()) < 100:
                    percent_table['Not used'] = round(100 - sum(percent_table.values()), ndigits=3)

                if sum(list(percent_table.values())) > 0:  # Avoid null plot

                    title = "Prime Segment percent against total time for phase {}".format(phase)

                    proc_report.create_plot_pie(self.plots_path, title, percent_table, min_values=0.1)
                    fig = os.path.join('plots', title.replace(' ', '_') + '.png')
                    proc_report.rst_insert_figure(fig, title=title, text=objective_summary)

            else:

                proc_report.write_text('No segments for the phase {}!'.format(phase))

        proc_report.write_text('')

        proc_report.write_head_section('Working group and Segments times')

        # proc_report.write_text(
        #     'Note: In this section "cutted" means "Sum of selected segment from original ones", and then:\n'
        #     '\n* "cutted/orig %": "cutted" against the corresponding original segment '
        #     '\n* "cutted/total %": "cutted against the total time of the corresponding phase(s)"\n')

        proc_report.write_text(
            'Note: In this section "cutted" means "Sum of selected segment from original ones", and then:\n'
            '\n* "Opportunities": Sum of all the segment opportunity windows'
            '\n* "Selected": Sum of all the segment instances windows selected'
            '\n* "% Selected": % of selected instance against the original segment opportunity windows'
            '\n* "% Selected/Total": % of selected instance against the total time allowed for a given phases"')

        for phase in self.report_order:

            phase_description = self.mission_phases[phase].description
            (start, end) = (self.mission_phases[phase].start, self.mission_phases[phase].end)
            call_roll = self.mission_phases[phase].call_roll

            proc_report.write_head_subsection('{}: {}'.format(phase, phase_description))
            proc_report.write_text('\n[{}: {}] <=> {}\n\n'.format(start, end, end - start))
            proc_report.write_text('\n{} calibration'.format(len(call_roll)))
            proc_report.write_text(': instances {} of the phase\n\n'.format(len(call_roll)))

            if len(wg_seg_radio_metrics[phase]) > 1:   # do not print empty tables
                proc_report.print_rst_table(wg_seg_radio_metrics[phase])

            else:
                proc_report.write_text('No segments for the phase {}!'.format(phase))

        # proc_report.write_text('[{}: {}] <=> {}'.format(self.start, self.end, self.total_time))
        proc_report.print_summary_end()

        if 'generate_only_rst_report' in list(self.config.keys()):
            if self.config['generate_only_rst_report']:
                logging.info('End report')
                return 0

        proc_report.rst_to_html()

        # We no longer generate the pdf report --> proc_report.rst2pdf(self.get_template_rst2pdf())

        proc_report.pandoc_html_to_docx(docx_style_file=self.get_template_docx())

        logging.info('End report')

    def get_template_rst2pdf(self):
        """
        Get the rst2pdf.style template hosted in source code within templates sub-directory

        :return: rst2pdf.style  path
        :rtype: python path
        """

        here = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(here, 'templates')
        template_file = os.path.join(template_file, 'default_rst2pdf.style')

        if not os.path.exists(template_file):
            logging.error('reference template file "%s" missing' % template_file)
            sys.exit()

        logging.info('{} loaded'.format(template_file))

        return template_file

    def get_template_docx(self):
        """
        Get the style.docx template hosted in source code within templates sub-directory

        orientation_landscape: Flag to enforce A4 landscape orientation; default False

        :return: style.docx path
        :rtype: python path
        """

        default_template = 'custom-reference.docx'

        here = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(here, 'templates')
        template_file = os.path.join(template_file, default_template)

        if not os.path.exists(template_file):
            logging.error('reference template file "%s" missing' % template_file)
            sys.exit()

        logging.info('{} loaded'.format(template_file))

        return template_file
