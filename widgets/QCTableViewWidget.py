from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class QCTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def update(self, event):
        self.viewport().repaint()
        super().dataChanged(event)

    def mouseDoubleClickEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("Double")
            event.accept()
            super().mouseDoubleClickEvent(event)

    # def mousePressEvent(self, event):
    #     if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonRelease:
    #         pass
    #     else:
    #         print("double")
    #         event.accept()
    #         super().mousePressEvent(event)

