from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt4.QtGui import QIcon
from database_table_info import DatabaseTableInfo


class DatabaseTableInfoPlugin(QPyDesignerCustomWidgetPlugin):
	def __init__(self):
		QPyDesignerCustomWidgetPlugin.__init__(self)
		self.description = 'Subclasses the QTableWidget class to add some helper methods for dealing with the view code.'

	def name(self):
		return 'DatabaseTableInfo'

	def group(self):
		return 'PyHeidi Custom Widgets'

	def icon(self):
		return QIcon()

	def isContainer(self):
		return False

	def includeFile(self):
		return 'database_table_info'

	def toolTip(self):
		return self.description

	def whatsThis(self):
		return self.description

	def createWidget(self, parent):
		return DatabaseTableInfo(parent)
