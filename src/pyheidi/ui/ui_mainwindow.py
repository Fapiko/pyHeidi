# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Aug 26 22:41:31 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1218, 849)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setBaseSize(QtCore.QSize(200, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/heidi.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.databaseTree = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.databaseTree.sizePolicy().hasHeightForWidth())
        self.databaseTree.setSizePolicy(sizePolicy)
        self.databaseTree.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.databaseTree.setBaseSize(QtCore.QSize(350, 0))
        self.databaseTree.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.databaseTree.setRootIsDecorated(False)
        self.databaseTree.setUniformRowHeights(True)
        self.databaseTree.setHeaderHidden(True)
        self.databaseTree.setColumnCount(1)
        self.databaseTree.setObjectName(_fromUtf8("databaseTree"))
        self.databaseTree.headerItem().setText(0, _fromUtf8("1"))
        self.twMachineTabs = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twMachineTabs.sizePolicy().hasHeightForWidth())
        self.twMachineTabs.setSizePolicy(sizePolicy)
        self.twMachineTabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.twMachineTabs.setObjectName(_fromUtf8("twMachineTabs"))
        self.machineTab = QtGui.QWidget()
        self.machineTab.setObjectName(_fromUtf8("machineTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.machineTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.processListTab = QtGui.QTabWidget(self.machineTab)
        self.processListTab.setObjectName(_fromUtf8("processListTab"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.processListTree = QtGui.QTreeWidget(self.tab)
        self.processListTree.setObjectName(_fromUtf8("processListTree"))
        self.verticalLayout_4.addWidget(self.processListTree)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/resultset_next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.processListTab.addTab(self.tab, icon1, _fromUtf8(""))
        self.hostTabDB = QtGui.QWidget()
        self.hostTabDB.setObjectName(_fromUtf8("hostTabDB"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.hostTabDB)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tableWidget = QtGui.QTableWidget(self.hostTabDB)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/database.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.processListTab.addTab(self.hostTabDB, icon2, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.processListTab)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/computer.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.twMachineTabs.addTab(self.machineTab, icon3, _fromUtf8(""))
        self.databaseTab = QtGui.QWidget()
        self.databaseTab.setObjectName(_fromUtf8("databaseTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.databaseTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.databaseInfoTable = QtGui.QTableWidget(self.databaseTab)
        self.databaseInfoTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.databaseInfoTable.setAlternatingRowColors(False)
        self.databaseInfoTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.databaseInfoTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.databaseInfoTable.setCornerButtonEnabled(False)
        self.databaseInfoTable.setObjectName(_fromUtf8("databaseInfoTable"))
        self.databaseInfoTable.setColumnCount(8)
        self.databaseInfoTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.databaseInfoTable.setHorizontalHeaderItem(7, item)
        self.databaseInfoTable.horizontalHeader().setDefaultSectionSize(80)
        self.databaseInfoTable.horizontalHeader().setHighlightSections(False)
        self.databaseInfoTable.horizontalHeader().setMinimumSectionSize(50)
        self.databaseInfoTable.horizontalHeader().setStretchLastSection(True)
        self.databaseInfoTable.verticalHeader().setVisible(False)
        self.databaseInfoTable.verticalHeader().setDefaultSectionSize(20)
        self.databaseInfoTable.verticalHeader().setMinimumSectionSize(15)
        self.horizontalLayout.addWidget(self.databaseInfoTable)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/database.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.twMachineTabs.addTab(self.databaseTab, icon4, _fromUtf8(""))
        self.tableTab = QtGui.QWidget()
        self.tableTab.setObjectName(_fromUtf8("tableTab"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tableTab)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.splitter_3 = QtGui.QSplitter(self.tableTab)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.tableTabs = QtGui.QTabWidget(self.splitter_3)
        self.tableTabs.setStyleSheet(_fromUtf8("QPushButton {\n"
"    padding: 0px;\n"
"}"))
        self.tableTabs.setObjectName(_fromUtf8("tableTabs"))
        self.tableTabsBasic = QtGui.QWidget()
        self.tableTabsBasic.setObjectName(_fromUtf8("tableTabsBasic"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.tableTabsBasic)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.tableTabsBasic)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.tableName = QtGui.QLineEdit(self.tableTabsBasic)
        self.tableName.setObjectName(_fromUtf8("tableName"))
        self.gridLayout_3.addWidget(self.tableName, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tableTabsBasic)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.tableComment = QtGui.QPlainTextEdit(self.tableTabsBasic)
        self.tableComment.setObjectName(_fromUtf8("tableComment"))
        self.gridLayout_3.addWidget(self.tableComment, 1, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_3)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/table.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tableTabs.addTab(self.tableTabsBasic, icon5, _fromUtf8(""))
        self.tableTabsOptions = QtGui.QWidget()
        self.tableTabsOptions.setObjectName(_fromUtf8("tableTabsOptions"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tableTabsOptions)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.tableTabsOptions)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.tableOptionsAutoIncrement = QtGui.QLineEdit(self.tableTabsOptions)
        self.tableOptionsAutoIncrement.setObjectName(_fromUtf8("tableOptionsAutoIncrement"))
        self.gridLayout.addWidget(self.tableOptionsAutoIncrement, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tableTabsOptions)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.tableOptionsDefaultCollation = QtGui.QComboBox(self.tableTabsOptions)
        self.tableOptionsDefaultCollation.setObjectName(_fromUtf8("tableOptionsDefaultCollation"))
        self.gridLayout.addWidget(self.tableOptionsDefaultCollation, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/wrench.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tableTabs.addTab(self.tableTabsOptions, icon6, _fromUtf8(""))
        self.tableTabsIndexes = QtGui.QWidget()
        self.tableTabsIndexes.setObjectName(_fromUtf8("tableTabsIndexes"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tableTabsIndexes)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.addColumnButton_2 = QtGui.QPushButton(self.tableTabsIndexes)
        self.addColumnButton_2.setStyleSheet(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addColumnButton_2.setIcon(icon7)
        self.addColumnButton_2.setFlat(True)
        self.addColumnButton_2.setObjectName(_fromUtf8("addColumnButton_2"))
        self.verticalLayout_7.addWidget(self.addColumnButton_2)
        self.removeColumnButton_2 = QtGui.QPushButton(self.tableTabsIndexes)
        self.removeColumnButton_2.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeColumnButton_2.setIcon(icon8)
        self.removeColumnButton_2.setFlat(True)
        self.removeColumnButton_2.setObjectName(_fromUtf8("removeColumnButton_2"))
        self.verticalLayout_7.addWidget(self.removeColumnButton_2)
        self.pushButton = QtGui.QPushButton(self.tableTabsIndexes)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/cross.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon9)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_7.addWidget(self.pushButton)
        self.moveColumnUpButton_2 = QtGui.QPushButton(self.tableTabsIndexes)
        self.moveColumnUpButton_2.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/resultset_up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moveColumnUpButton_2.setIcon(icon10)
        self.moveColumnUpButton_2.setFlat(True)
        self.moveColumnUpButton_2.setObjectName(_fromUtf8("moveColumnUpButton_2"))
        self.verticalLayout_7.addWidget(self.moveColumnUpButton_2)
        self.moveColumnDownButton_2 = QtGui.QPushButton(self.tableTabsIndexes)
        self.moveColumnDownButton_2.setEnabled(False)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/resultset_down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moveColumnDownButton_2.setIcon(icon11)
        self.moveColumnDownButton_2.setFlat(True)
        self.moveColumnDownButton_2.setObjectName(_fromUtf8("moveColumnDownButton_2"))
        self.verticalLayout_7.addWidget(self.moveColumnDownButton_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.treeWidget = QtGui.QTreeWidget(self.tableTabsIndexes)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("Name"))
        self.horizontalLayout_3.addWidget(self.treeWidget)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/lightning.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tableTabs.addTab(self.tableTabsIndexes, icon12, _fromUtf8(""))
        self.layoutWidget = QtGui.QWidget(self.splitter_3)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_8.setMargin(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self._2 = QtGui.QHBoxLayout()
        self._2.setObjectName(_fromUtf8("_2"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self._2.addWidget(self.label)
        self.addColumnButton = QtGui.QPushButton(self.layoutWidget)
        self.addColumnButton.setIcon(icon7)
        self.addColumnButton.setFlat(True)
        self.addColumnButton.setObjectName(_fromUtf8("addColumnButton"))
        self._2.addWidget(self.addColumnButton)
        self.removeColumnButton = QtGui.QPushButton(self.layoutWidget)
        self.removeColumnButton.setEnabled(False)
        self.removeColumnButton.setIcon(icon8)
        self.removeColumnButton.setFlat(True)
        self.removeColumnButton.setObjectName(_fromUtf8("removeColumnButton"))
        self._2.addWidget(self.removeColumnButton)
        self.moveColumnUpButton = QtGui.QPushButton(self.layoutWidget)
        self.moveColumnUpButton.setEnabled(False)
        self.moveColumnUpButton.setIcon(icon10)
        self.moveColumnUpButton.setFlat(True)
        self.moveColumnUpButton.setObjectName(_fromUtf8("moveColumnUpButton"))
        self._2.addWidget(self.moveColumnUpButton)
        self.moveColumnDownButton = QtGui.QPushButton(self.layoutWidget)
        self.moveColumnDownButton.setEnabled(False)
        self.moveColumnDownButton.setIcon(icon11)
        self.moveColumnDownButton.setFlat(True)
        self.moveColumnDownButton.setObjectName(_fromUtf8("moveColumnDownButton"))
        self._2.addWidget(self.moveColumnDownButton)
        spacerItem2 = QtGui.QSpacerItem(13, 13, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem2)
        self.verticalLayout_8.addLayout(self._2)
        self.tableInfoTable = DatabaseTableInfo(self.layoutWidget)
        self.tableInfoTable.setStyleSheet(_fromUtf8("QTableWidget::item {\n"
"    padding: 0px;\n"
"}"))
        self.tableInfoTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableInfoTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableInfoTable.setObjectName(_fromUtf8("tableInfoTable"))
        self.tableInfoTable.setColumnCount(12)
        self.tableInfoTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tableInfoTable.setHorizontalHeaderItem(11, item)
        self.tableInfoTable.verticalHeader().setVisible(False)
        self.verticalLayout_8.addWidget(self.tableInfoTable)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.discardTableButton = QtGui.QPushButton(self.layoutWidget)
        self.discardTableButton.setEnabled(False)
        self.discardTableButton.setObjectName(_fromUtf8("discardTableButton"))
        self.horizontalLayout_2.addWidget(self.discardTableButton)
        self.saveTableButton = QtGui.QPushButton(self.layoutWidget)
        self.saveTableButton.setEnabled(False)
        self.saveTableButton.setObjectName(_fromUtf8("saveTableButton"))
        self.horizontalLayout_2.addWidget(self.saveTableButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addWidget(self.splitter_3)
        self.twMachineTabs.addTab(self.tableTab, icon5, _fromUtf8(""))
        self.txtStatus = QtGui.QTextEdit(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtStatus.sizePolicy().hasHeightForWidth())
        self.txtStatus.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtStatus.setFont(font)
        self.txtStatus.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.txtStatus.setObjectName(_fromUtf8("txtStatus"))
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1218, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSession_Manager = QtGui.QAction(MainWindow)
        self.actionSession_Manager.setObjectName(_fromUtf8("actionSession_Manager"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionRefresh = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/arrow_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon13)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.menuFile.addAction(self.actionSession_Manager)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi(MainWindow)
        self.twMachineTabs.setCurrentIndex(2)
        self.processListTab.setCurrentIndex(0)
        self.tableTabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "pyHeidi", None))
        self.processListTree.setSortingEnabled(True)
        self.processListTree.headerItem().setText(0, _translate("MainWindow", "id", None))
        self.processListTree.headerItem().setText(1, _translate("MainWindow", "User", None))
        self.processListTree.headerItem().setText(2, _translate("MainWindow", "Host", None))
        self.processListTree.headerItem().setText(3, _translate("MainWindow", "DB", None))
        self.processListTree.headerItem().setText(4, _translate("MainWindow", "Command", None))
        self.processListTree.headerItem().setText(5, _translate("MainWindow", "Time", None))
        self.processListTree.headerItem().setText(6, _translate("MainWindow", "State", None))
        self.processListTree.headerItem().setText(7, _translate("MainWindow", "Info", None))
        self.processListTab.setTabText(self.processListTab.indexOf(self.tab), _translate("MainWindow", "Processes", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Database", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Size", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Items", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Last Modification", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Tables", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Views", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Functions", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Procedures", None))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Triggers", None))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Events", None))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Default Collation", None))
        self.processListTab.setTabText(self.processListTab.indexOf(self.hostTabDB), _translate("MainWindow", "Databases (0)", None))
        self.twMachineTabs.setTabText(self.twMachineTabs.indexOf(self.machineTab), _translate("MainWindow", "Host: ", None))
        self.databaseInfoTable.setSortingEnabled(True)
        item = self.databaseInfoTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name", None))
        item = self.databaseInfoTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Rows", None))
        item = self.databaseInfoTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Size", None))
        item = self.databaseInfoTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Created", None))
        item = self.databaseInfoTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Updated", None))
        item = self.databaseInfoTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Engine", None))
        item = self.databaseInfoTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Comment", None))
        item = self.databaseInfoTable.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Type", None))
        self.twMachineTabs.setTabText(self.twMachineTabs.indexOf(self.databaseTab), _translate("MainWindow", "Database: ", None))
        self.label_2.setText(_translate("MainWindow", "Name:", None))
        self.tableName.setPlaceholderText(_translate("MainWindow", "Enter table name", None))
        self.label_3.setText(_translate("MainWindow", "Comment:", None))
        self.tableTabs.setTabText(self.tableTabs.indexOf(self.tableTabsBasic), _translate("MainWindow", "Basic", None))
        self.label_4.setText(_translate("MainWindow", "Auto increment:", None))
        self.label_5.setText(_translate("MainWindow", "Default collation:", None))
        self.tableTabs.setTabText(self.tableTabs.indexOf(self.tableTabsOptions), _translate("MainWindow", "Options", None))
        self.addColumnButton_2.setText(_translate("MainWindow", "Add Column", None))
        self.removeColumnButton_2.setText(_translate("MainWindow", "Remove Column", None))
        self.pushButton.setText(_translate("MainWindow", "Clear", None))
        self.moveColumnUpButton_2.setText(_translate("MainWindow", "Up", None))
        self.moveColumnDownButton_2.setText(_translate("MainWindow", "Down", None))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Type / Length", None))
        self.tableTabs.setTabText(self.tableTabs.indexOf(self.tableTabsIndexes), _translate("MainWindow", "Indexes", None))
        self.label.setText(_translate("MainWindow", "Columns:", None))
        self.addColumnButton.setText(_translate("MainWindow", "Add Column", None))
        self.removeColumnButton.setText(_translate("MainWindow", "Remove Column", None))
        self.moveColumnUpButton.setText(_translate("MainWindow", "Up", None))
        self.moveColumnDownButton.setText(_translate("MainWindow", "Down", None))
        item = self.tableInfoTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "#", None))
        item = self.tableInfoTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name", None))
        item = self.tableInfoTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Datatype", None))
        item = self.tableInfoTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Length/Set", None))
        item = self.tableInfoTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Unsigned", None))
        item = self.tableInfoTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Allow NULL", None))
        item = self.tableInfoTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Zerofill", None))
        item = self.tableInfoTable.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Default", None))
        item = self.tableInfoTable.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Comment", None))
        item = self.tableInfoTable.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Collation", None))
        item = self.tableInfoTable.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Expression", None))
        item = self.tableInfoTable.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "Virtuality", None))
        self.discardTableButton.setText(_translate("MainWindow", "Discard", None))
        self.saveTableButton.setText(_translate("MainWindow", "Save", None))
        self.twMachineTabs.setTabText(self.twMachineTabs.indexOf(self.tableTab), _translate("MainWindow", "Table: ", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionSession_Manager.setText(_translate("MainWindow", "Session Manager", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh", None))
        self.actionRefresh.setShortcut(_translate("MainWindow", "F5", None))

from database_table_info import DatabaseTableInfo
import resources_rc
