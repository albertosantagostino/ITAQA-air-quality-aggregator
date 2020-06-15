#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

import json
import pandas as pd
import uuid

from copy import deepcopy
from datetime import datetime

from itaqa.geography import Italy, converter


class AirQualityStation():
    """
    Represent an air quality measurament from a specific sensor/station

    Args:
        name (str): Name of the station

    Attributes:
        name (str): Name of the station
        region (Italy.Region): Region in which the station is located
        province (Italy.Province): Province in which the station is located
        comune (str): Comune in which the station is located
        geolocation (list): Geographic coordinates (lat, lng, alt)
        metadata(dict): Information on station, data, and uuid
        data(pandas.DataFrame): Air pollution data of the station

    Examples:
        AirQualityStation('Torino Rebaudengo')

    Raises:
        ValueError: If name is empty
    """
    def __init__(self, name):
        # Validate station name
        if not name:
            raise ValueError("Station name cannot be empty")
        else:
            self.name = name

        # Geographic information on the location of the station
        self.region = Italy.Region.UNSET
        self.province = Italy.Province.UNSET
        self.comune = None
        self.geolocation = None

        # Metadata
        # TODO: Make creation time UTC
        # TODO: Create a function to update metadata information (max date, min date, measured pollutants)
        self.metadata = {'creation': datetime.now().strftime("%Y%m%dT%H%M%S"), 'uuid': str(uuid.uuid4())}

        # Data
        self.data = pd.DataFrame()

    def __repr__(self):
        return f"AirQualityStation('{self.name}','{self.region}','{self.province},'{self.comune}')"

    def __str__(self):
        print_str = f"AirQualityStation\n\nName:\t\t{self.name:20}\n"
        print_str += f"Location:\t{self.comune}, {self.province}, {self.region}\n"
        print_str += f"Geolocation:\t{self.geolocation}\n"
        print_str += f"Data stored:\t{self.data.shape} (Total: {self.data.size})\n"
        # TODO: Print also amount of data stored and available pollutants in a compact way
        #print_str += f"Metadata:\t{self.metadata}"
        return print_str

    def __lt__(self, other):
        """Comparator operator, sort based on name (for grouping)"""
        return self.name < other.name

    def set_address(self, region=None, province=None, comune=None):
        """Set region, province, comune of the station"""
        if region and isinstance(region, Italy.Region):
            self.region = region
        if province and isinstance(province, Italy.Province):
            self.province = province
        if comune:
            self.comune = comune

    def set_geolocation(self, lat, lng, alt=None):
        """Set geographic coordinates of the station"""
        # TODO: Validate coordinates, catch invalid values
        self.geolocation = [lat, lng, alt]


def encode_msgpack(AQS):
    """Encoder from AQS to msgpack"""
    if isinstance(AQS, AirQualityStation):
        # Convert pd.Timestamp to Unix time before encoding (ensure original object is not modified)
        AQS_data_copy = deepcopy(AQS.data)
        AQS_data_copy['Timestamp'] = AQS_data_copy['Timestamp'].map(lambda dt: int(dt.value / (10**9)))
        return {
            '__AirQualityStation__': True,
            'm_name': AQS.name,
            'm_region': AQS.region.value,
            'm_province': AQS.province.value,
            'm_comune': AQS.comune,
            'm_geolocation': AQS.geolocation,
            'm_metadata': json.dumps(AQS.metadata),
            'm_data': AQS_data_copy.to_json()
        }
    else:
        return None


def decode_msgpack(obj):
    """Decoder from msgpack to AQS"""
    AQS = None
    if '__AirQualityStation__' in obj:
        AQS = AirQualityStation(obj['m_name'])
        AQS.region = Italy.Region(obj['m_region'])
        AQS.province = Italy.Province(obj['m_province'])
        AQS.comune = obj['m_comune']
        AQS.geolocation = obj['m_geolocation']
        AQS.metadata = json.loads(obj['m_metadata'])
        AQS.data = pd.DataFrame(json.loads(obj['m_data']))
        # Convert Unix time to pd.Timestamp after decoding
        AQS.data['Timestamp'] = AQS.data['Timestamp'].map(lambda unix_time: pd.Timestamp(unix_time * (10**9)))
    return AQS
