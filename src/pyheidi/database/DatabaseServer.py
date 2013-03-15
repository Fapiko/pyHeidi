import MySQLdb
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QTreeWidgetItem
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
from database.Database import Database

class DatabaseServer:
	def __init__(self, name, connection, applicationWindow):
		"""
		@type name: str
		@type connection: MySQLdb.Connection
		@type applicationWindow: MainApplicationWindow
		"""
		self.name = name
		self.connection = connection
		self.applicationWindow = applicationWindow
		self.databases = list()
		self.currentDatabase = None
		self.collations = list()

		serverItem = HeidiTreeWidgetItem()
		serverItem.setText(0, name)
		serverItem.setIcon(0, QIcon('../resources/icons/server.png'))
		serverItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
		serverItem.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
		serverItem.itemType = 'server'

		self.databaseTreeItem = serverItem

		applicationWindow.mainWindow.databaseTree.addTopLevelItem(serverItem)

	def execute(self, *args):
		"""
		@type query: str
		@type params: list
		"""
		cursor = self.connection.cursor()
		if len(args) == 1:
			cursor.execute(args[0])
		elif len(args) == 2:
			cursor.execute(args[0], args[1])

		statusWindow = self.applicationWindow.mainWindow.txtStatus
		statusWindow.append("%s;" % args[0])

		return cursor

	def getDatabase(self, index):
		"""
		@type index: int
		@rtype: Database
		"""
		return self.databases(index)

	def reloadDatabases(self):
		cursor = self.execute('SHOW DATABASES')
		for row in cursor:
			self.addDatabase(row['Database'])

	def addDatabase(self, name):
		"""
		@type server: DatabaseServer
		@type name: str
		"""
		database = Database(self, name)
		self.databases.append(database)

	def refreshProcessList(self):
		"""
		@type server: DatabaseServer
		"""
		processListTree = self.applicationWindow.mainWindow.processListTree
		processListTree.clear()

		cursor = self.execute('SHOW FULL PROCESSLIST')

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

		self.applicationWindow.mainWindow.processListTab.setTabText(0, "Process List (%d)" % numProcesses)

	def setCurrentDatabase(self, database):
		"""
		@type database: Database
		"""
		self.currentDatabase = database
		database.setAsCurrentDatabase()

	def findDatabaseByName(self, name):
		"""
		@type name: str
		@rtype: Database
		"""
		for database in self.databases:
			if database.name == name:
				return database

	def getCollations(self):
		"""
		@rtype: list
		"""
		if len(self.collations) == 0:
			cursor = self.execute("SHOW COLLATION")
			for collation in cursor:
				self.collations.append(collation)

		return self.collations
