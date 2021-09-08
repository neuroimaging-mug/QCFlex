"""
Name    : ScatterViewYDataHandler.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 08.09.2021 17:04
Desc    : 
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize

import numpy as np

from settings import SELECTION_COLOR

class ScatterViewHandler(object):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.selVariableCollection = []
        self.xVariable = None

    def getAvailableColors(self):
        """Retrieves the selected colors from all current ylabels"""
        selected_colors = [el.currentColor for el in self.selVariableCollection]
        return list(SELECTION_COLOR.keys() - selected_colors)

    def setNewColor(self):
        """Updates the color of a Ylabel"""

    def addYEntry(self, *args, **kwargs):
        new_entry = YData(*args, parent=self)
        self.selVariableCollection.append(new_entry)
        self.layout.addLayout(new_entry.hbox)

    def addXEntry(self, *args, **kwargs):
        new_entry = XData(*args)
        self.xVariable = new_entry
        self.layout.addWidget(new_entry.dropdown)

    def getXEntry(self):
        return self.xVariable

    def removeYDataEntry(self, reference):
        def searchEntry(reference, array):
            for idx in range(len(array)):
                if reference == array[idx]:
                    return idx
            print("Reference not found!")
            return None

        btn_collection = [ el.btnRemove for el in self.selVariableCollection ]
        idx = searchEntry(reference, btn_collection)
        selected_entry = self.selVariableCollection[idx]
        selected_entry.removeEntries()
        self.layout.removeItem(selected_entry.hbox)
        del self.selVariableCollection[idx]

    def getSelectedVariables(self):
        return [el.dropdown.currentText() for el in self.selVariableCollection]

    def getAllVariableSelectors(self):
        return []

    def updateAvailableVariables(self, available_columns, selectable_columns):
        for el in self.selVariableCollection:
            for rdx, (item, _) in enumerate(selectable_columns):
                if item not in available_columns:
                    # print([box.itemText(i) for i in range(box.count())])
                    el.dropdown.view().setRowHidden(rdx, True)
                else:
                    el.dropdown.view().setRowHidden(rdx, False)

class YData(object):
    def __init__(self, hbox, dropdown, btnAdd, btnRemove, parent=None):
        self.hbox = hbox
        self.dropdown = dropdown
        self.btnAdd = btnAdd
        self.btnRemove = btnRemove
        self.parent = parent
        self.btnColor = None

        self.insertElements()

    def insertElements(self):
        """Adds all elements to the horizontal layout!"""


        availableColors = self.parent.getAvailableColors()
        if len(availableColors) > 0:
            self.currentColor = availableColors[0]
        else:
            raise Warning("Too many yLabels selected for the defined color palette."
                          "Define more compatible colors in the settings.py file!")

        # define color button
        self.btnColor = QPushButton("")
        self.btnColor.setFixedSize(QSize(20, 20))
        self.btnColor.setStyleSheet(f"""background-color: {self.currentColor};
                                    border-radius: 50px;
                                    border: 1px solid white""")
        self.hbox.addWidget(self.btnColor)

        self.hbox.addWidget(self.dropdown)
        self.hbox.addWidget(self.btnAdd)
        if self.btnRemove is not None:
            self.hbox.addWidget(self.btnRemove)



    def removeEntries(self):
        self.dropdown.deleteLater()
        self.btnAdd.deleteLater()
        self.btnRemove.deleteLater()
        self.btnColor.deleteLater()

class XData(object):
    def __init__(self, hbox, dropdown, parent=None):
        self.hbox = hbox
        self.dropdown = dropdown
        # self.color = color

    def insertElements(self):
        self.hbox.addWidget(self.dropdown)
        # if self.color:
        #     self.

    def updateAvailableVariables(self, availableColumns):
        self.dropdown.addItems(availableColumns)
