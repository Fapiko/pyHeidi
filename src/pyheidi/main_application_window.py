from PyQt4.QtCore import Qt, QString
from PyQt4.QtGui import QIcon, QMainWindow, QResizeEvent, QTableWidgetItem, QTreeWidgetItem
from ui.ui_mainwindow import Ui_MainWindow
from database.DatabaseServer import DatabaseServer
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
from utilities.byte_sized_strings import byteSizedStrings
import re

class MainApplicationWindow(QMainWindow):
	"""
	@type configDb: sqlite3.Connection
	@type obeyResize: bool
	@type servers: list
	"""
	configDb = None
	servers = []
	obeyResize = False

	def __init__(self, configDb):
		self.configDb = configDb

		QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)

		mainWindow.actionRefresh.activated.connect(self.actionRefresh)
		mainWindow.databaseTree.currentItemChanged.connect(self.updateDatabaseTreeSelection)
		mainWindow.databaseInfoTable.horizontalHeader().sectionResized.connect(self.databaseTreeColumnResized)

		self.mainWindow = mainWindow
		self.restoreSizePreferences()
		self.show()



	def addDatabase(self, server, name):
		"""
		@type server: DatabaseServer
		@type name: str
		"""
		database = HeidiTreeWidgetItem()
		database.setText(0, name)
		database.setIcon(0, QIcon('../resources/icons/database.png'))
		database.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
		database.itemType = 'database'

		serverItem = self.mainWindow.databaseTree.topLevelItem(server.treeIndex)
		serverItem.addChild(database)
		serverItem.setExpanded(True)

	def addDbServer(self, server):
		"""
		@type server: DatabaseServer
		"""
		serverItem = HeidiTreeWidgetItem()
		serverItem.setText(0, server.name)
		serverItem.setIcon(0, QIcon('../resources/icons/server.png'))
		serverItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
		serverItem.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
		serverItem.itemType = 'server'

		self.mainWindow.databaseTree.addTopLevelItem(serverItem)
		server.treeIndex = self.mainWindow.databaseTree.indexOfTopLevelItem(serverItem)
		self.servers.append(server)

		self.reloadServerDatabases(server)
		self.refreshProcessList(server)

	def reloadServerDatabases(self, server):
		"""
		@type server: DatabaseServer
		"""
		cursor = server.connection.cursor()

		cursor.execute('SHOW DATABASES')
		for row in cursor:
			self.addDatabase(server, row['Database'])

	def refreshProcessList(self, server):
		"""
		@type server: DatabaseServer
		"""
		processListTree = self.mainWindow.processListTree
		processListTree.clear()

		cursor = server.connection.cursor()
		cursor.execute('SHOW FULL PROCESSLIST')

		numProcesses = 0
		for row in cursor:
			numProcesses += 1

			for value in row:
				if row[value] is None:
					row[value] = ''
				elif type(row[value] != str):
					row[value] = str(row[value])

			processItem = QTreeWidgetItem()
			processItem.setText(0, row['Id'])
			processItem.setText(1, row['User'])
			processItem.setText(2, row['Host'])
			processItem.setText(3, row['db'])
			processItem.setText(4, row['Command'])
			processItem.setText(5, row['Time'])
			processItem.setText(6, row['State'])
			processItem.setText(7, row['Info'])
			processListTree.addTopLevelItem(processItem)

		self.mainWindow.processListTab.setTabText(0, "Process List (%d)" % numProcesses)

	def actionRefresh(self):
		# We'll eventually need to add logic to detect what page we're currently on
		self.refreshProcessList(self.servers[0])

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

	def updateCurrentDatabase(self, database):
		"""
		@type database: HeidiTreeWidgetItem
		"""
		dbName = database.text(0)
		connection = self.getServer(0).connection
		cursor = connection.cursor()

		mainWindow = self.mainWindow
		databaseTab = mainWindow.databaseTab
		twMachineTabs = mainWindow.twMachineTabs
		twMachineTabs.setTabText(twMachineTabs.indexOf(databaseTab), "Database: %s" % dbName)
		twMachineTabs.setCurrentWidget(databaseTab)
		databaseTable = mainWindow.databaseInfoTable
		for i in reversed(range(databaseTable.rowCount())):
			databaseTable.removeRow(i)

		cursor.execute("SHOW TABLE STATUS FROM `%s`" % dbName)
		for row in cursor:
			if row['Create_time'] is None:
				createdTime = ''
			else:
				createdTime = row['Create_time'].isoformat(' ')

			if row['Update_time'] is None:
				updatedTime = ''
			else:
				updatedTime = row['Update_time'].isoformat(' ')

			index = databaseTable.rowCount()
			databaseTable.insertRow(index)
			databaseTable.setItem(index, 0, QTableWidgetItem(row['Name']))
			databaseTable.setItem(index, 1, QTableWidgetItem(str(row['Rows'])))
			databaseTable.setItem(index, 2, QTableWidgetItem(byteSizedStrings(row['Data_length'])))
			databaseTable.setItem(index, 3, QTableWidgetItem(createdTime))
			databaseTable.setItem(index, 4, QTableWidgetItem(updatedTime))
			databaseTable.setItem(index, 5, QTableWidgetItem(row['Engine']))
			databaseTable.setItem(index, 6, QTableWidgetItem(row['Comment']))
			databaseTable.setItem(index, 7, QTableWidgetItem('table'))

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
		# print "%d %d %d" % (index, width, previousWidth)
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


