from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QTableWidgetItem, QTreeWidgetItem
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
from utilities.byte_sized_strings import byteSizedStrings
from database.Table import Table

class Database:
	def __init__(self, server, name):
		"""
		@type server: DatabaseServer
		@type applicationWindow: MainApplicationWindow
		@type databaseTreeItem: HeidiTreeWidgetItem
		"""
		self.name = name
		self.applicationWindow = server.applicationWindow
		self.server = server
		self.tables = []

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
		database = self.databaseTreeItem

		# Clear old tables from the database tree view
		for index in reversed(range(database.childCount())):
			database.removeChild(database.child(index))

		cursor = self.server.execute("SHOW TABLE STATUS FROM `%s`" % self.name)
		for row in cursor:
			Table(row['Name'], self, rows = row['Rows'],
					size = row['Data_length'], created = row['Create_time'],
					updated = row['Update_time'], engine = row['Engine'],
					comment = row['Comment'])

	def getDatabaseTreeItem(self):
		"""
		@rtype: HeidiTreeWidgetItem
		"""
		return self.databaseTreeItem


	def setAsCurrentDatabase(self):
		if len(self.tables) == 0:
			self.refreshTables()

		mainWindow = self.applicationWindow.mainWindow
		databaseTab = mainWindow.databaseTab
		twMachineTabs = mainWindow.twMachineTabs
		twMachineTabs.setTabText(twMachineTabs.indexOf(databaseTab), "Database: %s" % self.name)
		twMachineTabs.setCurrentWidget(databaseTab)

		databaseTable = mainWindow.databaseInfoTable
		for i in reversed(range(databaseTable.rowCount())):
			databaseTable.removeRow(i)

		for table in self.tables:
			index = databaseTable.rowCount()
			databaseTable.insertRow(index)
			nameItem = QTableWidgetItem(table.name)
			nameItem.setIcon(QIcon('../resources/icons/table.png'))
			databaseTable.setItem(index, 0, nameItem)
			databaseTable.setItem(index, 1, QTableWidgetItem(str(table.rows)))
			databaseTable.setItem(index, 2, QTableWidgetItem(byteSizedStrings(table.size)))
			databaseTable.setItem(index, 3, QTableWidgetItem(table.getCreateTime()))
			databaseTable.setItem(index, 4, QTableWidgetItem(table.getUpdatedTime()))
			databaseTable.setItem(index, 5, QTableWidgetItem(table.engine))
			databaseTable.setItem(index, 6, QTableWidgetItem(table.comment))
			databaseTable.setItem(index, 7, QTableWidgetItem('table'))

