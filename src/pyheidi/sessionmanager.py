import sys
from PyQt4 import QtGui, QtCore
from sqlite3 import *

class SessionManager(QtGui.QDialog):
	def __init__(self):
		super(SessionManager, self).__init__()
		self.initUI()
			
	def initUI(self):
		comboNetworkType = QtGui.QComboBox(self)
		comboNetworkType.addItem('TCP/IP')
		
		# No session label... TODO: should really move this text to resource file
		self.labelNoSession = QtGui.QLabel('New here? In order to connect to a MySQL server, you have to create a so called "session" at first. Just click the "New" button on the bottom left to create your first session.\n\nGive it a friendly name (e.g. "Local DB Server") so you\'ll recall it the next time you start HeidiSQL.')
		self.labelNoSession.setWordWrap(True)
		
		# Setup input fields for settings tab
		checkCompressProtocol = QtGui.QCheckBox('Compressed client/server protocol')
		checkCompressProtocol.setEnabled(False)
		checkPasswordPrompt = QtGui.QCheckBox("Prompt")
		checkPasswordPrompt.setEnabled(False)
		comboDatabases = QtGui.QComboBox()
		comboDatabases.setEditable(True)
		comboDatabases.setEditText('Separated by semicolon')
		comboDatabases.setDisabled(True)
		spinPort = QtGui.QSpinBox()
		spinPort.setRange(0, 65535)
		spinPort.setMinimumWidth(65)
		spinPort.setValue(3306)
		textHostname = QtGui.QLineEdit()
		textHostname.setText('127.0.0.1')
		textPassword = QtGui.QLineEdit()
		textPassword.setEchoMode(QtGui.QLineEdit.Password)
		textStartupScript = QtGui.QLineEdit()
		textStartupScript.setDisabled(True)
		textUser = QtGui.QLineEdit()
		textUser.setText('root')
		
		# Create the Server Manager tree
		self.treeServerManager = QtGui.QTreeWidget(self)
		self.treeServerManager.header().close()
		self.treeServerManager.setRootIsDecorated(False)
		self.treeServerManager.itemChanged.connect(self.slotNewServerChanged)
		#self.treeServerManager.itemSelectionChanged.connect(self.slotServerSelectionChanged)
		
		# Layout for password text field and password check box
		layoutH6 = QtGui.QHBoxLayout()
		layoutH6.addWidget(textPassword)
		layoutH6.addWidget(checkPasswordPrompt)
		
		# Layout to smallimize the port input field
		layoutH7 = QtGui.QHBoxLayout()
		layoutH7.addWidget(spinPort)
		layoutH7.addStretch(1)
		
		# Setup the tab widget
		self.tabWidget = QtGui.QTabWidget(self)
		tabSettings = QtGui.QWidget()
		tabSettings.tabSettingsLayout = QtGui.QFormLayout(tabSettings)
		tabSettings.tabSettingsLayout.addRow('Network type:', comboNetworkType)
		tabSettings.tabSettingsLayout.addRow('Hostname / IP:', textHostname)
		tabSettings.tabSettingsLayout.addRow('User:', textUser)
		tabSettings.tabSettingsLayout.addRow('Password:', layoutH6)
		tabSettings.tabSettingsLayout.addRow('Port:', layoutH7)
		tabSettings.tabSettingsLayout.addRow('', checkCompressProtocol)
		tabSettings.tabSettingsLayout.addRow('Databases:', comboDatabases)
		tabSettings.tabSettingsLayout.addRow('Startup script:', textStartupScript)
		
		self.tabWidget.addTab(tabSettings, QtGui.QIcon("resources/icons/wrench.png"), "Settings")
		self.tabWidget.setVisible(False)
		
		# Create the buttons
		buttonNew = QtGui.QPushButton('New')
		self.buttonSave = QtGui.QPushButton('Save')
		self.buttonSave.setDisabled(True)
		self.buttonDelete = QtGui.QPushButton('Delete')
		self.buttonDelete.setDisabled(True)
		self.buttonOpen = QtGui.QPushButton('Open')
		self.buttonOpen.setDisabled(True)
		buttonCancel = QtGui.QPushButton('Cancel')
		
		# Layout for buttons at bottom of session manager
		layoutH4 = QtGui.QHBoxLayout()
		layoutH4.addWidget(buttonNew)
		layoutH4.addWidget(self.buttonSave)
		layoutH4.addWidget(self.buttonDelete)
		
		# Layout for session manager pane
		layoutV1 = QtGui.QVBoxLayout()
		layoutV1.addWidget(QtGui.QLabel('Saved sessions:'))
		layoutV1.addWidget(self.treeServerManager)
		layoutV1.addLayout(layoutH4)
		
		layoutH1 = QtGui.QHBoxLayout()
		layoutH1.addLayout(layoutV1)
		
		# Layout for the open/cancel buttons under the tab widget
		layoutH5 = QtGui.QHBoxLayout()
		layoutH5.addStretch(1);
		layoutH5.addWidget(self.buttonOpen)
		layoutH5.addWidget(buttonCancel)
		
		self.layoutV2 = QtGui.QVBoxLayout()
		#layoutV2.addWidget(tabWidget)
		self.layoutV2.addSpacing(17)
		self.layoutV2.addWidget(self.labelNoSession)
		self.layoutV2.addStretch(1)
		self.layoutV2.addLayout(layoutH5)
		
		# Layout to separate the session manager and tab widget panes
		layoutH3 = QtGui.QHBoxLayout(self)
		layoutH3.addLayout(layoutH1)
		layoutH3.addLayout(self.layoutV2)
		layoutH3.setStretch(0, 30)
		layoutH3.setStretch(1, 70)
		
		# Setup signals
		buttonNew.clicked.connect(self.slotButtonNewClicked)
		buttonCancel.clicked.connect(self.slotButtonCancelClicked)
		self.buttonDelete.clicked.connect(self.slotButtonDeleteClicked)
		self.buttonOpen.clicked.connect(self.slotButtonOpenClicked)
		self.buttonSave.clicked.connect(self.slotButtonSaveClicked)
		
		self.setLayout(layoutH3)
			
		self.setWindowTitle('Session manager')
		self.setWindowIcon(QtGui.QIcon('resources/icons/heidi.ico'))
		self.setModal(True)
		self.setGeometry(300, 300, 700, 400)
		
	def addNewServer(self):
		# Add new server to tree view
		newServer = QtGui.QTreeWidgetItem()
		newServer.setText(0, 'Unnamed')
		newServer.setIcon(0, QtGui.QIcon('resources/icons/server_add.png'))
		newServer.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
		
		self.treeServerManager.addTopLevelItem(newServer)
		self.treeServerManager.setCurrentItem(newServer)
		
	def slotButtonCancelClicked(self):
		sys.exit(0)
		
	def slotButtonDeleteClicked(self):
		currentServer = self.treeServerManager.currentItem()
		numServers = self.treeServerManager.topLevelItemCount()
		
		for i in range(0, numServers):
			if self.treeServerManager.topLevelItem(i) == currentServer:
				self.treeServerManager.takeTopLevelItem(i)
				break
				
		if numServers == 1:
			self.toggleSettingsPane()
		
	def slotButtonNewClicked(self):
		self.addNewServer()
		self.toggleSettingsPane()
		
	def slotButtonSaveClicked(self):
		conn = connect('userdata.db')
		curs = conn.cursor()
		
	def slotNewServerChanged(self, item, column):
		print(item.text(0))
		
	def slotButtonOpenClicked(self):
		print('open')
		 
	def toggleSettingsPane(self):
		if self.treeServerManager.topLevelItemCount() > 0:
			# Toggle settings window on
			self.labelNoSession.setVisible(False)
			self.layoutV2.removeItem(self.layoutV2.itemAt(0))
			self.layoutV2.removeItem(self.layoutV2.itemAt(1))
			self.layoutV2.removeWidget(self.labelNoSession)
			self.layoutV2.insertWidget(0, self.tabWidget)
			self.layoutV2.setStretch(1, 1)
			self.tabWidget.setVisible(True)
			self.buttonDelete.setEnabled(True)
			self.buttonOpen.setEnabled(True)
			self.buttonSave.setEnabled(True)
		else:
			# Toggle settings window off and show the no sessions message
			self.labelNoSession.setVisible(True)
			self.layoutV2.removeWidget(self.tabWidget)
			self.layoutV2.insertSpacing(0, 17)
			self.layoutV2.insertWidget(1, self.labelNoSession)
			self.layoutV2.insertStretch(2, 1)
			self.tabWidget.setVisible(False)
			self.buttonDelete.setEnabled(False)
			self.buttonOpen.setEnabled(False)
			self.buttonSave.setEnabled(False)