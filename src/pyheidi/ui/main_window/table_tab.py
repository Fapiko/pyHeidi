from PyQt4.QtGui import QCheckBox, QComboBox, QTableWidgetItem
from PyQt4.QtCore import Qt, QSize, QStringList
from database.Table import Table
from database.column import Column

class TableTab:
	def __init__(self, applicationWindow):
		"""
		@type applicationWindow: MainApplicationWindow
		"""
		self.applicationWindow = applicationWindow
		self.tableTab = applicationWindow.mainWindow.tableTab
		self.table = Table("", None)

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
		columnsTable.cellChanged.connect(self.columnItemChanged)
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
		dataTypes.currentIndexChanged.connect(self.dataTypeChanged)

		collationsCombo = QComboBox()
		collationsCombo.addItem('')
		for collation in collations:
			collationsCombo.addItem(collation['Collation'])

		virtualityCombo = QComboBox()
		virtualityCombo.addItems(self.buildQStringList(['', 'VIRTUAL', 'PERSISTENT']))

		unsignedCheckBox = QCheckBox()
		unsignedCheckBox.stateChanged.connect(self.unsignedStateChanged)

		nullCheckBox = QCheckBox()
		nullCheckBox.setCheckState(Qt.Checked)
		nullCheckBox.stateChanged.connect(self.nullStateChanged)

		zerofill = QCheckBox()
		zerofill.stateChanged.connect(self.zerofillStateChanged)

		columnIdField = QTableWidgetItem(str(index + 1))
		columnIdField.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		columnIdField.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		columnsTable.insertRow(index)
		columnsTable.setItem(index, 0, columnIdField)
		columnsTable.setItem(index, 1, QTableWidgetItem("Column %s" % (index + 1)))
		columnsTable.setCellWidget(index, 2, dataTypes)
		columnsTable.setCellWidget(index, 4, unsignedCheckBox)
		columnsTable.setCellWidget(index, 5, nullCheckBox)
		columnsTable.setCellWidget(index, 6, zerofill)
		columnsTable.setItem(index, 7, QTableWidgetItem('No default'))
		columnsTable.setCellWidget(index, 9, collationsCombo)
		columnsTable.setCellWidget(index, 11, virtualityCombo)
		applicationWindow.mainWindow.removeColumnButton.setEnabled(True)
		column = Column(name = columnsTable.item(index, 1).text(),
						dataType = dataTypes.currentText(),
						# length = columnsTable.item(index, 3).text(),
						unsigned = unsignedCheckBox.isChecked(),
						allowsNull = nullCheckBox.isChecked(),
						zerofill = zerofill.isChecked(),
						default = columnsTable.item(index, 7).text(),
						# comment = columnsTable.item(index, 8).text(),
						collation = collationsCombo.currentText(),
						# expression = columnsTable.item(index, 10).text(),
						virtuality = virtualityCombo.currentText())
		self.table.columns.append(column)
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

	def dataTypeChanged(self, dataType):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable
		dataType = columnsTable.cellWidget(0, 2).itemText(dataType)

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].dataType != columnsTable.cellWidget(i, 2).currentText():
				self.table.columns[i].dataType = dataType
				break

	def columnItemChanged(self, row, column):
		# This if allows us to avoid change events triggered from initially
		# populating the row in the GUI
		if row < len(self.table.columns):
			columnsTable = self.applicationWindow.mainWindow.tableInfoTable
			tableColumn = self.table.columns[row]

			text = columnsTable.item(row, column).text()
			if column == 1:
				tableColumn.name = text
			elif column == 3:
				tableColumn.setLength(text)
			elif column == 7:
				tableColumn.setDefault(text)
			elif column == 8:
				tableColumn.comment = text
			elif column == 10:
				tableColumn.setExpression(text)

			print tableColumn

	def unsignedStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].unsigned != columnsTable.cellWidget(i, 4).isChecked():
				print self.table.columns[i]
				self.table.columns[i].unsigned = state
				print self.table.columns[i]

	def nullStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].allowsNull != columnsTable.cellWidget(i, 5).isChecked():
				print self.table.columns[i]
				self.table.columns[i].allowsNull = state
				print self.table.columns[i]

	def zerofillStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].zerofill != columnsTable.cellWidget(i, 6).isChecked():
				print self.table.columns[i]
				self.table.columns[i].zerofill = state
				print self.table.columns[i]
