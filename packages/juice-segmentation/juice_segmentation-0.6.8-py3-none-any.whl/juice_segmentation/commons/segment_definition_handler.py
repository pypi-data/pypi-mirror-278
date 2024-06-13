"""
Created on April, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle segment definition file

"""

import logging
import os
import sys

from esac_juice_pyutils.commons.json_handler import load_to_dic


class SegmentDefinitionHandler(object):
    """
    This Class allows read and parse segment definition file
    """

    def __init__(self, input_file, output_dir="./"):

        self.output_dir = output_dir

        map_list = read(input_file)

        self.dico = get_dico(map_list)

        self.map_segment_vs_group = get_map_segment_vs_group(self.dico)


def read(input_file):
    """
    Read json info from file

    :param input_file: path of input file
    :return: list of segment definition
    """

    logging.debug('Reading file: {}'.format(input_file))

    if not os.path.exists(input_file):
        logging.error('File does not exist: {}'.format(input_file))
        sys.exit()

    else:

        map_list = load_to_dic(input_file)

    return map_list


def get_dico(map_list):
    """
    Return dico of segment

    :return: segment: dictionary including key, value
    """

    from collections import namedtuple

    dico = {}
    for seg in map_list:

        seg_def = namedtuple('Struct', seg.keys())(*seg.values())
        dico[seg_def.name] = seg_def

    return dico


def get_map_segment_vs_group(input_dico):
    """
    Return dico of segment

    :return: segment: dictionary including key, value
    """

    dico = {}
    for k, v in input_dico.items():

        dico[k] = v.group

    return dico
