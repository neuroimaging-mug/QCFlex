import numpy as np
import qimage2ndarray as q2n
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QCImageViewer(QGraphicsView):
    setLoadedId = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_zoom = 0
        self.empty = True
        self.scene = QGraphicsScene(self)
        self.photo = QGraphicsPixmapItem()
        self.scene.addItem(self.photo)
        self.setScene(self.scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            # TODO: Simplify to one url
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.setImage(links[0])
        else:
            event.ignore()

    def hasImage(self):
        return not self.empty

    def fitInView(self, scale=True):
        rect = QRectF(self.photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasImage():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(view_rect.width() / scene_rect.width(),
                             view_rect.height() / scene_rect.height())
                self.scale(factor, factor)
            self.current_zoom = 0

    def setImage(self, url):
        image = Image.open(url)
        pixmap = QPixmap(q2n.array2qimage(np.array(image)))

        if pixmap and not pixmap.isNull():
            self.empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.photo.setPixmap(pixmap)
        else:
            self.empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self.photo.setPixmap(QPixmap())

        if self.empty:
            self.fitInView()

        #self.setLoadedId.emit(str(url))

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.fitInView()

        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if self.hasImage():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.current_zoom += 1
            else:
                factor = 0.8
                self.current_zoom -= 1

            if self.current_zoom > 0:
                self.scale(factor, factor)
            elif self.current_zoom == 0:
                self.fitInView()
            else:
                self.current_zoom = 0
                self.fitInView()

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self.photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)
