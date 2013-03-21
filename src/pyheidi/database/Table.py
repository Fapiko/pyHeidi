from PyQt4.QtGui import QIcon
from qthelpers.HeidiTreeWidgetItem import HeidiTreeWidgetItem

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
			self.setDabase(database)

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
		self.database.server.execute("SHOW CREATE TABLE `%s`.`%s`" %
									 (self.database.name, self.name))

	def setDabase(self, database):
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
