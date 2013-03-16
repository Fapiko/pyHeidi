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
		mainWindow.discardTableButton.clicked.connect(self.discardChanges)
		mainWindow.saveTableButton.clicked.connect(self.saveChanges)
		mainWindow.tableName.textEdited.connect(self.checkSaveDiscardState)

	def createTableAction(self):
		applicationWindow = self.applicationWindow
		mainWindow = applicationWindow.mainWindow

		applicationWindow.showTableTab()
		machineTabs = mainWindow.twMachineTabs
		tableTab = mainWindow.tableTab

		machineTabs.setTabText(machineTabs.indexOf(tableTab), 'Table: [Untitled]')
		machineTabs.setCurrentWidget(tableTab)

		self.previousState = {
			'table_name': '',
			'columns': None
		}

	def addColumnRow(self):
		applicationWindow = self.applicationWindow
		columnsTable = applicationWindow.mainWindow.tableInfoTable
		collations = applicationWindow.currentDatabase.server.getCollations()
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

		collationsCombo = QComboBox()
		collationsCombo.addItem('')
		for collation in collations:
			collationsCombo.addItem(collation['Collation'])

		virtualityCombo = QComboBox()
		virtualityCombo.addItems(self.buildQStringList(['', 'VIRTUAL', 'PERSISTENT']))

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
		columnsTable.setCellWidget(index, 9, collationsCombo)

		applicationWindow.mainWindow.removeColumnButton.setEnabled(True)
		self.checkSaveDiscardState()


	def buildQStringList(self, items):
		"""
		@rtype: QStringList
		"""
		returnData = QStringList()
		for item in items:
			returnData.append(item)

		return returnData

	def removeCurrentColumnRow(self):
		tableInfoTable = self.applicationWindow.mainWindow.tableInfoTable
		tableInfoTable.removeRow(tableInfoTable.currentRow())
		self.checkSaveDiscardState()

	def moveCurrentColumnUp(self):
		print 'move current column up!'

	def moveCurrentColumnDown(self):
		print 'move current column down!'

	def dataTypesSizeHint(self):
		return QSize(300, 400)

	def discardChanges(self):
		print 'discard changes!'

	def saveChanges(self):
		print 'save changes!'

	def checkSaveDiscardState(self):
		mainWindow = self.applicationWindow.mainWindow
		tableName = mainWindow.tableName.text()
		columnCount = mainWindow.tableInfoTable.rowCount()
		if tableName != '' and columnCount > 0:
			mainWindow.saveTableButton.setEnabled(True)
		else:
			mainWindow.saveTableButton.setEnabled(False)

		showDiscardButton = False
		previousState = self.previousState
		for key in previousState:
			if key == 'table_name':
				if tableName != previousState['table_name']:
					showDiscardButton = True
					break
			elif key == 'columns':
				if previousState['columns'] is None and columnCount > 0:
					showDiscardButton = True
					break

		mainWindow.discardTableButton.setEnabled(showDiscardButton)

