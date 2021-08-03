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

        # Transform columns to be connected to QDropdownMenus
        self.selectable_columns = []
        for col in self.valid_colums:
            self.selectable_columns.append([col, None])



        self.ydata_collection = []

        self.xdata_box = QComboBox()
        self.xdata_box.addItems(self.getAvailableColumns())
        layout.addWidget(self.xdata_box)
        self.ydata_collection.append((None, self.xdata_box, None, None))

        self.hbox = QHBoxLayout()
        layout.addLayout(self.hbox)

        self.ydata_collection_layout = QVBoxLayout()
        layout.addLayout(self.ydata_collection_layout)

        self.ydata_box = QComboBox()
        self.ydata_box.addItems(self.getAvailableColumns())
        self.hbox.addWidget(self.ydata_box)
        self.ydata_collection.append((None, self.ydata_box, None, None))






        def addNewVariableSelector():
            """
            Add a new row of variable selection dropdown and add/remove button to scatterview.

            :return:
            """
            ydata_box_new = QComboBox()
            ydata_box_new.addItems(self.getAvailableColumns())
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
            hbox.addWidget(ydata_box_new)
            hbox.addWidget(add)
            hbox.addWidget(remove)
            self.ydata_collection.append((hbox, ydata_box_new, add, remove))
            self.ydata_collection_layout.addLayout(hbox)



        add = QPushButton()
        add.setFixedWidth(20)
        add.setIcon(QIcon(str(Path("files/plus-solid.svg"))))
        add.clicked.connect(addNewVariableSelector)
        self.hbox.addWidget(add)

        ##
        self.xdata_box.currentTextChanged.connect(self.updatePlotDataXY)
        self.ydata_box.currentTextChanged.connect(self.updatePlotDataXY)

        # self.xdata_box.setCurrentIndex(1)
        # self.ydata_box.setCurrentIndex(2)


        self.setCentralWidget(cw)

    def removeCurrentVariableSelector(self):
        sender = self.sender()
        print(self.ydata_collection[1:])
        add_data_selectors = np.array(self.ydata_collection[1:]) # the first one is the first y data selector

        row_idx, btn_idx = np.where(add_data_selectors == sender)
        selected_row = add_data_selectors[row_idx]

        selected_layout = selected_row[0][0]
        for i in range(selected_layout.count()):
            # item = selected_layout.itemAt(i)
            item = selected_layout.itemAt(i).widget().deleteLater()
            # print(item)
            selected_layout.removeItem(item)

        self.ydata_collection_layout.removeItem(selected_layout)
        del self.ydata_collection[row_idx[0]+1]


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

        selected_columns = []
        # Get selected variables
        for idx, row in enumerate(self.ydata_collection):
            if idx == 0:
                selected_columns.append(row.currentText())
            else:
                selected_columns.append(row[1])

        for sel in selected_columns:
            if sel in available_columns:
                available_columns.remove(sel)

        return available_columns

    def updateAvailableColumns(self):
        sender = self.sender()
        selected_text = sender.currentText()

        # Free current selection
        for el in self.selectable_columns:
            if sender in el:
                el[1] = None

        # Assign to new selection
        for el in self.selectable_columns:
            if selected_text == el[0]:
                el[1] = sender

        avail = self.getAvailableColumns()


        for idx, (_, box, _, _)  in enumerate(self.ydata_collection):
            if box != sender:
                box.blockSignals(True)
                ct = box.currentText()
                box.clear()
                avail_conc = avail + [ct]
                box.addItems(avail_conc)
                box.setCurrentIndex(avail_conc.index(ct))
                box.blockSignals(False)

    def getAvailableColumns(self):
        avail = []
        for el in self.selectable_columns:
            if el[1] == None:
                avail.append(el[0])

        return avail

    def updatePlotDataXY(self):
        """
        Updates the plot with the columns selected in the dropdown boxes
        :return:
        """

        # Get current selected labels from all fields
        labels = []
        for idx, el in enumerate(self.ydata_collection[1:]):
            labels.append(el[1].currentText())

        xlabel=self.xdata_box.currentText()
        ylabels=labels

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabels].values

        if len(labels) == 1:
            self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabels)
        else:
            self.c1.updatePlotMultiColumns(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabels, colors=['blue', 'darkorange', 'yellowgreen', 'forestgreen', 'red'])

        self.updateAvailableColumns()

    def updatePlotData(self):
        self.c1.refreshPlot(self.parent.current_index)

    def setCurrentIndex(self, current_index):
        self.current_index = current_index

    def setData(self, xdata, ydata):
        pass