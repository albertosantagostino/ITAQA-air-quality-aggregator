#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lombardia data downloader and parser
"""

import collections
import csv
import logging
import pandas as pd
import progressbar

from datetime import datetime
from pathlib import Path

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.core.defs import Pollutant
from itaqa.geography import Italy
from itaqa.utils import csv_utils, AQS_utils

logger = logging.getLogger(__name__)


def get_AQS_list(dt_range, redownload):
    """
    Return the list of the air quality stations from Lombardia

    Data origin: ARPA Lombardia
    Website: https://www.dati.lombardia.it
    """
    min_dt, max_dt = dt_range

    metadata_url = 'https://www.dati.lombardia.it/resource/ib47-atvt.csv'
    if min_dt.year == max_dt.year:
        ref_year = min_dt.year
        if ref_year == 2020:
            data_url = 'https://www.dati.lombardia.it/api/views/nicp-bhqi/rows.csv'
        elif ref_year == 2019:
            data_url = 'https://www.dati.lombardia.it/api/views/kujm-kavy/rows.csv'
        elif ref_year == 2018:
            data_url = 'https://www.dati.lombardia.it/api/views/bgqm-yq56/rows.csv'
        else:
            raise ValueError("Data table unknown for the specified year")
    else:
        raise ValueError("Cannot use different years as min and max date for now")

    metadata_file = f'dump/data/lombardia_metadata_{ref_year}.out'
    data_file = f'dump/data/lombardia_data_{ref_year}.out'

    # Download data from ARPA Lombardia
    # TODO: Check if redownload is false but no data is present locally
    if redownload:
        logger.info("Started download from ARPA Lombardia")
        csv_utils.download_csv(metadata_url, metadata_file)
        csv_utils.download_csv(data_url, data_file)
    else:
        if Path(metadata_file).exists() and Path(data_file).exists():
            logger.info("Using stored csv for data")
        else:
            raise FileNotFoundError("Data not existing, run agagin with redownload=True")

    metadata_reader, metadata_len = csv_utils.read_csv(metadata_file)
    data_reader, data_len = csv_utils.read_csv(data_file)
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
                    logger.warning("Dataframe should be empty at this step")
                stations_dict[str(key)] = AQS
            else:
                ignored_pollutants.add(station['nometiposensore'])

    # Fill AQS objects with data, reading the data CSV row by row
    header_row = next(data_reader, None)
    data_dict = collections.defaultdict(dict)
    missing_sensors = set()
    # TODO: Make the progress bar representative
    print("(The status bar is not representative right now (will be fixed), it should take less than indicated")
    with progressbar.ProgressBar(max_value=data_len) as bar:
        for row in data_reader:
            datetime_object = datetime.strptime(row[1], '%d/%m/%Y %I:%M:%S %p')
            # Include only data in specified datetime range
            if (datetime_object >= min_dt) and (datetime_object <= max_dt):
                if (row[2] != '-9999'):
                    sensor_id = row[0]
                    if sensor_id in stations_dict:
                        dt = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                        data_dict[sensor_id][dt] = row[2]
                    else:
                        missing_sensors.add(sensor_id)
            bar.update(data_reader.line_num)

    # Create df for all AQS (performance friendly approach: assigned to AQS.data only here)
    for k, v in data_dict.items():
        AQS = stations_dict[k]
        data_df = pd.DataFrame(list(v.items()), columns=AQS.data.columns)
        AQS.data = AQS.data.append(data_df, ignore_index=True)

    # Notify the user on parsing outcome (ignored items)
    if missing_sensors:
        missing_sensors_list = list(missing_sensors)
        missing_sensors_list.sort()
        logger.warn("Some sensors were not present in metadata dict")
        print([sensor_id for sensor_id in missing_sensors_list])
    if ignored_pollutants:
        ignored_pollutants_list = list(ignored_pollutants)
        ignored_pollutants_list.sort()
        logger.info("Some pollutants were ignored")
        print([pt for pt in ignored_pollutants_list])

    # Convert dict to list
    stations_list = [v for v in stations_dict.values()]
    # Remove stations without data
    remove_empty_stations(stations_list)
    # Sort by timestamp and reset index of each DataFrame
    for station in stations_list:
        station.data.sort_values(by='Timestamp', inplace=True)
        station.data.reset_index(drop=True, inplace=True)
    # Sort by name
    stations_list.sort()
    # Merge stations with the same name (indicating the same place)
    stations_grouped = AQS_utils.group_by_name(stations_list)
    stations_merged = AQS_utils.merge_by_group(stations_grouped)

    return stations_merged


def remove_empty_stations(stations_list, min_entries=1):
    new_stations_list = []
    for station in stations_list:
        if station.data.size >= min_entries:
            new_stations_list.append(station)
    return new_stations_list


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
