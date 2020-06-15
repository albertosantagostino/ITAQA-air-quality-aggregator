#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle CSV files
"""

import csv
import pickle
import requests


def save_csv(csv_data, relative_file_path):
    """Save a csv locally"""
    # TODO: Hardcode directory?
    with open(relative_file_path, 'w') as csvfile:
        csvfile.write(csv_data)


def download_csv(url, file_path):
    """Download a csv, given the url"""
    print(f"Download started ({url})")
    with requests.Session() as s:
        ret = s.get(url)
    csv_file = ret.content.decode('utf-8')
    pickle.dump(csv_file, open(file_path, 'wb'))


def read_csv(file_path):
    """Read a pickled csv file"""
    csv_file = pickle.load(open(file_path, 'rb')).splitlines()
    reader = csv.reader(csv_file)
    return reader, len(csv_file)
