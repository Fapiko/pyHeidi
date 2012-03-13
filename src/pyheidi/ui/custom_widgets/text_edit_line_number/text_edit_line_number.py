from PyQt4.QtGui import QTextEdit

class QTextEditLineNumber(QTextEdit):

	def __init__(self, parent = None):
		print parent
		QTextEdit.__init__(self, parent)

