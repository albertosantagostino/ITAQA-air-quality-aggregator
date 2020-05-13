#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

import pandas as pd
import uuid
from datetime import datetime
import pandas as pd

from ITAQA.geography import Italy, converter


class AirQualityStation():
    """
    Represent an air quality measurament from a specific sensor/station

    Args:
        station_name (str): Name of the station

    Attributes:
        station_name (str): Name of the station
        region (Italy.Region): Region in which the station is located
        province (Italy.Province): Province in which the station is located
        comune (str): Comune in which the station is located
        geolocation (tuple): Geographic coordinates in the format (lat, lng, alt)
        metadata(dict): Information on the object
        data(pandas.DataFrame): Air pollution data of the station

    Examples:
        AirQualityStation("Torino Rebaudengo")

    Raises:
        ValueError: If station_name is empty
    """
    def __init__(self, station_name):
        # Validate service name
        if not station_name:
            raise ValueError("Station name cannot be empty")
        else:
            self.station_name = station_name

        # Geographic information on the location of the station
        self.region = Italy.Region.UNSET
        self.province = Italy.Province.UNSET
        self.comune = None
        self.geolocation = None

        # Metadata
        # TODO: Make creation time UTC
        self.metadata = {'creation': datetime.now().strftime("%Y%m%dT%H%M%S"), 'uuid': uuid.uuid4()}

        # Data
        self.data = pd.DataFrame()

    def __repr__(self):
        return f"AirQualityStation('{self.station_name}','{self.region}','{self.province},'{self.comune}')"

    def __str__(self):
        print_str = f"AirQualityStation\n\nName:\t\t{self.station_name:20}\n"
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
        self.geolocation = (lat, lng, alt)

    def update_data(self, data_pd):
        """Set pollution DataFrame"""
        # TODO: Don't write again data already present (if provided with new days, update the dataframe)
        # TODO: Days on rows and pollutants on columns
        # TODO: Validate data before assignment, check if in the expected format
        # TODO: Update metadata information (data stored, max date, min date, measured pollutants)
        self.data = data_pd