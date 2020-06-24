#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle CSV files
"""

import csv
import pickle
import requests


def save_csv(csv_data, file_path):
    """Save a csv locally"""
    # TODO: Hardcode directory?
    with open(file_path, 'w') as csvfile:
        csvfile.write(csv_data)


def download_csv(url, file_path):
    """Download a csv file and pickle it"""
    print(f"Downloading {url}...")
    with requests.Session() as session:
        ret = session.get(url)
    csv_file = ret.content.decode('utf-8')
    pickle.dump(csv_file, open(file_path, 'wb'))


def read_csv(file_path):
    """Read a pickled csv file"""
    csv_file = pickle.load(open(file_path, 'rb')).splitlines()
    reader = csv.reader(csv_file)
    return reader, len(csv_file)
