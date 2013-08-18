from PyQt4.Qt import QTableWidgetItem

class DatabaseTab:
	def __init__(self, applicationWindow):
		"""
		@type applicationWindow: MainApplicationWindow
		"""
		self.applicationWindow = applicationWindow
		mainWindow = applicationWindow.mainWindow

		mainWindow.databaseInfoTable.itemDoubleClicked.connect(self.updateCurrentTable)

	def updateCurrentTable(self, tableTreeItem):
		"""
		@type tableTreeItem: QTableWidgetItem
		"""
		self.applicationWindow.updateCurrentTable(tableTreeItem.text())
