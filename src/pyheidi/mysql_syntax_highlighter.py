from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QColor

class MysqlSyntaxHighlighter(QSyntaxHighlighter):
	STATE__MULTILINE_COMMENT = 0
	STATE__NORMAL = 1

	def __init__(self, doc):
		QSyntaxHighlighter.__init__(self, doc)

	def highlightBlock(self, text):
		"""
		@type text: QString
		"""
		state = self.previousBlockState()
		start = 0

		for i in range(len(text)):
			if (state == self.STATE__MULTILINE_COMMENT):
				if (text.mid(i, 2) == '*/'):
					state = self.STATE__NORMAL
					self.setFormat(start, i - start + 2, QColor("grey"))

			if (text.mid(i, 2) == '/*'):
				start = i
				state = self.STATE__MULTILINE_COMMENT

		if (state == self.STATE__MULTILINE_COMMENT):
			self.setFormat(start, text.length() - start, QColor("grey"))

		self.setCurrentBlockState(state)

