#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Emilia-Romagna data downloader and parser
"""

import pandas as pd
import urllib

from datetime import datetime, timedelta
from functools import reduce

from itaqa.core.defs import Pollutant


def get_csv(pollutant=Pollutant.UNSET, days=10):
    """
    Return a csv containing the latest N days of measurament of Emilia-Romagna
    air quality (pollutant of choice)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    # TODO: Support arbitrary date ranges
    # TODO: Catch HTTPError for unavailable pages and drop them
    # TODO: Discard or warn if page contains "Dati in attesa di validazione"
    end_date = datetime.today() - timedelta(2)

    date_list = pd.date_range(end=end_date, periods=days).tolist()
    date_string_list = [x.strftime('%Y%m%d') for x in date_list]

    pd_singleday_list = []    # List of prepped tables for merging + output

    base_url = 'https://apps.arpae.it/qualita-aria/bollettino-qa/'
    for date_string in date_string_list:
        url = base_url + date_string
        html_doc = urllib.request.urlopen(url).read()

        pd_table_list = pd.read_html(html_doc)
        pd_table_list.pop(-1)    # Last table is just pollutants threshold values

        for pd_table in pd_table_list:
            # TODO: Improve - e.g. do most stuff as inplace
            # TODO: Add robust-ish checks rather than "blind" hardcoded indices?
            # Drop last columns (threshold overshooting counts)
            pd_table.drop(pd_table.columns[[10, 11, 12, 13]], axis=1, inplace=True)
            # Rename headers
            # TODO: Decide "how to yapf" these kinds of lists
            pd_table.columns = [
                'Province', 'Station', Pollutant.PM10, Pollutant.PM2_5, Pollutant.NO2, Pollutant.O3, 'O3_8h',
                Pollutant.BENZENE, Pollutant.CO, Pollutant.SO2
            ]
            # Split Station field into Station, Type
            # TODO: Differentiate between Location and Name in Station field...
            station_data = pd_table['Station'].str.split(" / ", n=1, expand=True)
            pd_table['Station'] = station_data[0]
            pd_table['Type'] = station_data[1]

        # New data frame merging all stations for the single day and pollutant
        pd_singleday = pd.concat(pd_table_list, axis=0)[['Station', pollutant]]
        pd_singleday.reset_index(drop=True)
        pd_singleday.columns = ['Station', date_string]

        pd_singleday_list.append(pd_singleday)

    pd_output = reduce(lambda x, y: pd.merge(x, y, on='Station'), pd_singleday_list)
    # TODO: Support values such as "< 3" or "n.d." and numeric vs text

    return pd_output.to_csv()


def get_PM10_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (PM10)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.PM10)


def get_PM2_5_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (PM2.5)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.PM2_5)


def get_NO2_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (NO2)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.NO2)


def get_O3_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (O3)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.O3)


def get_Benzene_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (Benzene)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.BENZENE)


def get_CO_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (CO)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.CO)


def get_SO2_csv():
    """
    Return a csv containing the latest 10 days of measurament of Emilia-Romagna
    air quality (SO2)

    Data origin: ARPA Emilia-Romagna
    Website: https://apps.arpae.it/qualita-aria/bollettino-qa
    """

    return get_csv(Pollutant.SO2)
