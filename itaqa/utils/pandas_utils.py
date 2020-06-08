#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle pandas DataFrame objects
"""

import pandas as pd


def print_entire(df):
    """Print the entire DataFrame, displaying all rows and columns"""
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
