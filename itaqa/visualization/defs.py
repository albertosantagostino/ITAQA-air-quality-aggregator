#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definition of visualization-related constants and values
"""

SUBPLOT_LAYOUT = {(4, 4): (2, 2), (5, 6): (3, 2), (7, 8): (4, 2), (9, 9): (3, 3)}


def get_geometry_from_subplots_amount(subplots):
    """Return the correspondant geometry (rows, cols) depending on the amount of pollutants to plot"""
    for k, v in SUBPLOT_LAYOUT.items():
        if subplots >= k[0] and subplots <= k[1]:
            return v


def get_pollutant_color(pollutant):
    """Return the color representing a pollutant"""
    if pollutant == 'PM10':
        return '#0f1a66'
    elif pollutant == 'PM2_5':
        return '#2c79a5'
    elif pollutant == 'NO2':
        return '#5e4abf'
    elif pollutant == 'NO':
        return '#8c78ed'
    elif pollutant == 'NOX':
        return '#2d7bce'
    elif pollutant == 'O3':
        return '#138913'
    elif pollutant == 'BENZENE':
        return '#91024a'
    elif pollutant == 'CO':
        return '#3c8c71'
    elif pollutant == 'SO2':
        return '#774f11'
    else:
        raise ValueError(f"Unknown pollutant ({pollutant})")
