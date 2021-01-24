#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle and manipulate AirQualityStationCollection objects
"""

import json
import logging
import warnings

from collections import defaultdict
from itertools import groupby

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.core.AirQualityStationCollection import AirQualityStationCollection
from itaqa.utils.AQS_utils import merge_AQS_data

logger = logging.getLogger(__name__)


def group_by_name(AQSC):
    """Return a dict with as key the name of the station and as value a list of AQS objects"""
    AQS_by_name = defaultdict(list)
    for k, g in groupby(AQSC.AQS_list, lambda x: x.name):
        for station in g:
            AQS_by_name[k].append(station)
    return AQS_by_name


def merge_by_group(AQSC, AQS_group):
    """Merge multiple groups of AQS and return a list of merged AQS objects"""
    for k in AQS_group:
        # Setup new resulting AQS
        new_AQS = AirQualityStation(k)
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
            new_AQS.metadata['premerge_history'][pollutant]['geolocation'] = station.geolocation

        # Take first frame and merge all the others
        merged_df = frames.pop()
        for frame in frames:
            merged_df = merged_df.merge(frame, how='outer', left_index=True, right_index=True)
        merged_df.reset_index(inplace=True)
        new_AQS.data = merged_df

        # Remove from AQSC the merged stations and add the new one
        AQSC.remove([AQS.uuid for AQS in AQS_group[k]])
        AQSC.add(new_AQS)


def remove_empty_stations(AQSC):
    """Remove AQS without any data inside"""
    empty_stations = [AQS.uuid for AQS in AQSC.AQS_list if AQS.data.size < 1]
    if empty_stations:
        AQSC.remove(empty_stations)


def merge_AQSC(AQSC1, AQSC2):
    """
    Merge the data of two AQSCs and return a new AQSC

    Given two AQSCs, check the amount of AQSs and merge them
    This function is to be used to merge AQSs containing data relative to different timestamps
    For example to merge two collections relative to different years
    """
    if len(AQSC1.AQS_list) != len(AQSC2.AQS_list):
        warning.warn("The AQSCs contain a different number of AQSs")

    new_AQSC = AirQualityStationCollection()

    AQSC1_names = [AQS.name for AQS in AQSC1.AQS_list]
    AQSC2_names = [AQS.name for AQS in AQSC2.AQS_list]

    AQS_names = list(set(AQSC1_names) & set(AQSC2_names))
    AQS_names.sort()

    for AQS_name in AQS_names:
        AQS1 = AQSC1.search(AQS_name)
        AQS2 = AQSC2.search(AQS_name)
        merged_AQS = merge_AQS_data([AQS1, AQS2])
        new_AQSC.add(merged_AQS)

    return new_AQSC


def merge_AQSC_multiple(AQSC_list):
    """
    Merge the data of multiple AQSCs and return a new AQSC

    Given a list of AQSC, check the amount of AQS contained in each and merge them
    This function is to be used to merge AQSs containing data relative to different timestamps
    For example to merge two collections relative to different years
    """
    new_AQSC = AirQualityStationCollection()

    all_names = list()
    for AQSC in AQSC_list:
        all_names.append([AQS.name for AQS in AQSC.AQS_list])

    AQS_names = list(set().union(*all_names))
    AQS_names.sort()

    for AQS_name in AQS_names:
        AQSs_to_merge = list()
        for AQSC in AQSC_list:
            AQS = AQSC.search(AQS_name)
            AQSs_to_merge.append(AQS)
        merged_AQS = merge_AQS_data(AQSs_to_merge)
        new_AQSC.add(merged_AQS)

    return new_AQSC
