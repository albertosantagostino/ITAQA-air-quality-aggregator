#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

import uuid
import json
import pandas as pd
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
        AirQualityStation("Torino Rebaudengo")

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


def encode_msgpack(obj):
    """Encoder for serialization, from AQS to msgpack"""
    if isinstance(obj, AirQualityStation):
        return {
            '__AirQualityStation__': True,
            'm_name': obj.name,
            'm_region': obj.region.value,
            'm_province': obj.province.value,
            'm_comune': obj.comune,
            'm_geolocation': obj.geolocation,
            'm_metadata': json.dumps(obj.metadata),
            'm_data': obj.data.to_json()
        }
    else:
        return None


def decode_msgpack(obj):
    """Decoder for serialization, from msgpack to AQS"""
    decoded_obj = None
    if '__AirQualityStation__' in obj:
        decoded_obj = AirQualityStation(obj['m_name'])
        decoded_obj.region = Italy.Region(obj['m_region'])
        decoded_obj.province = Italy.Province(obj['m_province'])
        decoded_obj.comune = obj['m_comune']
        decoded_obj.geolocation = obj['m_geolocation']
        decoded_obj.metadata = json.loads(obj['m_metadata'])
        decoded_obj.data = pd.DataFrame(json.loads(obj['m_data']))
    return decoded_obj
