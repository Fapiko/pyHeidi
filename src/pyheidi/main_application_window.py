from PyQt4 import QtGui
from ui.ui_mainwindow import Ui_MainWindow
from mysql_syntax_highlighter import MysqlSyntaxHighlighter

class MainApplicationWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.mainWindow = Ui_MainWindow()
		self.mainWindow.setupUi(self)

		self.mainWindow.spltHorizontal1.setStretchFactor(0, 1)
		self.mainWindow.spltVertical1.setStretchFactor(1, 1)

		self.logHighlighter = MysqlSyntaxHighlighter(self.mainWindow.txtStatus.document())

#		self.show()

	def log(self, message):
		self.mainWindow.txtStatus.append(message + "\n")