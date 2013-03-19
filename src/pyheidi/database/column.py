class Column:
	def __init__(self, name=None, dataType=None, length=None, unsigned=False,
			allowsNull=True, zerofill=False, default=None, comment='',
			collation=None, expression=None, virtuality=None):
		self.name = name
		self.dataType = dataType
		self.length = length
		self.unsigned = unsigned
		self.allowsNull = allowsNull
		self.zerofill = zerofill
		self.setDefault(default)
		self.comment = comment
		self.collation = collation
		self.expression = expression
		self.virtuality = virtuality

	def setDefault(self, text):
		if text == 'No default' or text == '':
			default = None

	def __str__(self):
		return_string = "`%s` %s" % (self.name, self.dataType)


		if self.allowsNull:
			return_string += ' NULL'
		else:
			return_string += ' NOT NULL'

		return return_string