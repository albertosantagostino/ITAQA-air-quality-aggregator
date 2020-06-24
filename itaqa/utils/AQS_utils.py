#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle and manipulate multiple AQS objects
"""

import pandas as pd

from itertools import groupby
from collections import defaultdict

from itaqa.core import AirQualityStation


def group_by_name(AQS_list):
    """Return a dict with as key the name of the station and as value a list of AQS objects"""
    AQS_by_name = defaultdict(list)
    for k, g in groupby(AQS_list, lambda x: x.name):
        for station in g:
            AQS_by_name[k].append(station)

    return AQS_by_name


def merge_by_group(AQS_group):
    """Merge multiple groups of AQS and return a list of merged AQS objects"""
    merged_AQS_list = []
    for k in AQS_group:
        # Setup new resulting AQS
        new_AQS = AirQualityStation.AirQualityStation(k)
        new_AQS.set_address(region=AQS_group[k][0].region,
                            province=AQS_group[k][0].province,
                            comune=AQS_group[k][0].comune)
        # TODO: Compute geolocation
        new_AQS.metadata['premerge_history'] = {}
        frames = []

        for station in AQS_group[k]:
            frames.append(station.data.set_index('Timestamp'))
            # TODO: Refactor to handle stations with more than one pollutant before merge
            cols = station.data.columns.to_list()
            cols.remove('Timestamp')
            pollutant = cols[0]
            new_AQS.metadata['premerge_history'][pollutant] = {}
            new_AQS.metadata['premerge_history'][pollutant]['name'] = station.name
            new_AQS.metadata['premerge_history'][pollutant]['uuid'] = station.metadata['uuid']
            new_AQS.metadata['premerge_history'][pollutant]['creation'] = station.metadata['creation']
            # TODO: Move geolocation in more accessible place?
            new_AQS.metadata['premerge_history'][pollutant]['geolocation'] = station.geolocation
        # Take first frame and merge all the others
        merged_df = frames.pop()
        for frame in frames:
            merged_df = merged_df.merge(frame, how='outer', left_index=True, right_index=True)
        merged_df.reset_index(inplace=True)
        new_AQS.data = merged_df
        merged_AQS_list.append(new_AQS)

    return merged_AQS_list
