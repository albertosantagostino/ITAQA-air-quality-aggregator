#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQSC viewer and AQS explorer GUI
"""

import logging
import sys

from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QGuiApplication, QKeySequence
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFileDialog,
    QGridLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QPushButton,
    QShortcut,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
)

from itaqa.core.AirQualityStationCollection import AirQualityStationCollection
from itaqa.core.defs import Pollutant

logger = logging.getLogger(__name__)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__()

        ## Text widgets
        # AQS list selector and list
        self.files_list = QListWidget()
        self.files_list.setFixedHeight(140)
        # AQS list information
        self.AQSC_info = QTextBrowser()
        self.AQSC_info.setMinimumHeight(80)
        # Stored AQS
        self.AQS_stored = QListWidget()
        self.AQS_stored.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.AQS_stored.setMinimumHeight(200)
        self.AQS_info = QTextBrowser()
        # AQS pollutants table
        self.table_pl = QTableWidget()
        self.table_pl.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_pl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        fnt = QFont()
        fnt.setPointSize(8)
        self.table_pl.setFont(fnt)
        self.table_pl.setRowCount(len(Pollutant) - 1)
        self.table_pl.setColumnCount(2)
        self.table_pl.setVerticalHeaderLabels([pl.name for pl in Pollutant if pl.name != 'UNSET'])
        self.table_pl.setHorizontalHeaderLabels(['Present', 'Count'])
        self.table_pl.setMinimumHeight(190)
        self.table_pl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pl.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        ## Buttons
        button_browse_folder = QPushButton("Browse...")
        button_browse_folder.setMinimumHeight(60)
        self.button_AQS_plot = QPushButton("Plot/Visualize\n(<spacebar>)")
        self.button_AQS_plot.setDisabled(True)
        shortcut_AQS_plot = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.button_AQS_plot.setMinimumHeight(60)

        ## Layouts
        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignTop)
        buttons_layout.addWidget(self.button_AQS_plot)
        buttons_layout.addStretch()

        # Main grid
        grid = QGridLayout()
        grid.addWidget(QLabel("Serialized AirQualityStationCollection (AQSC) objects:"), 0, 0)
        grid.addWidget(button_browse_folder, 2, 2)
        grid.addWidget(self.files_list, 2, 0, 1, 2)
        grid.addWidget(QLabel("AQSC information:"), 3, 0)
        grid.addWidget(self.AQSC_info, 4, 0, 1, 2)
        grid.addWidget(QLabel("AQS stored:"), 5, 0)
        grid.addWidget(self.AQS_stored, 6, 0, 3, 1)
        grid.addWidget(self.AQS_info, 6, 1, 1, 1)
        grid.addWidget(self.table_pl, 7, 1, 2, 1)
        grid.addLayout(buttons_layout, 6, 2, 3, 1)

        ## Window properties
        self.setLayout(grid)
        self.setWindowTitle("ITAQA AirQualityStationCollection Explorer")
        self.setGeometry(0, 0, 800, 700)
        self.setMinimumSize(800, 700)
        # Set position depending on the screen geometry
        geometry = QGuiApplication.screens()[0].geometry()
        self.move((geometry.width() - self.width()) / 2, (geometry.height() - self.height()) / 2)

        ## Signals and events
        self.files_list.itemClicked.connect(self.refresh_selected_AQSC_info)
        # TODO: Multiselection support and use itemSelectionChanged always (to support keyboard scroll)
        # self.files_list.itemSelectionChanged.connect(...)
        self.AQS_stored.itemClicked.connect(self.refresh_selected_AQS_info)
        button_browse_folder.clicked.connect(self.browse_folder)
        self.button_AQS_plot.clicked.connect(self.AQS_plot)
        shortcut_AQS_plot.activated.connect(self.AQS_plot)

        # Global data containers
        self.dir_path = ''
        self.AQSC_loaded = None
        self.AQS_selected = None

    def browse_folder(self):
        """Open 'browse folder' dialog"""
        root_path = Path.cwd()
        if root_path.joinpath('dump').exists():
            root_path = root_path.joinpath('dump')
        self.dir_path = QFileDialog.getExistingDirectory(self,
                                                         caption="Select AQSC directory",
                                                         directory=str(root_path))
        files = sorted(Path(self.dir_path).iterdir())
        for ff in files:
            if ff.suffix == '.msgpack':
                self.files_list.addItem(ff.name)

    def refresh_selected_AQSC_info(self, item):
        """List all .msgpack files in the selected folder"""
        AQSC_selected = Path(self.dir_path + '/' + item.text())
        self.AQSC_loaded = AirQualityStationCollection(file_path=AQSC_selected)
        filename_info = parse_filename(item.text())
        self.AQSC_info.setMarkdown(f"Stored AQS: **{len(self.AQSC_loaded.AQS_list)}**\n\n" +
                                   f"Date range: from **{filename_info['min_dt']}** to "
                                   f"**{filename_info['max_dt']}**")
        self.AQS_stored.clear()
        for AQS in self.AQSC_loaded.AQS_list:
            self.AQS_stored.addItem(AQS.name)

    def refresh_selected_AQS_info(self, item):
        """Update the shown information on the selected AQS"""
        self.AQS_selected = self.AQSC_loaded.search(item.text())
        if isinstance(self.AQS_selected, list):
            raise ValueError("More than one station with the same name")
        tot_data = self.AQS_selected.data.shape[0]
        pls = ', '.join(map(str, [pl for pl in self.AQS_selected.data.columns.to_list() if pl != 'Timestamp']))
        self.AQS_info.setMarkdown(f"**{self.AQS_selected.name}**\n\nEntries: **{tot_data}**\n\nPollutants:\n\n{pls}")
        self.table_pl.clearContents()

        # Get the pollutant table cells styles
        red_cell, green_cell = prepare_table_cells()
        fnt = QFont()
        fnt.setBold(True)
        # For each known pollutant, fill the pollutant table based on the ones stored in the AQS
        pl_list = [pl.name for pl in Pollutant if pl.name != 'UNSET']
        for i, pl in enumerate(pl_list):
            header_pl = self.table_pl.model().headerData(i, Qt.Vertical)
            if header_pl in [pl for pl in self.AQS_selected.data.columns.to_list() if pl != 'Timestamp']:
                self.table_pl.setItem(i, 0, QTableWidgetItem(green_cell))
                count_cell = QTableWidgetItem(str(self.AQS_selected.data[pl].count()))
                count_cell.setFont(fnt)
                self.table_pl.setItem(i, 1, count_cell)
            else:
                self.table_pl.setItem(i, 0, QTableWidgetItem(red_cell))

        self.button_AQS_plot.setEnabled(True)

    def AQS_plot(self):
        """Call AQS.plot()"""
        self.AQS_selected.plot()

    def clear_selection(self):
        """Clear all widgets"""
        self.AQSC_info.clear()
        self.AQS_stored.clear()
        self.AQS_info.clear()


def prepare_table_cells():
    """Prepare pollutant table cells"""
    red_cell = QTableWidgetItem()
    red_cell_brush = QBrush()
    red_cell_brush.setStyle(Qt.BrushStyle(Qt.DiagCrossPattern))
    red_cell_brush.setColor(QColor(255, 0, 0))
    red_cell.setBackground(red_cell_brush)
    green_cell = QTableWidgetItem()
    green_cell_brush = QBrush()
    green_cell_brush.setStyle(Qt.BrushStyle(Qt.Dense4Pattern))
    green_cell_brush.setColor(QColor(0, 255, 0))
    green_cell.setBackground(green_cell_brush)
    return red_cell, green_cell


def parse_filename(filename):
    """Given a filename returns information on the creation, dt_range and region"""
    # TODO: Implement here a fallback mode that manually gets the information if filename is invalid
    tok = filename.split('_')
    filename_info = {}
    filename_info['creation'] = datetime.strptime(tok[0], '%Y%m%d%H%M%S')
    filename_info['min_dt'] = datetime.strptime(tok[1], 'm%y%m%d').strftime('%Y-%m-%d')
    filename_info['max_dt'] = datetime.strptime(tok[2], 'M%y%m%d').strftime('%Y-%m-%d')
    filename_info['region'] = tok[3]
    return filename_info


def start_GUI():
    """Entrypoint: start viewer"""
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the main Dialog
    dialog = Dialog(app)
    dialog.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
