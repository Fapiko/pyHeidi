import MySQLdb
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QTreeWidgetItem
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
from database.Database import Database

class DatabaseServer:
	"""
	@type name: str
	@type connection: MySQLdb.Connection
	@type treeIndex: int
	@type applicationWindow: MainApplicationWindow
	@type databases: list
	@type databaseTreeItem: HeidiTreeWidgetItem
	"""
	name = ""
	connection = None
	treeIndex = -1
	statusWindow = None
	databases = []
	databaseTreeItem = None

	def __init__(self, name, connection, applicationWindow):
		"""
		@type name: str
		@type connection: MySQLdb.Connection
		@type applicationWindow: MainApplicationWindow
		"""
		self.name = name
		self.connection = connection
		self.applicationWindow = applicationWindow

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
		database = Database(self, self.applicationWindow, name)
		self.databases.append(database)
