from PyQt4.QtGui import QCheckBox, QComboBox, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt4.QtCore import Qt, QSize, QStringList
from database.table import Table
from database.column import Column
from ui.main_window.table_info_row import TableInfoRow
from qthelpers import helper_methods

class TableTab:
	def __init__(self, applicationWindow):
		"""
		@type applicationWindow: MainApplicationWindow
		"""
		self.applicationWindow = applicationWindow
		self.tableTab = applicationWindow.mainWindow.tableTab
		self.table = Table("", None)
		# Set this to True when programmatically manipulating the columns table
		# to prevent GUI events from causing sync issues with our columns
		self.lockCellChanges = False

		self.previousState = None

		mainWindow = applicationWindow.mainWindow
		mainWindow.addColumnButton.clicked.connect(self.addNewRow)
		mainWindow.removeColumnButton.clicked.connect(self.removeCurrentColumnRow)
		mainWindow.moveColumnDownButton.clicked.connect(self.moveCurrentColumnDown)
		mainWindow.moveColumnUpButton.clicked.connect(self.moveCurrentColumnUp)
		mainWindow.discardTableButton.clicked.connect(self.discardChanges)
		mainWindow.saveTableButton.clicked.connect(self.saveChanges)
		mainWindow.tableName.textEdited.connect(self.nameEdited)
		mainWindow.tableInfoTable.itemSelectionChanged.connect(self.selectedColumnChanged)

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

	def addNewRow(self):
		self.addColumnRow()

	def addColumnRow(self, column=None):
		self.lockCellChanges = True
		applicationWindow = self.applicationWindow
		columnsTable = applicationWindow.mainWindow.tableInfoTable
		columnsTable.cellChanged.connect(self.columnItemChanged)

		tableInfoTable = self.applicationWindow.mainWindow.tableInfoTable

		if column is None:
			column = Column()

		row = TableInfoRow(tableInfoTable, column)
		tableInfoTable.addRow(row)

		self.lockCellChanges = False
		self.checkSaveDiscardState()

	def removeCurrentColumnRow(self):
		tableInfoTable = self.applicationWindow.mainWindow.tableInfoTable
		tableInfoTable.removeRow(tableInfoTable.currentRow())
		self.checkSaveDiscardState()

	def moveCurrentColumnUp(self):
		row = self.applicationWindow.mainWindow.tableInfoTable.selectedIndexes()[0].row()
		self.moveRowTo(row, row - 1)

	def moveCurrentColumnDown(self):
		row = self.applicationWindow.mainWindow.tableInfoTable.selectedIndexes()[0].row()
		self.moveRowTo(row, row + 1)

	def dataTypesSizeHint(self):
		return QSize(300, 400)

	def discardChanges(self):
		print 'discard changes!'

	def saveChanges(self):
		print self.table.getCreateTable()
		self.applicationWindow.currentServer.execute(self.table.getCreateTable())

	def moveRowTo(self, source, destination):
		self.lockCellChanges = True
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable
		columns = self.table.columns

		moveColumn = columns.pop(source)
		if source > destination:
			columns.insert(destination, moveColumn)
			source += 1
		else:
			columns.insert(destination, moveColumn)
			destination += 1

		columnsTable.insertRow(destination)

		for i in [0, 1, 3, 7, 8, 10]:
			newItem = columnsTable.item(source, i)
			if newItem is not None:
				newItem = newItem.clone()
				columnsTable.setItem(destination, i, newItem)

		for i in [2, 4, 5, 6, 9, 11]:
			newWidget = columnsTable.cellWidget(source, i)
			columnsTable.setCellWidget(destination, i, newWidget)

		columnsTable.setCurrentCell(destination, 0)
		columnsTable.removeRow(source)

		for i in xrange(columnsTable.rowCount()):
			columnsTable.item(i, 0).setText(str(i + 1))

		self.lockCellChanges = False
		self.checkMoveColumnButtonState()

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
		if previousState is not None:
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
		if self.lockCellChanges is False:
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

	def unsignedStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].unsigned != columnsTable.cellWidget(i, 4).isChecked():
				self.table.columns[i].unsigned = state

	def nullStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].allowsNull != columnsTable.cellWidget(i, 5).isChecked():
				self.table.columns[i].allowsNull = state

	def zerofillStateChanged(self, state):
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable

		for i in xrange(columnsTable.rowCount()):
			if self.table.columns[i].zerofill != columnsTable.cellWidget(i, 6).isChecked():
				self.table.columns[i].zerofill = state

	def selectedColumnChanged(self):
		self.checkMoveColumnButtonState()

	def checkMoveColumnButtonState(self):
		mainWindow = self.applicationWindow.mainWindow
		columnsTable = self.applicationWindow.mainWindow.tableInfoTable
		row = columnsTable.selectedIndexes()[0].row() + 1

		totalRows = columnsTable.rowCount()
		if totalRows < 2:
			mainWindow.moveColumnUpButton.setEnabled(False)
			mainWindow.moveColumnDownButton.setEnabled(False)
		else:
			if row < totalRows:
				mainWindow.moveColumnDownButton.setEnabled(True)
			else:
				mainWindow.moveColumnDownButton.setEnabled(False)

			if row > 1:
				mainWindow.moveColumnUpButton.setEnabled(True)
			else:
				mainWindow.moveColumnUpButton.setEnabled(False)

	def nameEdited(self):
		self.table.name = self.applicationWindow.mainWindow.tableName.text()
		self.checkSaveDiscardState()

	def resetColumn(self, index):
		column = self.table.columns[index]

		columnsTable = self.applicationWindow.mainWindow.tableInfoTable
		dataTypes = columnsTable.cellWidget(index, 2)
		unsignedCheckbox = columnsTable.cellWidget(index, 4)
		allowsNullCheckbox = columnsTable.cellWidget(index, 5)

		columnsTable.setItem(index, 1, QTableWidgetItem(column.name))
		dataTypes.setCurrentIndex(dataTypes.findText(column.dataType.upper()))
		if column.length is not None:
			columnsTable.setItem(index, 3, QTableWidgetItem(column.length))
		if column.unsigned:
			unsignedCheckbox.setChecked(True)
		if column.allowsNull is False:
			allowsNullCheckbox.setChecked(False)

	def populateDefaultCollationField(self, server):
		"""
		@type server: DatabaseServer
		@type defaultCollation: str
		"""
		field = self.applicationWindow.mainWindow.tableOptionsDefaultCollation
		collations = server.getCollations()
		for collation in collations:
			field.addItem(collation['Collation'])

	def setCurrentTable(self, table):
		"""
		@type table: Table
		"""
		self.table = table

		table.refresh()
		applicationWindow = self.applicationWindow
		applicationWindow.showTableTab()
		mainWindow = applicationWindow.mainWindow
		tableTab = mainWindow.tableTab

		twMachineTabs = mainWindow.twMachineTabs
		twMachineTabs.setTabText(twMachineTabs.indexOf(tableTab), "Table: %s" % table.name)
		twMachineTabs.setCurrentWidget(tableTab)

		self.updateUI()

	def updateUI(self):
		table = self.table

		mainWindow = self.applicationWindow.mainWindow

		mainWindow.tableName.setText(table.name)
		mainWindow.tableComment.setPlainText(table.comment)

		for i in range(0, mainWindow.tableInfoTable.rowCount()):
			mainWindow.tableInfoTable.removeRow(0)

		for column in table.columns:
			self.addColumnRow(column)

		self.setAutoincrementValue(table.autoincrement)
		self.setDefaultCollationValue(table.defaultCollation)

	def setDefaultCollationValue(self, collation):
		field = self.applicationWindow.mainWindow.tableOptionsDefaultCollation
		field.setCurrentIndex(field.findText(collation))

	def setAutoincrementValue(self, autoincrement):
		if autoincrement is None:
			autoincrement = ''

		self.applicationWindow.mainWindow.tableOptionsAutoIncrement.setText(autoincrement)
