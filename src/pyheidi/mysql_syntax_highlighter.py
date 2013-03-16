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
		commentFormat.setFontWeight(0)
		commentFormat.setForeground(QColor('grey'))
		self.commentFormat = commentFormat

		mysqlObjectFormat = QTextCharFormat()
		mysqlObjectFormat.setFontItalic(True)
		mysqlObjectFormat.setFontWeight(0)
		mysqlObjectFormat.setForeground(QColor().fromRgb(128, 128, 0))
		self.mysqlObjectFormat = mysqlObjectFormat

		self.mysqlObjectRegex = re.compile('(`.+?`)')

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
		commentRanges = []
		for i in range(len(text)):
			if state == self.STATE__MULTILINE_COMMENT:
				if text.mid(i, 2) == '*/':
					state = self.STATE__NORMAL
					formatEnd = i - start + 2
					self.setFormat(start, formatEnd, commentFormat)
					if self.previousBlockState() == self.STATE__MULTILINE_COMMENT:
						commentRangeStart = 0;

					commentRanges.append((commentRangeStart, formatEnd))

			if text[i] == '#':
				self.setFormat(i, len(text) - i, commentFormat)

			if text.mid(i, 2) == '/*':
				start = i
				state = self.STATE__MULTILINE_COMMENT
				commentRangeStart = i

		if state == self.STATE__MULTILINE_COMMENT:
			self.setFormat(start, text.length() - start, commentFormat)
		else:
			matches = self.mysqlObjectRegex.finditer(text)
			if matches:
				for matchObject in matches:
					group = matchObject.group()
					if self.checkCommentRanges(commentRanges, matchObject):
						self.setFormat(matchObject.start(), len(group), self.mysqlObjectFormat)

		self.setCurrentBlockState(state)

	def checkCommentRanges(self, commentRanges, match):
		"""
		@type commentRanges: list
		@type match: MatchObject
		@rtype: bool
		"""
		for range in commentRanges:
			if match.start() < range[1]:
				return False

		return True
