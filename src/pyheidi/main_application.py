import sys
from PyQt4 import QtGui
from session_manager import SessionManager
from main_application_window import MainApplicationWindow

class MainApplication():
	"""
	@type configDb: sqlite3.Connection
	"""
	configDb = None

	def __init__(self):
		app = QtGui.QApplication(sys.argv)
		mainApplicationWindow = MainApplicationWindow()
		mainApplicationWindow.hide()
		sessionManager = SessionManager(mainApplicationWindow)
		sessionManager.show()

		self.mainApplicationWindow = mainApplicationWindow

		self.configDb = sessionManager.conn
		cursor = self.configDb.cursor()

		cursor.execute("INSERT INTO settings (name, value) VALUES ('mainwindow.width', '%s')", str(self.mainApplicationWindow.width()))
		# Ensure settings table exists and create it if not
		cursor.execute("SELECT name FROM sqlite_master WHERE Type='table' and name = 'settings'")
		if cursor.fetchone() is None:
			self.createSettingsTable()

		app.exec_()

	def createSettingsTable(self):

		cursor = self.configDb.cursor()
		cursor.execute("""
			CREATE TABLE settings(
				id INTEGER PRIMARY KEY,
				name TEXT,
				value TEXT
			);
		""")

		print self.mainApplicationWindow.width().__str__()
		print "INSERT INTO settings (name, value) VALUES ('mainwindow.width', %s)" % self.mainApplicationWindow.width()
		cursor.execute("INSERT INTO settings (name, value) VALUES ('mainwindow.width', '%s')", str(self.mainApplicationWindow.width()))
		cursor.execute("INSERT INTO settings (name, value) VALUES ('mainwindow.height', '%s')", str(self.mainApplicationWindow.height()))

		self.configDb.commit()