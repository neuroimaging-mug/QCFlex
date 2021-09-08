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

from pathlib import Path
import pandas as pd
import numpy as np

from ScatterViewYDataHandler import *


class ScatterView(QMainWindow):
    """
    Window that displays graphs
    """
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

        # # Transform columns to be connected to QDropdownMenus
        # self.selectable_columns = []
        # for col in self.valid_colums:
        #     self.selectable_columns.append([col, None])

        self.ydata_collection = []

        xdata_layout = QHBoxLayout()

        xdata_box = QComboBox()

        self.yDataCollection = ScatterViewHandler(self.valid_colums)

        xdata_box.currentTextChanged.connect(self.updatePlotDataXY)
        self.yDataCollection.addXEntry(xdata_layout, xdata_box)
        self.yDataCollection.xVariable.updateAvailableVariables(self.valid_colums)

        layout.addLayout(self.yDataCollection.layout)

        def addNewVariableSelector():
            """
            Add a new row of variable selection dropdown and add/rermove button to scatterview.

            :return:
            """
            ydata_box_new = QComboBox()
            # ydata_box_new.addItems(y.getAvailableColumns())
            ydata_box_new.currentTextChanged.connect(self.updatePlotDataXY)
            hbox = QHBoxLayout()

            # Add Button
            add = QPushButton()
            add.clicked.connect(addNewVariableSelector)
            add.setFixedWidth(20)
            add.setIcon(QIcon(str(Path("files/plus-solid.svg"))))

            # Delete Button
            remove = QPushButton()
            remove.clicked.connect(self.removeCurrentVariableSelector)
            remove.setIcon(QIcon(str(Path("files/minus-solid.svg"))))
            remove.setFixedWidth(20)
            #
            # hbox.addWidget(ydata_box_new)
            # hbox.addWidget(add)
            # hbox.addWidget(remove)
            ydata_box_new.currentTextChanged.connect(self.updatePlotDataXY)
            self.yDataCollection.addYEntry(hbox, ydata_box_new, add, remove)
            # self.ydata_collection.append((hbox, ydata_box_new, add, remove))
            # self.ydata_collection_layout.addLayout(hbox)

        hbox = QHBoxLayout()

        add = QPushButton()
        add.setFixedWidth(20)
        add.setIcon(QIcon(str(Path("files/plus-solid.svg"))))
        add.clicked.connect(addNewVariableSelector)

        ydata_box = QComboBox()
        # ydata_box.addItems(self.yDataCollection.getAvailableColumns())

        self.yDataCollection.addYEntry(hbox, ydata_box, add, None)
        ydata_box.currentTextChanged.connect(self.updatePlotDataXY)

        self.yDataCollection.initVariableAssignment()
        self.setCentralWidget(cw)

    def removeCurrentVariableSelector(self):
        sender = self.sender()

        self.yDataCollection.removeYDataEntry(sender)
        self.updatePlotDataXY()

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

    def getValidColumns(self):
        """
        Selects only columns names, that are not selected by the dropdown boxes
        :return: list of available column names
        """
        available_columns = self.evaluateValidColumns(self.df)

        selected_columns = self.yDataCollection.getSelectedVariables()

        for sel in selected_columns:
            if sel in available_columns:
                available_columns.remove(sel)

        return available_columns

    def updateAvailableColumns(self):
        sender = self.sender()
        if type(sender) == QComboBox:
            # Update available items in all other Dropdown Menus
            self.yDataCollection.updateAvailableVariables()
        else:
            print("WARNING: updateAvailableColumns - Wrong sender detected...")

    def updatePlotDataXY(self):
        """
        Updates the plot with the columns selected in the dropdown boxes
        :return:
        """

        # Get current selected labels from all fields
        labels = []
        colors = []
        for idx, el in enumerate(self.yDataCollection.selVariableCollection):
            labels.append(el.dropdown.currentText())
            colors.append(el.currentColor)

        xlabel = self.yDataCollection.getXEntry().dropdown.currentText()
        ylabels = labels

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabels].values

        if len(labels) == 1:
            self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabels)
        else:
            self.c1.updatePlotMultiColumns(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabels,
                                           colors=colors)
        self.updateAvailableColumns()

    def updatePlotData(self):
        self.c1.refreshPlot(self.parent.current_index)

    def setCurrentIndex(self, current_index):
        self.current_index = current_index

    def setData(self, xdata, ydata):
        pass
