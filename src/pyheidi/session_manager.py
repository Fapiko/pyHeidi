import atexit
import sys
import MySQLdb
import MySQLdb.cursors
import _mysql_exceptions
from database.database_server import DatabaseServer
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QShortcut
from sqlite3 import *
import time

class SessionManager(QtGui.QDialog):
	def __init__(self, mainApplicationWindow, configDb):
		"""
		@mainApplicationWindow: MainApplicationWindow
		"""
		atexit.register(self.shutdownEvent)
		
		self.conn = configDb
		self.conn.row_factory = Row
		self.curs = self.conn.cursor()
		mainApplicationWindow.configDb = self.conn
		
		self.currentSessionData = {}
		self.sessionIds = []
		
		super(SessionManager, self).__init__()
		self.initUI()
		self.loadSessionManager()
		self.treeServerManager.setCurrentItem(self.treeServerManager.topLevelItem(0))
		self.mainApplicationWindow = mainApplicationWindow

		self.show()
		self.slotButtonOpenClicked()
			
	def initUI(self):
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
		self.comboNetworkType = QtGui.QComboBox(self)
		self.comboNetworkType.addItem('TCP/IP')
		self.spinPort = QtGui.QSpinBox()
		self.spinPort.setRange(0, 65535)
		self.spinPort.setMinimumWidth(65)
		self.textHostname = QtGui.QLineEdit()
		self.textPassword = QtGui.QLineEdit()
		self.textPassword.setEchoMode(QtGui.QLineEdit.Password)
		textStartupScript = QtGui.QLineEdit()
		textStartupScript.setDisabled(True)
		self.textUser = QtGui.QLineEdit()
		
		# Create the Server Manager tree
		self.treeServerManager = QtGui.QTreeWidget(self)
		self.treeServerManager.header().close()
		self.treeServerManager.setRootIsDecorated(False)
		self.treeServerManager.itemSelectionChanged.connect(self.slotServerSelectionChanged)
		
		# Layout for password text field and password check box
		layoutH6 = QtGui.QHBoxLayout()
		layoutH6.addWidget(self.textPassword)
		layoutH6.addWidget(checkPasswordPrompt)
		
		# Layout to smallimize the port input field
		layoutH7 = QtGui.QHBoxLayout()
		layoutH7.addWidget(self.spinPort)
		layoutH7.addStretch(1)
		
		# Setup the tab widget
		self.tabWidget = QtGui.QTabWidget(self)
		tabSettings = QtGui.QWidget()
		tabSettings.tabSettingsLayout = QtGui.QFormLayout(tabSettings)
		tabSettings.tabSettingsLayout.addRow('Network type:', self.comboNetworkType)
		tabSettings.tabSettingsLayout.addRow('Hostname / IP:', self.textHostname)
		tabSettings.tabSettingsLayout.addRow('User:', self.textUser)
		tabSettings.tabSettingsLayout.addRow('Password:', layoutH6)
		tabSettings.tabSettingsLayout.addRow('Port:', layoutH7)
		tabSettings.tabSettingsLayout.addRow('', checkCompressProtocol)
		tabSettings.tabSettingsLayout.addRow('Databases:', comboDatabases)
		tabSettings.tabSettingsLayout.addRow('Startup script:', textStartupScript)
		
		self.tabWidget.addTab(tabSettings, QtGui.QIcon("../resources/icons/wrench.png"), "Settings")
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
		self.textHostname.textEdited.connect(self.sessionModified)
		self.textUser.textEdited.connect(self.sessionModified)
		self.textPassword.textEdited.connect(self.sessionModified)
		self.spinPort.valueChanged.connect(self.sessionModified)

		QShortcut("Ctrl+S", self, self.slotButtonSaveClicked)
		
		self.setLayout(layoutH3)

		self.setWindowTitle('Session manager')
		self.setWindowIcon(QtGui.QIcon('../resources/icons/heidi.ico'))
		self.setModal(True)
		self.setGeometry(300, 300, 700, 400)
		
	def addNewServer(self):
		# Add new server to tree view
		newServer = QtGui.QTreeWidgetItem()
		newServer.setText(0, 'Unnamed')
		newServer.setIcon(0, QtGui.QIcon('../resources/icons/server_add.png'))
		newServer.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
		
		self.sessionIds.append(None)
		self.treeServerManager.addTopLevelItem(newServer)
		self.treeServerManager.setCurrentItem(newServer)

	def loadSettings(self):
		index = self.treeServerManager.indexOfTopLevelItem(self.treeServerManager.currentItem())

		settings = None
		if (index != -1):
			self.curs = self.conn.execute("SELECT * FROM sessions WHERE id = ?", [self.sessionIds[index]])
			settings = self.curs.fetchone()
			self.currentSessionData = settings
		
		if settings != None:
			self.textHostname.setText(settings['hostname'])
			self.textUser.setText(settings['username'])
			self.textPassword.setText(settings['password'])
			self.spinPort.setValue(settings['port'])
		else:
			self.initializeSessionData()
			self.textHostname.setText('127.0.0.1')
			self.textPassword.setText('');
			self.textUser.setText('root')
			self.spinPort.setValue(3306)
	
	# Populates the session manager list
	def loadSessionManager(self):
		try:
			self.curs = self.conn.execute("SELECT id, name FROM sessions")
		except OperationalError:
			self.createSessionsTable()
		
		for row in self.curs:
			newServer = QtGui.QTreeWidgetItem()
			newServer.setText(0, row['name'])
			newServer.setIcon(0, QtGui.QIcon('../resources/icons/server.png'))
			newServer.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
			
			self.treeServerManager.addTopLevelItem(newServer)
			self.sessionIds.append(row['id'])
			
		self.toggleSettingsPane()
	
	# Called whenever a session setting is modified
	# TODO: Look into a way to remove the asterisk when user edits an item
	def sessionModified(self):
		session = self.treeServerManager.currentItem();
		
		name = session.text(0)
		if (name[-2:] == ' *'):
			name = name[:len(name) - 2]

		# Check to see if session has been reverted back to normal or not to determine if we need to change the name
		if (
			self.textHostname.text() != self.currentSessionData['hostname'] or
			self.textPassword.text() != self.currentSessionData['password'] or
			self.textUser.text() != self.currentSessionData['username'] or
			self.spinPort.value() != self.currentSessionData['port']
		):
			changed = True
		else:
			changed = False
			
		if (changed == True):
			session.setText(0, name + ' *')
			self.buttonSave.setEnabled(True)
			session.setIcon(0, QtGui.QIcon('../resources/icons/server_edit.png'))
		else:
			session.setText(0, name)
			self.buttonSave.setEnabled(False)
			session.setIcon(0, QtGui.QIcon('../resources/icons/server.png'))
			
		
	def shutdownEvent(self):
		self.conn.commit()
		self.conn.close()
		
		
	def slotButtonCancelClicked(self):
		sys.exit(0)
		
		
	def slotButtonDeleteClicked(self):
		currentServer = self.treeServerManager.currentItem()
		numServers = self.treeServerManager.topLevelItemCount()
		
		# Loop through server manager tree until we find the right server, then delete
		for i in range(0, numServers):
			if self.treeServerManager.topLevelItem(i) == currentServer:
				sessionId = self.sessionIds.pop(i)
				self.treeServerManager.takeTopLevelItem(i)
				self.curs.execute("DELETE FROM sessions WHERE id = ?", [sessionId])
				break
				
		if numServers == 1:
			self.toggleSettingsPane()
			
		
	def slotButtonNewClicked(self):
		self.addNewServer()
		self.toggleSettingsPane()
		
		
	def slotButtonOpenClicked(self):
		session = self.getCurrentSession()
		applicationWindow = self.mainApplicationWindow

		try:
			dbConnection = MySQLdb.connect(host = session['hostname'], user = session['username'], passwd = session['password'],
				port = session['port'], cursorclass = MySQLdb.cursors.DictCursor)
			dbServer = DatabaseServer(session['name'], dbConnection, applicationWindow)
			applicationWindow.show()
			applicationWindow.addDbServer(dbServer)
			self.hide()

		except _mysql_exceptions.OperationalError as e:
			message = "Connection Error [%d]: %s" % (e[0], e[1])
			QMessageBox.critical(self, 'Connection Error', message)



	def slotButtonSaveClicked(self):
		session = self.getCurrentSession()
		sessionName = session['name']
		sessionTreeItem = self.treeServerManager.currentItem()
		
		if sessionName[-1] == '*':
			sessionName = sessionName[:len(sessionName) - 2]

		if session['index'] is None:
			self.curs = self.conn.execute("SELECT name FROM sqlite_master WHERE Type='table' and name = 'sessions'")

			if self.curs.fetchone() is None:
				self.createSessionsTable()

			self.curs.execute(
				"INSERT INTO sessions (name, network_type, hostname, username, password, port) VALUES (?, ?, ?, ?, ?, ?)",
					[
						sessionName,
						session['network_type'],
						session['hostname'],
						session['username'],
						session['password'],
						session['port']
					]
			)
		else:
			self.curs.execute(
				"UPDATE sessions SET name = ?, network_type = ?, hostname = ?, username = ?, password = ?, port = ? WHERE id = ?",
					(
						sessionName,
						session['network_type'],
						session['hostname'],
						session['username'],
						session['password'],
						session['port'],
						session['index']
					)
			)

		self.buttonSave.setEnabled(False)
		sessionTreeItem.setText(0, sessionName)
		# Set server icon to unedited
		sessionTreeItem.setIcon(0, QtGui.QIcon('../resources/icons/server.png'))
			
		
	def slotServerSelectionChanged(self):
		self.loadSettings()
		
		 
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


	def createSessionsTable(self):
		self.curs.execute("""
			CREATE TABLE sessions(
			   id INTEGER PRIMARY KEY,
			   name TEXT,
			   network_type INTEGER,
			   hostname TEXT,
			   username TEXT,
			   password TEXT,
			   port INTEGER,
			   compressed BOOL,
			   startup_script TEXT
			);
		""")

	def initializeSessionData(self):
		self.currentSessionData = {'hostname': '', 'password': '', 'username': '', 'port': ''}

	def getStringFromQString(self, string):
		"""
		@type string: QString
		"""
		return unicode(string.toUtf8(), "utf-8");

	def getCurrentSession(self):
		sessionIndex = self.treeServerManager.indexOfTopLevelItem(self.treeServerManager.currentItem())
		session = {
			'id': sessionIndex,
			'name': self.getStringFromQString(self.treeServerManager.currentItem().text(0)),
			'network_type': self.comboNetworkType.currentIndex(),
			'hostname': self.getStringFromQString(self.textHostname.text()),
			'username': self.getStringFromQString(self.textUser.text()),
			'password': self.getStringFromQString(self.textPassword.text()),
			'port': self.spinPort.value(),
			'index': self.sessionIds[sessionIndex]
		}

		return session