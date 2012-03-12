import sys
from PyQt4 import QtGui
from session_manager import SessionManager
from main_application_window import MainApplicationWindow

class MainApplication():
	def __init__(self):
		app = QtGui.QApplication(sys.argv)

		self.mainApplicationWindow = MainApplicationWindow()
#		self.mainApplicationWindow.log("/* Hello, Mr. Facepalmer */");
#		self.mainApplicationWindow.show()
		self.sessionManager = SessionManager(self.mainApplicationWindow)
		self.sessionManager.show()

		app.exec_()