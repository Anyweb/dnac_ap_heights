#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth
import time
import re
import urllib3

import sys
sys.path.append('./input_files')

from input_files import device_credentials
from input_files import list_floors

# Disable invalid certificate warnings.
urllib3.disable_warnings()


def get_token():
    # prepare credentials
    dnac_hostname = device_credentials.device['hostname']
    dnac_user = device_credentials.device['user']
    dnac_passw = device_credentials.device['pass']

    # get token
    base_url_token = "https://" + dnac_hostname + "/dna/system/api/v1/"
    base_url = "https://" + dnac_hostname
    url_token = "auth/token"
    url = base_url_token + url_token

    DNAC_token_header = {'content-type': 'application/json'}

    response = requests.post(url, auth=HTTPBasicAuth(username=dnac_user, password=dnac_passw),
                             headers=DNAC_token_header, verify=False)
    token = response.json()['Token']

    return token, base_url


def get_all_floors():
    token, base_url = get_token()
    url_addon = '/dna/intent/api/v1/site?type=floor'
    url = base_url + url_addon

    my_headers = {'x-auth-token': token}
    response = requests.get(url, headers=my_headers, verify=False)
    data = response.json()
    return data


def get_ids_from_floors(flor_json_data):
    floor_id_list=[]
    print("Floor IDs from DNAC:")
    for floor in flor_json_data['response']:
        floor_id = floor['id']
        print(floor_id)
        floor_id_list.append(floor_id)

    return floor_id_list


def get_all_accesspoints_from_floor(floor_id):
    token, base_url = get_token()
    url_addon = '/api/v1/dna-maps-service/domains/' + floor_id + '/aps'
    url = base_url + url_addon

    my_headers = {'x-auth-token': token}
    response = requests.get(url, headers=my_headers, verify=False)
    data = response.json()
    return data


def change_accesspoints_from_floor(floor_id, body_data):
    token, base_url = get_token()
    url_addon = '/api/v1/dna-maps-service/domains/' + floor_id + '/aps'
    url = base_url + url_addon

    my_headers = {'x-auth-token': token}
    response = requests.put(url, headers=my_headers, json=body_data, verify=False)
    data = response.json()
    return data


def change_ap_height(ap_data, height):
    changed_ap_list=[]
    for ap in ap_data['items']:
        new_ap_dict={ "attributes": {"instanceUuid": ap["attributes"]["instanceUuid"]}, "position": {"x": ap["position"]["x"], "y": ap["position"]["y"], "z": height}}
        changed_ap_list.append(new_ap_dict)

    return changed_ap_list


def change_accesspoint_height():
    floor_list = list_floors.floor_inputs
    floor_height = list_floors.floor_height
    print("Set access points to height [ft]: " + floor_height)
    if len(floor_list) != 0:
        print("Floor IDs from File:")
        print(json.dumps(floor_list))
    else:
        floor_data = get_all_floors()
        floor_list = get_ids_from_floors(floor_data)

    for floor in floor_list:
        try:
            ap_data = get_all_accesspoints_from_floor(floor)
            print("Access points on floor " + floor + ":")
            for ap in ap_data['items']:
                print(ap["attributes"]["name"])
        except:
            print("Error: no access points returned on floor: " + floor)
            print("Continue to next floor")
            continue

        changed_height_json = change_ap_height(ap_data, floor_height)
        change_response = change_accesspoints_from_floor(floor, changed_height_json)
        print(json.dumps(change_response))


if __name__ == '__main__':
    change_accesspoint_height()
