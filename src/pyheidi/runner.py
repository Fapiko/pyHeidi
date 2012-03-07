import sys
from sessionmanager import SessionManager
from mainapplication import MainApplication
from PyQt4 import QtGui

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	sessionManager = SessionManager()
	sessionManager.show()
	app.exec_()