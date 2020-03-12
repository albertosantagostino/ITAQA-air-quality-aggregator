#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle CSV files
"""

import csv

def save_csv(csv_data, relative_file_path):
    # TODO: Add a specific directory to save data
    with open(relative_file_path, 'w') as csvfile:
        csvfile.write(csv_data)
