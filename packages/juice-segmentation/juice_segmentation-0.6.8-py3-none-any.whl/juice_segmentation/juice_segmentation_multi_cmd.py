"""
Created on Jun, 2021

@author: Claudio Munoz Crego (ESAC)

This module allows to call juice_segmentation module using a command line.

"""

import argparse
import logging
import os
import signal
import sys

from esac_juice_pyutils.commons.my_log import setup_logger
from esac_juice_pyutils.commons.json_handler import load_to_dic

from juice_segmentation.commons.sht_rest_api import PlanStats

from juice_segmentation import version


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters
    - JsonFile: path of the configuration file
    - version: package version number
    - loglevel: debug, info
    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--JsonFile",
                        help="Path of JsonFile defining report(s) required",
                        required=True)

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

    if args.JsonFile:
        if not os.path.exists(args.JsonFile):
            logging.error('Configuration File "{}" does not exist'.format(args.JsonFile))
            sys.exit(0)
        elif not os.path.isfile(args.JsonFile):
            logging.error('"{}" is not a file'.format(args.JsonFile))
            sys.exit(0)
        else:
            config_file = os.path.abspath(args.JsonFile)
            cfg_file = load_to_dic(config_file)

    else:
        logging.error('Please define MTP Configuration File')
        sys.exit(0)

    logging.info('start')

    from juice_segmentation.segmentation_multi.segmentation import generate_proposal_file

    here = os.path.abspath(os.path.dirname(__file__))
    working_dir = os.path.dirname(config_file)
    os.chdir(working_dir)

    output_dir = cfg_file['main']["output_dir"]
    if not os.path.isdir(output_dir):
        logging.error('output directory path does not exists: {}'.format(os.path.abspath(output_dir)))
        logging.error('Please create it')
        sys.exit()

    if "plan_name" in list(cfg_file['main'].keys()):

        user_name = None
        password = None

        if "user_name" in list(cfg_file['main'].keys()):
            user_name = cfg_file['main']['user_name']

            if "password" in list(cfg_file['main'].keys()):
                password = cfg_file['main']['password']

        plan = PlanStats(output_dir=output_dir,
                         plan_name=cfg_file['main']['plan_name'],
                         crema_id=cfg_file['main']['crema_id'],
                         user_name=user_name, password=password)

        input_file = plan.get_segmentation_plan()
        logging.info('Using SHT Plan via REST-API as input: {}'.format(input_file))

    else:
        input_file = cfg_file['main']["input_segmentation_file_path"]
        logging.info('Using Local copy of SHT Plan as input: {}'.format(input_file))

    create_csv = True
    if 'create_csv' in cfg_file['main']:
        create_csv = cfg_file['main']["create_csv"]

    if 'wg_segments_to_ignore' in cfg_file['main'].keys():

        if cfg_file['main']['wg_segments_to_ignore']:
            generate_proposal_file(input_file, output_dir, cfg_file['main'], create_csv=create_csv,
                                   wg_segments_to_ignore=cfg_file['main']["wg_segments_to_ignore"])
    else:

        generate_proposal_file(input_file, output_dir, cfg_file['main'], create_csv=create_csv)

    os.chdir(here)
    logging.debug('goto root original directory: {}'.format(here))

    logging.info('end!')


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


if __name__ == "__main__":

    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        logging.exception(e)
        print("<h5>Internal Error. Please contact SGS System</h5>")

    sys.exit(0)  # setting exit code to 0, indicating success
