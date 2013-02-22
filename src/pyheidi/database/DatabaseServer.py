import MySQLdb

class DatabaseServer:
	"""
	@type name: string
	@type connection: MySQLdb.Connection
	@type treeIndex: number
	"""
	name = ""
	connection = ""
	treeIndex = -1
	def __init__(self, name, connection):
		"""
		@type connection: MySQLdb.Connection
		"""
		self.name = name
		self.connection = connection

