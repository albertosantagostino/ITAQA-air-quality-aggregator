#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lombardia data downloader and parser
"""

import csv
import requests
import warnings

import pandas as pd

import ipdb
import json
import os
import progressbar

from datetime import datetime

from ITAQA.core.defs import Pollutant
from ITAQA.core.AirQualityStation import AirQualityStation
from ITAQA.geography import Italy
from ITAQA.utils import network_utils


def get_AQS_list(minimum_relevant_date):
    """
    Return the list of the air quality stations from Lombardia

    Data origin: ARPA Lombardia
    Website: https://www.dati.lombardia.it
    """
    # TODO: The whole function must be heavily optimized

    # Download data from ARPA Lombardia
    metadata_url = 'https://www.dati.lombardia.it/resource/ib47-atvt.csv'
    data_url = 'https://www.dati.lombardia.it/api/views/nicp-bhqi/rows.csv'

    metadata_reader, metadata_len = network_utils.obtain_csv_data(metadata_url)
    data_reader, data_len = network_utils.obtain_csv_data(data_url)
    # TODO: Check that csv columns are the expected ones (consolidate csv)

    # Prepare header
    header_row = next(metadata_reader, None)
    # Fix rows with wrong title
    header_row[16] = 'Limiti amministrativi 2014'
    header_row[17] = 'Limiti amministrativi 2015'

    # TODO: Merge the next part, skip not needed data
    # Create a metadata DataFrame
    metadata_dict = {}
    for row in metadata_reader:
        tuplelist = []
        for i in range(1, len(row)):
            if (header_row[i] == 'location'):
                row[i] = row[i].replace(',  ', '')
            if (header_row[i] == 'unitamisura'):
                row[i] = row[i].replace('Â', '')
            tuplelist.append((header_row[i], row[i]))
        sensor_id = int(row[0])
        metadata_dict[sensor_id] = {key: value for (key, value) in tuplelist}
    metadata_pd = pd.DataFrame(metadata_dict)

    # For every station/sensor in the metadata, create an AirQualityStation object
    stations_dict = {}
    for key in metadata_pd:
        station = metadata_pd[key]
        AQS = AirQualityStation(station['nomestazione'])
        AQS.set_address(region=Italy.Region.LOMBARDIA,
                        province=Italy.Province[station['provincia']],
                        comune=station['comune'])
        AQS.set_geolocation(lat=station['lat'], lng=station['lng'], alt=station['quota'])
        stations_dict[str(key)] = AQS

    # Prepare header
    header_row = next(data_reader, None)

    count = 0
    data_amount = data_len
    with progressbar.ProgressBar(max_value=data_amount) as bar:
        for row in data_reader:
            # If the measurament is not invalid, consider it
            if (row[2] != '-9999'):
                sensor_id = row[0]
                # If the sensor_id of the measurament is known
                if sensor_id in stations_dict:
                    AQS = stations_dict[row[0]]
                    # Convert datetime in correct format
                    value, date = row[2], row[1]
                    datetime_object = datetime.strptime(date, '%d/%m/%Y %I:%M:%S %p')
                    # Include only data with specified date
                    if datetime_object > minimum_relevant_date:
                        date = datetime_object.strftime('%Y%m%dT%H%M%S')
                        pollutant = get_pollutant_enum(station['nometiposensore'])
                        # If first time, init data (TODO: Refactor)
                        if AQS.data.empty:
                            data_pd = pd.DataFrame(index=[pollutant.name])
                            AQS.update_data(data_pd)
                        AQS.data.at[pollutant.name, date] = value
                    count += 1
                else:
                    warnings.warn(f"{sensor_id} is not present in metadata dict. Please check", RuntimeWarning)
            bar.update(count)
    # TODO: Unify stations and update stations metadata
    return stations_dict


def get_pollutant_enum(custom_pollutant_name):
    if custom_pollutant_name == 'Ossidi di Azoto':
        return Pollutant.NOX
    elif custom_pollutant_name == 'Ozono':
        return Pollutant.O3
    elif custom_pollutant_name == 'Biossido di Azoto':
        return Pollutant.NO2
    elif custom_pollutant_name == 'Biossido di Zolfo':
        return Pollutant.SO2
    elif custom_pollutant_name == 'Monossido di Carbonio':
        return Pollutant.CO
    elif custom_pollutant_name == 'Particelle sospese PM2.5':
        return Pollutant.PM2_5
    elif custom_pollutant_name == 'PM10 (SM2005)':
        return Pollutant.PM10
    else:
        warnings.warn(f"{custom_pollutant_name} is not present in Pollutant enum", RuntimeWarning)


if __name__ == "__main__":
    minimum_relevant_date = datetime(year=2020, month=3, day=19)
    stations_dict = get_AQS_list(minimum_relevant_date)
    ipdb.set_trace()
