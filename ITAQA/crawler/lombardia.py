#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lombardia data downloader and parser
"""

import csv
import requests

import pandas as pd

import ipdb
import json


def get_PM10_csv():

    # Download csv
    # TODO: Handle connection exceptions
    with requests.Session() as s:
        ret = s.get('https://www.dati.lombardia.it/resource/ib47-atvt.csv')

    decoded_csv = ret.content.decode('utf-8').splitlines()
    reader = csv.reader(decoded_csv)

    # Prepare header
    header_row = next(reader, None)
    header_row[16] = 'Limiti amministrativi 2014'
    header_row[17] = 'Limiti amministrativi 2015'

    metadata_dict = {}
    # TODO: Optimization
    for row in reader:
        tuplelist = []
        for i in range(1, len(row)):
            if (header_row[i] == 'location'):
                row[i] = row[i].replace(',  ', '')
            if (header_row[i] == 'unitamisura'):
                row[i] = row[i].replace('Â', '')
            tuplelist.append((header_row[i], row[i]))
        sensor_id = int(row[0])
        metadata_dict[sensor_id] = {key: value for (key, value) in tuplelist}

    metadata_pd = pd.DataFrame(metadata_dict)


if __name__ == "__main__":
    get_PM10_csv()
