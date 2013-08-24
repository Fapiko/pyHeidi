import sys
from PyQt4 import QtGui
from session_manager import SessionManager
from main_application_window import MainApplicationWindow
import sqlite3

class MainApplication():
	"""
	@type configDb: sqlite3.Connection
	"""
	configDb = None

	def __init__(self):
		self.configDb = sqlite3.connect('../userdata.db')
		configDb = self.configDb
		configDb.row_factory = sqlite3.Row
		cursor = configDb.cursor()

		# Ensure settings table exists and create it if not
		cursor.execute("SELECT name FROM sqlite_master WHERE Type='table' and name = 'settings'")
		if cursor.fetchone() is None:
			self.createSettingsTable()

		app = QtGui.QApplication(sys.argv)
		mainApplicationWindow = MainApplicationWindow(configDb)
		mainApplicationWindow.hide()
		sessionManager = SessionManager(mainApplicationWindow, configDb)
		# sessionManager.show()

		self.mainApplicationWindow = mainApplicationWindow
		self.sessionManager = sessionManager

		app.exec_()

	def createSettingsTable(self):
		cursor = self.configDb.cursor()
		cursor.execute("""
			CREATE TABLE settings(
				id INTEGER PRIMARY KEY,
				name TEXT UNIQUE,
				value TEXT
			);
		""")

		self.configDb.commit()