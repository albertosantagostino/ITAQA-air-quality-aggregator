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
        AirQualityStation('Mordor')

    Raises:
        ValueError: If name is empty
    """
    def __init__(self, name):
        if not name:
            raise ValueError("Station name cannot be empty")
        else:
            self.name = name

        self.region = Italy.Region.UNSET
        self.province = Italy.Province.UNSET
        self.comune = None
        self.geolocation = None
        self.metadata = {'uuid': str(uuid.uuid4())}
        self._data = pd.DataFrame()

    def __repr__(self):
        return f"AirQualityStation('{self.name}', {self.metadata['uuid']})"

    def __str__(self):
        data_info = self.metadata['data_info']
        print_str = f"{90*'-'}\n"
        print_str += f"AirQualityStation\n\nName:\t\t{self.name:20}\n"
        print_str += f"Location:\t{self.comune}, {self.province}, {self.region}\n"
        print_str += f"Geolocation:\t{self.geolocation}\n"
        print_str += f"Data stored:\t{data_info['shape']} (Total: {data_info['total']})\n"
        print_str += f"Pollutants:\t{', '.join(map(str, data_info['pollutants']))}\n"
        print_str += f"{90*'-'}"
        return print_str

    def __lt__(self, other):
        """Comparator operator, sort based on name (for grouping)"""
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
        self.metadata['last_edit'] = datetime.now().strftime('%Y%m%dT%H%M%S')
        self.update_metadata_datainfo()

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

    def update_metadata_datainfo(self):
        data_info = {}
        data_info['total'] = int(self.data.size)
        data_info['shape'] = self.data.shape
        if data_info['total'] > 0:
            data_info['min_date'] = self.data['Timestamp'].min().strftime('%Y-%m-%d %H:%M:%S')
            data_info['max_date'] = self.data['Timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
        cols = self.data.columns.to_list()
        cols.remove('Timestamp')
        data_info['pollutants'] = cols
        self.metadata['data_info'] = data_info

    @staticmethod
    def encode_msgpack(AQS):
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
            # Not proud of this, I will think about it later
            df = pd.DataFrame.from_dict(json.loads(obj['m_data']))
            # Convert Unix time to pd.Timestamp
            df['Timestamp'] = df['Timestamp'].map(lambda unix_time: pd.Timestamp(unix_time * (10**9)))
            AQS.data = df
        return AQS
