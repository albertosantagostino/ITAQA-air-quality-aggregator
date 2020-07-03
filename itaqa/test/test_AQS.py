#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for AirQualityStation objects
"""

import pandas as pd
import pytest

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.utils.AQS_utils import check_AQS_equality
from itaqa.utils.serialization_utils import load_AQS_from_msgpack, dump_AQS_to_msgpack
from datetime import datetime, timedelta


@pytest.fixture
def dummy_AQS():
    AQS = AirQualityStation('Mount Doom')
    AQS.set_address(comune='Mordor')
    AQS.set_geolocation(lat=-39.15683, lng=175.6315464, alt=291)
    dts = [datetime(year=1970, month=1, day=1, hour=6) + timedelta(hours=i) for i in range(1, 30, 2)]
    AQS.data = pd.DataFrame(columns=['Timestamp', 'SO2'])
    for dt in dts:
        new_data = pd.DataFrame([[dt, 0.1]], columns=AQS.data.columns)
        AQS.data = AQS.data.append(new_data, ignore_index=True)
    return AQS


def test_serialization(dummy_AQS):
    """
    Check if serialiaztion is currently working properly
    [Fail] If msgpack encoding/decoding is broken
    """
    # Encode AQS to msgpack
    encoded_AQS = AirQualityStation.encode_msgpack(dummy_AQS)
    # Decode msgpack to AQS
    decoded_AQS = AirQualityStation.decode_msgpack(encoded_AQS)
    # Check equality
    assert check_AQS_equality([dummy_AQS, decoded_AQS], compare_metadata=False, compare_data=True)


def test_serialization_regression_load():
    """
    Check if old serialized stations are still loadable
    [Fail] If msgpack serialization format changed
    """
    try:
        load_AQS_from_msgpack('itaqa/test/test_data/AQS_MountDoom.msgpack')
    except Exception:
        pytest.fail("myFunc() raised ExceptionType unexpectedly!")
