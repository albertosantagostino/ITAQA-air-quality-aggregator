#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entrypoint to download data, create AQS collection, generate plots
"""

from datetime import datetime, timedelta

from itaqa.core import AirQualityStation
from itaqa.crawler import lombardia
from itaqa.utils.serialization_utils import dump_AQS_to_msgpack, load_AQS_from_msgpack

import csv
import ipdb


def main():
    """ITAQA entrypoint script"""
    # Select relevant time range
    min_date = datetime(year=2020, month=1, day=1)
    max_date = datetime.now()

    # Obtain AQS
    AQS_lombardia = lombardia.get_AQS_list(dt_range=[min_date, max_date], redownload=False)
    ipdb.set_trace()


if __name__ == "__main__":
    main()
