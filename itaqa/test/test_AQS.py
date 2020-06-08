#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for AirQualityStation objects
"""

from itaqa.core import AirQualityStation

from datetime import datetime, timedelta
import pandas as pd

import pytest


@pytest.fixture
def dummy_AQS():
    AQS = AirQualityStation.AirQualityStation('Mount Doom')
    AQS.set_address(comune='Mordor')
    AQS.set_geolocation(lat=-39.15683, lng=175.6315464, alt=291)
    dts = [datetime(year=1970, month=1, day=1, hour=6) + timedelta(hours=i) for i in range(1, 30, 2)]
    AQS.data = pd.DataFrame(columns=['Timestamp', 'SO2'])
    for dt in dts:
        new_data = pd.DataFrame([[dt, 0.1]], columns=AQS.data.columns)
        AQS.data = AQS.data.append(new_data, ignore_index=True)
    return AQS


def test_serialization(dummy_AQS):
    # Encode AQS to msgpack
    encoded_AQS = AirQualityStation.encode_msgpack(dummy_AQS)
    # Decode msgpack to AQS
    decoded_AQS = AirQualityStation.decode_msgpack(encoded_AQS)
    # Check equality
    check_AQS_equality(dummy_AQS, decoded_AQS)


def check_AQS_equality(AQS1, AQS2):
    assert AQS1.name == AQS2.name
    assert AQS1.region.value == AQS2.region.value
    assert AQS1.province.value == AQS2.province.value
    assert AQS1.comune == AQS2.comune
    assert AQS1.geolocation == AQS2.geolocation
    assert AQS1.metadata == AQS2.metadata
    assert (AQS1.data.values == AQS2.data.values).all()
