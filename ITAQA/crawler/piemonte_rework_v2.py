#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Piemonte data downloader and parser
"""

import pandas as pd
import csv
import operator
import progressbar
import ipdb

from ITAQA.core.defs import Pollutant
from ITAQA.core.AirQualityStation import AirQualityStation
from ITAQA.geography import Italy

AQS_list = []


def main():
    with open('data.csv') as csvfile:
        data = pd.read_csv(csvfile,
                           sep=';',
                           parse_dates={'Datetime': ['Data', 'Ora']},
                           dayfirst=True,
                           infer_datetime_format=True)

        new_data = pd.DataFrame()
        stations = data.station.unique()
        idx = 1

        print(f"Reading {len(stations)} AQS from CSV...")
        for station in stations:
            print(f"Parsing {station}... ({idx}/{len(stations)})")
            station_data = data.loc[data['station'] == station]
            dts = station_data.Datetime.unique()
            parsed_dts = 0
            with progressbar.ProgressBar(max_value=len(dts)) as dts_bar:
                for dt in dts:
                    entries = station_data.loc[data.Datetime == dt]
                    current_sensors = entries.Sensore.unique()
                    new = {get_pollutant_enum_name(sensor): get_value(entries, sensor) for sensor in current_sensors}
                    new_record = pd.DataFrame.from_records(new,
                                                           index=[pd.to_datetime(str(dt)).strftime("%Y%m%dT%H%M%S")])
                    new_data = new_data.append(new_record)
                    parsed_dts += 1
                    dts_bar.update(parsed_dts)
            AQS = AirQualityStation(station)
            AQS.set_address(region=Italy.Region.PIEMONTE)
            AQS.update_data(new_data)
            AQS_list.append(AQS)
            idx += 1

        ipdb.set_trace()


def get_value(entries, sensor):
    try:
        return float(entries.loc[entries['Sensore'] == sensor]['Valore validato'])
    except TypeError:
        ipdb.set_trace()
        raise TypeError(f"Unexpected type while getting sensor value: {sensor}")


def get_pollutant_enum_name(sensor_type):
    if sensor_type == 'Biossido di zolfo (SO2)':
        return Pollutant.SO2.name
    elif sensor_type == 'Biossido di azoto (NO2)':
        return Pollutant.NO2.name
    elif sensor_type == 'Benzene':
        return Pollutant.BENZENE.name
    else:
        raise ValueError(f"Unknown sensor type: {sensor_type}")


if __name__ == "__main__":
    main()
