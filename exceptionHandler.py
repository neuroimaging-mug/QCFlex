import numpy as np
from PIL import Image, ImageDraw
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class ExceptionHandler:
    def __init__(self, parent, text):
        self.text = text
        self.parent = parent

        self.showDialogue()

    def showDialogue(self):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
        msg.setWindowTitle("Window Title") # ("Error loading table")
        msg.setText(self.text)
        msg.exec_()
