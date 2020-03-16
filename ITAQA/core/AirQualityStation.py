#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class AirQualityStation
"""

from ITAQA.geography import Italy


class AirQualityStation():
    """
    Represent an air quality measurament from a specific station in Italy

    Args:
        station_name: Name of the station
        region:       Italy's region
        province:     Italy's province

    Examples:
        AirQualityStation("Torino Rebaudengo", "Italy.Region.PIEMONTE", "Italy.Province.TORINO")

    Raises:
        ValueError: If station_name is empty
    """
    def __init__(self, station_name, region=None, province=None):
        # Validate service name
        if not station_name:
            raise ValueError("Station name cannot be empty")
        else:
            self.station_name = station_name
        if not region:
            self.region = Italy.Region.UNSET
        else:
            self.region = region
        if not province:
            self.province = Italy.Province.UNSET
        else:
            self.province = province

        self.geolocation = None

        self.metadata = None
        self.data = {}

    def __repr__(self):
        return f"AirQualityStation('{self.station_name}','{self.region}','{self.province}')"
