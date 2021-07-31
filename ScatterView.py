"""
Name    : ScatterView.py.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 31.07.2021 20:03
Desc    :
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from widgets.MplWidget import MplCanvas

from utils import loadTableFile

import pandas as pd
import numpy as np

class ScatterView(QMainWindow):
    sendIndexClickedOn = pyqtSignal(int)
    receiveCurrentIndex = pyqtSignal(int)

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle("application main window")
        self.parent = parent

        cw = QWidget()

        layout = QVBoxLayout()
        cw.setLayout(layout)



        self.df = loadTableFile(self.parent.table_filename)

        self.c1 = MplCanvas(self, width=5, height=4, dpi=100)
        self.c1.transmit_data_index.connect(self.onForwardDataClickedOn)

        layout.addWidget(self.c1)

        navi_toolbar = NavigationToolbar(self.c1, self)
        layout.addWidget(navi_toolbar)

        self.valid_colums = self.evaluateValidColumns(self.df)

        self.xdata_box = QComboBox()
        self.xdata_box.addItems(list(self.valid_colums))
        layout.addWidget(self.xdata_box)

        self.ydata_box = QComboBox()
        self.ydata_box.addItems(list(self.valid_colums))
        layout.addWidget(self.ydata_box)

        self.xdata_box.currentTextChanged.connect(self.updatePlotDataX)
        self.ydata_box.currentTextChanged.connect(self.updatePlotDataY)

        self.xdata_box.setCurrentIndex(1)
        self.ydata_box.setCurrentIndex(1)

        self.setCentralWidget(cw)

    @pyqtSlot(int)
    def onForwardDataClickedOn(self, index):
        print(f"Got index {index}")
        # update row selection
        self.sendIndexClickedOn.emit(index)

    def evaluateValidColumns(self, df):
        columns = df.columns
        valid_cols = []
        for col in columns:
            data = df[col].values
            data = pd.to_numeric(data, errors='coerce')
            if not np.isnan(data).all():
                valid_cols.append(col)
                df[col] = data
        return valid_cols

    def updatePlotDataX(self, new_column_name):
        print("Init update of X-Axis!")

        xlabel = new_column_name
        ylabel = self.ydata_box.currentText()

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabel].values

        self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabel)

    def updatePlotDataY(self, new_column_name):
        print("Init update of Y-Axis!")

        xlabel=self.xdata_box.currentText()
        ylabel=new_column_name

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabel].values

        self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabel)

    def updatePlotData(self):
        self.c1.refreshPlot(self.parent.current_index)

    def setCurrentIndex(self, current_index):
        self.current_index = current_index

    def setData(self, xdata, ydata):
        pass