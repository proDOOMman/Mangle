# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dev/ui/downloader.ui'
#
# Created: Fri Jun 17 17:40:59 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Downloader(object):
    def setupUi(self, Downloader):
        Downloader.setObjectName(_fromUtf8("Downloader"))
        Downloader.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Downloader)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pageProgressBar = QtGui.QProgressBar(Downloader)
        self.pageProgressBar.setProperty(_fromUtf8("value"), 0)
        self.pageProgressBar.setObjectName(_fromUtf8("pageProgressBar"))
        self.verticalLayout.addWidget(self.pageProgressBar)
        self.pageLabel = QtGui.QLabel(Downloader)
        self.pageLabel.setObjectName(_fromUtf8("pageLabel"))
        self.verticalLayout.addWidget(self.pageLabel)
        self.picProgressBar = QtGui.QProgressBar(Downloader)
        self.picProgressBar.setProperty(_fromUtf8("value"), 0)
        self.picProgressBar.setObjectName(_fromUtf8("picProgressBar"))
        self.verticalLayout.addWidget(self.picProgressBar)
        self.picLabel = QtGui.QLabel(Downloader)
        self.picLabel.setObjectName(_fromUtf8("picLabel"))
        self.verticalLayout.addWidget(self.picLabel)
        self.log = QtGui.QTextBrowser(Downloader)
        self.log.setObjectName(_fromUtf8("log"))
        self.verticalLayout.addWidget(self.log)

        self.retranslateUi(Downloader)
        QtCore.QMetaObject.connectSlotsByName(Downloader)

    def retranslateUi(self, Downloader):
        Downloader.setWindowTitle(QtGui.QApplication.translate("Downloader", "Downloading...", None, QtGui.QApplication.UnicodeUTF8))
        self.pageLabel.setText(QtGui.QApplication.translate("Downloader", "Downloading pages list...", None, QtGui.QApplication.UnicodeUTF8))
        self.picLabel.setText(QtGui.QApplication.translate("Downloader", "Downloading images list...", None, QtGui.QApplication.UnicodeUTF8))

