import MySQLdb

class DatabaseServer:
	"""
	@type name: string
	@type connection: MySQLdb.Connection
	@type treeIndex: number
	"""
	name = ""
	connection = None
	treeIndex = -1

	def __init__(self, name, connection):
		"""
		@type name: str
		@type connection: MySQLdb.Connection
		"""
		self.name = name
		self.connection = connection

