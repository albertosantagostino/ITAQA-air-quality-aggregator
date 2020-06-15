#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lombardia data downloader and parser
"""

import collections
import csv
import warnings
import pandas as pd
import progressbar

from datetime import datetime

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.core.defs import Pollutant
from itaqa.geography import Italy
from itaqa.utils import csv_utils, pandas_utils


def get_AQS_list(dt_range, redownload=False):
    """
    Return the list of the air quality stations from Lombardia

    Data origin: ARPA Lombardia
    Website: https://www.dati.lombardia.it
    """

    min_dt, max_dt = dt_range
    if redownload:
        # Download data from ARPA Lombardia
        metadata_url = 'https://www.dati.lombardia.it/resource/ib47-atvt.csv'
        if min_dt.year == max_dt.year:
            ref_year = min_dt.year
            if ref_year == 2020:
                data_url = 'https://www.dati.lombardia.it/api/views/nicp-bhqi/rows.csv'
            elif ref_year == 2019:
                data_url = 'https://www.dati.lombardia.it/api/views/kujm-kavy/rows.csv'
            else:
                raise ValueError('Data table unknown for the specified year')
        else:
            raise ValueError("Cannot use different years as min and max date for now")
        csv_utils.download_csv(metadata_url, f'dump/lombardia/metadata_{ref_year}.out')
        csv_utils.download_csv(data_url, f'dump/lombardia/data_{ref_year}.out')

    # TODO: Check that csv columns are the expected ones (consolidate csv)
    metadata_reader, metadata_len = csv_utils.read_csv(f'dump/lombardia/metadata_{ref_year}.out')
    data_reader, data_len = csv_utils.read_csv(f'dump/lombardia/data_{ref_year}.out')

    # Create metadata
    header_row = next(metadata_reader, None)
    # Fix rows with wrong title
    header_row[16] = 'Limiti amministrativi 2014'
    header_row[17] = 'Limiti amministrativi 2015'
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

    # Create an AirQualityStation for each station in metadata
    stations_dict = {}
    ignored_pollutants = set()
    for key in metadata_pd:
        station = metadata_pd[key]
        # Check if the station is still active. If not, ignore it (TODO: Refactor/remove)
        if not station.datastop:
            station_name = station['nomestazione']
            AQS = AirQualityStation(station_name)
            AQS.set_address(region=Italy.Region.LOMBARDIA,
                            province=Italy.Province[station['provincia']],
                            comune=station['comune'])
            AQS.set_geolocation(lat=station['lat'], lng=station['lng'], alt=station['quota'])
            pollutant = get_pollutant_enum(station['nometiposensore'])
            # If the station is measuring a pollutant of interest
            if pollutant:
                if AQS.data.empty:
                    data_pd = pd.DataFrame(columns=['Timestamp', pollutant.name])
                    AQS.data = data_pd
                else:
                    warnings.warn("Dataframe should be empty at this step", RuntimeWarning)
                stations_dict[str(key)] = AQS
            else:
                ignored_pollutants.add(station['nometiposensore'])

    print("The following pollutants were ignored:")
    for pt in ignored_pollutants:
        print(f"- {pt}")

    # Fill AQS objects with data, reading the data CSV row by row
    header_row = next(data_reader, None)
    with progressbar.ProgressBar(max_value=data_len) as bar:
        for row in data_reader:
            datetime_object = datetime.strptime(row[1], '%d/%m/%Y %I:%M:%S %p')
            # Include only data in specified datetime range
            if (datetime_object >= min_dt) and (datetime_object <= max_dt):
                if (row[2] != '-9999'):
                    sensor_id = row[0]
                    if sensor_id in stations_dict:
                        AQS = stations_dict[sensor_id]
                        dt = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                        new_data_df = pd.DataFrame([[dt, row[2]]], columns=AQS.data.columns)
                        AQS.data = AQS.data.append(new_data_df, ignore_index=True)
                    else:
                        warnings.warn(f"Sensor {sensor_id} is not present in metadata dict", RuntimeWarning)
            bar.update(data_reader.line_num)

    # Manipulate filled stations
    remove_empty_stations(stations_dict)
    # correlation_map = aggregate_stations(stations_dict)
    # unify_stations(stations_dict, correlation_map)

    # Convert dict to list
    stations_list = [v for v in stations_dict.values()]

    # Sort by timestamp and reset index of each DataFrame
    for station in stations_list:
        station.data.sort_values(by='Timestamp', inplace=True)
        station.data.reset_index(drop=True, inplace=True)
    # Sort by name
    stations_list.sort()

    return stations_list


def remove_empty_stations(stations_dict, min_entries=1):
    """
    Remove all stations that store less than the specified amount of data
    """
    targets = []
    for key in stations_dict:
        station = stations_dict[key]
        if station.data.size <= min_entries:
            targets.append(key)
    # Delete empty entries
    for key in targets:
        del stations_dict[key]


def aggregate_stations(stations_dict):
    """
    Returns a map of all stations id that probably refer to the same place
    """
    # TODO: Return correlation_map based on metadata['uuid'], not on metadata id
    # TODO: Deprecated due to new function that uses name for aggregation
    # Create a map id:name
    station_names_dict = {station_id: station.name for station_id, station in stations_dict.items()}

    correlation_map = collections.defaultdict(list)
    for k, v in station_names_dict.items():
        correlation_map[v].append(str(k))

    return correlation_map


def unify_stations(stations_dict, correlation_map):
    """
    TODO: Is this needed?
    Unify stations that are geographically nearby
    """
    for key in correlation_map:
        AQSs = []
        stations = correlation_map[key]
        for station_id in stations:
            AQSs.append(stations_dict[str(station_id)])
        # TODO: Check distance and if needed unify


def get_pollutant_enum(pollutant_name):
    """
    Return the enum representing the pollutant
    """
    if (pollutant_name == 'Ossidi di Azoto') or (pollutant_name == 'Monossido di Azoto'):
        return Pollutant.NOX
    elif pollutant_name == 'Ozono':
        return Pollutant.O3
    elif pollutant_name == 'Biossido di Azoto':
        return Pollutant.NO2
    elif pollutant_name == 'Biossido di Zolfo':
        return Pollutant.SO2
    elif pollutant_name == 'Monossido di Carbonio':
        return Pollutant.CO
    elif pollutant_name == 'Particelle sospese PM2.5':
        return Pollutant.PM2_5
    elif pollutant_name == 'PM10 (SM2005)':
        return Pollutant.PM10
    else:
        return None
