# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtexteditlinenumber.ui'
#
# Created: Mon Mar 12 23:33:52 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QTextEditLineNumber(object):
    def setupUi(self, QTextEditLineNumber):
        QTextEditLineNumber.setObjectName(_fromUtf8("QTextEditLineNumber"))
        QTextEditLineNumber.resize(648, 340)
        self.horizontalLayout = QtGui.QHBoxLayout(QTextEditLineNumber)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineNumberArea = QtGui.QWidget(QTextEditLineNumber)
        self.lineNumberArea.setObjectName(_fromUtf8("lineNumberArea"))
        self.horizontalLayout.addWidget(self.lineNumberArea)
        self.textArea = QtGui.QTextEdit(QTextEditLineNumber)
        self.textArea.setObjectName(_fromUtf8("textArea"))
        self.horizontalLayout.addWidget(self.textArea)
        self.scrollBar = QtGui.QScrollBar(QTextEditLineNumber)
        self.scrollBar.setOrientation(QtCore.Qt.Vertical)
        self.scrollBar.setObjectName(_fromUtf8("scrollBar"))
        self.horizontalLayout.addWidget(self.scrollBar)

        self.retranslateUi(QTextEditLineNumber)
        QtCore.QMetaObject.connectSlotsByName(QTextEditLineNumber)

    def retranslateUi(self, QTextEditLineNumber):
        QTextEditLineNumber.setWindowTitle(QtGui.QApplication.translate("QTextEditLineNumber", "Form", None, QtGui.QApplication.UnicodeUTF8))

