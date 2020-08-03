#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

import json
import pandas as pd
import uuid

from copy import deepcopy
from datetime import datetime

from itaqa.geography import Italy
from itaqa.visualization import plotting


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
        AirQualityStation('Mount Doom')
    """
    def __init__(self, name):
        self.name = name
        self.region = Italy.Region.UNSET
        self.province = Italy.Province.UNSET
        self.comune = None
        self.geolocation = None
        self.metadata = {'uuid': str(uuid.uuid4())}
        self._data = pd.DataFrame()

    def __repr__(self):
        return f"AirQualityStation('{self.name}')"

    def __str__(self):
        ret = f"{90*'-'}\n"
        ret += f"AirQualityStation\n\nName:\t\t{self.name:20}\n"
        ret += f"Location:\t{self.comune}, {self.province}, {self.region}\n"
        ret += f"Geolocation:\t{self.geolocation}\n"
        ret += f"Data shape:\t{self.data.shape}\n"
        ret += f"Pollutants:\t{', '.join(map(str, [pl for pl in self.data.columns.to_list() if pl != 'Timestamp']))}\n"
        ret += f"{90*'-'}"
        return ret

    def __lt__(self, other):
        return self.name < other.name

    @property
    def data(self):
        """Data property"""
        return self._data

    @data.setter
    def data(self, value):
        """Data setter"""
        # TODO: Check if provided data is a valid pandas df with a Timestamp column
        self._data = value

    @property
    def uuid(self):
        return self.metadata['uuid']

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
        # TODO: Make this a named tuple
        self.geolocation = [lat, lng, alt]

    def plot(self, mode='multiple', pollutant=None):
        """Call visualization functions and create plotly graphs"""
        if mode == 'single':
            plotting.AQS_plot(self, pollutant)
        if mode == 'multiple':
            plotting.AQS_multiplot(self)

    @staticmethod
    def encode_AQS_msgpack(AQS):
        """Encoder from AQS to msgpack"""
        if isinstance(AQS, AirQualityStation):
            # Convert pd.Timestamp to Unix time (ensure original object is not affected)
            data_copy = deepcopy(AQS.data)
            data_copy['Timestamp'] = data_copy['Timestamp'].map(lambda dt: int((pd.Timestamp(dt)).value / (10**9)))
            return {
                '__AirQualityStation__': True,
                'm_name': AQS.name,
                'm_region': AQS.region.value,
                'm_province': AQS.province.value,
                'm_comune': AQS.comune,
                'm_geolocation': AQS.geolocation,
                'm_metadata': json.dumps(AQS.metadata),
                'm_data': json.dumps(data_copy.to_dict())
            }
        else:
            return None

    @staticmethod
    def decode_AQS_msgpack(obj):
        """Decoder from msgpack to AQS"""
        AQS = None
        if '__AirQualityStation__' in obj:
            AQS = AirQualityStation(obj['m_name'])
            AQS.region = Italy.Region(obj['m_region'])
            AQS.province = Italy.Province(obj['m_province'])
            AQS.comune = obj['m_comune']
            AQS.geolocation = obj['m_geolocation']
            AQS.metadata = json.loads(obj['m_metadata'])
            # Not proud of this, I will think about it later
            df = pd.DataFrame.from_dict(json.loads(obj['m_data']))
            # Convert Unix time to pd.Timestamp
            df['Timestamp'] = df['Timestamp'].map(lambda unix_time: pd.Timestamp(unix_time * (10**9)))
            AQS.data = df
        return AQS
