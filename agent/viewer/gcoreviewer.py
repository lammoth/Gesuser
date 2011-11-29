#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gesuser.gui.gguiviewer import GGuiViewer
from gesuser.interfaces.gagent import GAgent

## \class GCoreMainAgent
# \brief GESUSER main agent core.
class GCoreViewer(object):
    def __init__(self):
        # Bot instance
        self.bot = None

        # Muc name
        self.muc = "clients"

        # Dictionary with tools data
        self.tools = dict()

        # GUI Handlers Dictionary
        self.gui_handlers = {
                            "CONNECT_AGENT_CB": self.request_connect_agent,
                            "DISCONNECT_AGENT_CB": self.request_disconnect_agent,
        }

        # BOT Handlers Dictionary
        self.bot_handlers = {
                            "UPDATE_LIST_CB": self.request_update_list,
        }

        # Gui setup
        self.gui = None
        self._setup_gui()

        # Indentity setup
        self.jid = str("%s@%s/GESUSER_Client" % ("viewer", "winterfall.local"))
        self.nick = "viewer"

    ## \fn _setup_gui(self)
    # \brief Sets up the GUI
    def _setup_gui(self):
        # Interface instance
        self.qtapp = QApplication(sys.argv)
        self.qtapp.setOrganizationName("cga")
        self.qtapp.setApplicationName("GESUSER")
        self.gui = GGuiViewer(handlers = self.gui_handlers)

    ## \fn run(self)
    # \brief Starts the main program
    def run(self):
        self.gui.show()
        self.qtapp.exec_()

    ## \fn request_create_resource(self, muc_name)
    # \brief Called then the user click on the Create resource button.
    # \param muc_name Name of the resource to be created.
    def request_connect_agent(self):
        self.muc_jid = self.generate_muc_jid()
        self.bot = GAgent( jid=self.jid,
                            muc_jid=self.muc_jid,
                            nick=self.nick,
                            parent=self,
                            handlers=self.bot_handlers
                        )
        #self.bot.set_core_handlers(self.bot_handlers)
        self.bot.connect(("winterfall.local", 5222))
        self.bot.process(threaded=True)

    def request_update_list(self,tools):
        self.gui.update_gui(tools)

    def request_disconnect_agent(self):
        pass

    ## \fn generate_muc_jid(self)
    # \brief Generates a new MUC jid.
    def generate_muc_jid(self):
        return "%s@conference.%s" % (self.muc, "winterfall.local")

if __name__=="__main__":
    s = GCoreViewer()
    s.run()