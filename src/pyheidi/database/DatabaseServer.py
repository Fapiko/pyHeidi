import MySQLdb
from PyQt4.QtGui import QTextEdit

class DatabaseServer:
	"""
	@type name: str
	@type connection: MySQLdb.Connection
	@type treeIndex: int
	@type statusWindow: QTextEdit
	"""
	name = ""
	connection = None
	treeIndex = -1
	statusWindow = None

	def __init__(self, name, connection, statusWindow):
		"""
		@type name: str
		@type connection: MySQLdb.Connection
		"""
		self.name = name
		self.connection = connection
		self.statusWindow = statusWindow

	def execute(self, *args):
		"""
		@type query: str
		@type params: list
		"""
		cursor = self.connection.cursor()
		if len(args) == 1:
			cursor.execute(args[0])
		elif len(args) == 2:
			cursor.execute(args[0], args[1])

		statusWindow = self.getStatusWindow()
		statusWindow.append("%s;" % args[0])

		return cursor

	def getStatusWindow(self):
		"""
		@rtype: QTextEdit
		"""
		return self.statusWindow
