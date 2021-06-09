from PyQt5.QtWidgets import *


class QCTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def update(self, event):
        self.viewport().repaint()
        super().dataChanged(event)
