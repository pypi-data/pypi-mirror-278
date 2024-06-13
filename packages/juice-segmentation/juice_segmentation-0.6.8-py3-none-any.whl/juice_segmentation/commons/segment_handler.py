"""
Created on April 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle segment files

"""

import copy
import logging
import os
import sys
from operator import itemgetter

import juice_segmentation.commons.sht_rest_api as rest_api
from esac_juice_pyutils.commons.json_handler import load_to_dic, create_file
from esac_juice_pyutils.periods.event_period_merger import PeriodMerger
from esac_juice_pyutils.periods.intervals_handler import IntervalHandlers
from juice_segmentation.commons.segment_definition_handler import SegmentDefinitionHandler, get_dico, \
    get_map_segment_vs_group
from juice_segmentation.wg.wg_utils import json_str_2_datatime, datetime2utc_json


class SegmentHandler(object):
    """
    This Class allows read and parse segment files
    """

    def __init__(self, input_file, output_dir="./",
                 wg_segments_to_ignore=[], start=None, end=None):

        self.output_dir = output_dir
        self.input_file = input_file

        self.main_dico = read_segment(input_file)

        self.select_period_if_provided(start, end)

        if len(wg_segments_to_ignore) > 0:
            self.remove_segment_to_ignore(wg_segments_to_ignore)

        self.sht_units_vs_category = self.get_sht_units()

    def select_period_if_provided(self, start=None, end=None):
        """
        Select sub_period if start or end not None

        :param start: start of sub period
        :param end: end of sub period
        """

        new_segment_list = []

        segments = self.main_dico['segments']
        for ele in segments:

            seg_start = json_str_2_datatime(ele['start'])
            seg_end = json_str_2_datatime(ele['end'])

            if start:

                if seg_end < start:

                    continue

                elif start > seg_start:

                    ele['start'] = datetime2utc_json(start)

            if end:

                if seg_start > end:

                    continue

                elif end < seg_end:

                    ele['end'] = datetime2utc_json(end)

            new_segment_list.append(ele)

        self.main_dico['segments'] = new_segment_list

    def create_sub_plan_for_selected_period(self, start, end, output_dir='./'):
        """
        Create sub plan in json format for [start, end] periods

        :param start: start of scheduling period
        :param end: end of scheduling period
        :param output_dir: output directory path
        """
        import json

        start_str = str(start).replace(':', '').replace('-', '').replace(' ', '')
        end_str = str(end).replace(':', '').replace('-', '').replace(' ', '')
        out_file_path = os.path.join(output_dir, f'wg_all_{start_str}_{end_str}.json')

        with open(out_file_path, "w") as outfile:
            json.dump(self.main_dico, outfile, indent=4)

        logging.info(f'file create: {outfile}')

    def remove_segment_to_ignore(self, wg_segments_to_ignore):
        """
        Remove segment to ignore if any

        :param wg_segments_to_ignore: dictionary including WG, segment to ignore
        """

        new_segment_list = []

        segments = self.main_dico['segments']
        for ele in segments:

            seg = ele['segment_definition']

            seg_to_add = True

            for wg_seg in wg_segments_to_ignore:

                if wg_seg in seg:
                    seg_to_add = False
                    break

            if seg_to_add:
                new_segment_list.append(ele)

        self.main_dico['segments'] = new_segment_list

    def select_segment(self, wg_segments=[]):
        """
        Remove segment to ignore if any

        :param wg_segments_to_ignore: dictionary including WG, segment to ignore
        """

        new_segment_list = []

        segments = self.main_dico['segments']
        for ele in segments:

            seg = ele['segment_definition']

            seg_to_add = False

            for wg_seg in wg_segments:

                if wg_seg in seg:
                    seg_to_add = True
                    break

            if seg_to_add:
                new_segment_list.append(ele)

        self.main_dico['segments'] = new_segment_list

        return self.main_dico['segments']

    def get_dico(self):
        """
        Return dico of segment

        :return: segment: dictionary including key, value
        """

        from collections import namedtuple

        dico = {}
        for seg in self.main_dico['segments']:

            seg['start'] = json_str_2_datatime(seg['start'])
            seg['end'] = json_str_2_datatime(seg['end'])

            seg_def = namedtuple('Struct', seg.keys())(*seg.values())
            if seg_def.segment_definition not in dico.keys():
                dico[seg_def.segment_definition] = [seg_def]
            else:
                dico[seg_def.segment_definition].append(seg_def)

        return dico

    def get_clean_dico(self):

        from collections import namedtuple

        merge = PeriodMerger()
        interval = IntervalHandlers()

        dico = {}
        for seg in self.main_dico['segments']:

            seg['start'] = json_str_2_datatime(seg['start'])
            seg['end'] = json_str_2_datatime(seg['end'])

            if seg['segment_definition'] not in dico.keys():
                dico[seg['segment_definition']] = [seg]
            else:
                dico[seg['segment_definition']].append(seg)

        keys = [k for k in list(dico.keys()) if 'OPNAV' not in k]

        for segment_definition in keys:

            seg_def = dico[segment_definition]

            new_seg_def = [seg_def[0]]
            prev_seg = new_seg_def[0]

            for i in range(1, len(seg_def)):

                seg = seg_def[i]

                p1 = [prev_seg['start'], prev_seg['end']]
                p2 = [seg['start'], seg['end']]

                overlap = merge.get_period_overlap(p1, p2)

                if overlap:
                    merge_period = interval.merge_intervals([p1, p2])[0]

                    new_seg_def[i - 1]['start'] = merge_period[0]
                    new_seg_def[i - 1]['end'] = merge_period[1]

                if seg['start'] == prev_seg['end']:

                    new_seg_def[i - 1]['end'] = seg['end']

                else:

                    new_seg_def.append(seg)
                    prev_seg = seg

            dico[segment_definition] = new_seg_def

        for k, seg_def_list in dico.items():

            for i in range(len(seg_def_list)):
                dico[k][i] = namedtuple('Struct', seg_def_list[i].keys())(*seg_def_list[i].values())

        return dico

    def get_list_of_segments(self, seg_vs_wg, sort=True):
        """
        Return dico of segment

        :param seg_vs_wg:
        :param sort:
         :return: segment_list: dictionary including key, value
        """

        segment_list = []

        for seg in self.main_dico['segments']:

            seg_name = seg['segment_definition']

            if seg_name not in seg_vs_wg.keys():
                logging.error(
                    'segment "{}" is not defined in segment_definition file: {}'.format(seg_name, self.input_file))
                logging.error('It will be ignored; Please review segmentation file input')
                continue

            start, end = seg['start'], seg['end']

            segment_list.append([seg_name, start, end, '', seg_vs_wg[seg_name]])

        if sort:
            segment_list = sorted(segment_list, key=itemgetter(1, 2, 3, 4))

        return segment_list

    def create_csv_segment_file(self, segment_definition_file_path=None,
                                crema_id='CREMA_3_0',
                                wg_csv_file_path='input/wg_all.csv'):
        """
        Create segment file

        :param segment_definition_file_path: segment definition file path
        :param crema_id: crema identifier
        :param wg_csv_file_path: output file path for wg_all csv file
        :return:
        """

        if segment_definition_file_path is not None:

            segment_def_handler = SegmentDefinitionHandler(segment_definition_file_path)
            get_vs_group = segment_def_handler.map_segment_vs_group

        else:

            response_json = rest_api.get_and_create_segmentation_file(crema=crema_id, generate_json_file=False)
            dico = get_dico(response_json)
            get_vs_group = get_map_segment_vs_group(dico)

        new_list = self.get_list_of_segments(get_vs_group)

        f = open(wg_csv_file_path, 'w')
        for rec in new_list:
            (r_segment, r_start, r_end, dummy, r_wg) = (rec[0], rec[1].replace('.000Z', 'Z'),
                                                        rec[2].replace('.000Z', 'Z'), rec[3], rec[4])
            f.write('{},{},{},{},{}\n'.format(r_segment, r_start, r_end, dummy, r_wg))

        logging.info('file create: {}'.format(wg_csv_file_path))

    def create_json_segment_from_list(self, segment_list, opportunity_vs_prime=None, new_plan_name=None,
                                      other_insertion_rules=None,
                                      segment_with_dv_not_shared_by_group=[]):
        """
        Create json contents from list of working group - segment

        For each segment instance get segment attributes and parameters from original Segmentation Plan

            * if original segment has resource or resource type and is cut then create a new group to specify
             the resources and resource types

            * if segment instance is other segment scheduled via generic scheduling and DV assigned, then include it
             in the final segment instance

        :param segment_with_dv_not_shared_by_group:
        :param segment_list: list of working group-segment
        :param opportunity_vs_prime: opportunity_vs_prime mapping
        :param new_plan_name: new plan Name,
        :param other_insertion_rules: rules for generic scheduling; use to set DATA_VOLUME
        for segment instance when needed (in json plan)
        :param segment_with_dv_not_shared_by_group: list of segments which scheduled subsegment DVs are not to be share
        by group but assigned for subsegment so scheduled sub-segment have a total
        DV_final = n * (DV_initially_specified)
        """

        original_seg = self.get_dico()

        if new_plan_name is None:
            new_plan_name = self.main_dico["mnemonic"] + '_new'

        new_json = {"trajectory": self.main_dico["trajectory"],
                    "mnemonic": new_plan_name,
                    "name": self.main_dico["name"] + '_new',
                    "description": self.main_dico["description"]}

        if "is_public" in list(self.main_dico.keys()):
            new_json["is_public"] = self.main_dico["is_public"]

        new_segments = new_json["segments"] = []
        new_json["segment_groups"] = self.main_dico["segment_groups"]

        if "refine_log" in list(self.main_dico.keys()):
            new_json["refine_log"] = self.main_dico["refine_log"]

        if "spice_info" in list(self.main_dico.keys()):
            new_json["spice_info"] = self.main_dico["spice_info"]
        else:
            new_json["kernels"] = self.main_dico["kernels"]

        new_json["default_block"] = self.main_dico["default_block"]
        new_json["default_slew_policy"] = self.main_dico["default_slew_policy"]

        new_segment_group = {}
        segment_groups = new_json["segment_groups"]

        for seg in segment_list:

            seg_id = seg[0]
            seg_start, seg_end = json_str_2_datatime(seg[1]), json_str_2_datatime(seg[2])
            seg_time = (seg_end - seg_start).total_seconds()

            wg_id = seg[4]
            segment_definition = seg_id

            if segment_definition in segment_with_dv_not_shared_by_group:
                segment_with_dv_shared_by_group = False
            else:
                segment_with_dv_shared_by_group = True

            if opportunity_vs_prime:
                segment_definition = segment_opportunity_2_prime_name(seg_id, wg_id, opportunity_vs_prime)

            if seg_id in original_seg.keys():

                segment_identified = False

                for seg_inst in original_seg[seg_id]:

                    total_time = (seg_inst.end - seg_inst.start).total_seconds()

                    if seg_inst.start <= seg_start < seg_inst.end:

                        if seg_inst.start < seg_end <= seg_inst.end:

                            # print({"start": datetime2utc_json(seg_start),
                            #     "end":  datetime2utc_json(seg_end),
                            #     "segment_definition": segment_definition,
                            #     "overwritten": seg_inst.overwritten,
                            #     "instrument_overwritten": seg_inst.instrument_overwritten,
                            #     "timeline": "PRIME"})

                            my_seg = {}
                            if hasattr(seg_inst, 'id'):
                                my_seg["id"] = seg_inst.id

                            my_seg["start"] = datetime2utc_json(seg_start)
                            my_seg["end"] = datetime2utc_json(seg_end)

                            if hasattr(seg_inst, 'resources'):
                                my_seg["resources"] = seg_inst.resources
                                my_seg = self.update_resource_and_group(
                                    seg_inst, segment_groups, total_time, seg_time, my_seg, new_segment_group,
                                    segment_with_dv_shared_by_group)
                            elif hasattr(seg_inst, 'instrument_resources'):
                                my_seg["instrument_resources"] = seg_inst.instrument_resources
                                my_seg = self.update_resource_and_group(
                                    seg_inst, segment_groups, total_time, seg_time, my_seg, new_segment_group,
                                    segment_with_dv_shared_by_group)
                            elif hasattr(seg_inst, 'resources') and hasattr(seg_inst, 'instrument_resources'):
                                my_seg["resources"] = seg_inst.resources
                                my_seg["instrument_resources"] = seg_inst.instrument_resources
                                my_seg = self.update_resource_and_group(
                                    seg_inst, segment_groups, total_time, seg_time, my_seg, new_segment_group,
                                    segment_with_dv_shared_by_group)
                            else:
                                my_seg["segment_definition"] = segment_definition

                            if hasattr(seg_inst, 'segment_group'):
                                my_seg["segment_group"] = seg_inst.segment_group

                            my_seg["overwritten"] = seg_inst.overwritten
                            my_seg["instrument_overwritten"] = seg_inst.instrument_overwritten
                            my_seg["timeline"] = "PRIME"

                            if hasattr(seg_inst, 'pointing_request_snippet'):
                                my_seg["pointing_request_snippet"] = seg_inst.pointing_request_snippet
                            if hasattr(seg_inst, 'slew_policy'):
                                my_seg["slew_policy"] = seg_inst.slew_policy

                            new_segments.append(my_seg)

                            segment_identified = True

                            break  # only one solution expected

                if not segment_identified:
                    logging.warning('Segment cannot be linked to original segment '
                                    '(this means is no part of original segment): {}'.format(seg))
            else:

                logging.debug('Segment {} not in original segment'.format(seg_id))

                new_segments.append({
                    "start": datetime2utc_json(seg_start),
                    "end": datetime2utc_json(seg_end),
                    "segment_definition": segment_definition,
                    "overwritten": False,
                    "instrument_overwritten": False,
                    "timeline": "PRIME",
                    "pointing_request_snippet": "",
                    "slew_policy": "KEEP_BLOCK"
                })

        # segment_groups = self.main_dico["segment_groups"]
        # list_of_seg_types = list(seg_types_total_duration.keys())
        # new_segments_groups = new_json["segment_groups"] = self.main_dico[
        #     "segment_groups"]  # TODO: reset resources: need total time per WG, instrument

        return new_json

    def create_json_segment_file_from_segment_csv(self, csv_file):
        """
        Create json from Working group - segment csv file

        :param csv_file: csv path
        """

        segment_list = []
        f = open(csv_file, 'r')
        for ele in f.readlines():
            segment_list.append(ele.split(','))

        new_json = self.create_json_segment_from_list(segment_list)
        file_name = os.path.basename(csv_file).replace('.csv', '.json')
        file_name = os.path.join(os.path.dirname(csv_file), file_name)
        create_file(file_name, new_json)
        logging.info('file create: {}'.format(file_name))

    def create_json_segment_file_from_list(self, wg_seg, file_path, opportunity_vs_prime, new_plan_name,
                                           other_insertion_rules=None, segment_with_dv_not_shared_by_group=[]):
        """
        Create json from Working group - segment list

        :param opportunity_vs_prime: mapp segment opportunity name to segment prime names
        :param file_path: json file path
        :param wg_seg: Working group - segment list
        :param new_plan_name: New plan Name
        :param other_insertion_rules: rules for generic scheduling;
        use to set DATA_VOLUME for segment instance when needed (in json plan)
        :param segment_with_dv_not_shared_by_group: list of segments which scheduled subsegment DVs are not to be share
        by group but assigned for subsegment so scheduled sub-segment have a total
        DV_final = n * DV_initially_specified
        """

        new_json = self.create_json_segment_from_list(
            wg_seg,
            opportunity_vs_prime, new_plan_name,
            other_insertion_rules=other_insertion_rules,
            segment_with_dv_not_shared_by_group=segment_with_dv_not_shared_by_group)

        create_file(file_path, new_json)
        logging.info('file create: {}'.format(file_path))

    def update_resources(self, resources, total_duration, duration):
        """
        Update simulation resources if needed

        :param resources: experiment Data rate or data volume
        :param total_duration: total duration
        :param duration: experiment durations
        :return: new_resources: updated experiment Data rate or data volume
        """

        new_resources = copy.deepcopy(resources)

        for resource in new_resources:

            unit = resource['unit']

            category = self.sht_units_vs_category[unit]

            if category == 'DATA_VOLUME':

                resource['value'] = resource['value'] * duration / total_duration
                print(resource['value'])

            elif category == 'ENERGY':

                resource['value'] = resource['value'] * duration / total_duration

            elif category == 'DATA_RATE':

                pass  # Nothing todo

            elif category == 'POWER':

                pass  # Nothing todo

        return new_resources

    def update_resource_and_group(self, seg_inst, segment_groups, total_duration, duration, my_seg, new_group,
                                  segment_with_dv_shared_by_group=True):
        """
        Update segment instance(s) and group resources if needed

        This means if the original segment resource are DATA_VOLUME or ENERGY
        In this case a new group is created with those resources which are removed from segment instance(s)

        :param seg_inst: segment instance object
        :param segment_groups: segment groups
        :param total_duration: total duration original segment
        :param duration: duration of segment in seconds
        :param my_seg: current segment
        :param new_group: current groups
        :param segment_with_dv_shared_by_group: segment DVs are share by group
        :return:
        """

        list_of_segment_group = [seg_group['mnemonic'] for seg_group in segment_groups]
        new_resources = []
        new_instrument_resources = []
        new_mnemonic = None

        mnemonic = seg_inst.segment_definition
        # logging.debug('id: {}; mnemonic: {}; new_mnemonic: {}'.format(seg_inst.id, mnemonic, new_mnemonic))

        if duration < total_duration:
            mnemonic = seg_inst.segment_definition
        elif duration == total_duration:
            my_seg["segment_definition"] = seg_inst.segment_definition
            return my_seg

        resources = []
        if hasattr(seg_inst, 'resources'):
            resources = seg_inst.resources

        for resource in resources:

            category = resource['category']

            if (category == 'DATA_VOLUME' or category == 'ENERGY') and segment_with_dv_shared_by_group:

                new_group_resource = {"instrument_type": resource["instrument_type"],
                                      "category": resource["category"],
                                      "target": resource["target"],
                                      "unit": resource["unit"],
                                      "value": resource["value"]}

                if mnemonic not in list_of_segment_group:

                    if str(mnemonic).endswith('_'):
                        new_mnemonic = mnemonic + '{}'.format(seg_inst.id)
                    else:
                        new_mnemonic = mnemonic + '_{}'.format(seg_inst.id)

                    if new_mnemonic not in list(new_group.keys()):

                        new_group[new_mnemonic] = {}
                        new_group[new_mnemonic]["name"] = new_mnemonic + '_GROUP'
                        new_group[new_mnemonic]["mnemonic"] = new_mnemonic
                        new_group[new_mnemonic]["resources"] = [new_group_resource]

                    else:

                        if "resources" in list(new_group[new_mnemonic].keys()):
                            for r in new_group[new_mnemonic]["resources"]:

                                if new_group_resource != r:
                                    # logging.warning('resource duplicated for {}: {}'.format(new_mnemonic, r))
                                    new_group[new_mnemonic]["resources"].append(new_group_resource)

            else:
                new_resources.append(resource)

        my_seg["resources"] = new_resources
        if len(my_seg["resources"]) == 0:
            my_seg.pop("resources")

        instrument_resources = []

        if hasattr(seg_inst, 'instrument_resources'):
            instrument_resources = seg_inst.instrument_resources

        for instrument_resource in instrument_resources:

            category = instrument_resource['category']

            if (category == 'DATA_VOLUME' or category == 'ENERGY') and segment_with_dv_shared_by_group:

                new_group_instrument_resource = {"instrument": instrument_resource["instrument"],
                                                 "category": instrument_resource["category"],
                                                 "target": instrument_resource["target"],
                                                 "unit": instrument_resource["unit"],
                                                 "value": instrument_resource["value"]}

                if mnemonic not in list_of_segment_group:

                    if str(mnemonic).endswith('_'):
                        new_mnemonic = mnemonic + '{}'.format(seg_inst.id)
                    else:
                        new_mnemonic = mnemonic + '_{}'.format(seg_inst.id)

                    if new_mnemonic not in list(new_group.keys()):

                        new_group[new_mnemonic] = {}
                        new_group[new_mnemonic]["name"] = new_mnemonic + '_GROUP'
                        new_group[new_mnemonic]["mnemonic"] = new_mnemonic
                        new_group[new_mnemonic]["instrument_resources"] = [new_group_instrument_resource]

                    elif "instrument_resources" not in new_group[new_mnemonic]:

                        new_group[new_mnemonic]["instrument_resources"] = [new_group_instrument_resource]

                    else:

                        for r in new_group[new_mnemonic]["instrument_resources"]:

                            if new_group_instrument_resource != r:
                                # logging.warning('resource duplicated for {}: {}'.format(new_mnemonic, r))
                                new_group[new_mnemonic]["instrument_resources"].append(new_group_instrument_resource)

            else:
                new_instrument_resources.append(instrument_resource)

        my_seg["instrument_resources"] = new_instrument_resources
        if len(my_seg["instrument_resources"]) == 0:
            my_seg.pop("instrument_resources")

        if new_mnemonic:

            my_seg["segment_definition"] = mnemonic

            if new_mnemonic not in list_of_segment_group:
                segment_groups.append(new_group[new_mnemonic])
                logging.info('New instrument group created: {}'.format(new_mnemonic))

            my_seg["segment_group"] = new_mnemonic
            my_seg["origin"] = "segment linked to new group from segmentation scheduler"

        else:

            my_seg["segment_definition"] = seg_inst.segment_definition

        return my_seg

    def add_resources_for_other_rules(self, seg_inst, other_resources):
        """
        Add resources specification for seg_inst in other_resources (if needed)

        :param seg_inst:
        :param other_resources:
        :return:
        """
        pass

    def get_sht_units(self):
        """
        Generate MAPPS units versus category

        :return: sht_units_vs_type
        """

        sht_config = rest_api.get_config()
        sht_units = sht_config['units']

        sht_units_vs_category = {}
        for unit in sht_units:
            sht_units_vs_category[unit['mnemonic']] = unit['category']

        return sht_units_vs_category


def segment_opportunity_2_prime_name(seg_id, wg_id, opportunity_vs_prime):
    """
    Rename segment to prime name if and only if it is a segment opportunity.
    This means the segment name is no changed else

    :param seg_id: segment identifier
    :param wg_id:  working group identifier
    :param opportunity_vs_prime: opportunity_vs_prime mapping
    :return: segment_definition, the segment name
    """

    segment_definition = seg_id

    if seg_id in opportunity_vs_prime[wg_id].keys():
        opp_seg_prime_name = opportunity_vs_prime[wg_id][seg_id]
        segment_definition = seg_id.replace(seg_id, opp_seg_prime_name)
    else:
        identifier = '_'.join(seg_id.split('_')[:-1])
        if identifier in opportunity_vs_prime[wg_id].keys():
            opp_seg_prime_name = opportunity_vs_prime[wg_id][identifier]
            opp_seg_prime_name = opp_seg_prime_name.replace('_xx', '').replace('_PExx', '')
            segment_definition = seg_id.replace(identifier, opp_seg_prime_name)

    return segment_definition


def read_segment(input_file):
    """
    Read json info from file

    :param input_file: input file path
    :return: segment: dictionary including key, value
    """

    logging.debug('Reading file: {}'.format(input_file))

    if not os.path.exists(input_file):
        logging.error('File does not exist: {}'.format(input_file))
        sys.exit()

    else:

        try:

            dico = load_to_dic(input_file)

            # Reorder list of segment; should not be needed, but just in case
            from operator import itemgetter
            dico['segments'] = sorted(dico['segments'], key=itemgetter('start', 'end'))

        except Exception as e:
            print(e)
            logging.error('Error reading file: Please check {}'.format(input_file))
            sys.exit()

    return dico


def get_absolute_start_end_segment(input_file):
    """
    Get absolute start/end segmentation plan  json info from file

    :param input_file: input file path
    :return: start, end time
    """

    segments = read_segment(input_file)['segments']
    start = segments[0]['start']
    end = segments[-1]['end']

    return start, end