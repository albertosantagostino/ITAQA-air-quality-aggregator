#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ITAQA

ITaly Air Quality Aggregator
Entrypoint of the project, using this script:
- Download AQS lists for multiple regions
- Update AQS lists with the most recent data
- Run unit tests
"""

import logging
import ipdb
import os
import pandas as pd
import pytest
import sys

from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
from datetime import datetime

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.crawler.defs import REGION_CRAWLERS
from itaqa.utils.AQS_utils import group_by_name, merge_by_group
from itaqa.utils.serialization_utils import dump_AQS_to_msgpack, load_AQS_from_msgpack

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
    get_AQS_list = REGION_CRAWLERS[region]
    AQS_list = get_AQS_list(dt_range=[min_date, max_date], redownload=redownload)
    dump_AQS_to_msgpack(AQS_list, f'dump/{region}/{filename}')
    logger.info(f"Download completed! Saved in 'dump/{region}/{filename}'")


def update_AQS():
    """
    Update mode

    Given an existing AQS list, update it with the latest data, or given 2 lists, merge them
    """
    # TODO
    ipdb.set_trace()


def run_tests():
    """
    Run tests

    Run all the tests existing in the folder itaqa/test
    """
    pytest.main(['-s', '-v', 'itaqa/test'])


def sandbox():
    """
    Sandbox for experiments and code testing
    """
    print("To use the sandbox, simply edit/add your code in the sandbox() section of itaqa.py")
    # AQS = load_AQS_from_msgpack('dump/test_data.msgpack')
    # AQS_by_name = group_by_name(AQS)
    # AQS_merged = merge_by_group(AQS_by_name)
    ipdb.set_trace()


if __name__ == "__main__":
    # Check if the script is invoked using arguments
    if not len(sys.argv) > 1:
        print("No argument passed, show help using -h")
        sys.exit(1)

    # Create arguments parser
    desc = f"+{30*'-'}+\n|{12*' '}ITAQA{13*' '}|\n|{30*' '}|\n| ITaly Air Quality Aggregator |\n+{30*'-'}+\n\n"
    desc += "This script is the entrypoint of the project. From here you can download data, run\n"
    desc += "unit tests or play around adding code in the sandbox section\n\n"
    epilog = "For help on a specific command, run: 'python itaqa.py {command} -h'\n\n"
    epilog += "Example usage:\n'python itaqa.py download --region lombardia --min_date 20200101 --filename test'"
    parser = ArgumentParser(description=desc, usage=SUPPRESS, formatter_class=RawTextHelpFormatter, epilog=epilog)
    parser._action_groups.pop()
    parser._action_groups[0].title = "Available modes"
    subparsers = parser.add_subparsers()

    # Mode: download
    dl_parser = subparsers.add_parser('download', help="Download new data, save the AQS list in dump/REGION/")
    dl_parser.set_defaults(mode='download')
    dl_parser._action_groups.pop()
    dl_required = dl_parser.add_argument_group("required arguments")
    dl_optional = dl_parser.add_argument_group("optional arguments")
    dl_required.add_argument('--region', required=True, help="Region of Italy")
    dl_required.add_argument('--min_date', required=True, help="Minimum download date (YYMMDD)")
    dl_optional.add_argument('--max_date', help="Maximum download date (YYMMDD, default=today)")
    dl_optional.add_argument('--filename', help="Output file name (default=autogenerated)")
    dl_optional.add_argument('--redownload', default=True, help="Force the redownload of fresh tables")

    # Mode: update
    # TODO: Given a file, calculate the most recent date and update it merging new downloaded data
    up_parser = subparsers.add_parser('update', help='Update existing AQS collection with new data')
    up_parser.set_defaults(mode='update')

    # Mode: test
    ts_parser = subparsers.add_parser('test', help='Run unit tests (pytest)')
    ts_parser.set_defaults(mode='test')

    # Mode: sandbox
    sb_parser = subparsers.add_parser('sandbox', help='Run sandbox')
    sb_parser.set_defaults(mode='sandbox')

    parameters = parser.parse_args()
    logger.info(f"python {' '.join(sys.argv)}")

    # Validate region and dates, if they are used
    dt_now = datetime.now()
    if parameters.mode == 'download':
        if parameters.region not in REGION_CRAWLERS:
            print(f"Invalid region ({parameters.region})")
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
        filename = 'AQS_list'
        if parameters.filename:
            filename = parameters.filename.replace('.msgpack', '')
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
        update_AQS()

    elif parameters.mode == 'test':
        run_tests()

    elif parameters.mode == 'sandbox':
        sandbox()

    sys.exit(0)