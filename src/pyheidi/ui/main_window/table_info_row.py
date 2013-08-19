from database.column import Column


class TableInfoRow:
	def __init__(self, column):
		"""
		@type column: Column
		"""
		self.column = column
