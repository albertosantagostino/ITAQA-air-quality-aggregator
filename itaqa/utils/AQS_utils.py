#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities to handle and manipulate multiple AQS objects
"""

from itaqa.core import AirQualityStation

import pandas as pd
from itertools import groupby
from collections import defaultdict


def group_by_name(AQS_list):
    """Return a dict with as key the name of the station and as value a list of AQS objects"""
    AQS_by_name = defaultdict(list)
    for k, g in groupby(AQS_list, lambda x: x.name):
        for station in g:
            AQS_by_name[k].append(station)

    return AQS_by_name


def merge_group(AQS_group):
    """Merge multiple groups of AQS and return a list of merged AQS objects"""
    merged_AQS_list = []
    for k in AQS_group:
        new_AQS = AirQualityStation.AirQualityStation(k)
        new_AQS.set_address(region=AQS_group[k][0].region,
                            province=AQS_group[k][0].province,
                            comune=AQS_group[k][0].comune)
        frames = []
        for station in AQS_group[k]:
            frames.append(station.data.set_index('Timestamp'))
        merged_df = frames.pop()
        for frame in frames:
            merged_df = merged_df.merge(frame, how='outer', left_index=True, right_index=True)
        merged_df.reset_index(inplace=True)
        new_AQS.data = merged_df

        # TODO: Merge metadata and geolocation

        merged_AQS_list.append(new_AQS)

    return merged_AQS_list
