from PyQt4.QtGui import QIcon
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem
import re
from column import Column
from index import Index

class Table:
	def __init__(self, name, database = None, rows = None, size = None, created = None,
			updated = None, engine = None, comment = None, columns = None,
			autoincrement = None, defaultCollation = None, indexes = None):
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
		@type autoincrement: int
		@type defaultCollation: str
		@type indexes: list
		"""
		self.name = name
		self.created = created
		self.updated = updated
		self.rows = rows
		self.size = size
		self.engine = engine
		self.comment = comment
		self.autoincrement = autoincrement
		self.defaultCollation = defaultCollation

		self.database = database
		if database is not None:
			self.setDatabase(database)

		if columns is not None:
			self.columns = columns
		else:
			self.columns = []

		if indexes is not None:
			self.indexes = indexes
		else:
			self.indexes = []


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

	def refresh(self):
		cursor = self.database.server.execute("SHOW TABLE STATUS FROM `%s` WHERE Name = '%s'" %
	  			(self.database.name, self.name))
		self.defaultCollation = cursor.fetchone()['Collation']

		self.refreshColumns()

	def refreshColumns(self):
		cursor = self.database.server.execute("SHOW CREATE TABLE `%s`.`%s`" %
				(self.database.name, self.name))

		for row in cursor:
			self.parseCreateTableString(row['Create Table'])

	def parseCreateTableString(self, createTableString):
		createTablePattern = re.compile('CREATE TABLE `(?P<name>[a-z_]+)` \((?P<columns>.*?)\) ENGINE=(?P<engine>[a-z]+) (AUTO_INCREMENT=(?P<autoincrement>\d+) )?DEFAULT CHARSET=(?P<charset>[a-z\d]+)',
				re.IGNORECASE | re.DOTALL)
		matches = createTablePattern.match(createTableString)

		if matches is None:
			print "Error:\n" + createTableString

		# print matches.group('primary_key');

		columns = matches.group('columns').strip().split("\n")
		for index, column in enumerate(columns):
			column = column.strip()
			column = column.strip(',')

			primaryKeyMatch = re.match("^(PRIMARY KEY \((?P<columns>.*)\))", column)
			uniqueKeyMatch = re.match("^(UNIQUE KEY `(?P<key_name>.*?)` \((?P<columns>.*)\))", column)
			keyMatch = re.match("^(KEY `(?P<key_name>.*?)` \((?P<columns>.*)\))", column)

			if primaryKeyMatch is not None:
				indexColumns = self.columnStringsToObjects(Index.parseColumnNamesFromString(primaryKeyMatch.group('columns')))
				self.indexes.append(Index('PRIMARY', 'PRIMARY', indexColumns))
			elif uniqueKeyMatch is not None:
				indexColumns = self.columnStringsToObjects(Index.parseColumnNamesFromString(uniqueKeyMatch.group('columns')))
				self.indexes.append(Index('UNIQUE', uniqueKeyMatch.group('key_name'), indexColumns))
			elif keyMatch is not None:
				indexColumns = self.columnStringsToObjects(Index.parseColumnNamesFromString(keyMatch.group('columns')))
				self.indexes.append(Index('KEY', keyMatch.group('key_name'), indexColumns))
			else:
				self.columns.append(Column.fromString(column))

		self.name = matches.group('name')
		self.autoincrement = matches.group('autoincrement')

	def columnStringsToObjects(self, columnsList):
		columns = []
		for column in columnsList:
			columns.append(self.getColumnByName(column))

		return columns

	def getColumnByName(self, name):
		for column in self.columns:
			if column.name == name:
				return column

		return None
