#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to handle serialization
"""

import msgpack

from itaqa.core.AirQualityStation import AirQualityStation


def dump_AQS_to_msgpack(AQS, file_path):
    """Serialize and dump one or multiple AQS to a file"""
    with open(file_path, 'wb') as fp:
        packed = msgpack.packb(AQS, default=AirQualityStation.encode_AQS_msgpack)
        fp.write(packed)


def load_AQS_from_msgpack(file_path):
    """Load AQS from a file"""
    with open(file_path, 'rb') as fp:
        bytedata = fp.read()
    return msgpack.unpackb(bytedata, object_hook=AirQualityStation.decode_AQS_msgpack)
