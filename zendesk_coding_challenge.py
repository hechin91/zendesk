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
pd.set_option('display.max_colwidth', -1)

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

def parse_json(session, outfile_path=None):
    """
    Takes a http session as input, returns pandas dataframe

    Arguments:
        session - http session
        outfile_path (OPTIONAL) - path to tsv file
    """
    data = session.json()
    data = json.dumps(data)
    data = pd.read_json(data)
    data = json_normalize(data=data['tickets'])
    data = (data[['id', 'external_id', 'submitter_id', 'assignee_id' ,'url', 'priority',
     'created_at', 'updated_at', 'subject', 'description', 'tags', 'status']])
    if outfile_path:
        data.to_csv(outfile_path, sep="\t")
    return data

def load_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('credentials', type=str,
                        help='File containing user:password combination')
    parser.add_argument('--chunk-size', default=25, type=int,
                        help='Display this many tickets per page (DEFAULT 25)')
    parser.add_argument('--outfile-path', default=None, type=str,
                        help='Write json data to tab separated file')

    args = parser.parse_args()

    # authentication credentials from file
    credentials_utf8 = get_credentials(args.credentials)

    # do the API call
    url = 'https://henrychin.zendesk.com/api/v2/tickets.json'
    session = get_from_api(url, user_password=credentials_utf8)

    # get json and parse json, write to outfile
    data = parse_json(session, args.outfile_path)
    return data, args.chunk_size
