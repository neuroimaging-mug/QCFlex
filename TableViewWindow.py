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

from widgets.QCPandasTableWidget import *
from widgets.QCTableViewWidget import QCTableView



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

        self.scatter = ScatterView(self)
        self.scatter.show()
        self.scatter.sendIndexClickedOn.connect(self.doubleClicked_table)

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
        self.current_index = row_index
        self.updateCurrentImage.emit(True)
        self.data.selectRow(self.current_index)

        self.scatter.updatePlotData()

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

    def getSelectedRowData(self):
        sel_rows = self.data.selectionModel().selectedRows()[0]

        model = self.data.model()

        headers = model.getHeaders()
        data_array = dict()

        for key in REQUIRED_TABLE_COLUMNS:
            path_idx = list(headers).index(key)
            model_idx = model.index(sel_rows.row(), path_idx)
            selected_data = model.data(model_idx)
            data_array[key] = selected_data

        return data_array

    def updateQCEntry(self, status, comment=''):
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

    def tableSaveExceptionMessageBox(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Error saving table")
        msg.setText(error.args[1])
        msg.exec_()

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