"""
Created on April 2021

@author: Claudio Munoz Crego (ESAC)

This module allows to call spice_segmentation module using a command line.

"""

import argparse
import logging
import os
import signal
import sys

from esac_juice_pyutils.commons.my_log import setup_logger

from juice_segmentation import version


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters
    - outputDir: path of the Output directory
    - inputDir: path of the input directory
    - version: package version number
    - loglevel: debug, info
    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--inputDir",
                        help="Path of input directory where to find spice csv files",
                        required=True)

    parser.add_argument("-o", "--outputDir",
                        help="Path of output for juice_x_y.csv",
                        required=False)

    parser.add_argument("-s", "--start",
                        help="start time (i.e., '2031-01-19T19:14:21')",
                        required=False)

    parser.add_argument("-e", "--end",
                        help="end time (i.e., '2035-09-29T00:00:00')",
                        required=False)

    parser.add_argument("-v", "--version",
                        help="version number",
                        action="version",
                        version='%(prog)s {}'.format(version))

    parser.add_argument("-l", "--loglevel",
                        help=" Must be debug, info ",
                        required=False)

    args = parser.parse_args()
    return args


def main():
    """
        Entry point for processing

        :return:
        """

    signal.signal(signal.SIGINT, func_signal_handler)

    args = parse_options()

    if args.loglevel:
        if args.loglevel in ['info', 'debug']:
            setup_logger(args.loglevel)
        else:
            setup_logger()
            logging.warning(
                'log level value "{0}" not valid (use debug);  So default INFO level applied'.format(args.loglevel))
    else:
        setup_logger()

    if not args.inputDir:
        logging.error('Please provide inputDir')
        sys.exit(0)

    if not os.path.exists(args.inputDir):
        logging.error('inputDir does not exist: {}'.format(args.inputDir))
        sys.exit(0)
    elif not os.path.isdir(args.inputDir):
        logging.error('inputDir is not a directory: {}'.format(args.inputDir))
        sys.exit(0)
    else:
        input_dir = os.path.abspath(args.inputDir)

    if args.outputDir:

        if not os.path.exists(args.outputDir):
            logging.error('outputDir does not exist: {}'.format(args.outputDir))
            sys.exit(0)
        elif not os.path.isdir(args.outputDir):
            logging.error('outputDir is not a directory: {}'.format(args.outputDir))
            sys.exit(0)
        else:
            output_dir = os.path.abspath(args.outputDir)

    else:
        output_dir = './'
        logging.info('output dir node provided; Set to local dir "./" = {}'.format(os.path.abspath(output_dir)))

    from juice_segmentation.spice_segmentation.spice_segmentation \
        import generate_spice_segmentation_non_overlapping_segment

    start, end = check_start_end(args.start, args.end)

    from juice_segmentation.spice_segmentation import input_file_pattern

    generate_spice_segmentation_non_overlapping_segment(
        input_dir, output_dir, start=start, end=end, input_file_pattern=input_file_pattern)


def debug():
    """
    debug: Print exception and stack trace
    """

    e = sys.exc_info()
    print("type: %s" % e[0])
    print("Msg: %s" % e[1])
    import traceback
    traceback.print_exc(e[2])
    traceback.print_tb(e[2])


def check_start_end(start_0, end_0):

    import esac_juice_pyutils.commons.tds as tds

    date_format = '%Y-%m-%dT%H:%M:%S'

    start = None
    end = None

    if start_0 is not None:
        start = tds.str2datetime(start_0, date_format)
        if start is None:
            sys.exit()

    if end_0 is not None:
        end = tds.str2datetime(end_0, date_format)
        if end is None:
            sys.exit()

    if start and end and start >= end:
        logging.error('start >= end: {} >= {}; Please review input parameters'.format(start, end))
        sys.exit()

    return start, end


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        logging.exception(e)
        print("<h5>Internal Error. Please contact SGS System</h5>")

    sys.exit(0)  # setting exit code to 0, indicating success
