import datetime
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from widgets.MplWidget import MplCanvas
from widgets.QCPandasTableWidget import *
from widgets.QCTableViewWidget import QCTableView

QC_STATUS_FAIL = 0
QC_STATUS_PASS = 1
BTN_DEFAULT_STYLESHEET = "color: white; background:rgb(60, 63, 65);"
BTN_PASS_STYLESHEET = "color: black; background-color: green;"
BTN_FAIL_STYLESHEET = "color: white; background-color: red;"
DELAY = 100  # msec to wait after pass/fail was clicked


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

        self.show()

    def initMenuBarLoadActions(self):
        self.actionLoad_File.triggered.connect(self.loadFile)

    def initMenuBarSaveActions(self):
        self.actionSave.triggered.connect(self.table.tableSaveEvent)
        self.actionSave.setEnabled(True)
        self.actionSave_As.triggered.connect(self.table.tableSaveAsEvent)
        self.actionSave_As.setEnabled(True)

    def loadFile(self):
        dlg = QFileDialog()
        dlg.setNameFilters(["CSV files (*.csv)"])
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()

        self.testFile(filenames[0])

    def testFile(self, text=None):
        if hasattr(self, 'table'):
            print("Table already loaded!")
            return

        if text == None:
            fpath = self.loadFilePath.text()
        else:
            print("Clicked Load!")
            fpath = text

        if TableViewWindow.evaluateProvidedTable(fpath):
            self.image_basepath = Path(fpath).parents[0]

            self.imageView.setLoadedId.connect(self.setLoadedId)

            self.table = TableViewWindow(fpath, self)
            self.initButtonConnections()

            self.table.updateCurrentImage.connect(self.updateCurrentImage)

            ## Load first image
            self.updateCurrentImage()

            self.table.show()

            self.initMenuBarSaveActions()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            msg.setWindowTitle("Error loading table")
            msg.setText("An exception occured during loading the provided table file!")
            msg.exec_()

    def updateCurrentImage(self):
        self.current_data = self.table.getSelectedRowData()
        fpath = Path(self.current_data['imgpath'])
        if not fpath.is_absolute():
            fpath = self.image_basepath / fpath
        if os.path.isfile(fpath):
            self.img_available = True
            self.imageView.setImage(fpath)

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

            if self.current_data['comment'] != '':
                self.commentBoxEdit.document().setPlainText(self.current_data['comment'])
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

    def initButtonConnections(self):
        self.passBtn.clicked.connect(self.clickedPassFail)
        self.passBtn.setShortcut(Qt.Key_Space)
        self.failBtn.clicked.connect(self.clickedPassFail)
        self.failBtn.setShortcut(Qt.Key_F)
        self.previousBtn.clicked.connect(self.table.getPreviousId)
        self.previousBtn.setShortcut(Qt.Key_Left)
        self.nextBtn.clicked.connect(self.table.getNextId)
        self.nextBtn.setShortcut(Qt.Key_Right)

        self.updateComment.clicked.connect(self.sendUpdate)

        self.table.data.doubleClicked.connect(self.table.doubleClicked_table)

    def clickedPassFail(self, ):
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

    def sendUpdate(self, source=None):
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
        rows = sorted(set(index.row() for index in
                          self.table.data.selectedIndexes()))
        for row in rows:
            print('Row %d is selected' % row)

    def setLoadedId(self, id):
        self.activeIdLabel.setText(id)


class ScatterView(QMainWindow):
    sendIndexClickedOn = pyqtSignal(int)
    receiveCurrentIndex = pyqtSignal(int)

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle("application main window")
        self.parent = parent

        cw = QWidget()

        layout = QVBoxLayout()
        cw.setLayout(layout)

        def loadTableFile(fname: Path):
            try:
                filepath = fname
                df = pd.read_csv(filepath, sep=';', decimal=',')
                new_header = df.iloc[0]
                df.colums = new_header
                return df

            except ValueError:
                return None

        self.df = loadTableFile(self.parent.table_filename)

        self.c1 = MplCanvas(self, width=5, height=4, dpi=100)
        self.c1.transmit_data_index.connect(self.onForwardDataClickedOn)

        layout.addWidget(self.c1)

        navi_toolbar = NavigationToolbar(self.c1, self)
        layout.addWidget(navi_toolbar)

        self.valid_colums = self.evaluateValidColumns(self.df)

        self.xdata_box = QComboBox()
        self.xdata_box.addItems(list(self.valid_colums))
        layout.addWidget(self.xdata_box)

        self.ydata_box = QComboBox()
        self.ydata_box.addItems(list(self.valid_colums))
        layout.addWidget(self.ydata_box)

        self.xdata_box.currentTextChanged.connect(self.updatePlotDataX)
        self.ydata_box.currentTextChanged.connect(self.updatePlotDataY)

        self.xdata_box.setCurrentIndex(1)
        self.ydata_box.setCurrentIndex(1)

        self.setCentralWidget(cw)

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

    def updatePlotDataX(self, new_column_name):
        print("Init update of X-Axis!")

        xlabel = new_column_name
        ylabel = self.ydata_box.currentText()

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabel].values

        self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabel)

    def updatePlotDataY(self, new_column_name):
        print("Init update of Y-Axis!")

        xlabel=self.xdata_box.currentText()
        ylabel=new_column_name

        x_sel = self.df[xlabel].values
        y_sel = self.df[ylabel].values

        self.c1.updatePlot(x_sel, y_sel, self.parent.current_index, xlabel=xlabel, ylabel=ylabel)

    def updatePlotData(self):
        self.c1.refreshPlot(self.parent.current_index)

    def setCurrentIndex(self, current_index):
        self.current_index = current_index

    def setData(self, xdata, ydata):
        pass


class TableViewWindow(QMainWindow):
    updateCurrentImage = pyqtSignal(bool)

    def __init__(self, table_path, parent=None):
        super(TableViewWindow, self).__init__(parent)
        self.main_window = parent
        self.table_filename = table_path
        self.image_basepath = Path(table_path).absolute().parents[0]
        self.resize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.current_index = 0

        self.setupUi(self)

        self.scatter = ScatterView(self)
        self.scatter.show()
        self.scatter.sendIndexClickedOn.connect(self.doubleClicked_table)

    @staticmethod
    def evaluateProvidedTable(fname):
        out = TableViewWindow.loadTableFile(fname)
        if isinstance(out, pd.DataFrame):
            print("Building Table Window!")
            return True
        else:
            return False

    def getNextId(self):
        if (self.current_index + 1) < len(self.df):
            self.current_index += 1
            self.getCurrentId()
            self.updateCurrentImage.emit(True)
            self.scatter.updatePlotData()

    def getPreviousId(self):
        self.current_index -= 1
        if self.current_index >= 0:
            self.getCurrentId()
            self.updateCurrentImage.emit(True)
            self.scatter.updatePlotData()
        else:
            self.current_index += 1

    def getCurrentId(self):
        self.data.selectRow(self.current_index)
        print(self.current_index)

    def doubleClicked_table(self, index):
        if type(index) == int:
            row_index = index
        else:
            row_index = index.row()
        self.current_index = row_index
        self.updateCurrentImage.emit(True)
        self.data.selectRow(self.current_index)

        self.scatter.updatePlotData()

        print(f"Selected row: {row_index}")

    # TODO remove redundant function!
    def loadTableFile(fname: Path):
        try:
            filepath = fname
            df = pd.read_csv(filepath, sep=';', decimal='.')
            new_header = df.iloc[0]
            df.colums = new_header
            return df

        except ValueError:
            return None

    def setupUi(self, test):
        test.setObjectName("test")
        test.resize(800, 600)
        self.centralwidget = QWidget(test)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.data = QCTableView(self.centralwidget)
        self.data.setObjectName("tableView")
        self.data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Define Background of current row, even if window is out of focus
        palette = QPalette()
        palette.setColor(QPalette.Inactive, QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
        palette.setColor(QPalette.Inactive, QPalette.HighlightedText, Qt.white)
        self.data.setPalette(palette)

        self.df = TableViewWindow.loadTableFile(self.table_filename)

        self.model = PandasTableModel(self.df)
        self.data.setModel(self.model)
        self.data.selectRow(self.current_index)

        self.horizontalLayout.addWidget(self.data)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        test.setCentralWidget(self.centralwidget)

    def getSelectedRowData(self):
        sel_rows = self.data.selectionModel().selectedRows()[0]

        model = self.data.model()

        headers = model.getHeaders()
        data_array = dict()

        for key in ['PatientID', 'imgpath', 'QC', 'comment']:
            path_idx = list(headers).index(key)
            model_idx = model.index(sel_rows.row(), path_idx)
            selected_data = model.data(model_idx)
            data_array[key] = selected_data

        return data_array

    def updateQCEntry(self, status, comment=''):
        # get selected row!
        sel_row = self.data.selectionModel().selectedRows()[0]
        row_idx = sel_row.row()
        model = self.data.model()

        headers = model.getHeaders()

        qc_column = list(headers).index('QC')

        self.df.iloc[row_idx, qc_column] = status

        # Update comments field
        comment_column = list(headers).index('comment')
        self.df.iloc[row_idx, comment_column] = comment

        if self.main_window.autoContinueCheckbox.isChecked():
            self.getNextId()
        else:
            self.getSelectedRowData()
            self.updateCurrentImage.emit(True)

        self.saveTable()

    def tableSaveExceptionMessageBox(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Error saving table")
        msg.setText(error.args[1])
        msg.exec_()

    def tableSaveEvent(self):
        try:
            if self.main_window.previous_saveas_path is None:
                self.tableSaveAsEvent()
            else:
                self.saveTable(self.main_window.previous_saveas_path)
        except PermissionError as e:
            self.tableSaveExceptionMessageBox(e)

    def tableSaveAsEvent(self):
        name = QFileDialog.getSaveFileName(self, 'SaveFile', filter="CSV files (*.csv)")
        try:
            self.saveTable(name[0])
            self.main_window.previous_saveas_path = name[0]
        except PermissionError as e:
            self.tableSaveExceptionMessageBox(e)

    def saveTable(self, name='Test.csv'):
        self.df.to_csv(name, index_label=None, sep=';')


if __name__ == "__main__":
    app = QApplication([])
    main_window = QCMainWindow()
    main_window.show()
    sys.exit(app.exec_())
