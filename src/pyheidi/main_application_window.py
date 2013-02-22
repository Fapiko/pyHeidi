from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon, QMainWindow, QTreeWidgetItem
from ui.ui_mainwindow import Ui_MainWindow

class MainApplicationWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)

#		mainWindow.databaseTree.setBaseSize()

		self.mainWindow = mainWindow
		self.show()

	def reloadDbs(self, dbConnection):
		cursor = dbConnection.cursor()
		self.dbConnection = dbConnection
		self.dbCursor = cursor

		cursor.execute('SHOW DATABASES')
		for row in cursor:
			self.addDatabase(row[0])

	def addDatabase(self, name):
		database = QTreeWidgetItem()
		database.setText(0, name)
		database.setIcon(0, QIcon('../resources/icons/database.png'))
		database.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)

		self.mainWindow.databaseTree.addTopLevelItem(database)
		print name



