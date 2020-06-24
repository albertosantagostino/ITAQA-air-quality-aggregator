#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definition of pollutants and eventually other required enums (station type, ...)
"""

from enum import Enum, auto


class Pollutant(Enum):
    """Enum holding pollutant types"""
    # yapf: disable
    PM10    = auto()
    PM2_5   = auto()
    NO2     = auto()
    NOX     = auto()
    O3      = auto()
    BENZENE = auto()
    CO      = auto()
    SO2     = auto()
    UNSET   = auto()
    # yapf: enable