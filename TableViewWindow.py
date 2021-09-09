"""
Name    : TableViewWindow.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 31.07.2021 20:13
Desc    : 
"""
from settings import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer

from pathlib import Path
from ScatterView import ScatterView
from utils import loadTableFile
import pandas as pd
import os
from widgets.QCPandasTableWidget import *
from widgets.QCTableViewWidget import QCTableView

from datetime import datetime
import logging as lg

class TableViewWindow(QMainWindow):
    updateCurrentImage = pyqtSignal(bool)

    def __init__(self, table_path, parent=None):
        super(TableViewWindow, self).__init__(parent)
        self.main_window = parent
        self.table_filename = table_path
        self.image_basepath = Path(table_path).absolute().parents[0]
        self.resize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.current_index = 0

        self.setupUi(self)

        # Setting the geometry of all windows for a better overview!
        ## Move main window to the right
        geo = QGuiApplication.primaryScreen().availableGeometry()
        print(geo.width(), geo.height())
        sw = geo.width()
        sh = geo.height()
        v_offset = 30
        h_offset = 0
        main_window_width = int(sw * 0.6)
        main_window_height = int(sh * 1)
        scatter_window_width = int(sw * 0.4)
        scatter_window_height = int(sh * 0.5)
        table_window_width = int(sw * 0.4)
        table_window_height = sh - scatter_window_height

        # Setting main window geometry
        position = (sw - main_window_width, v_offset)
        self.main_window.setGeometry(*position, main_window_width, main_window_height - v_offset)

        # Setting table view geometry
        position = (0, scatter_window_height)
        self.setGeometry(*position, scatter_window_width, scatter_window_height)

        ## Create Scatter View window
        self.scatter = ScatterView(self)
        self.scatter.show()
        self.scatter.sendIndexClickedOn.connect(self.doubleClicked_table)

        # Setting scatter view geometry
        position = (0, v_offset)
        self.scatter.setGeometry(*position, table_window_width, table_window_height- v_offset * 2)

    def updateTableData(self, fpath):
        """Updates the table data when the table object already exists!"""
        lg.info("Updating table data.")
        print("Updating table data.")
        self.table_filename = fpath
        self.df = loadTableFile(self.table_filename)

        self.current_index = 0

        self.model = PandasTableModel(self.df)
        self.data.setModel(self.model)
        self.data.selectRow(self.current_index)

    def getNextId(self):
        if (self.current_index + 1) < len(self.df):
            self.current_index += 1
            self.getCurrentId()
            self.updateCurrentImage.emit(True)
            self.scatter.updatePlotData()

    def getPreviousId(self):
        self.current_index -= 1
        if self.current_index >= 0:
            self.getCurrentId()
            self.updateCurrentImage.emit(True)
            self.scatter.updatePlotData()
        else:
            self.current_index += 1

    def getCurrentId(self):
        self.data.selectRow(self.current_index)
        print(self.current_index)

    def doubleClicked_table(self, index):
        if type(index) == int:
            row_index = index
        else:
            row_index = index.row()

        if self.current_index == row_index:
            # Same row was selected... skipping...
            pass

        self.current_index = row_index
        self.data.selectRow(self.current_index)
        self.updateCurrentImage.emit(True)

        self.scatter.updatePlotDataXY()

        print(f"Selected row: {row_index}")

    def setupUi(self, test):
        test.setObjectName("test")
        test.resize(800, 600)
        self.centralwidget = QWidget(test)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.data = QCTableView(self.centralwidget)
        self.data.setObjectName("tableView")
        self.data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Define Background of current row, even if window is out of focus
        palette = QPalette()
        palette.setColor(QPalette.Inactive, QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
        palette.setColor(QPalette.Inactive, QPalette.HighlightedText, Qt.white)
        self.data.setPalette(palette)

        self.df = loadTableFile(self.table_filename)

        self.model = PandasTableModel(self.df)
        self.data.setModel(self.model)
        self.data.selectRow(self.current_index)

        self.horizontalLayout.addWidget(self.data)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        test.setCentralWidget(self.centralwidget)

    def deleteUI(self):
        self.scatter.close()
        self.data.close()

    def getSelectedRowData(self):
        sel_rows = self.data.selectionModel().selectedRows()[0]

        model = self.data.model()

        headers = model.getHeaders()
        data_array = dict()

        for key in REQUIRED_TABLE_COLUMNS:  # TODO: Handle exception if not all required colums are provided!
            path_idx = list(headers).index(key)
            model_idx = model.index(sel_rows.row(), path_idx)
            selected_data = model.data(model_idx)
            data_array[key] = selected_data

        return data_array

    def updateQCEntry(self, status, comment=''):
        """Update the QC entry in the table view"""
        # get selected row!
        sel_row = self.data.selectionModel().selectedRows()[0]
        row_idx = sel_row.row()
        model = self.data.model()

        headers = model.getHeaders()

        qc_column = list(headers).index('QC')

        self.df.iloc[row_idx, qc_column] = status

        # Update comments field
        comment_column = list(headers).index('comment')
        self.df.iloc[row_idx, comment_column] = comment

        if self.main_window.autoContinueCheckbox.isChecked():
            self.getNextId()
        else:
            self.getSelectedRowData()
            self.updateCurrentImage.emit(True)

        self.saveTable()
        self.update() #

    def tableSaveExceptionMessageBox(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Error saving table")
        msg.setText(error.args[1])
        msg.exec_()


    def saveBonusData(self):
        """
        Storing time stamp of last save in json file in appdata folder.

        :return:
        """
        import json
        from shutil import copyfile
        appdata_path = Path("appdata")
        appdata_path.mkdir(parents=True, exist_ok=True)
        pfile = appdata_path / Path(".programdata.json")


        identifier = Path(self.table_filename).stem

        data = {}
        now = datetime.now()
        if pfile.exists():
            copyfile(pfile, str(pfile) + f'_{datetime.timestamp(now)}.bku')

        tstamp = datetime.timestamp(now)
        data.update({"last_save": now})

        if not pfile.exists() or os.path.getsize(pfile) == 0:
            data.update({"first_save": now})
            data.update({'total_time_spent': now - now})
            data.update({"filepath": self.table_filename})
            with open(pfile, "w") as wf:
                json.dump({identifier: data}, wf, indent=4, default=str)

        with open(pfile, "r") as rf:
            try:
                contents = json.load(rf)
            except ValueError as e:
                print('invalid json: %s' % e)
        if identifier in contents.keys():
            data_loaded = contents[identifier]
            if all(key in data_loaded for key in ("first_save", "last_save")):
                # first_timestamp = datetime.strptime(data_loaded['first_save'], "%Y-%m-%d %H:%M:%S.%f")
                last_timestamp = datetime.strptime(data_loaded['last_save'], "%Y-%m-%d %H:%M:%S.%f")
                timedelta = datetime.now() - last_timestamp
                data_loaded['last_save'] = now
                data_loaded['total_time_spent'] = (
                            datetime.strptime(data_loaded['total_time_spent'], "%H:%M:%S") + timedelta).strftime(
                    "%H:%M:%S")
                print(f"Total time spend in this evaluation file: {timedelta}")
                data_loaded['filepath'] = self.table_filename
                contents.update({identifier: data_loaded})
                with open(pfile, "w") as wf:
                    json.dump(contents, wf, indent=4, default=str)
        else:
            data.update({"first_save": now})
            data.update({'total_time_spent': now - now})
            data['filepath'] = self.table_filename
            contents.update({identifier: data})
            with open(pfile, "w") as wf:
                json.dump(contents, wf, indent=4, default=str)

    def tableSaveEvent(self):
        try:
            if self.main_window.previous_saveas_path is None:
                self.tableSaveAsEvent()
            else:
                self.saveTable(self.main_window.previous_saveas_path)
        except PermissionError as e:
            self.tableSaveExceptionMessageBox(e)

    def tableSaveAsEvent(self):
        name = QFileDialog.getSaveFileName(self, 'SaveFile', filter="CSV files (*.csv)")
        try:
            self.saveTable(name[0])
            self.main_window.previous_saveas_path = name[0]
        except PermissionError as e:
            self.tableSaveExceptionMessageBox(e)

    def saveTable(self, name='Test.csv'):
        self.df.to_csv(name, index_label=None, sep=';')
        self.saveBonusData()
        self.main_window.updateTimeLabel()