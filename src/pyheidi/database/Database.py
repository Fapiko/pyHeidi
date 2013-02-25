from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QTreeWidgetItem
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem

class Database:
	"""
	@type name: str
	@type mainAppWindow: MainApplicationWindow
	@type tables: list
	@type databaseTreeItem: HeidiTreeWidgetItem
	@type server: DatabaseServer
	"""
	name = None
	maiAppnWindow = None
	tables = None
	databaseTreeItem = None
	server = None

	def __init__(self, server, mainAppWindow, name):
		"""
		@type server: DatabaseServer
		@type mainAppWindow: MainApplicationWindow
		@type databaseTreeItem: HeidiTreeWidgetItem
		@param name: str
		"""
		self.name = name
		self.mainAppWindow = mainAppWindow

		self.server = server

		database = HeidiTreeWidgetItem()
		database.setText(0, name)
		database.setIcon(0, QIcon('../resources/icons/database.png'))
		database.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
		database.itemType = 'database'
		database.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

		serverItem = server.databaseTreeItem
		serverItem.addChild(database)
		serverItem.setExpanded(True)

		self.databaseTreeItem = database


	def refreshTables(self):
		window = self.mainAppWindow.mainWindow
		database = self.databaseTreeItem
		cursor = self.server.execute("SHOW TABLE STATUS FROM `%s`" % self.name)

		# Clear old tables from the database tree view
		for index in reversed(range(database.childCount())):
			database.removeChild(database.child(index))
