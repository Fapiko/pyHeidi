from PyQt4.QtCore import Qt, QString
from PyQt4.QtGui import QIcon, QMainWindow, QResizeEvent, QTreeWidgetItem
from ui.ui_mainwindow import Ui_MainWindow
from database.DatabaseServer import DatabaseServer
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
import sqlite3

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
		mainWindow.databaseTree.currentItemChanged.connect(self.updateCurrentDatabase)

		self.mainWindow = mainWindow
		self.show()

		cursor = configDb.cursor()
		cursor.execute("SELECT * FROM settings WHERE name = 'mainwindow.width' OR name = 'mainwindow.height'")
		for row in cursor:
			if row['name'] == 'mainwindow.width':
				width = int(row['value'])
			elif row['name'] == 'mainwindow.height':
				height = int(row['value'])

		self.resize(width, height)
		self.obeyResize = True

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
			self.addDatabase(server, row[0])

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
			processItem = QTreeWidgetItem()
			for index, field in enumerate(row):
				if field is not None:
					if type(field) is not str:
						field = str(field)
					processItem.setText(index, field)

				processListTree.addTopLevelItem(processItem)

		self.mainWindow.processListTab.setTabText(0, "Process List (%d)" % numProcesses)

	def actionRefresh(self):
		# We'll eventually need to add logic to detect what page we're currently on
		self.refreshProcessList(self.servers[0])

	def updateCurrentDatabase(self, currentDatabase, previousDatabase):
		"""
		@type currentDatabase: QTreeWidgetItem
		@type previousDatabase: QTreeWidgetItem
		"""

	def resizeEvent(self, resizeEvent):
		"""
		@type resizeEvent: QResizeEvent
		"""
		if self.obeyResize:
			cursor = self.configDb.cursor()
			cursor.execute("UPDATE settings SET value = ? WHERE name = 'mainwindow.width'", [self.width()])
			cursor.execute("UPDATE settings SET value = ? WHERE name = 'mainwindow.height'", [self.height()])
			self.configDb.commit()
			print str(self.width()) + ' ' + str(self.height())


