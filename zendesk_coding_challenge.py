#!/usr/local/bin/python3
import os
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
