from PyQt4.QtGui import QTextEdit

class CodeEditor(QTextEdit):
	def __init__(self, *args):
		QTextEdit.__init__(self, args)
