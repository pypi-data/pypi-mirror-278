"""
Created on March 2022

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT rest-api

"""

import os
import sys
import logging
import requests
import getpass

from esac_juice_pyutils.commons.json_handler import create_file


class PlanStats(object):
    """
    This Class allows read and parse SHT plan files
    """

    def __init__(self, output_dir="./", plan_name="", url_base="https://juicesoc.esac.esa.int",
                 crema_id=None, user_name=None, password=None):

        self.output_dir = output_dir
        self.plan_name = plan_name
        self.url_base = url_base
        self.crema_id = crema_id
        self.token = None

        self.list_of_plans = self.get_list_of_plans()

        if user_name:
            if password is None:
                password = getpass.getpass(
                    "Enter the password corresponding to user_name '{}' to connect to SHT: ".format(user_name))

            self.token = get_token(url_base, user_name, password)
            if self.token is None:
                logging.error('Seems you user_name/password are not correct = {}/{}'.format(user_name, password))
                sys.exit()

            self.list_of_plans = self.get_list_of_trajectory_plans()

    def get_list_of_plans(self):
        """
        Get the list of public Plans

        :return: list_of_plans:  the list of all public plan
        """

        list_of_plans = get_list_of_plans(output_dir=self.output_dir, file_name='plan')

        return list_of_plans

    def get_list_of_trajectory_plans(self):
        """
        Get the list of Crema dependent Plans

        'url_base/trajectory/{mnemonic}/plan' where mnemonic is the "crema_id"
        * if the token is not provided get the list of public plans for crema_id
        * if the token is provided get the list of private plans for crema_id

        :return: list_of_plans:  the list of Crema dependent Plans
        """

        url = os.path.join(self.url_base, 'rest_api', 'trajectory', self.crema_id)
        list_of_plans = get_list_of_plans(url=url, output_dir=self.output_dir, file_name='plan', token=self.token)

        return list_of_plans

    def get_list_of_trajectories(self):
        """
        Get the list of Crema

        Note: this list is private, so token (user_name+password) is needed

        'url_base/trajectory"
        :return: list_of_trajectories:  the list of Crema dependent Plans
        """
        if self.token is None:

            logging.error('Cannot request list of trajectories without specifying user_name and password')
            sys.exit()

        url = os.path.join(self.url_base, 'rest_api', 'trajectory')
        list_of_plans = get_list_of_plans(url=url, output_dir=self.output_dir, file_name='plan', token=self.token)

        return list_of_plans

    def get_plan_stats(self):

        plan_id = self.get_plan_id(self.plan_name)

        if plan_id is None:
            logging.error('Plan "{}" does not exist or not public in SHT "{}/rest_api/plan"'.format(self.plan_name,
                                                                                                    self.url_base))
            sys.exit()

        else:

            stats = get_plan_stats(plan_id, output_dir=self.output_dir, token=self.token)

        return stats

    def get_segmentation_plan(self):
        """
        Ret
        :return:
        """

        plan_id = self.get_plan_id(self.plan_name)

        if plan_id is None:
            logging.error('Plan "{}" does not exist or not public in SHT: "{}/rest_api/plan"'.format(self.plan_name,
                                                                                                     self.url_base))
            sys.exit()

        else:

            response_json = get_plan_stats(plan_id, output_dir=self.output_dir, file_name='', timeout=120,
                                           token=self.token)

        file_path = os.path.join(self.output_dir, 'segmentation_plan.json')
        create_file(file_path, response_json)
        logging.info('file created: {}'.format(file_path))

        return file_path

    def get_plan_id(self, plan_mnemonic):

        plan_id = None

        for p in self.list_of_plans:

            if p['name'] == plan_mnemonic:
                plan_id = p['id']
                break

        return plan_id


def get_plans(url, timeout=20, token=None):
    """
    Get json plan via REST_API

    :param url: url of Plan
    :param timeout: number of seconds to try retransmission before timeout
    :param token: SHT REST-API token
    :return: response.json: segmentation definition json
    """

    try:

        if token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + token
            }

            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            # Code here will only run if the request is successful

        else:

            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as err:
        logging.error('requests.exceptions.HTTPError')
        print(err)

    except requests.exceptions.ConnectionError as err:
        logging.error('requests.exceptions.ConnectionError')
        print(err)

    except requests.exceptions.Timeout as err:
        logging.error('requests.exceptions.Timeout')
        print(err)

    except requests.exceptions.RequestException as err:
        logging.error('requests.exceptions.RequestException')
        print(err)

    sys.exit()


def post_plans(url, path_to_json=None, timeout=20, token=None):
    """
    Post Plan segmentation definition json via REST_API

    :param url: url Plan
    :param path_to_json: path to json Plan
    :param timeout: number of seconds to try retransmission before timeout
    :param token: SHT REST-API token
    :return: response.json: segmentation definition json
    """

    if token:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + token
        }
    else:
        headers = None

    try:

        response = requests.post(url, json=path_to_json, timeout=timeout, headers=headers)
        response.raise_for_status()
        # Code here will only run if the request is successful

        return response.json()

    except requests.exceptions.HTTPError as err:
        print(err)

    except requests.exceptions.ConnectionError as err:
        print(err)

    except requests.exceptions.Timeout as err:
        print(err)

    except requests.exceptions.RequestException as err:
        print(err)

    sys.exit()


def get_and_create_segmentation_file(crema="CREMA_3_0",
                                     url_root='https://juicesoc.esac.esa.int/rest_api/trajectory',
                                     file_name='segment_definition',
                                     output_dir='./',
                                     generate_json_file=True):
    """
    Create segmentation definition json file using REST_API

    :param crema: Crema Id
    :param url_root: url root name
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    crema = str(crema).upper()

    url = os.path.join(url_root, crema)
    url = os.path.join(url, file_name)

    file_path = os.path.join(output_dir, file_name)

    response_json = get_plans(url)
    logging.info(f'REST_API completed: {url}')

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json


def get_list_of_plans(url='https://juicesoc.esac.esa.int/rest_api',
                      file_name='plan',
                      output_dir='./',
                      generate_json_file=True,
                      token=None):
    """
    Get a list of plan and create a json file using REST_API
    - file_name='plan': list of all public plans (don't take into account the token)
    - file_name='trajectory/{mnemonic}/plan' where mnemonic is the "crema_id"
        * if the token is not provided get the list of public plans for crema_id
        * if the token is provided get the list of private plans for crema_id

    :param url: rest-api url
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    url = os.path.join(url, file_name)

    file_path = os.path.join(output_dir, file_name)

    response_json = get_plans(url, token=token)
    logging.info(f'REST_API completed: {url}')

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json


def get_plan_stats(id, url_root='https://juicesoc.esac.esa.int/rest_api/plan',
                   file_name='stats',
                   output_dir='./',
                   generate_json_file=False,
                   timeout=10,
                   token=None):
    """
    Create json stats file using REST_API

    :param id: plan id within SHT Plans
    :param url_root: rest-api url
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    :param timeout: maximum time allowed for request in seconds
    :param token: authentication key
    """

    url = os.path.join(url_root, str(id), file_name)

    file_path = os.path.join(output_dir, file_name)

    logging.info('requesting REST_API: {}'.format(url))
    response_json = get_plans(url, timeout=timeout, token=token)
    logging.info('REST_API completed: {}'.format(url))

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json


def get_config(url='https://juicesoc.esac.esa.int/rest_api/config',
               output_dir='./',
               generate_json_file=False,
               timeout=20):
    """
    Create segmentation config json file using REST_API

    :param url: rest-api url
    :param timeout: maximum number of seconds allowed to get info
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    file_path = os.path.join(output_dir, "sht_config_units.json")

    logging.info('requesting REST_API: {}'.format(url))
    response_json = get_plans(url, timeout=timeout)
    logging.info('REST_API completed: {}'.format(url))

    if generate_json_file:
        create_file(file_path, response_json)
        logging.info('file created: {}'.format(file_path))

    return response_json


def upload_plan(new_json_plan, url='https://juicesoc.esac.esa.int/rest_api/plan',
                timeout=10):

    """
    Upload plan
    :param new_json_plan: path of new plan
    :param url: rest-api url
    :param timeout: maximum number of seconds allowed to get connection
    :return: response_json
    """

    json = os.path.abspath(new_json_plan)

    logging.info('requesting REST_API: {}'.format(url))
    response_json = post_plans(url, json, timeout=timeout)
    logging.info('REST_API completed: {}'.format(url))

    return response_json


def get_token(url_base, username, password):
    """
    GET SHT REST-API token

    :param url_base: url base root
    :param username: SHT username
    :param password: SHT password
    :return: token
    """
    url = url_base + '/api-token-auth/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data)
    if response.status_code != 200:
        return None
    return response.json().get('token')
