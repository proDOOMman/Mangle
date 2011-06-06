# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dev/ui/options.ui'
#
# Created: Mon Jun  6 19:59:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogOptions(object):
    def setupUi(self, DialogOptions):
        DialogOptions.setObjectName(_fromUtf8("DialogOptions"))
        DialogOptions.resize(350, 350)
        self.verticalLayout = QtGui.QVBoxLayout(DialogOptions)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(DialogOptions)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditTitle = QtGui.QLineEdit(self.groupBox)
        self.lineEditTitle.setObjectName(_fromUtf8("lineEditTitle"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditTitle)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(DialogOptions)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBoxDevice = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxDevice.setObjectName(_fromUtf8("comboBoxDevice"))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxDevice)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.checkboxOverwrite = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxOverwrite.setObjectName(_fromUtf8("checkboxOverwrite"))
        self.verticalLayout_2.addWidget(self.checkboxOverwrite)
        self.checkboxOrient = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxOrient.setObjectName(_fromUtf8("checkboxOrient"))
        self.verticalLayout_2.addWidget(self.checkboxOrient)
        self.checkboxResize = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxResize.setObjectName(_fromUtf8("checkboxResize"))
        self.verticalLayout_2.addWidget(self.checkboxResize)
        self.checkboxQuantize = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxQuantize.setObjectName(_fromUtf8("checkboxQuantize"))
        self.verticalLayout_2.addWidget(self.checkboxQuantize)
        self.checkboxFrame = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxFrame.setObjectName(_fromUtf8("checkboxFrame"))
        self.verticalLayout_2.addWidget(self.checkboxFrame)
        self.checkboxSplit = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxSplit.setObjectName(_fromUtf8("checkboxSplit"))
        self.verticalLayout_2.addWidget(self.checkboxSplit)
        self.checkboxReverse = QtGui.QCheckBox(self.groupBox_2)
        self.checkboxReverse.setObjectName(_fromUtf8("checkboxReverse"))
        self.verticalLayout_2.addWidget(self.checkboxReverse)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(DialogOptions)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogOptions)

    def retranslateUi(self, DialogOptions):
        DialogOptions.setWindowTitle(QtGui.QApplication.translate("DialogOptions", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DialogOptions", "Book", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogOptions", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("DialogOptions", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogOptions", "Device", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDevice.setItemText(0, QtGui.QApplication.translate("DialogOptions", "Kindle 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDevice.setItemText(1, QtGui.QApplication.translate("DialogOptions", "Kindle 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDevice.setItemText(2, QtGui.QApplication.translate("DialogOptions", "Kindle 3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDevice.setItemText(3, QtGui.QApplication.translate("DialogOptions", "Kindle DX", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDevice.setItemText(4, QtGui.QApplication.translate("DialogOptions", "Kindle DXG", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxOverwrite.setText(QtGui.QApplication.translate("DialogOptions", "Overwrite existing files", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxOrient.setText(QtGui.QApplication.translate("DialogOptions", "Orient images to match aspect ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxResize.setText(QtGui.QApplication.translate("DialogOptions", "Resize images to center on screen", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxQuantize.setText(QtGui.QApplication.translate("DialogOptions", "Dither images to match device palette", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxFrame.setText(QtGui.QApplication.translate("DialogOptions", "Draw frame around images", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxSplit.setText(QtGui.QApplication.translate("DialogOptions", "Split images to match aspect ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.checkboxReverse.setText(QtGui.QApplication.translate("DialogOptions", "Reverse split order", None, QtGui.QApplication.UnicodeUTF8))

