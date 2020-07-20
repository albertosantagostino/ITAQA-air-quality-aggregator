#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class AirQualityStationCollection
"""

import warnings

from pathlib import Path
from rich.console import Console
from rich.table import Column, Table

from itaqa.core.AirQualityStation import AirQualityStation
from itaqa.utils.serialization_utils import load_AQS_from_msgpack


class AirQualityStationCollection():
    """
    Represent a collection of AirQualityStation objects, encapsulating it as a dictonary

    Args:
        name (str): Name of the collection

    Attributes:
        name (str): Name of the collection
        AQS_collection(dict): Dict of AirQualityStation objects

    Examples:
        AirQualityStationCollection('Mordor')

    Raises:
        ValueError: If name is empty
    """
    def __init__(self, name, file=None):
        if not name:
            raise ValueError("AQS collection name cannot be empty")
        else:
            self.name = name

        self._AQS_collection = dict()

        if file and Path(file).exists():
            AQS_list = load_AQS_from_msgpack(file)
            self.add(AQS_list)

    def __str__(self):
        self.info()
        return f"(You may use directly the info() method to obtain this info table"

    def __repr__(self):
        return f"AirQualityStationCollection('{self.name}')"

    def __iter__(self):
        yield from self.AQS_collection.values()

    @property
    def AQS_collection(self):
        """Return the AQS collection itself as a dict"""
        return self._AQS_collection

    @property
    def AQS_list(self):
        """Return a list of the AQS objects in the collection"""
        return [v for v in self.AQS_collection.values()]

    def add(self, AQS):
        """Add to the collection the provided AQS object(s)"""
        if isinstance(AQS, AirQualityStation):
            if not AQS.uuid in self.AQS_collection:
                self.AQS_collection[AQS.uuid] = AQS
            else:
                warnings.warn("AQS already present in collection, skipping addition")
        elif isinstance(AQS, list):
            for single_AQS in AQS:
                self.add(single_AQS)
        else:
            warnings.warn("Only AQS objects or multiple AQS (as lists) can be added")

    def remove(self, uuid):
        """Remove from the collection one or multiple AQS that match the provided uuid(s)"""
        if isinstance(uuid, list):
            for single_uuid in uuid:
                self.remove(single_uuid)
        try:
            del self.AQS_collection[uuid]
        except KeyError:
            warnings.warn("No AQS with the specified uuid, ignoring command")

    def search(self, name):
        """Get the AQS that match (even partially, not case sensitive) the specified name"""
        res = [AQS for AQS in self.AQS_collection.values() if name.lower() in AQS.name.lower()]
        if len(res) == 1:
            return res[0]
        return res

    def info(self):
        """Generate an informative rich.table of the contained AQS"""
        table = Table(show_header=True, header_style="bold red")
        console = Console()
        table.add_column("AQS")
        table.add_column("Comune")
        table.add_column("Pollutants")
        table.add_column("Entries")
        table.add_column("Datetime range", style='dim')
        for vv in self.AQS_collection.values():
            # yapf: disable
            table.add_row(
                f"[bold]{vv.name}[/bold]",
                f"{vv.comune}",
                ", ".join(map(str,vv.metadata['data_info']['pollutants'])),
                str(vv.metadata['data_info']['shape'][0]),
                str(vv.data['Timestamp'].min()) + " - " + str(vv.data['Timestamp'].max()))
            # yapf: enable
        console.print(table)