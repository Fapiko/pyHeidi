import sys
from PyQt4 import QtGui
from session_manager import SessionManager
from main_application_window import MainApplicationWindow

class MainApplication():
	def __init__(self):
		app = QtGui.QApplication(sys.argv)
		mainApplicationWindow = MainApplicationWindow()
		mainApplicationWindow.hide()
		sessionManager = SessionManager(mainApplicationWindow)
		sessionManager.show()

#		mainApplicationWindow.show()
#		mainApplicationWindow.showMaximized()
		app.exec_()