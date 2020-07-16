#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQS collection viewer
"""

import logging
import sys

from pathlib import Path
from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QGridLayout, QLabel, QFileDialog, QListWidget, QFrame, QTextBrowser
from PyQt5.QtGui import QFont

from itaqa.utils.serialization_utils import load_AQS_from_msgpack

logger = logging.getLogger(__name__)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__()

        # AQS list selector and list
        self.browse_AQS_folder = QPushButton("Select folder...")
        self.AQS_lists = QListWidget()
        self.current_folder_dict = {}

        # AQS list information
        self.text_info = QTextBrowser()

        # Stored AQS
        self.AQS_stored = QListWidget()
        self.AQS_info = QTextBrowser()

        # Layout
        grid = QGridLayout()
        grid.addWidget(QLabel("Serialized AQS lists:"), 0, 0)
        grid.addWidget(self.browse_AQS_folder, 0, 1)
        grid.addWidget(self.AQS_lists, 2, 0, 1, 2)
        grid.addWidget(QLabel("List information:"), 3, 0)
        grid.addWidget(self.text_info, 4, 0, 1, 2)
        grid.addWidget(QLabel("Stored AQS:"), 5, 0)
        grid.addWidget(self.AQS_stored, 6, 0)
        grid.addWidget(self.AQS_info, 6, 1)

        # Window properties
        self.setLayout(grid)
        self.setWindowTitle("ITAQA Visualizer")
        self.setGeometry(500, 350, 800, 400)
        self.setMinimumSize(700, 400)

        # Add button signals and events
        self.browse_AQS_folder.clicked.connect(self.browse_folder)
        self.AQS_lists.itemClicked.connect(self.browse_msgpack_list)
        self.AQS_stored.itemClicked.connect(self.show_AQS)

        # Global data containers
        self.dir_path = ''
        self.loaded_AQS_list = []
        self.sel_AQS = None

    def browse_folder(self):
        self.dir_path = QFileDialog.getExistingDirectory(
            self, caption="Open AQS lists directory", directory='/home/alberto/code/ITAQA-air-quality-aggregator/dump')
        files = sorted(Path(self.dir_path).iterdir())
        for ff in files:
            if ff.suffix == '.msgpack':
                self.AQS_lists.addItem(ff.name)

    def browse_msgpack_list(self, item):
        selected_msgpack = Path(self.dir_path + '/' + item.text())
        try:
            self.loaded_AQS_list = load_AQS_from_msgpack(selected_msgpack)
        except ValueError:
            logger.error("Cannot load the selected AQS msgpack")
            self.clear_selection()
        else:
            self.text_info.setMarkdown(
                f"**{item.text()}**\n\nStored AQS: **{len(self.loaded_AQS_list)}**\n\Date range: TODO")
            self.AQS_stored.clear()

            for AQS in self.loaded_AQS_list:
                self.AQS_stored.addItem(AQS.name)

    def show_AQS(self, item):
        # TODO: Refactor when AQS_list is encapsulated
        for AQS in self.loaded_AQS_list:
            if AQS.name == item.text():
                self.sel_AQS = AQS
        tot_data = self.sel_AQS.metadata['data_info']['total']
        pollutants = ', '.join(map(str, self.sel_AQS.metadata['data_info']['pollutants']))
        self.AQS_info.setMarkdown(f"**{self.sel_AQS.name}**\n\nData stored: **{tot_data}**\n\nPollutants: {pollutants}")

    def clear_selection(self):
        self.text_info.clear()
        self.AQS_stored.clear()
        self.AQS_info.clear()


def start_viewer():
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Create and show the form
    form = Dialog(app)
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
