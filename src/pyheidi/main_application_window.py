from PyQt4.QtCore import Qt, QByteArray, QPoint
from PyQt4.QtGui import QColor, QIcon, QMainWindow, QMenu, QResizeEvent
from ui.ui_mainwindow import Ui_MainWindow
from database.database_server import DatabaseServer
import re
from mysql_syntax_highlighter import MysqlSyntaxHighlighter
from ui.main_window.table_tab import TableTab
from ui.main_window.database_tab import DatabaseTab

class MainApplicationWindow(QMainWindow):
	def __init__(self, configDb):
		self.obeyResize = False
		self.servers = []
		self.configDb = configDb

		QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)

		databaseInfoTable = mainWindow.databaseInfoTable
		mainWindow.actionRefresh.activated.connect(self.actionRefresh)
		mainWindow.databaseTree.currentItemChanged.connect(self.updateDatabaseTreeSelection)
		databaseInfoTable.horizontalHeader().sectionResized.connect(self.databaseTreeColumnResized)
		mainWindow.databaseTree.itemExpanded.connect(self.databaseTreeItemExpanded)
		mainWindow.txtStatus.setTextColor(QColor('darkBlue'))
		mainWindow.twMachineTabs.removePage(mainWindow.databaseTab)
		mainWindow.twMachineTabs.removePage(mainWindow.tableTab)

		mainWindow.tableInfoTable.mainApplicationWindow = self

		# mainWindow.txtStatus.append("# Single Comment")
		# mainWindow.txtStatus.append("/* Multi\nLine Comment")
		# mainWindow.txtStatus.append("*/")
		# mainWindow.txtStatus.append("SHOW CREATE TABLE FOR `apiclarify`.`facepalm`;")
		# mainWindow.txtStatus.append("/* multi-line\n commentz */ SHOW CREATE TABLE FOR `apiclarify`.`facepalm`;")
		# mainWindow.txtStatus.append("/* comment */ SHOW CREATE TABLE FOR `apiclarify`.`facepalm`; /* commentz */")
		# mainWindow.txtStatus.append("/* comment SHOW CREATE TABLE FOR `apiclarify`.`facepalm`; commentz */")
		# mainWindow.txtStatus.append("/* comment \nSHOW CREATE TABLE FOR `apiclarify`.`facepalm`; commentz */")
		# mainWindow.txtStatus.append("SELECT * FROM test_command;")
		# mainWindow.txtStatus.append("SHOW TABLE STATUS; # Inline comment")
		# mainWindow.txtStatus.append("/* comment */ SHOW DATABASES; /* commentz */")
		# mainWindow.txtStatus.append("SHOW DATABASEN; /* start multiline")
		# mainWindow.txtStatus.append("commenting */")
		# mainWindow.txtStatus.append('SELECT * FROM facepalm; /* i can haz comment? */')

		self.logHighlighter = MysqlSyntaxHighlighter(mainWindow.txtStatus.document())

		self.mainWindow = mainWindow
		self.restoreSizePreferences()
		self.show()

		self.tableTab = TableTab(self)
		self.databaseTab = DatabaseTab(self)

		self.closeEvent = self.onClose

		databaseInfoTable.setContextMenuPolicy(Qt.CustomContextMenu)
		databaseInfoTable.customContextMenuRequested.connect(self.databaseContextMenu)

	def databaseContextMenu(self, point):
		"""
		@type point: QPoint
		"""
		databaseMenu = QMenu()
		databaseCreateMenu = databaseMenu.addMenu(QIcon('../resources/icons/application_form_add.png'), 'Create new')
		databaseCreateMenu.menuAction().setIconVisibleInMenu(True)
		databaseMenu.addMenu(databaseCreateMenu)

		createTableMenuItem = databaseCreateMenu.addAction(QIcon('../resources/icons/table.png'), 'Table')
		createTableMenuItem.setIconVisibleInMenu(True)
		createTableMenuItem.triggered.connect(self.tableTab.createTableAction)
		databaseMenu.exec_(self.mainWindow.databaseInfoTable.viewport().mapToGlobal(point))

	def addDbServer(self, server):
		"""
		@type server: DatabaseServer
		"""
		self.servers.append(server)
		self.currentServer = server
		server.reloadDatabases()
		server.refreshProcessList()

	def actionRefresh(self):
		# We'll eventually need to add logic to detect what page we're currently on
		self.currentServer.refreshProcessList()

	def updateDatabaseTreeSelection(self, currentItem, previousItem):
		"""
		@type currentItem: HeidiTreeWidgetItem
		@type previousItem: HeidiTreeWidgetItem
		"""
		if currentItem.itemType == 'database':
			self.updateCurrentDatabase(currentItem)
		elif currentItem.itemType == 'server':
			# Remove any tabs not dealing with server specific stuff
			mainWindow = self.mainWindow
			mainWindow.twMachineTabs.removePage(mainWindow.databaseTab)
			mainWindow.twMachineTabs.removePage(mainWindow.tableTab)

			# Initialize the machine tab
			machineTab = self.mainWindow.machineTab
			twMachineTabs = self.mainWindow.twMachineTabs
			twMachineTabs.setTabText(twMachineTabs.indexOf(machineTab), "Host: %s" % currentItem.text(0))
			twMachineTabs.setCurrentWidget(self.mainWindow.machineTab)
		elif currentItem.itemType == 'table':
			self.updateCurrentDatabase(currentItem.parent())
			self.showTableTab()
			tableName = currentItem.text(0)
			self.currentDatabase.setCurrentTable(self.currentDatabase.findTableByName(tableName))

	def updateCurrentDatabase(self, databaseTreeItem):
		"""
		@type databaseTreeItem: HeidiTreeWidgetItem
		"""
		dbName = databaseTreeItem.text(0)
		server = self.getServer(0)
		database = server.findDatabaseByName(dbName)
		self.currentDatabase = database
		server.setCurrentDatabase(database)

	def resizeEvent(self, resizeEvent):
		"""
		@type resizeEvent: QResizeEvent
		"""
		if self.obeyResize:
			cursor = self.configDb.cursor()
			cursor.execute("REPLACE INTO settings (name, value) VALUES ('mainwindow.width', ?)", [self.width()])
			cursor.execute("REPLACE INTO settings (name, value) VALUES ('mainwindow.height', ?)", [self.height()])
			self.configDb.commit()

	# Pretty much just using this getter for type hinting as PyCharm doesn't
	# seem to support inline hints afaik
	def getServer(self, index):
		"""
		@type index: int
		@rtype: DatabaseServer
		"""
		return self.servers[index]

	def databaseTreeColumnResized(self, index, previousWidth, width):
		# Last item auto stretches to take up the rest of the table
		if index != 7:
			cursor = self.configDb.cursor()
			cursor.execute("REPLACE INTO `settings` (name, value) VALUES ('databaseinfotable.%d.width', ?)" % index, [width])

	def restoreSizePreferences(self):
		cursor = self.configDb.cursor()
		cursor.execute("SELECT * FROM settings")

		mainWindowHeight = self.height()
		mainWindowWidth = self.width()
		mainWindowX = self.pos().x()
		mainWindowY = self.pos().y()
		splitter2Sizes = []
		dbInfoTableRegex = re.compile("^databaseinfotable\.[0-7]\.width")
		splitter2SizesRegex = re.compile("^splitter_2\.[0-7]")
		for row in cursor:
			if row['name'] == 'mainwindow.width':
				mainWindowWidth = int(row['value'])
			elif row['name'] == 'mainwindow.height':
				mainWindowHeight = int(row['value'])
			elif row['name'] == 'mainwindow.x':
				mainWindowX = int(row['value'])
			elif row['name'] == 'mainwindow.y':
				mainWindowY = int(row['value'])
			elif row['name'] == 'tableIndexes.columnWidth':
				self.mainWindow.indexes.setColumnWidth(0, int(row['value']))
			elif dbInfoTableRegex.match(row['name']):
				index = int(row['name'].split('.')[1])
				self.mainWindow.databaseInfoTable.setColumnWidth(index, int(row['value']))
			elif splitter2SizesRegex.match(row['name']):
				splitter2Sizes.append(int(row['value']))

		self.mainWindow.splitter_2.setSizes(splitter2Sizes)
		self.setGeometry(mainWindowX, mainWindowY, mainWindowWidth, mainWindowHeight)
		self.obeyResize = True

	def databaseTreeItemExpanded(self, item):
		"""
		@type item: HeidiTreeWidgetItem
		"""
		if item.itemType == 'database':
			database = self.currentServer.findDatabaseByName(item.text(0))
			if len(database.tables) == 0:
				database.refreshTables()

	def showDatabaseTab(self):
		self.showTab(self.mainWindow.databaseTab, QIcon('../resources/icons/database.png'), 'Database:')

	def showTableTab(self):
		self.showTab(self.mainWindow.tableTab, QIcon('../resources/icons/table.png'), 'Table:')

	def showTab(self, tab, name, icon):
		"""
		@type tab: QTabWidget
		@type icon: QIcon
		@type name: str
		"""
		self.mainWindow.twMachineTabs.addTab(tab, name, icon)

	def updateCurrentTable(self, tableName):
		"""
		@type tableTreeItem: HeidiTreeWidgetItem
		"""
		table = self.currentDatabase.findTableByName(tableName)
		table.setAsCurrentTable()

	def onClose(self, closeEvent):
		cursor = self.configDb.cursor()
		cursor.execute("REPLACE INTO `settings` (name, value) VALUES ('mainwindow.x', ?), ('mainwindow.y', ?)", [self.pos().x(), self.pos().y()])

		sizes = self.mainWindow.splitter_2.sizes()
		for i, size in enumerate(sizes):
			cursor.execute("REPLACE INTO `settings` (name, value) VALUES ('splitter_2.%d', ?)" % i, [size])

		indexSize = self.mainWindow.indexes.columnWidth(0)
		cursor.execute("REPLACE INTO `settings` (name, value) VALUES ('tableIndexes.columnWidth', ?)", [indexSize])

		self.configDb.commit()

		QMainWindow.closeEvent(self, closeEvent)
