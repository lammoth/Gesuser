# -*- coding: utf-8 -*-

##\namespace Main Agent GUI

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gesuser.gui.ui_gesuseragent import Ui_GesuserAgent

##\class GGuiMainAgent
# \brief Main Agent's GUI. Inherited from QT main window and the gesuser UI.
class GGuiViewer(QMainWindow, Ui_GesuserAgent):
    ## \fn __init__(self, handlers, parent)
    # \brief GUI constructor, sets up the GUI and other things.
    # \param handlers Handlers dictionary in the form EVENT:method
    # \param parent Parent of the GUI
    def __init__(self, handlers, parent=None):
        super(GGuiViewer, self).__init__(parent)
        self.settings = QSettings()
        self.setupUi(self)
        self.handlers = handlers
        # Setup the various widgets signals
        self._setup_signals()

    ## \fn _setup_signals(self)
    # \brief Connects widgets' signals with different methods.
    def _setup_signals(self):
        self.connect(self.connectBtn, SIGNAL("clicked()"), self.connect_agent)
        self.connect(self.disconnectBtn, SIGNAL("clicked()"), self.disconnect_agent)

    ## \fn connect_agent(self)
    # \brief Requests the core to connect the agent
    def connect_agent(self):
        # Connect xmmp client
        self.handlers["CONNECT_AGENT_CB"]()

    def update_gui(self, tools):
        print "Updating tool list"
        self.toolsList.clear()
        for t in tools:
            print t
            self.toolsList.addItem(t)

    ## \fn disconnect_agent(self)
    # \brief Requests the core to disconnect the agent
    def disconnect_agent(self):
        # Disconnect xmmp client
        self.handlers["DISCONNECT_AGENT_CB"]()