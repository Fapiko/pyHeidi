class Index:
	def __init__(self, type, name, columns):
		"""
		@type type: str
		@type name: str
		@type columns: list
		"""
		self.type = type.upper()
		self.name = name
		self.columns = columns

	@staticmethod
	def parseColumnNamesFromString(columnString):
		columns = columnString.split(',');
		for index, column in enumerate(columns):
			column = column.strip()
			columns[index] = column.strip('`')

		return columns

	def __str__(self):
		if self.type == 'KEY':
			type = 'KEY'
		else:
			type = "%s KEY" % self.type

		if self.type != 'PRIMARY':
			name = "`%s`" % self.name
		else:
			name = ''

		columns = '`'
		print self.columns
		for column in self.columns:
			columns += "%s`, " % column.name
		columns = columns[:-2]

		return "%s %s (%s)" % (type, name, columns)
