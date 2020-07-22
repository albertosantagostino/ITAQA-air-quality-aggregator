#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle pandas DataFrame objects
"""

import pandas as pd


def print_full(df):
    """Print the entire df, displaying all rows and columns"""
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


def merge_dfs(dfs):
    """Given two dfs, concatenate them removing duplicates"""
    # TODO: Check if both have the same columns and fields and if there are gaps in data
    # TODO: Support more than 2 dfs
    dataconcat = pd.concat([dfs[0], dfs[1]])
    return dataconcat.drop_duplicates().set_index('Timestamp').reset_index()


def reorder_columns(df):
    """Given a df, reorder the columns alphabetically"""
    cols = df.columns.tolist()
    cols.remove('Timestamp')
    cols.sort()
    cols.insert(0, 'Timestamp')
    return df[cols]
