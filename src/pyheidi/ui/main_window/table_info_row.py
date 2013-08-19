from PyQt4.QtCore import Qt, QStringList
from PyQt4.QtGui import QCheckBox, QComboBox, QHBoxLayout, QLabel, QTableWidgetItem, QWidget
from database.column import Column


class TableInfoRow:
	def __init__(self, parent, column):
		"""
		@type parent: DatabaseTableInfo
		@type column: Column
		"""
		self.parent = parent
		self.column = column

	@staticmethod
	def generateDataTypesField():
		"""
		@rtype: QComboBox
		"""
		dataTypes = QComboBox()
		dataTypes.addItems(TableInfoRow.buildQStringList(['TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'BIGINT', 'BIT']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['FLOAT', 'DOUBLE', 'DECIMAL']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['CHAR', 'VARCHAR', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['BINARY', 'VARBINARY', 'TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['DATE', 'TIME', 'YEAR', 'DATETIME', 'TIMESTAMP']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['POINT', 'LINESTRING', 'POLYGON', 'GEOMETRY', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']))
		dataTypes.insertSeparator(dataTypes.count())
		dataTypes.addItems(TableInfoRow.buildQStringList(['ENUM', 'SET']))

		return dataTypes

	@staticmethod
	def generateIdField(id=''):
		"""
		@rtype: QTableWidgetItem
		"""
		idField = QTableWidgetItem(str(id))
		idField.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		idField.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

		return idField

	@staticmethod
	def buildQStringList(items):
		"""
		@rtype: QStringList
		"""
		returnData = QStringList()
		for item in items:
			returnData.append(item)

		return returnData

	@staticmethod
	def generateUnsignedCheckboxField():
		"""
		@rtype: QCheckBox
		"""
		return TableInfoRow.generateCenteredCheckbox()

	@staticmethod
	def generateCenteredCheckbox():
		"""
		@rtype: QCheckBox
		"""
		field = QWidget()
		checkbox = QCheckBox()
		layout = QHBoxLayout(field)
		layout.addWidget(checkbox, 0, Qt.AlignHCenter)
		layout.setMargin(1)
		field.setLayout(layout)
		field.checkbox = checkbox

		return field

	@staticmethod
	def generateCollationsField(server):
		"""
		@rtype: QComboBox
		"""
		collations = server.getCollations()

		field = QComboBox()
		field.addItem('')
		for collation in collations:
			field.addItem(collation['Collation'])

		return field

	@staticmethod
	def generateVirtualityField():
		"""
		@rtype: QComboBox
		"""
		field = QComboBox()
		field.addItems(TableInfoRow.buildQStringList(['', 'VIRTUAL', 'PERSISTENT']))

		return field

	@staticmethod
	def generateNameField(index, name=None):
		"""
		@rtype: QTableWidgetItem
		"""
		if name is None:
			name = "Column %s" % index

		return QTableWidgetItem(name)

	def insertAtEnd(self):
		index = self.parent.rowCount()
		self.insertAt(index)

	def insertAt(self, index):
		parent = self.parent
		column = self.column

		self.idField = TableInfoRow.generateIdField(index)
		self.nameField = TableInfoRow.generateNameField(index, column.name)
		self.dataTypesField = TableInfoRow.generateDataTypesField()
		self.unsignedField = TableInfoRow.generateCenteredCheckbox()
		self.nullField = TableInfoRow.generateCenteredCheckbox()
		self.zerofillField = TableInfoRow.generateCenteredCheckbox()
		self.collationsField = TableInfoRow.generateCollationsField(self.parent.getMainApplicationWindow().currentDatabase.server)
		self.virtualityField = TableInfoRow.generateVirtualityField()

		parent.insertRow(index)
		parent.setItem(index, 0, self.idField)
		parent.setItem(index, 1, self.nameField)
		parent.setCellWidget(index, 2, self.dataTypesField)
		parent.setCellWidget(index, 4, self.unsignedField)
		parent.setCellWidget(index, 5, self.nullField)
		parent.setCellWidget(index, 5, self.zerofillField)
		parent.setItem(index, 7, QTableWidgetItem('No default'))
		parent.setCellWidget(index, 9, self.collationsField)
		parent.setCellWidget(index, 11, self.virtualityField)
