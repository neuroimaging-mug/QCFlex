# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QCMainWindow(object):
    def setupUi(self, QCMainWindow):
        QCMainWindow.setObjectName("QCMainWindow")
        QCMainWindow.resize(1000, 800)
        QCMainWindow.setStyleSheet("background: rgb(51, 51, 51); ")
        self.centralWidget = QtWidgets.QWidget(QCMainWindow)
        self.centralWidget.setMinimumSize(QtCore.QSize(1000, 0))
        self.centralWidget.setStyleSheet("font-color: rgb(255, 255, 255); ")
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rightColumn = QtWidgets.QVBoxLayout()
        self.rightColumn.setObjectName("rightColumn")
        self.activeIdLabel = QtWidgets.QLabel(self.centralWidget)
        self.activeIdLabel.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.activeIdLabel.setFont(font)
        self.activeIdLabel.setStyleSheet("color: white; ")
        self.activeIdLabel.setObjectName("activeIdLabel")
        self.rightColumn.addWidget(self.activeIdLabel)
        self.widget = QtWidgets.QWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setStyleSheet("background: rgb(41, 41, 41)")
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.imageView = QCImageViewer(self.widget)
        self.imageView.setObjectName("imageView")
        self.horizontalLayout_3.addWidget(self.imageView)
        self.rightColumn.addWidget(self.widget)
        self.controlls = QtWidgets.QGroupBox(self.centralWidget)
        self.controlls.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlls.sizePolicy().hasHeightForWidth())
        self.controlls.setSizePolicy(sizePolicy)
        self.controlls.setMinimumSize(QtCore.QSize(0, 0))
        self.controlls.setStyleSheet("color: white;")
        self.controlls.setObjectName("controlls")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.controlls)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ControllsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.ControllsHorizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.ControllsHorizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.ControllsHorizontalLayout.setSpacing(6)
        self.ControllsHorizontalLayout.setObjectName("ControllsHorizontalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.controlls)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(self.controlls)
        self.textEdit.setEnabled(False)
        self.textEdit.setMarkdown("** Shortcuts:**\n"
"\n"
"  Space Bar -> Pass\n"
"\n"
"  \"f\" -> Fail\n"
"\n"
"  Left/Right Arrows -> Next/Previous Image\n"
"\n"
"** The table must include following columns:**\n"
"  \"ID\"\n"
"\n"
"  \"QC\"\n"
"\n"
"  \"imgpath\" ->  relative image path (CONTAINING FOLDER FOR NOW)\n"
"\n"
"  \"comment\"\n"
"\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_5.addWidget(self.textEdit)
        self.ControllsHorizontalLayout.addLayout(self.horizontalLayout_5)
        self.passBtn = QtWidgets.QPushButton(self.controlls)
        self.passBtn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        self.passBtn.setFont(font)
        self.passBtn.setStyleSheet("color: white; \n"
"background:rgb(60, 63, 65);\n"
"")
        self.passBtn.setObjectName("passBtn")
        self.ControllsHorizontalLayout.addWidget(self.passBtn)
        self.failBtn = QtWidgets.QPushButton(self.controlls)
        self.failBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.failBtn.setStyleSheet("color: white; \n"
"background:rgb(60, 63, 65);\n"
"")
        self.failBtn.setObjectName("failBtn")
        self.ControllsHorizontalLayout.addWidget(self.failBtn)
        self.commentBoxLayout_2 = QtWidgets.QVBoxLayout()
        self.commentBoxLayout_2.setObjectName("commentBoxLayout_2")
        self.commentLabel = QtWidgets.QLabel(self.controlls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.commentLabel.setFont(font)
        self.commentLabel.setStyleSheet("color: white;")
        self.commentLabel.setObjectName("commentLabel")
        self.commentBoxLayout_2.addWidget(self.commentLabel)
        self.commentBoxEdit = QtWidgets.QPlainTextEdit(self.controlls)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.commentBoxEdit.setFont(font)
        self.commentBoxEdit.setStyleSheet("color: white;")
        self.commentBoxEdit.setObjectName("commentBoxEdit")
        self.commentBoxLayout_2.addWidget(self.commentBoxEdit)
        self.updateComment = QtWidgets.QPushButton(self.controlls)
        self.updateComment.setMinimumSize(QtCore.QSize(0, 30))
        self.updateComment.setStyleSheet("color: white; \n"
"background:rgb(60, 63, 65);\n"
"")
        self.updateComment.setObjectName("updateComment")
        self.commentBoxLayout_2.addWidget(self.updateComment)
        self.ControllsHorizontalLayout.addLayout(self.commentBoxLayout_2)
        self.previousBtn = QtWidgets.QPushButton(self.controlls)
        self.previousBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.previousBtn.setStyleSheet("color: white; \n"
"background:rgb(60, 63, 65);\n"
"")
        self.previousBtn.setObjectName("previousBtn")
        self.ControllsHorizontalLayout.addWidget(self.previousBtn)
        self.nextBtn = QtWidgets.QPushButton(self.controlls)
        self.nextBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.nextBtn.setStyleSheet("color: white; \n"
"background:rgb(60, 63, 65);\n"
"")
        self.nextBtn.setObjectName("nextBtn")
        self.ControllsHorizontalLayout.addWidget(self.nextBtn)
        self.horizontalLayout_2.addLayout(self.ControllsHorizontalLayout)
        self.rightColumn.addWidget(self.controlls)
        self.rightColumn.setStretch(0, 1)
        self.verticalLayout.addLayout(self.rightColumn)
        self.scatterPlots = QtWidgets.QHBoxLayout()
        self.scatterPlots.setObjectName("scatterPlots")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scatterPlots.addLayout(self.horizontalLayout)
        self.excelPathLabel = QtWidgets.QLabel(self.centralWidget)
        self.excelPathLabel.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.excelPathLabel.setFont(font)
        self.excelPathLabel.setStyleSheet("color: white;")
        self.excelPathLabel.setScaledContents(False)
        self.excelPathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.excelPathLabel.setObjectName("excelPathLabel")
        self.scatterPlots.addWidget(self.excelPathLabel)
        self.loadFilePath = QCLineEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadFilePath.sizePolicy().hasHeightForWidth())
        self.loadFilePath.setSizePolicy(sizePolicy)
        self.loadFilePath.setMinimumSize(QtCore.QSize(0, 30))
        self.loadFilePath.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loadFilePath.setFont(font)
        self.loadFilePath.setStyleSheet("color: white;")
        self.loadFilePath.setAlignment(QtCore.Qt.AlignCenter)
        self.loadFilePath.setObjectName("loadFilePath")
        self.scatterPlots.addWidget(self.loadFilePath)
        self.verticalLayout.addLayout(self.scatterPlots)
        QCMainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(QCMainWindow)
        QtCore.QMetaObject.connectSlotsByName(QCMainWindow)

    def retranslateUi(self, QCMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QCMainWindow.setWindowTitle(_translate("QCMainWindow", "QCMainWindow"))
        self.activeIdLabel.setText(_translate("QCMainWindow", "Currently loaded file"))
        self.controlls.setTitle(_translate("QCMainWindow", "Controlls"))
        self.textEdit.setHtml(_translate("QCMainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\"> Shortcuts:</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  Space Bar -&gt; Pass</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  &quot;f&quot; -&gt; Fail</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  Left/Right Arrows -&gt; Next/Previous Image</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\"> The table must include following columns:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  &quot;PatientID&quot;</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  &quot;QC&quot;</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  &quot;imgpath&quot; -&gt;  relative image path (CONTAINING FOLDER FOR NOW)</span></p>\n"
"<p style=\" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">  &quot;comment&quot;</span></p></body></html>"))
        self.passBtn.setText(_translate("QCMainWindow", "PASS"))
        self.failBtn.setText(_translate("QCMainWindow", "FAIL"))
        self.commentLabel.setText(_translate("QCMainWindow", "Comment:"))
        self.commentBoxEdit.setPlainText(_translate("QCMainWindow", "Enter your comments here!"))
        self.updateComment.setToolTip(_translate("QCMainWindow", "<html><head/><body><p>Only update the comment and keep the pre-existing choice of the QC</p></body></html>"))
        self.updateComment.setText(_translate("QCMainWindow", "Update Comment"))
        self.previousBtn.setText(_translate("QCMainWindow", "PREVIOUS"))
        self.nextBtn.setText(_translate("QCMainWindow", "NEXT"))
        self.excelPathLabel.setText(_translate("QCMainWindow", "Table File Path"))
        self.loadFilePath.setText(_translate("QCMainWindow", "Path to your .CSV file (either Drag File here or enter local file path)"))
from widgets.QCImageViewer import QCImageViewer
from widgets.QCLineEdit import QCLineEdit
