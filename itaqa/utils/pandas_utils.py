#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle pandas DataFrame objects
"""

import pandas as pd


def print_full(df):
    """Print the entire DataFrame, displaying all rows and columns"""
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


def add_new_data(old_df, new_df):
    """Given two pandas DF, concatenate them removing duplicates"""
    # TODO: Check if both have the same columns and if there are gaps in data
    dataconcat = pd.concat([old_df, new_df])
    return dataconcat.drop_duplicates().set_index('Timestamp').reset_index()
