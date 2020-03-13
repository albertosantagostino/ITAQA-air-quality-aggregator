#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entrypoint to download/handle data and generate plots

WIP: Evaluate future switch to a simple GUI
"""

from ITAQA.core import AirQualityStation
from ITAQA.crawler import piemonte

import csv
import ipdb


def main():

    # WIP
    data_piemonte = piemonte.get_PM10_csv()

    with open('piemonte.csv', 'w') as csvfile:
        csvfile.write(data_piemonte)

    ipdb.set_trace()


if __name__ == "__main__":
    main()
