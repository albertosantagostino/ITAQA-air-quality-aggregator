#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test utilities
"""


def check_AQS_equality(AQS1, AQS2):
    """Check AQS equality"""
    assert AQS1.name == AQS2.name
    assert AQS1.region.value == AQS2.region.value
    assert AQS1.province.value == AQS2.province.value
    assert AQS1.comune == AQS2.comune
    assert AQS1.geolocation == AQS2.geolocation
    assert AQS1.metadata == AQS2.metadata
    assert (AQS1.data.values == AQS2.data.values).all()
