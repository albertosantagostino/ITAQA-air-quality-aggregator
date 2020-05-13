#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entrypoint to download/handle data and generate plots

WIP: Evaluate future switch to a simple GUI
"""

from datetime import datetime

from itaqa.core import AirQualityStation
from itaqa.crawler import lombardia

import csv
import ipdb


def main():

    minimum_date = datetime(year=2020, month=4, day=30)
    now = datetime.now()

    AQS_lombardia = lombardia.get_AQS_list(dt_range=[minimum_date, now], redownload=False)
    ipdb.set_trace()


if __name__ == "__main__":
    main()
