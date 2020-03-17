#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

from datetime import datetime

from ITAQA.geography import Italy


class AirQualityStation():
    """
    Represent an air quality measurament from a specific station in Italy

    Args:
        station_name (str): Name of the station

    Attributes:
        station_name (str): Name of the station
        region (Italy.Region): Region in which the station is located
        province (Italy.Province): Province in which the station is located
        comune (str): Comune in which the station is located
        geolocation (tuple): Geographic coordinates in the format (lat, lon, alt)
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

        # Metadata and data
        # TODO: Make the time in UTC Time and add 'Z' in the end
        self.metadata = {'created_on': datetime.now().strftime("%Y%m%d-%H%M%S")}
        self.data = {}

    def __repr__(self):
        return f"AirQualityStation('{self.station_name}','{self.region}','{self.province},'{self.comune}')"

    def __str__(self):
        # TODO: Return table or extensive information, including amount of data collected
        return f"AirQualityStation\n\nName:{self.station_name}"

    def set_address(self, region=None, province=None, comune=None):
        """Set region, province, comune of the station"""
        if not region:
            self.region = Italy.Region.UNSET
        else:
            self.region = region
        if not province:
            self.province = Italy.Province.UNSET
        else:
            self.province = province
        if not comune:
            self.comune = None

    def set_geolocation(self, lat, lon, alt=None):
        """Set geographic coordinates of the station"""
        # TODO: Validate coordinates, catch invalid values
        self.geolocation = (lat, lon, alt)

    def update_data(self, data_pd):
        """Set pollution DataFrame"""
        # TODO: Avoid writing again data already present (if provided with new days update the dataframe)
        # TODO: On rows the day and on columns the pollutants
        # TODO: Validate data before assignment, check if in the expected format
        # TODO: Update metadata information (how many data, max date, min date, measured pollutants)
        self.data = data_pd
        