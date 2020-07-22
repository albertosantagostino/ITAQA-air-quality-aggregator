#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization functions
"""

from itaqa.visualization.defs import get_geometry_from_subplots_amount, get_pollutant_color
from plotly.subplots import make_subplots

import plotly.graph_objects as go


def AQS_plot(AQS, pollutant=None):
    """Create a single plot, with all the pollutants on the same graph area"""
    data_lines = get_data_lines(AQS)
    fig = go.Figure(data=data_lines)
    fig.layout.template = 'none'
    fig.update_layout(title=f'{AQS.name}', xaxis_title='Time', plot_bgcolor='rgba(0,0,0,0.04)')
    fig.show()


def AQS_multiplot(AQS):
    """Create multiple subplots (1 for pollutant), automatically choosing the layout"""
    data_lines = get_data_lines(AQS)
    # Determine rows and cols depending on the subplots to visualize
    if len(data_lines) <= 3:
        rows = len(data_lines)
        cols = 1
    else:
        rows, cols = get_geometry_from_subplots_amount(len(data_lines))

    fig = make_subplots(rows=rows,
                        cols=cols,
                        horizontal_spacing=0.05 / cols,
                        vertical_spacing=0.15 / rows,
                        shared_xaxes=True,
                        subplot_titles=([col for col in AQS.data.columns if col != 'Timestamp']))
    for idx, scatter in enumerate(data_lines):
        quo, rem = divmod(idx, rows)
        fig.add_trace(scatter, row=rem + 1, col=quo + 1)
    fig.update_layout(title=f'{AQS.name}',
                      title_font_size=30,
                      title_x=0.5,
                      plot_bgcolor='rgba(0,0,0,0.04)',
                      showlegend=False)
    # Tweak: link all x-axes when multiple columns are visualized
    for i in range(1, len(data_lines) + 1):
        fig['layout'][f'xaxis{str(i)}']['matches'] = 'x'
    fig.show()


def get_data_lines(AQS):
    """Obtain scatter lines for plotting from the data stored in the AQS"""
    data_lines = list()
    for pollutant in AQS.data.columns:
        if pollutant != 'Timestamp':
            data_line = go.Scattergl(x=AQS.data['Timestamp'],
                                     y=AQS.data[f'{pollutant}'],
                                     name=f'{pollutant}',
                                     mode='lines+markers',
                                     marker=dict(color='Black', size=3),
                                     line=dict(color=get_pollutant_color(pollutant), width=2))
            data_lines.append(data_line)
    return data_lines
