from PyQt4.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt4.QtGui import QColor
import re

class MysqlSyntaxHighlighter(QSyntaxHighlighter):
	STATE__MULTILINE_COMMENT = 0
	STATE__NORMAL = 1

	def __init__(self, doc):
		QSyntaxHighlighter.__init__(self, doc)
		commentFormat = QTextCharFormat()
		commentFormat.setFontItalic(True)
		commentFormat.setForeground(QColor('grey'))

		self.commentFormat = commentFormat

	def highlightBlock(self, text):
		"""
		@type text: QString
		"""

		commentFormat = self.commentFormat

		state = self.previousBlockState()
		start = 0

		# comment = re.compile('#.+$')
		# inlineSlashComment = re.compile('/\*(.+?)\*/')
		# multilineComment = re.compile('/\*(.+?)[^(\*/)]$')
		#
		# commentMatch = comment.search(text)
		# if commentMatch:
		# 	start = commentMatch.start(0)
		# 	self.setFormat(start, len(text) - start, commentFormat)

		# Hrmm, non-regex may be best specifically for seeking out comments as the mixture
		# of comment types could be confusing to handle

		for i in range(len(text)):
			if state == self.STATE__MULTILINE_COMMENT:
				if text.mid(i, 2) == '*/':
					state = self.STATE__NORMAL
					self.setFormat(start, i - start + 2, commentFormat)

			if text[i] == '#':
				self.setFormat(i, len(text) - i, commentFormat)

			if text.mid(i, 2) == '/*':
				start = i
				state = self.STATE__MULTILINE_COMMENT

		if state == self.STATE__MULTILINE_COMMENT:
			self.setFormat(start, text.length() - start, commentFormat)

		self.setCurrentBlockState(state)

