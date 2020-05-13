#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle CSV files
"""

import requests
import csv
import pickle


def save_csv(csv_data, relative_file_path):
    # TODO: Add a specific directory to save data
    with open(relative_file_path, 'w') as csvfile:
        csvfile.write(csv_data)


def obtain_csv_data(url):
    """Given the url of a csv file, read it"""
    # TODO: Handle connection issues
    # TODO: Add progress bar
    # TODO: Consider the header in the number of lines, if present
    with requests.Session() as s:
        ret = s.get(url)
    csv_content = ret.content.decode('utf-8').splitlines()
    reader = csv.reader(csv_content)

    return reader, len(csv_content)


def download_csv(url, file_path):
    """Given the url of a csv file, download it and save it locally"""
    with requests.Session() as s:
        ret = s.get(url)
    csv_file = ret.content.decode('utf-8')
    pickle.dump(csv_file, open(file_path, 'wb'))


def read_csv(file_path):
    """Given the path of a pickled csv file, read it"""
    csv_file = pickle.load(open(file_path, 'rb')).splitlines()
    reader = csv.reader(csv_file)
    return reader, len(csv_file)
