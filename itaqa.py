#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ITAQA

ITaly Air Quality Aggregator
Entrypoint of the project, using this script:
- Download AQS lists for multiple regions
- Update AQS lists with the most recent data
- Run unit tests
"""

import ipdb
import logging
import os
import pandas as pd
import pytest
import sys

from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
from datetime import datetime
from pathlib import Path

from itaqa.core.AirQualityStationCollection import AirQualityStationCollection
from itaqa.crawler.defs import REGION_CRAWLERS
from itaqa.utils.pandas_utils import print_full
from itaqa.gui.AQS_viewer import start_GUI

# Setup logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'main.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(format="[%(asctime)s] %(levelname)s: (%(name)s) %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    filename=log_file)
logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def download_AQS(region, min_date, max_date, filename, redownload):
    """
    Download mode

    Given a region and a time range, download the AQS list and store it locally
    """
    get_AQSC = REGION_CRAWLERS[region]
    AQSC = get_AQSC(dt_range=[min_date, max_date], redownload=redownload)
    AQSC.save(f'dump/{region}/{filename}')
    logger.info(f"Download completed! Saved in 'dump/{region}/{filename}'")


def update_AQS(file_path, overwrite=False):
    """
    Update mode

    Given an existing AQS list, update it with the latest data, or given 2 lists, merge them
    """
    print("TODO")
    # TODO: Given the filename determine the region
    # Load msgpack, check last entry date, download complementary AQS list and merge them
    # Save the new list (if specified, overwrite the old file)


def run_tests():
    """
    Run tests

    Run all the tests existing in the folder itaqa/test
    """
    pytest.main(['-s', '-v', 'itaqa/test'])


def sandbox(file_path=None):
    """
    Sandbox for experiments and code testing

    If a file is passed, it's loaded in "AQSC" for interactive debugging
    """
    if file_path:
        AQSC = AirQualityStationCollection(file_path=file_path)
    else:
        print("To use the sandbox, simply edit/add your code in the sandbox() section of itaqa.py")
        # << Add here code for testing >>
    AQSC.info()
    ipdb.set_trace()


if __name__ == "__main__":
    # Check if the script is invoked using arguments
    if not len(sys.argv) > 1:
        print("No argument passed, show help using -h")
        sys.exit(1)

    # Create arguments parser
    desc = f"+{30*'-'}+\n|{12*' '}ITAQA{13*' '}|\n|{30*' '}|\n| ITaly Air Quality Aggregator |\n+{30*'-'}+\n\n"
    desc += "This script is the entrypoint of ITAQA.\n"
    desc += "From here you can perform data download, update, visualization, you can\n"
    desc += "run unit tests or play around in the sandbox section\n\n"
    epilog = "For help on a specific command, run: 'python3 itaqa.py <COMMAND> -h'\n\n"
    epilog += "Sample usage:\n'python3 itaqa.py download --region lombardia --min_date 20200101 --filename test'"
    parser = ArgumentParser(description=desc, usage=SUPPRESS, formatter_class=RawTextHelpFormatter, epilog=epilog)
    parser._action_groups.pop()
    parser._action_groups[0].title = "Available modes"
    subparsers = parser.add_subparsers()

    # Mode: download
    dl_parser = subparsers.add_parser('download', help="Download new data, save the AQSC in dump/REGION/")
    dl_parser.set_defaults(mode='download')
    dl_parser._action_groups.pop()
    dl_required = dl_parser.add_argument_group("required arguments")
    dl_optional = dl_parser.add_argument_group("optional arguments")
    dl_required.add_argument('--region', required=True, help="Region of Italy")
    dl_required.add_argument('--min_date', required=True, help="Minimum download date (YYYYMMDD)")
    dl_optional.add_argument('--max_date', help="Maximum download date (YYYYMMDD, default=today)")
    dl_optional.add_argument('--filename', help="Output file name (default=autogenerated)")
    dl_optional.add_argument('--redownload', default=False, help="Force the redownload of fresh tables")

    # Mode: update
    up_parser = subparsers.add_parser('update', help='Update existing AQS collection with new data')
    up_parser.set_defaults(mode='update')
    up_required = up_parser.add_argument_group("required arguments")
    up_optional = up_parser.add_argument_group("optional arguments")
    up_required.add_argument('--file', help="Specify a file containing an AQSC to update")
    up_optional.add_argument('--overwrite', default=False, help="Overwrite the original file after the update")

    # Mode: view
    pl_parser = subparsers.add_parser('view', help='Enter interactive GUI mode to view and plot AQS data')
    pl_parser.set_defaults(mode='view')
    pl_optional = pl_parser.add_argument_group("optional arguments")
    pl_optional.add_argument('--file', help="Specify a file containing an AQSC to visualize")

    # Mode: test
    ts_parser = subparsers.add_parser('test', help='Run unit tests (pytest)')
    ts_parser.set_defaults(mode='test')

    # Mode: sandbox
    sb_parser = subparsers.add_parser('sandbox', help='Run sandbox')
    sb_parser.set_defaults(mode='sandbox')
    sb_optional = sb_parser.add_argument_group("optional arguments")
    sb_optional.add_argument('--file', help="Specify a file to load and debug interactively")

    parameters = parser.parse_args()
    logger.info(f"python3 {' '.join(sys.argv)}")

    # Validate region and dates, if they are used
    dt_now = datetime.now()
    if parameters.mode == 'download':
        if parameters.region not in REGION_CRAWLERS:
            raise ValueError(f"Invalid region or not implemented yet ({parameters.region})")
            sys.exit(1)
        try:
            min_date = datetime.strptime(parameters.min_date, '%Y%m%d')
        except ValueError:
            print(f"Invalid date ({parameters.min_date})")
            sys.exit(1)
        if parameters.max_date:
            try:
                max_date = datetime.strptime(parameters.max_date, '%Y%m%d')
            except ValueError:
                print(f"Invalid date ({parameters.min_date})")
                sys.exit(1)
        else:
            max_date = datetime(year=dt_now.year, month=dt_now.month, day=dt_now.day)
        filename = 'AQSC'
        if parameters.filename:
            filename = parameters.filename.replace('.msgpack', '')
        if not parameters.redownload:
            # TODO: Fix undesired behavior (if --redownload=False, still treated as True)
            logger.info("(No redownload flag set, will use latest downloaded data, may be outdated)")
        # yapf: disable
        filename = ''.join([
            dt_now.strftime('%Y%m%d%H%M%S_'),
            min_date.strftime('m%y%m%d_'),
            max_date.strftime('M%y%m%d_'),
            f'{parameters.region}_{filename}.msgpack'
        ])
        # yapf: enable
        download_AQS(parameters.region, min_date, max_date, filename, parameters.redownload)

    elif parameters.mode == 'update':
        if Path(parameters.file).exists():
            update_AQS(file_path=parameters.file, overwrite=parameters.overwrite)
        else:
            raise FileNotFoundError("The specified file doesn't exist")

    elif parameters.mode == 'view':
        # TODO: Support file as parameter
        start_GUI()

    elif parameters.mode == 'test':
        run_tests()

    elif parameters.mode == 'sandbox':
        if parameters.file:
            if Path(parameters.file).exists():
                sandbox(file_path=parameters.file)
            else:
                raise FileNotFoundError("The specified file doesn't exist")
        else:
            sandbox()

    sys.exit(0)
