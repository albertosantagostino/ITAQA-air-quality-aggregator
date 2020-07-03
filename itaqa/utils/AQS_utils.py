#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle and manipulate multiple AQS objects
"""

import logging
import pandas as pd

from itertools import groupby, combinations
from collections import defaultdict

from itaqa.core import AirQualityStation
from itaqa.utils.pandas_utils import merge_dfs

logger = logging.getLogger(__name__)


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
        # TODO: Compute geolocation and check if they are not so nearby
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


def merge_AQS_data(AQS_list):
    """Merge the data and return a new AQS. Used to add most recent data (with the same columns)"""
    equality = check_AQS_equality(AQS_list, compare_data=False, compare_metadata=False)
    if not equality:
        logging.warn("Some AQS in the list are not representing the same sensor/station, skipping data merge")
        return
    new_AQS = AirQualityStation.AirQualityStation(AQS_list[0].name)
    new_AQS.set_address(region=AQS_list[0].region, province=AQS_list[0].province, comune=AQS_list[0].comune)
    # TODO: Check if metadata is coherent among all the AQS
    new_AQS.metadata = AQS_list[0].metadata
    new_AQS.geolocation = AQS_list[0].geolocation
    # TODO: Support for more than 2 AQS
    new_AQS.data = merge_dfs([AQS_list[0].data, AQS_list[1].data])
    return new_AQS


def check_AQS_equality(AQS_list, compare_metadata=True, compare_data=True):
    """Check if the AQS in the list are all equal"""
    equality = True
    for lhs, rhs in combinations(AQS_list, 2):
        # yapf: disable
        equality = ((lhs.name == rhs.name) and \
                    (lhs.region.value == rhs.region.value) and \
                    (lhs.province.value == rhs.province.value) and \
                    (lhs.comune == rhs.comune) and \
                    (lhs.geolocation == rhs.geolocation))
        # yapf: disable
        if not equality:
            break
        if compare_data:
            if lhs.data.size == rhs.data.size:
                equality = (lhs.data.values == rhs.data.values).all()
            else:
                equality = lhs.data.values == rhs.data.values
            if not equality:
                break
        if compare_metadata:
            equality = lhs.metadata == rhs.metadata
            if not equality:
                break
        if not equality:
            break
    return equality
