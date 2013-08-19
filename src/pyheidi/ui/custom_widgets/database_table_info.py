from PyQt4.QtGui import QTableWidget


class DatabaseTableInfo(QTableWidget):
	def __init__(self, parent=None):
		self.columns = []
		QTableWidget.__init__(parent)

	def addColumn(self, column):
		"""
		@type column: Column
		"""
		self.columns.append(column)
