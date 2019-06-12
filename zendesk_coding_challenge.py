#!/usr/local/bin/python3
import os
import sys
import json
import pydoc
import base64
import argparse
import requests
import pandas as pd
from pandas.io.json import json_normalize

def get_credentials(infile_path):
    """
    Takes a file containing user:password combination, returns it as string

    Arguments:
        infile_path - path to file
    """
    assert os.path.exists(infile_path), "Check that file exists or is readable!"

    with open(infile_path, mode='r') as infile:
        lines = []
        for line in infile:
            line = line.strip()
            lines.append(line)
    return lines[0]

def get_from_api(url, user=None, token=None, password=None, user_password=None, b64=False):
    """
    Takes an url, username and either token or password, returns http session

    Arguments:
        url - http or https url
        user - user name of user
        token - API authentication token
        password - utf-8 string
        user_password - user:password
    """
    if token is None and password is None and user_password is None:
        raise Exception('Either a token or a password or user:password must be provided')
    if user_password:
        if b64 is False:
            usrpas = base64.b64encode(bytes(user_password, 'utf-8')).decode('ascii')
            headers = {'Content-Type': 'application/json', 'Authorization': "Basic %s" % usrpas}
            return requests.get(url, headers=headers)
        else:
            usrpas = user_password
            headers = {'Content-Type': 'application/json', 'Authorization': "Basic %s" % usrpas}
            return requests.get(url, headers=headers)
    if user:
        if token:
            return requests.get(url, auth=(''.join([user, '/token']), token))
        if password:
            usrpas = ':'.join([user, password])
            usrpas = base64.b64encode(bytes(usrpas, 'utf-8')).decode('ascii')
            headers = {'Content-Type': 'application/json', 'Authorization': "Basic %s" % usrpas}
            return requests.get(url, headers=headers)
    else:
        raise Exception('Please specify user if not providing user:password combination')
