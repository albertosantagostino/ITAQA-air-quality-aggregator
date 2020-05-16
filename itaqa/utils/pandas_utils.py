#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle pandas DataFrame objects
"""

import pandas as pd


def set_index_and_sort(df, index):
    """Set the index of the given DataFrame and sort it by the same index"""
    df = df.set_index(index)
    df = df.sort_index()
    return df


def print_entire(df):
    """Print the entire DataFrame, displaying all rows and columns"""
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
