from PyQt4.QtCore import Qt, QModelIndex
from PyQt4.QtGui import QIcon, QMainWindow, QTreeWidgetItem
from ui.ui_mainwindow import Ui_MainWindow
from database.DatabaseServer import DatabaseServer

class MainApplicationWindow(QMainWindow):
	servers = []
	def __init__(self):
		QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)

#		mainWindow.databaseTree.setBaseSize()

		self.mainWindow = mainWindow
		self.show()

	def addDatabase(self, server, name):
		"""
		@type server: DatabaseServer
		@type name: str
		"""
		database = QTreeWidgetItem()
		database.setText(0, name)
		database.setIcon(0, QIcon('../resources/icons/database.png'))
		database.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)

		serverItem = self.mainWindow.databaseTree.topLevelItem(server.treeIndex)
		serverItem.addChild(database)
		serverItem.setExpanded(True)

	def addDbServer(self, server):
		"""
		@type server: DatabaseServer
		"""
		serverItem = QTreeWidgetItem()
		serverItem.setText(0, server.name)
		serverItem.setIcon(0, QIcon('../resources/icons/server.png'))
		serverItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)

		self.mainWindow.databaseTree.addTopLevelItem(serverItem)
		server.treeIndex = self.mainWindow.databaseTree.indexOfTopLevelItem(serverItem)
		self.servers.append(server)

		self.reloadServerDatabases(server)

	def reloadServerDatabases(self, server):
		"""
		@type server: DatabaseServer
		"""
		cursor = server.connection.cursor()

		cursor.execute('SHOW DATABASES')
		for row in cursor:
			self.addDatabase(server, row[0])





