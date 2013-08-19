from PyQt4.QtGui import QIcon
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
import re
from column import Column

class Table:
	def __init__(self, name, database = None, rows = None, size = None, created = None,
			updated = None, engine = None, comment = None, columns = None):
		"""
		@type name: str
		@type database: Database
		@type rows: int
		@type size: int
		@type created: datetime
		@type updated: datetime
		@type engine: str
		@type comment: str
		@type columns: list
		"""
		self.name = name
		self.created = created
		self.updated = updated
		self.rows = rows
		self.size = size
		self.engine = engine
		self.comment = comment

		self.database = database
		if database is not None:
			self.setDatabase(database)

		if columns is not None:
			self.columns = columns
		else:
			self.columns = []


	# Just for type hinting... really need to figure out how to fix class
	# attribute type hints :(
	def getApplicationWindow(self):
		"""
		@rtype: MainApplicationWindow
		"""
		return self.database.applicationWindow

	def getCreateTime(self):
		return self.getTime(self.created)

	def getUpdatedTime(self):
		return self.getTime(self.updated)

	def getTime(self, timestamp):
		"""
		@type timestamp: datetime
		@rtype: str
		"""
		if timestamp is None:
			return ''
		else:
			return timestamp.isoformat(' ')

	def setAsCurrentTable(self):
		applicationWindow = self.getApplicationWindow()
		applicationWindow.showTableTab()
		mainWindow = applicationWindow.mainWindow
		tableTab = mainWindow.tableTab
		twMachineTabs = mainWindow.twMachineTabs

		twMachineTabs.setTabText(twMachineTabs.indexOf(tableTab), "Table: %s" % self.name)
		twMachineTabs.setCurrentWidget(tableTab)

		for i in range(0, mainWindow.tableInfoTable.rowCount()):
			mainWindow.tableInfoTable.removeRow(0)

		applicationWindow.tableTab.table = self

		self.updateUI()

	def setDatabase(self, database):
		self.database = database
		databaseTreeItem = database.getDatabaseTreeItem()
		tableTreeItem = HeidiTreeWidgetItem()
		tableTreeItem.itemType = 'table'
		tableTreeItem.setIcon(0, QIcon('../resources/icons/table.png'))
		tableTreeItem.setText(0, self.name)
		databaseTreeItem.addChild(tableTreeItem)
		database.tables.append(self)

	def getColumnString(self):
		columnsCombined = ''
		for column in self.columns:
			columnsCombined += "\t%s,\n" % column

		columnsCombined = columnsCombined[:-2]

		return "(\n%s\n)" % columnsCombined

	def getCreateTable(self):
		createString = "CREATE TABLE `%s` %s\nCOLLATE='%s'\nENGINE=%s" % (
			self.name, self.getColumnString(), 'utf8_general_ci', 'InnoDB')

		return createString

	def __str__(self):
		return self.getCreateTable()

	def updateUI(self):
		self.refreshColumns()
		mainWindow = self.getApplicationWindow().mainWindow

		mainWindow.tableName.setText(self.name)
		mainWindow.tableComment.setPlainText(self.comment)

		for column in self.columns:
			self.getApplicationWindow().tableTab.addColumnRow(column)

	def refreshColumns(self):
		cursor = self.database.server.execute("SHOW CREATE TABLE `%s`.`%s`" %
				(self.database.name, self.name))
		for row in cursor:
			for column in self.parseCreateTableString(row['Create Table'])['columns']:
				self.columns.append(Column.fromString(column))

	def parseCreateTableString(self, createTableString):
		createTablePattern = re.compile('CREATE TABLE `(?P<name>[a-z_]+)` \((?P<columns>.*?)(PRIMARY KEY .*\n)?\) ENGINE=(?P<engine>[a-z]+) (AUTO_INCREMENT=\d+ )?DEFAULT CHARSET=(?P<charset>[a-z\d]+)',
				re.IGNORECASE | re.DOTALL)
		matches = createTablePattern.match(createTableString)

		if matches is None:
			print "Error:\n" + createTableString

		columns = matches.group('columns').strip().split("\n")
		for index, column in enumerate(columns):
			column = column.strip()
			columns[index] = column.strip(',')

		returnDict = {
			'name': matches.group('name'),
			'columns': columns
		}

		return returnDict
