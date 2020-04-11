#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Piemonte data downloader and parser
"""

import pandas as pd
import csv
import operator
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
        dts = data.Datetime.unique()
        new_data = pd.DataFrame()

        for dt in dts:
            entries = data.loc[data.Datetime == dt]
            current_sensors = entries.Sensore.unique()
            new = {get_pollutant_enum_name(sensor): get_value(entries, sensor) for sensor in current_sensors}
            new_record = pd.DataFrame.from_records(new, index=[pd.to_datetime(str(dt)).strftime("%Y%m%dT%H%M%S")])
            new_data = new_data.append(new_record)

        AQS = AirQualityStation(data.station.unique().item())
        AQS.set_address(region=Italy.Region.PIEMONTE)
        AQS.update_data(new_data)
        AQS_list.append(AQS)
        ipdb.set_trace()


def get_value(entries, sensor):
    try:
        return float(entries.loc[entries['Sensore'] == sensor]['Valore validato'])
    except TypeError:
        ipdb.set_trace()


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
