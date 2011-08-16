import sys
from PyQt4 import QtGui, QtCore

class SessionManager(QtGui.QDialog):
	def __init__(self):
		super(SessionManager, self).__init__()
		self.initUI()
			
	def initUI(self):
		comboNetworkType = QtGui.QComboBox(self)
		comboNetworkType.addItem('TCP/IP')
		
		labelNoSession = QtGui.QLabel('New here? In order to connect to a MySQL server, you have to create a so called "session" at first. Just click the "New" button on the bottom left to create your first session.\n\nGive it a friendly name (e.g. "Local DB Server") so you\'ll recall it the next time you start HeidiSQL.')
		labelNoSession.setWordWrap(True)
		
		textHostname = QtGui.QLineEdit()
		textHostname.setText('127.0.0.1')
		
		serverManager = QtGui.QTreeView(self)
		
		tabWidget = QtGui.QTabWidget(self)
		tabSettings = QtGui.QWidget()
		tabSettings.tabSettingsLayout = QtGui.QFormLayout(tabSettings)
		tabSettings.tabSettingsLayout.addRow('Network type:', comboNetworkType)
		tabSettings.tabSettingsLayout.addRow('Hostname / IP:', textHostname)
		
		tabWidget.addTab(tabSettings, QtGui.QIcon("resources/icons/wrench.png"), "Settings")
		tabWidget.setVisible(False)
		
		buttonNew = QtGui.QPushButton('New')
		buttonSave = QtGui.QPushButton('Save')
		buttonSave.setDisabled(True)
		buttonDelete = QtGui.QPushButton('Delete')
		buttonDelete.setDisabled(True)
		buttonOpen = QtGui.QPushButton('Open')
		buttonOpen.setDisabled(True)
		buttonCancel = QtGui.QPushButton('Cancel')
		
		layoutH4 = QtGui.QHBoxLayout()
		layoutH4.addWidget(buttonNew)
		layoutH4.addWidget(buttonSave)
		layoutH4.addWidget(buttonDelete)
		
		layoutV1 = QtGui.QVBoxLayout()
		layoutV1.addWidget(QtGui.QLabel('Saved sessions:'))
		layoutV1.addWidget(serverManager)
		layoutV1.addLayout(layoutH4)
		
		layoutH1 = QtGui.QHBoxLayout()
		layoutH1.addLayout(layoutV1)
		
		layoutH5 = QtGui.QHBoxLayout()
		layoutH5.addStretch(1);
		layoutH5.addWidget(buttonOpen)
		layoutH5.addWidget(buttonCancel)
		
		layoutV2 = QtGui.QVBoxLayout()
		#layoutV2.addWidget(tabWidget)
		layoutV2.addSpacing(15)
		layoutV2.addWidget(labelNoSession)
		layoutV2.addStretch(1)
		layoutV2.addLayout(layoutH5)
		
		layoutH3 = QtGui.QHBoxLayout(self)
		layoutH3.addLayout(layoutH1)
		layoutH3.addLayout(layoutV2)
		
		layoutH3.setStretch(0, 30)
		layoutH3.setStretch(1, 70)
		
		self.setLayout(layoutH3)
			
		self.setWindowTitle('Session manager')
		self.setWindowIcon(QtGui.QIcon('resources/icons/heidi.ico'))
		self.setModal(True)
		self.setGeometry(300, 300, 700, 400)