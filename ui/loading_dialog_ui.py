# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_dialog_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_loadingWindow(object):
    def setupUi(self, loadingWindow):
        loadingWindow.setObjectName(_fromUtf8("loadingWindow"))
        loadingWindow.resize(409, 48)
        self.label = QtGui.QLabel(loadingWindow)
        self.label.setGeometry(QtCore.QRect(110, 20, 241, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(loadingWindow)
        QtCore.QMetaObject.connectSlotsByName(loadingWindow)

    def retranslateUi(self, loadingWindow):
        loadingWindow.setWindowTitle(_translate("loadingWindow", "Dialog", None))
        self.label.setText(_translate("loadingWindow", "Loading, Please Wait...", None))

