#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle data download
"""

import requests
import csv


def obtain_csv_data(url):
    """Given the url of a csv file, return a csv.reader object and the number of lines"""
    # TODO: Handle connection issues
    # TODO: Add progress bar
    # TODO: Consider the header in the number of lines, if present
    with requests.Session() as s:
        ret = s.get(url)
    csv_content = ret.content.decode('utf-8').splitlines()
    reader = csv.reader(csv_content)

    return reader, len(csv_content)
