"""
Created on February, 2018

@author: Claudio Munoz Crego (ESAC)

This Module allows to generate an rst report
"""

import logging
import os
import sys

from esac_juice_pyutils.commons.rst_handler import RstHandler


class RstReport(RstHandler):
    """
    This class allows to generate an rst report
    """

    def __init__(self, input_path, output_path='', out=sys.stdout):
        """
        :param output_path:
        :param out:
        :param input_path: path of directory containing plots
        """

        if not os.path.exists(input_path):
            logging.error('input path "{}" does not exist'.format(input_path))
        else:
            self.input_path = os.path.abspath(os.path.expandvars(input_path))

        if output_path == '':
            output_path = self.input_path
            if not os.path.exists(output_path):
                logging.error('output path "{}" does not exist'.format(output_path))

        self.output_dir = output_path

        super(RstReport, self).__init__(output_path, out)

    def print_summary_intro(self, title='Title', objective_summary='', metrics=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        self.write_head_chapter(title.upper())
        self.out.write('.. contents:: Table of Contents\n')
        # self.out.write('\n.. section - numbering::\n\n')

        self.write_head_section('Introduction')
        intro = ("\n"
                 ".. |date| date::\n"
                 ".. |time| date:: %H:%M:%S\n"
                 "\n"
                 "This document was automatically generated on |date| at |time|.\n\n")

        self.out.write(intro)

        self.out.write('\n' + objective_summary + '\n')
        if len(metrics) > 0:
            # self.print_rst_metrics_summary_table([['uno', 1.00,'unit']])
            self.print_rst_table(metrics)

    def print_summary_end(self):
        """
        Produces summary end
        """

        self.out.close()
        logging.info('rst file {} generated'.format(self.rst_file_name))

    def print_summary_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro for subsection

        :param title: subsection title
        :param objective_summary: summary of the objective of study
        :param metrics: summary metrics
        :param figure: subsection list of plots
        """

        self.write_head_subsection(title)
        self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            # self.print_rst_metrics_summary_table([['uno', 1.00,'unit']])
            self.print_rst_table(metrics)

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                if not os.path.exists(fig):
                    logging.error('input path "{}" does not exist'.format(fig))
                else:
                    self.rst_insert_figure(fig, title=title, text=objective_summary)

    def print_summary_sub_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro for sub-subsection

        :param title: sub-subsection title
        :param objective_summary: summary of the objective of study
        :param metrics: summary metrics
        :param figure: subsection list of plots
        """

        self.write_head_subsubsection(title)
        self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            self.print_rst_csv_table(metrics, title)
            self.out.write('\n')

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                self.rst_insert_figure(fig, title=title, text=objective_summary)

    def create_plot_pie(self, plots_path, title, percent, min_values=0):
        """
        Create pie plot

        :param min_values: the min value to plot, i.e. 0.01 %; mainly remove too small values
        :param plots_path: plots
        :param title: Plot title
        :param percent: percentage
        :return: plot_file_path: path of plot directory
        """

        import matplotlib.pyplot as plt

        percent_keys = list(percent.keys())
        for k in reversed(percent_keys):
            if percent[k] < min_values:
                del percent[k]

        labels = sorted(percent.keys())
        sizes = [percent[k] for k in labels]
        labels = ['{} [{}%]'.format(k, percent[k]) for k in labels]
        explode = [i % 2 * 0.1 for i, x in enumerate(percent.keys())]

        pies = plt.pie(sizes, startangle=90, autopct='%1.0f%%', pctdistance=0.9, radius=1.2,
                       explode=explode)

        plt.legend(pies[0], labels, bbox_to_anchor=(1, 0.5), loc="center right", fontsize=8,
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.50)

        plt.axis('equal')
        plot_file_path = os.path.join(plots_path, title.replace(' ', '_') + '.png')
        plt.savefig(plot_file_path)
        plt.close()

        return plot_file_path
