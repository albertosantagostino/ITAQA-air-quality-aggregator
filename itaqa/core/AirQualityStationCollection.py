#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class AirQualityStationCollection
"""

import msgpack
import warnings

from pathlib import Path
from rich.console import Console
from rich.table import Table

from itaqa.core.AirQualityStation import AirQualityStation


class AirQualityStationCollection():
    """
    Represent a collection of AirQualityStation objects, encapsulating it as a dictonary

    Args:
        name (str): Name of the collection

    Attributes:
        name (str): Name of the collection
        AQS_dict(dict): Dict of AirQualityStation objects

    Examples:
        AirQualityStationCollection('Mordor')
    """
    def __init__(self, name, AQS=None, file_path=None):
        self.name = name
        self._AQS_dict = dict()

        if AQS:
            self.add(AQS)
        if file_path:
            self.load(file_path)

    def __str__(self):
        self.info()
        return f"(You may use directly the info() method to obtain this info table"

    def __repr__(self):
        return f"AirQualityStationCollection('{self.name}')"

    def __iter__(self):
        yield from self.AQS_dict.values()

    def __getitem__(self, uuid):
        return self.AQS_dict[uuid]

    @property
    def AQS_dict(self):
        """Return the AQS collection itself as a dict"""
        return self._AQS_dict

    @AQS_dict.setter
    def set_AQS_dict(self, AQS_dict):
        """Update the AQS collection"""
        self._AQS_dict.update(AQS_dict)

    @property
    def AQS_list(self):
        """Return a list of the AQS objects in the collection"""
        AQS_list = [v for v in self.AQS_dict.values()]
        AQS_list.sort()
        return AQS_list

    def add(self, AQS):
        """Add to the collection the provided AQS object(s)"""
        if isinstance(AQS, AirQualityStation):
            if not AQS.uuid in self.AQS_dict:
                self.AQS_dict[AQS.uuid] = AQS
            else:
                warnings.warn("AQS already present in collection, skipping addition")
        elif isinstance(AQS, list):
            for single_AQS in AQS:
                self.add(single_AQS)
        elif isinstance(AQS, dict):
            for single_AQS in AQS.values():
                self.add(single_AQS)
        else:
            warnings.warn("Only AQS objects or multiple AQS (as lists) can be added")

    def remove(self, uuid):
        """Remove from the collection one or multiple AQS that match the provided uuid(s)"""
        if isinstance(uuid, list):
            for single_uuid in uuid:
                self.remove(single_uuid)
        else:
            try:
                del self.AQS_dict[uuid]
            except KeyError:
                warnings.warn("No AQS with the specified uuid, ignoring command")

    def search(self, name):
        """Get the AQS that match (even partially, not case sensitive) the specified name"""
        res = [AQS for AQS in self.AQS_list if name.lower() in AQS.name.lower()]
        if len(res) == 1:
            return res[0]
        return res

    def query(self, query):
        """
        Search using a query-like expression, using eval (not so nice, yup), return a dict of matching AQS

        Example: AQSC.expression_search('AQS.data.size < 1000')
        """
        return {AQS.uuid: AQS for AQS in self.AQS_list if eval(query)}

    def save(self, file_path):
        """Serialize and save the AQS collection (as a list of AQS) to a file"""
        with open(file_path, 'wb') as fp:
            packed = msgpack.packb(self.AQS_list, default=AirQualityStation.encode_AQS_msgpack)
            fp.write(packed)
        # TODO: Write json/yaml info file

    def load(self, file_path):
        """Load a serialized AQS collection"""
        if Path(file_path).exists():
            with open(file_path, 'rb') as fp:
                bytedata = fp.read()
            self.add(msgpack.unpackb(bytedata, object_hook=AirQualityStation.decode_AQS_msgpack))
        else:
            raise FileNotFoundError("The specified file doesn't exist")

    def info(self):
        """Generate an informative rich.table of the contained AQS"""
        table = Table(show_header=True, header_style="bold red")
        console = Console()
        table.add_column("AQS")
        table.add_column("UUID", style='dim')
        table.add_column("Comune")
        table.add_column("Pollutants")
        table.add_column("Entries")
        table.add_column("Datetime range", style='dim')
        for vv in self.AQS_dict.values():
            ts = vv.data['Timestamp']
            # yapf: disable
            table.add_row(
                f"[bold]{vv.name}[/bold]",
                f"{vv.uuid}",
                f"{vv.comune}",
                ", ".join(map(str,vv.metadata['data_info']['pollutants'])),
                str(vv.metadata['data_info']['shape'][0]),
                str(ts.min())[0:10] + " - " + str(ts.max())[0:10])
            # yapf: enable
        console.print(table)
