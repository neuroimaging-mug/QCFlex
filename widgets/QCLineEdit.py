from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QCLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def getBasePath(self):
        return Path(self.text())

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(Qt.MoveAction)
            super().dropEvent(event)
            pass
        if event.mimeData().hasUrls():

            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.setText(links[0])

        elif isinstance(event.source(), QListWidget):
            super().dropEvent(event)

        else:
            event.ignore()
