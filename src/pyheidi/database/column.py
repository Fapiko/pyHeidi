import re

class Column:
	def __init__(self, name=None, dataType=None, length=None, unsigned=False,
			allowsNull=True, zerofill=False, default=None, comment=None,
			collation=None, expression=None, virtuality=None):
		self.name = name
		self.dataType = dataType
		self.setLength(length)
		self.unsigned = unsigned
		self.allowsNull = allowsNull
		self.zerofill = zerofill
		self.setDefault(default)
		self.setComment(comment)
		self.collation = collation
		self.setExpression(expression)
		self.virtuality = virtuality

	def setDefault(self, text):
		if text == 'No default' or text == '':
			self.default = None
		else:
			self.default = text

	def setLength(self, length):
		if length == '':
			self.length = None
		else:
			self.length = length

	def setExpression(self, expression):
		if expression == '':
			self.expression = None
		else:
			self.expression = expression

	def setComment(self, comment):
		if comment == '':
			self.comment = None
		else:
			self.comment = comment

	def getSql(self):
		return_string = "`%s` %s" % (self.name, self.dataType)

		if self.length is not None:
			return_string += "(%s)" % self.length

		if self.unsigned:
			return_string += ' UNSIGNED'

		if self.zerofill:
			return_string += ' ZEROFILL'

		if self.allowsNull:
			return_string += ' NULL'
		else:
			return_string += ' NOT NULL'

		if self.default is not None:
			return_string += " DEFAULT '%s'" % self.default

		if self.comment is not None:
			return_string += " COMMENT '%s'" % self.comment

		return return_string

	def __str__(self):
		return self.getSql()

	@staticmethod
	def fromString(columnString):
		columnPattern = re.compile('`(?P<name>.+)` (?P<datatype>[a-z]+)(\((?P<length>\d+)\))?( )?(?P<allows_null>NOT NULL)?(DEFAULT [a-z]+)?( )?(AUTO_INCREMENT)?',
				re.IGNORECASE | re.DOTALL)
		matches = columnPattern.match(columnString)

		if matches is None:
			print columnString

		column = Column(
			matches.group('name'),
			matches.group('datatype'),
			matches.group('length')
		)

		if matches.group('allows_null') == 'NOT NULL':
			column.allowsNull = False

		return column
