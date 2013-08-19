from PyQt4.QtGui import QTableWidget


class DatabaseTableInfo(QTableWidget):
	def __init__(self, parent=None):
		super(DatabaseTableInfo, self).__init__(parent)
		self.rows = []

	def addRow(self, row):
		"""
		@type row: TableInfoRow
		"""
		self.rows.append(row)
		row.insertAtEnd()

	def getMainApplicationWindow(self):
		"""
		Just doing it for the type hinting
		@rtype: MainApplicationWindow
		"""
		return self.mainApplicationWindow
