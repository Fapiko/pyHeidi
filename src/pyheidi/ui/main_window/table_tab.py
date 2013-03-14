from PyQt4.QtGui import QCheckBox, QComboBox, QScrollArea, QSizePolicy, QTableWidgetItem
from PyQt4.QtCore import Qt, QSize, QStringList

class TableTab:
	def __init__(self, applicationWindow):
		"""
		@type applicationWindow: MainApplicationWindow
		"""
		self.applicationWindow = applicationWindow
		self.tableTab = applicationWindow.mainWindow.tableTab

		mainWindow = applicationWindow.mainWindow
		mainWindow.addColumnButton.clicked.connect(self.addColumnRow)
		mainWindow.removeColumnButton.clicked.connect(self.removeCurrentColumnRow)
		mainWindow.moveColumnDownButton.clicked.connect(self.moveCurrentColumnDown)
		mainWindow.moveColumnUpButton.clicked.connect(self.moveCurrentColumnUp)

	def createTableAction(self):
		mainWindow = self.applicationWindow.mainWindow
		self.applicationWindow.showTableTab()
		machineTabs = mainWindow.twMachineTabs
		tableTab = mainWindow.tableTab

		machineTabs.setTabText(machineTabs.indexOf(tableTab), 'Table: [Untitled]')
		machineTabs.setCurrentWidget(tableTab)
		print 'Create a table!'

	def addColumnRow(self):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable
		index = columnsTable.rowCount()

		dataTypes = QComboBox()
		dataTypes.addItems(self.buildQStringList(['TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'BIT']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['FLOAT', 'DOUBLE', 'DECIMAL']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['CHAR', 'VARCHAR', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['BINARY', 'VARBINARY', 'TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['DATE', 'TIME', 'YEAR', 'DATETIME', 'TIMESTAMP']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['POINT', 'LINESTRING', 'POLYGON', 'GEOMETRY', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(self.buildQStringList(['ENUM', 'SET']))

		nullCheckBox = QCheckBox()
		nullCheckBox.setCheckState(Qt.Checked)

		columnsTable.insertRow(index)
		columnsTable.setItem(index, 0, QTableWidgetItem(str(index + 1)))
		columnsTable.setItem(index, 1, QTableWidgetItem("Column %s" % (index + 1)))
		columnsTable.setCellWidget(index, 2, dataTypes)
		columnsTable.setCellWidget(index, 4, QCheckBox())
		columnsTable.setCellWidget(index, 5, nullCheckBox)
		columnsTable.setCellWidget(index, 6, QCheckBox())
		columnsTable.setItem(index, 7, QTableWidgetItem('No default'))
		print 'add column!'

	def buildQStringList(self, items):
		"""
		@rtype: QStringList
		"""
		returnData = QStringList()
		for item in items:
			returnData.append(item)

		return returnData

	def removeCurrentColumnRow(self):
		print 'remove current column!'

	def moveCurrentColumnUp(self):
		print 'move current column up!'

	def moveCurrentColumnDown(self):
		print 'move current column down!'

	def dataTypesSizeHint(self):
		return QSize(300, 400)