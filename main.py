"""
Name    : main.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 19.07.2021 20:08
Desc    :
"""

import datetime
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ScatterView import ScatterView
import pandas as pd
from settings import *
from TableViewWindow import TableViewWindow

from utils import evaluateProvidedTable

class QCMainWindow(QMainWindow):

    evaluateProvidedTable = pyqtSignal(Path)

    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.initMenuBarLoadActions()
        self.previous_saveas_path = None

        with open('stylesheet.css', "r") as fh:
            self.setStyleSheet(fh.read())

        self.img_available = False

        self.window_width = 500
        self.window_height = 500

        geo = QGuiApplication.primaryScreen().geometry()
        print(geo.width(), geo.height())
        self.position = ( ( geo.width() - self.window_width ) // 2 ,(geo.height() - self.window_height) // 2)
        # self.setGeometry((geo.width() - self.window_width) // 2, (geo.height() - self.window_height ) //2, self.window_width, self.window_height)
        self.setGeometry(*self.position, self.window_width, self.window_height)
        self.show()

    def initMenuBarLoadActions(self):
        """
        Connects buttons from the menu bar related to loading files
        :return:
        """
        self.actionLoad_File.triggered.connect(self.loadFile)

    def initMenuBarSaveActions(self):
        """
        Connects buttons from the menu bar related to saving
        :return:
        """
        self.actionSave.triggered.connect(self.table.tableSaveEvent)
        self.actionSave.setEnabled(True)
        self.actionSave_As.triggered.connect(self.table.tableSaveAsEvent)
        self.actionSave_As.setEnabled(True)

    def initMenuBarAboutActions(self):
        self.actionHelp.triggered.connect(self.callAbout)

    def callAbout(self):
        text = f"""<h3>QCFlex was developed by ... </h3>
<br></br>
Source can be found on GitHub: <a href='https://github.com/neuroimaging-mug/QCFlex'>QCFlex on GitHub</a>"""

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("About QCFlex")
        # msg.setTextFormat(Qt.RichText)
        # msg.setText("text <a href='http://www.trolltech.com'>Trolltech</a>")
        msg.setText(text)
        msg.exec_()

    def initButtonConnections(self):
        """
        Conntects all buttons with the correct functionality
        :return:
        """
        self.passBtn.clicked.connect(self.clickedPassFail)
        self.passBtn.setShortcut(Qt.Key_Space)
        self.failBtn.clicked.connect(self.clickedPassFail)
        self.failBtn.setShortcut(Qt.Key_F)
        self.previousBtn.clicked.connect(self.table.getPreviousId)
        self.previousBtn.setShortcut(Qt.Key_Left)
        self.nextBtn.clicked.connect(self.table.getNextId)
        self.nextBtn.setShortcut(Qt.Key_Right)

        self.updateComment.clicked.connect(self.sendUpdate)

        self.table.data.clicked.connect(self.table.doubleClicked_table)

    def loadFile(self):
        """
        Load the selected table file selected by the use in the interactive file explorer
        :return:
        """
        dlg = QFileDialog()
        dlg.setNameFilters(["CSV files (*.csv)"])
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()

        if (len(filenames) == 0):
            print("nothing selected")
            return

        self.testFile(filenames[0])


    def updateTimeLabel(self):
        import json
        from shutil import copyfile
        appdata_path = Path("appdata")
        appdata_path.mkdir(parents=True, exist_ok=True)
        pfile = appdata_path / Path(".programdata.json")
        identifier = Path(self.table.table_filename).stem

        if pfile.exists():
            try:
                with open(pfile, "r") as rf:
                    contents = json.load(rf)
                if identifier in contents.keys():
                    data_loaded = contents[identifier]
                    if all(key in data_loaded for key in ("first_save", "last_save")):
                        self.labelTimeSpent.setText(data_loaded['total_time_spent'])
            except:
                print("Something went wrong when loading the appdata file!")


    def testFile(self, text=None):
        """
        Tests the loaded table file to contain the correct columns
        :param text:
        :return:
        """
        # if hasattr(self, 'table'): # TODO: LP:20210829 funktioniert das? Es blockiert das Laden irgend einer neuen Datei. Man muss schauen, ob der gleiche Dateipfad geladen wurde.
        #     # print("Table already loaded!") # TODO: LP:20210829: anstatt print msgboxes verwenden (sofern es das in python gibt)
        #     raise Warning("Table already loaded!")
        #     return

        if text == None:
            fpath = self.loadFilePath.text()
        else:
            print("Clicked Load!")
            fpath = text

        if evaluateProvidedTable(fpath):
            self.image_basepath = Path(fpath).parents[0]

            self.imageView.setLoadedId.connect(self.setLoadedId)

            if hasattr(self, 'table'):
                #
                self.table.deleteUI()
                self.table.close()
                del self.table
                self.table = TableViewWindow(fpath, self)
            else:
                self.table = TableViewWindow(fpath, self)

            self.initButtonConnections()

            self.table.updateCurrentImage.connect(self.updateCurrentImage)

            ## Load first image
            self.updateCurrentImage()

            self.table.show()

            self.initMenuBarSaveActions()

            self.updateTimeLabel()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            msg.setWindowTitle("Error loading table")
            msg.setText("An exception occured during loading the provided table file!")
            msg.exec_()

    def updateCurrentImage(self):
        """
        Update the currently displayed graph after an update by the backend
        :return:
        """
        self.current_data = self.table.getSelectedRowData()
        fpath = Path(self.current_data['imgpath'])
        if not fpath.is_absolute():
            fpath = self.image_basepath / fpath
        if os.path.isfile(fpath):
            self.img_available = True
            self.imageView.setImage(fpath)
        else:
            tmpdir = Path(tempfile.gettempdir())
            img_w, img_h = 600, 150
            image = Image.new("RGBA", (img_w, img_h), (255, 255, 255))
            draw = ImageDraw.Draw(image)
            # font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", fontsize)

            text = f"{fpath} was not found!"
            w, h = draw.textsize(text)

            draw.text(((img_w - w) // 2, (img_h - h) // 2), text, (255, 0, 0))
            # img_resized = image.resize((188, 45), Image.ANTIALIAS)

            tmp_image_path = tmpdir / Path(str(datetime.datetime.now().timestamp()) + '.png')
            image.save(tmp_image_path)

            self.imageView.setImage(tmp_image_path)
            
        if self.current_data['QC'] != 'nan':
            self.updateComment.setEnabled(True)
            else:
                self.updateComment.setEnabled(False)

            # Update stylesheet of buttons to represent previous selections
            self.passBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)
            self.failBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)

            if self.current_data['QC'] == 'PASS':
                self.passBtn.setStyleSheet(BTN_PASS_STYLESHEET)
            elif self.current_data['QC'] == 'FAIL':
                self.failBtn.setStyleSheet(BTN_FAIL_STYLESHEET)
            else:
                self.passBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)
                self.failBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)

        if self.current_data['comment'] != '':
            self.commentBoxEdit.document().setPlainText(self.current_data['comment'])


    def clickedPassFail(self, ):
        """
        Method than handles the interaction with the PASS and FAIL buttons
        :return:
        """
        status = self.sender().text()
        if status == 'PASS':
            self.failBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)
            self.passBtn.setStyleSheet(BTN_PASS_STYLESHEET)
        if status == 'FAIL':
            self.failBtn.setStyleSheet(BTN_FAIL_STYLESHEET)
            self.passBtn.setStyleSheet(BTN_DEFAULT_STYLESHEET)

        # Visualize selection for DELAY time before triggering
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.sendUpdate)
        self.timer.start(DELAY)

        self.previous_sender = self.sender()
        self.sendUpdate(self.sender)

    def sendUpdate(self, source=None):
        """
        Updated entry of the currently selected row in the table after user interaction
        :param source:
        :return:
        """
        try:
            status = self.sender().text()
        except AttributeError:
            status = self.previous_sender.text()

        evaluateProvidedTable = pyqtSignal(Path)

        if status not in ['PASS', 'FAIL']:
            # In case that just a comment update was sent
            status = self.current_data['QC']

        print(status)

        self.table.updateQCEntry(status, self.commentBoxEdit.toPlainText().lower())

    def getNextId(self):
        """
        Selects the next table row when called
        :return:
        """
        rows = sorted(set(index.row() for index in
                          self.table.data.selectedIndexes()))
        for row in rows:
            print('Row %d is selected' % row)

    def setLoadedId(self, id):
        """
        Updated the selected table row when clicked
        :param id:
        :return:
        """
        self.activeIdLabel.setText(id)





if __name__ == "__main__":
    app = QApplication([])
    main_window = QCMainWindow()
    main_window.show()
    sys.exit(app.exec_())
