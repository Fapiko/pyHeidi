from PyQt4.QtGui import QColor, QMainWindow, QResizeEvent
from ui.ui_mainwindow import Ui_MainWindow
from database.DatabaseServer import DatabaseServer
import re
from mysql_syntax_highlighter import MysqlSyntaxHighlighter

class MainApplicationWindow(QMainWindow):
	def __init__(self, configDb):
		self.obeyResize = False
		self.servers = []
		self.configDb = configDb

		QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)

		mainWindow.actionRefresh.activated.connect(self.actionRefresh)
		mainWindow.databaseTree.currentItemChanged.connect(self.updateDatabaseTreeSelection)
		mainWindow.databaseInfoTable.horizontalHeader().sectionResized.connect(self.databaseTreeColumnResized)
		mainWindow.databaseTree.itemExpanded.connect(self.databaseTreeItemExpanded)
		mainWindow.txtStatus.setTextColor(QColor('darkBlue'))

		self.logHighlighter = MysqlSyntaxHighlighter(mainWindow.txtStatus.document())

		self.mainWindow = mainWindow
		self.restoreSizePreferences()
		self.show()

	def addDbServer(self, server):
		"""
		@type server: DatabaseServer
		"""
		self.servers.append(server)
		server.reloadDatabases()
		server.refreshProcessList()

	def actionRefresh(self):
		# We'll eventually need to add logic to detect what page we're currently on
		self.servers[0].refreshProcessList()

	def updateDatabaseTreeSelection(self, currentItem, previousItem):
		"""
		@type currentItem: HeidiTreeWidgetItem
		@type previousItem: HeidiTreeWidgetItem
		"""
		if currentItem.itemType == 'database':
			self.updateCurrentDatabase(currentItem)
		elif currentItem.itemType == 'server':
			machineTab = self.mainWindow.machineTab
			twMachineTabs = self.mainWindow.twMachineTabs
			twMachineTabs.setTabText(twMachineTabs.indexOf(machineTab), "Host: %s" % currentItem.text(0))
			twMachineTabs.setCurrentWidget(self.mainWindow.machineTab)

	def updateCurrentDatabase(self, databaseTreeItem):
		"""
		@type databaseTreeItem: HeidiTreeWidgetItem
		"""
		dbName = databaseTreeItem.text(0)
		server = self.getServer(0)
		database = server.findDatabaseByName(dbName)
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
		dbInfoTableRegex = re.compile("^databaseinfotable\.[0-7]\.width")
		for row in cursor:
			if row['name'] == 'mainwindow.width':
				mainWindowWidth = int(row['value'])
			elif row['name'] == 'mainwindow.height':
				mainWindowHeight = int(row['value'])
			elif dbInfoTableRegex.match(row['name']):
				index = int(row['name'].split('.')[1])
				self.mainWindow.databaseInfoTable.setColumnWidth(index, int(row['value']))

		self.resize(mainWindowWidth, mainWindowHeight)
		self.obeyResize = True

	def databaseTreeItemExpanded(self, item):
		"""
		@type item: HeidiTreeWidgetItem
		"""
		if item.itemType == 'database':
			database = self.servers[0].findDatabaseByName(item.text(0))
			if len(database.tables) == 0:
				database.refreshTables()




