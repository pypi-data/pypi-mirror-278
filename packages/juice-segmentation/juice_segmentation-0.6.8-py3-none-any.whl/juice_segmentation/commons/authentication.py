"""
Created October 2022

@author: Claudio Munoz Crego (ESAC)

This module provides the methods allowing to get plan using SHT rest-api
"""

import requests


def get_token(url_base, username, password):
    url = url_base + '/api-token-auth/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data)
    if response.status_code != 200:
        return None
    return response.json().get('token')


def save_plan(url_base, token, plan):
    url = url_base + '/rest_api/plan/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'JWT ' + token
    }
    response = requests.post(url, json=plan, headers=headers)
    print(response.status_code)
    print(response.text)


plan = {
    'trajectory': 'CREMA_5_0',
    'mnemonic': 'TEST_PLAN',
    'name': 'TEST_PLAN',
    'is_public': True,
    'segments': [],
    'segment_groups': []
}
