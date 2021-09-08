"""
Name    : ScatterViewYDataHandler.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 08.09.2021 17:04
Desc    : 
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import numpy as np

class ScatterViewHandler(object):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.selVariableCollection = []

    def addEntry(self, *args, **kwargs):
        new_entry = YData(*args)
        self.selVariableCollection.append(new_entry)
        self.layout.addLayout(new_entry.hbox)
    #
    # def getVariableSelectors(self):
    #     return [ el.btnRemove for el in self.selVariableCollection ]

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


class YData(object):
    def __init__(self, hbox, dropdown, btnAdd, btnRemove, parent=None):
        self.hbox = hbox
        self.dropdown = dropdown
        self.btnAdd = btnAdd
        self.btnRemove = btnRemove
        self.parent = parent

    def removeEntries(self):
        self.dropdown.deleteLater()
        self.btnAdd.deleteLater()
        self.btnRemove.deleteLater()


# class XData(object):
#     def __init__(self):
#



    # def addEntry(self):
