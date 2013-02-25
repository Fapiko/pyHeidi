from PyQt4 import QtGui
from ui.ui_mainwindow import Ui_MainWindow

class MainApplicationWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		mainWindow = Ui_MainWindow()
		mainWindow.setupUi(self)
		self.show()

		mainWindow.spltHorizontal1.setStretchFactor(0, 1)
		mainWindow.spltVertical1.setStretchFactor(1, 1)
